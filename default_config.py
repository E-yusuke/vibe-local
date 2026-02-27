"""
Default API configuration for vibe-local EXE builds.

This module allows setting default API credentials during EXE build time.
Users can override these defaults by setting environment variables.

Usage in build process:
    Before building EXE, set these environment variables:
    - DEFAULT_AZURE_API_KEY
    - DEFAULT_AZURE_ENDPOINT
    - DEFAULT_AZURE_DEPLOYMENT
    - DEFAULT_AZURE_API_VERSION
    
    Or for Gemini:
    - DEFAULT_GEMINI_API_KEY
    - DEFAULT_GEMINI_MODEL

Then modify this file to include the defaults:
    DEFAULT_AZURE_API_KEY = "your-key"
    DEFAULT_AZURE_ENDPOINT = "https://..."
"""

import os

# ============================================================================
# EDIT THESE VALUES BEFORE BUILDING EXE (or leave empty for users to set)
# ============================================================================

# Azure OpenAI defaults (leave empty "" to require users to set them)
DEFAULT_AZURE_API_KEY = ""
DEFAULT_AZURE_ENDPOINT = ""
DEFAULT_AZURE_DEPLOYMENT = "gpt-4-turbo"
DEFAULT_AZURE_API_VERSION = "2024-08-01-preview"

# Gemini defaults (leave empty "" to require users to set them)
DEFAULT_GEMINI_API_KEY = ""
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"

# ============================================================================


def apply_defaults():
    """
    Apply default configuration values from environment or hardcoded values.
    
    This function should be called at application startup to set defaults
    before attempting to get the LLM client.
    
    Priority:
    1. Environment variables (user-set)
    2. Defaults from this module (build-time set)
    3. Not set (user must provide)
    
    Returns:
        dict: Configuration applied (for debugging)
    """
    applied = {}
    
    # Apply Azure OpenAI defaults
    if DEFAULT_AZURE_API_KEY and not os.environ.get("AZURE_OPENAI_API_KEY"):
        os.environ["AZURE_OPENAI_API_KEY"] = DEFAULT_AZURE_API_KEY
        applied["AZURE_OPENAI_API_KEY"] = "***REDACTED***"
    
    if DEFAULT_AZURE_ENDPOINT and not os.environ.get("AZURE_OPENAI_ENDPOINT"):
        os.environ["AZURE_OPENAI_ENDPOINT"] = DEFAULT_AZURE_ENDPOINT
        applied["AZURE_OPENAI_ENDPOINT"] = DEFAULT_AZURE_ENDPOINT
    
    if DEFAULT_AZURE_DEPLOYMENT and not os.environ.get("AZURE_OPENAI_DEPLOYMENT"):
        os.environ["AZURE_OPENAI_DEPLOYMENT"] = DEFAULT_AZURE_DEPLOYMENT
        applied["AZURE_OPENAI_DEPLOYMENT"] = DEFAULT_AZURE_DEPLOYMENT
    
    if DEFAULT_AZURE_API_VERSION and not os.environ.get("AZURE_OPENAI_API_VERSION"):
        os.environ["AZURE_OPENAI_API_VERSION"] = DEFAULT_AZURE_API_VERSION
        applied["AZURE_OPENAI_API_VERSION"] = DEFAULT_AZURE_API_VERSION
    
    # Apply Gemini defaults
    if DEFAULT_GEMINI_API_KEY and not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = DEFAULT_GEMINI_API_KEY
        applied["GEMINI_API_KEY"] = "***REDACTED***"
    
    if DEFAULT_GEMINI_MODEL and not os.environ.get("GEMINI_MODEL"):
        os.environ["GEMINI_MODEL"] = DEFAULT_GEMINI_MODEL
        applied["GEMINI_MODEL"] = DEFAULT_GEMINI_MODEL
    
    return applied


def reset_to_user_only():
    """
    Reset environment variables to user-provided values only.
    Removes any defaults that were applied.
    """
    if DEFAULT_AZURE_API_KEY:
        if os.environ.get("AZURE_OPENAI_API_KEY") == DEFAULT_AZURE_API_KEY:
            os.environ.pop("AZURE_OPENAI_API_KEY", None)
    
    if DEFAULT_GEMINI_API_KEY:
        if os.environ.get("GEMINI_API_KEY") == DEFAULT_GEMINI_API_KEY:
            os.environ.pop("GEMINI_API_KEY", None)


def get_configured_defaults():
    """
    Get which defaults are currently configured (non-empty).
    
    Returns:
        dict: Currently configured defaults (keys only, values redacted)
    """
    defaults = {}
    
    if DEFAULT_AZURE_API_KEY:
        defaults["AZURE_OPENAI_API_KEY"] = True
    if DEFAULT_AZURE_ENDPOINT:
        defaults["AZURE_OPENAI_ENDPOINT"] = True
    if DEFAULT_AZURE_DEPLOYMENT:
        defaults["AZURE_OPENAI_DEPLOYMENT"] = True
    if DEFAULT_AZURE_API_VERSION:
        defaults["AZURE_OPENAI_API_VERSION"] = True
    
    if DEFAULT_GEMINI_API_KEY:
        defaults["GEMINI_API_KEY"] = True
    if DEFAULT_GEMINI_MODEL:
        defaults["GEMINI_MODEL"] = True
    
    return defaults


if __name__ == "__main__":
    # Test script
    print("Current defaults configuration:")
    print(f"  Azure API Key: {'***SET***' if DEFAULT_AZURE_API_KEY else 'NOT SET'}")
    print(f"  Azure Endpoint: {'***SET***' if DEFAULT_AZURE_ENDPOINT else 'NOT SET'}")
    print(f"  Azure Deployment: {DEFAULT_AZURE_DEPLOYMENT}")
    print(f"  Azure API Version: {DEFAULT_AZURE_API_VERSION}")
    print()
    print(f"  Gemini API Key: {'***SET***' if DEFAULT_GEMINI_API_KEY else 'NOT SET'}")
    print(f"  Gemini Model: {DEFAULT_GEMINI_MODEL}")
