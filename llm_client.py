"""
LLM Client adapter for Azure OpenAI and Google Gemini.
Provides a unified interface compatible with the original OllamaClient.
"""

import json
import os
import re
import sys
import uuid
import urllib.request
import urllib.error
import urllib.parse
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, config):
        self.max_tokens = config.max_tokens
        self.temperature = config.temperature
        self.context_window = config.context_window
        self.debug = config.debug
        self.timeout = 300

    @abstractmethod
    def check_connection(self, retries=3):
        """Check if the LLM service is reachable. Returns (ok, model_list)."""
        pass

    @abstractmethod
    def chat(self, model, messages, tools=None, stream=True):
        """Send chat request. Returns response in OpenAI-compatible format."""
        pass

    @abstractmethod
    def chat_sync(self, model, messages, tools=None):
        """Synchronous (non-streaming) chat. Returns simplified dict."""
        pass

    def tokenize(self, model, text):
        """Count tokens. Falls back to len//4."""
        return len(text) // 4


class AzureOpenAIClient(BaseLLMClient):
    """Azure OpenAI client."""

    def __init__(self, config):
        super().__init__(config)
        self.api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        self.endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        self.api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        self.deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4-turbo")
        self.custom_headers = {}

    def check_connection(self, retries=3):
        """Check if Azure OpenAI is reachable."""
        if not self.api_key or not self.endpoint:
            return False, []
        try:
            url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
            headers = self._build_headers()
            req = urllib.request.Request(url, headers=headers, method="HEAD")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200, [self.deployment]
        except Exception:
            return False, []

    def _build_headers(self):
        """Build request headers."""
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        headers.update(self.custom_headers)
        return headers

    def chat(self, model, messages, tools=None, stream=True):
        """Send chat request to Azure OpenAI."""
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        
        temp = self.temperature
        if tools:
            temp = min(self.temperature, 0.3)

        payload = {
            "messages": messages,
            "temperature": temp,
            "max_tokens": self.max_tokens,
            "stream": stream,
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        body = json.dumps(payload).encode("utf-8")
        headers = self._build_headers()
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")

        if self.debug:
            print(f"[debug] Azure OpenAI POST {self.deployment} stream={stream}", file=sys.stderr)

        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")[:500]
            e.close()
            raise RuntimeError(f"Azure OpenAI HTTP {e.code}: {error_body}") from e

        if stream:
            return self._iter_sse(resp)
        else:
            try:
                raw = resp.read(10 * 1024 * 1024)
            finally:
                resp.close()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON from Azure OpenAI: {raw[:200]}") from e
            return data

    def _iter_sse(self, resp):
        """Iterate over SSE stream from Azure OpenAI."""
        buf = b""
        try:
            while True:
                try:
                    chunk = resp.read(4096)
                except Exception:
                    break
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    line_bytes, buf = buf.split(b"\n", 1)
                    line = line_bytes.decode("utf-8", errors="replace").strip()
                    if line.startswith("data: "):
                        line = line[6:]
                    if not line or line == "[DONE]":
                        continue
                    try:
                        data = json.loads(line)
                        yield data
                    except json.JSONDecodeError:
                        continue
        finally:
            resp.close()

    def chat_sync(self, model, messages, tools=None):
        """Synchronous chat."""
        resp = self.chat(model=model, messages=messages, tools=tools, stream=False)
        choice = resp.get("choices", [{}])[0]
        message = choice.get("message", {})
        content = message.get("content", "") or ""
        raw_tool_calls = message.get("tool_calls", [])

        # Strip <think>...</think> blocks
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()

        # Normalize tool_calls
        tool_calls = []
        for tc in raw_tool_calls:
            func = tc.get("function", {})
            tc_id = tc.get("id", f"call_{uuid.uuid4().hex[:8]}")
            name = func.get("name", "")
            raw_args = func.get("arguments", "{}")
            if isinstance(raw_args, str) and len(raw_args) > 102400:
                raw_args = raw_args[:102400]
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                if not isinstance(args, dict):
                    args = {"raw": str(args)}
            except json.JSONDecodeError:
                try:
                    fixed = raw_args.replace("'", '"')
                    fixed = re.sub(r',\s*}', '}', fixed)
                    fixed = re.sub(r',\s*]', ']', fixed)
                    args = json.loads(fixed)
                except (json.JSONDecodeError, ValueError, TypeError, KeyError):
                    args = {"raw": raw_args}
            tool_calls.append({"id": tc_id, "name": name, "arguments": args})

        return {"content": content, "tool_calls": tool_calls}


class GeminiClient(BaseLLMClient):
    """Google Gemini API client."""

    def __init__(self, config):
        super().__init__(config)
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        self.api_base = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.custom_headers = {}

    def check_connection(self, retries=3):
        """Check if Gemini is reachable."""
        if not self.api_key:
            return False, []
        try:
            url = f"{self.api_base}models"
            headers = self._build_headers()
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200, [self.model_name]
        except Exception:
            return False, []

    def _build_headers(self):
        """Build request headers."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            **self.custom_headers,
        }

    def chat(self, model, messages, tools=None, stream=True):
        """Send chat request to Gemini."""
        url = f"{self.api_base}chat/completions?key={self.api_key}"
        
        temp = self.temperature
        if tools:
            temp = min(self.temperature, 0.3)

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temp,
            "max_tokens": self.max_tokens,
            "stream": stream,
        }
        
        if tools:
            payload["tools"] = [{"type": "function", "function": t} for t in tools]

        body = json.dumps(payload).encode("utf-8")
        headers = self._build_headers()
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")

        if self.debug:
            print(f"[debug] Gemini POST {self.model_name} stream={stream}", file=sys.stderr)

        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")[:500]
            e.close()
            raise RuntimeError(f"Gemini HTTP {e.code}: {error_body}") from e

        if stream:
            return self._iter_sse(resp)
        else:
            try:
                raw = resp.read(10 * 1024 * 1024)
            finally:
                resp.close()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON from Gemini: {raw[:200]}") from e
            return data

    def _iter_sse(self, resp):
        """Iterate over SSE stream from Gemini."""
        buf = b""
        try:
            while True:
                try:
                    chunk = resp.read(4096)
                except Exception:
                    break
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    line_bytes, buf = buf.split(b"\n", 1)
                    line = line_bytes.decode("utf-8", errors="replace").strip()
                    if line.startswith("data: "):
                        line = line[6:]
                    if not line or line == "[DONE]":
                        continue
                    try:
                        data = json.loads(line)
                        yield data
                    except json.JSONDecodeError:
                        continue
        finally:
            resp.close()

    def chat_sync(self, model, messages, tools=None):
        """Synchronous chat."""
        resp = self.chat(model=model, messages=messages, tools=tools, stream=False)
        choice = resp.get("choices", [{}])[0]
        message = choice.get("message", {})
        content = message.get("content", "") or ""
        raw_tool_calls = message.get("tool_calls", [])

        # Strip <think>...</think> blocks
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()

        # Normalize tool_calls
        tool_calls = []
        for tc in raw_tool_calls:
            func = tc.get("function", {})
            tc_id = tc.get("id", f"call_{uuid.uuid4().hex[:8]}")
            name = func.get("name", "")
            raw_args = func.get("arguments", "{}")
            if isinstance(raw_args, str) and len(raw_args) > 102400:
                raw_args = raw_args[:102400]
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                if not isinstance(args, dict):
                    args = {"raw": str(args)}
            except json.JSONDecodeError:
                try:
                    fixed = raw_args.replace("'", '"')
                    fixed = re.sub(r',\s*}', '}', fixed)
                    fixed = re.sub(r',\s*]', ']', fixed)
                    args = json.loads(fixed)
                except (json.JSONDecodeError, ValueError, TypeError, KeyError):
                    args = {"raw": raw_args}
            tool_calls.append({"id": tc_id, "name": name, "arguments": args})

        return {"content": content, "tool_calls": tool_calls}


def get_llm_client(config):
    """
    Factory function to get the appropriate LLM client.
    Priority: Azure OpenAI → Gemini (fallback)
    
    Returns:
        An initialized LLM client (AzureOpenAIClient or GeminiClient)
    
    Raises:
        RuntimeError: If no valid LLM API credentials are configured
    """
    # Try Azure OpenAI first (primary)
    azure_key = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").strip()
    
    if azure_key and azure_endpoint:
        try:
            client = AzureOpenAIClient(config)
            return client
        except Exception as e:
            if config.debug:
                print(f"[debug] Azure OpenAI initialization error: {e}", file=sys.stderr)
    
    # Fall back to Gemini (secondary)
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    if gemini_key:
        try:
            client = GeminiClient(config)
            return client
        except Exception as e:
            if config.debug:
                print(f"[debug] Gemini initialization error: {e}", file=sys.stderr)
    
    # If neither is configured, raise an error with helpful message
    raise RuntimeError(
        "❌ No LLM API credentials found.\n\n"
        "Please set ONE of the following:\n\n"
        "Option 1: Azure OpenAI (Recommended)\n"
        "  setx AZURE_OPENAI_API_KEY \"your-api-key-here\"\n"
        "  setx AZURE_OPENAI_ENDPOINT \"https://your-resource.openai.azure.com\"\n"
        "  setx AZURE_OPENAI_DEPLOYMENT \"gpt-4-turbo\"\n"
        "  setx AZURE_OPENAI_API_VERSION \"2024-08-01-preview\"\n\n"
        "Option 2: Google Gemini\n"
        "  setx GEMINI_API_KEY \"your-api-key-here\"\n"
        "  setx GEMINI_MODEL \"gemini-2.0-flash\"\n\n"
        "See SETUP_WINDOWS.md for detailed instructions."
    )
