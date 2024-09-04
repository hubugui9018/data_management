# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录为 /app
WORKDIR /app

# 将 requirements.txt 复制到容器的工作目录中
COPY requirements.txt /app/

# 创建虚拟环境
RUN python -m venv venv

# 激活虚拟环境并安装依赖
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# 复制项目文件到容器的工作目录中
COPY . /app/

# 暴露容器的 8000 端口
EXPOSE 8000

# 启动 Django 开发服务器（在激活虚拟环境的情况下）
CMD ["/bin/bash", "-c", "source venv/bin/activate && python manage.py runserver 0.0.0.0:8000"]