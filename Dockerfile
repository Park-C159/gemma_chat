# 使用带有 CUDA 支持的 PyTorch 官方镜像作为基础镜像
FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

# 设置工作目录为 /app
WORKDIR /app

# 复制本地 Node.js 压缩包到容器
COPY node-v20.16.0-linux-x64.tar.xz /tmp/

# 解压 Node.js 压缩包并设置 PATH 环境变量
RUN tar -xf /tmp/node-v20.16.0-linux-x64.tar.xz -C /usr/local --strip-components=1 && \
    rm /tmp/node-v20.16.0-linux-x64.tar.xz && \
    ln -s /usr/local/bin/node /usr/bin/node && \
    ln -s /usr/local/bin/npm /usr/bin/npm && \
    ln -s /usr/local/bin/npx /usr/bin/npx && \
    sed -i 's|http://archive.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# 复制 Vue 项目到容器
COPY gemma_vue/ ./gemma_vue/

# 设置工作目录为 Vue 项目根目录
WORKDIR /app/gemma_vue

# 使用淘宝镜像源并安装 Vue 项目的依赖，然后构建项目
RUN npm config set registry https://registry.npmmirror.com && \
    npm install && \
    npm run build

# 返回工作目录并复制 Flask 应用的相关文件到容器
WORKDIR /app
COPY . .

# 从 Vue 构建阶段复制构建好的文件到 /static 目录
RUN mkdir -p static && \
    cp -r gemma_vue/dist/* static/

# 安装 Python 依赖，使用清华大学的 PyPI 镜像源
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# 设置环境变量，用于 Hugging Face 镜像
ENV HF_ENDPOINT=https://hf-mirror.com


# COPY models/gemma-2-2b-it /app/models/gemma-2-2b-it
# 下载 Hugging Face 模型到指定目录
# RUN pip install --no-cache-dir huggingface_hub -i https://pypi.tuna.tsinghua.edu.cn/simple && \
#     huggingface-cli login --token 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 && \
#     huggingface-cli download google/gemma-2-2b-it --local-dir models/gemma-2-2b-it

# 暴露端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python", "app.py"]
