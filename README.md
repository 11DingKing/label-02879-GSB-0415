# 数独游戏

基于 Python 的数独小游戏，后端提供生成、验证、求解逻辑，支持本地 tkinter 桌面版与 Web 版。Docker 部署后通过浏览器访问 Web 版。

---

## How to Run

**使用 Docker（推荐，支持 ARM / x86）：**

```bash
docker-compose up --build -d
```

在浏览器打开：<http://127.0.0.1:8081/>

**本地运行 Web 版（需 Python 3.8+）：**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

访问 <http://127.0.0.1:8081/>

**本地运行桌面版（tkinter）：**

```bash
python main.py
```

---

## Services

| 服务名   | 说明           | 对外端口 |
|----------|----------------|----------|
| backend  | 数独 Web 服务（API + 前端页面） | 8081     |

---

## 测试账号

本项目为数独单机游戏，无需登录，无测试账号。打开页面即可选择难度、新游戏、检查答案、显示答案。

---

## 题目内容

> 我想用python制作一款数独游戏。帮我实现一下

---

## 项目结构

- `backend/`：数独后端
  - `sudoku.py`：生成、验证、求解逻辑
  - `app.py`：Flask Web 服务（端口 8081）
  - `static/index.html`：Web 前端页面
  - `Dockerfile`：跨平台镜像（ARM / x86）
- `main.py`：本地桌面版入口（tkinter）
- `docker-compose.yml`：一键构建并启动 backend 服务

## 多架构说明

基础镜像 `python:3.11-slim` 支持多架构。验收可在苹果电脑上执行：

```bash
docker pull --platform linux/arm64 python:3.11-slim
```

在 Mac（ARM）上执行 `docker-compose up --build -d` 将构建并运行 arm64 镜像，在 x86 上则构建 amd64 镜像。
