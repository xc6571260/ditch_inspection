FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    build-essential \
    git \
    curl \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean


# 這裡建立 python3、python 指令
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.10 /usr/bin/python && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

# 安裝 PyTorch (CUDA 12.4 專用)
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

WORKDIR /app
COPY . /app

CMD ["python", "main.py"]
