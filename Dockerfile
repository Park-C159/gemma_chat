# 使用 NVIDIA 官方提供的带有 CUDA 支持的 Python 镜像作为基础镜像
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04 AS base

# 安装 Python 和 Node.js
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录为 /app
WORKDIR /app

# 复制 Vue 项目到容器
COPY gemma_vue/ ./gemma_vue/

# 使用淘宝镜像源并安装 Vue 项目的依赖，然后构建项目
RUN cd gemma_vue && \
    npm config set registry https://registry.npmmirror.com/ && \
    npm install && \
    npm run build

# 复制 Flask 应用的相关文件到容器
COPY . .

# 从 Vue 构建阶段复制构建好的文件到 /static 目录
RUN mkdir -p static && \
    cp -r gemma_vue/dist/* static/

# 安装 Python 依赖
RUN pip3 install --no-cache-dir -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python3", "app.py"]
