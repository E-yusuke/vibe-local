FROM python:3.12-slim

# 必要最小限のシステムパッケージをインストール
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       git \
       curl \
    && rm -rf /var/lib/apt/lists/*

# uvのインストール（公式スクリプト使用）
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /workspace

# ポートを公開
EXPOSE 8501