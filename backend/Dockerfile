# 数独 backend - 跨平台镜像 (linux/amd64, linux/arm64)
# 基础镜像 python:3.11-slim 支持多架构，可用 docker pull --platform linux/arm64 python:3.11-slim 验证
# 在苹果电脑上构建即得到 arm64 镜像，在 x86 上构建得到 amd64 镜像
FROM python:3.11-slim

WORKDIR /app

# 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 应用代码
COPY sudoku.py .
COPY app.py .

# 对外端口
ENV PORT=8081
EXPOSE 8081

CMD ["python", "app.py"]
