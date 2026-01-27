---
tags: [docker, devops, containers]
date: 2024-02-20
status: complete
---

# Docker 基礎

Docker 是容器化平台，讓應用程式能在隔離環境中運行。

## 核心概念

### Image vs Container

- **Image**: 唯讀模板，包含應用程式和依賴
- **Container**: Image 的運行實例

### 與 VM 的差異

| 特性 | Docker | VM |
|------|--------|-----|
| 啟動時間 | 秒級 | 分鐘級 |
| 資源消耗 | 低 | 高 |
| 隔離程度 | 進程級 | 完整 OS |
| 可攜性 | 高 | 中 |

## 常用指令

### 映像操作

```bash
docker pull nginx:latest
docker images
docker rmi nginx:latest
```

### 容器操作

```bash
docker run -d -p 8080:80 nginx
docker ps
docker stop <container_id>
docker rm <container_id>
```

### 進入容器

```bash
docker exec -it <container_id> /bin/bash
```

## Dockerfile

建立自訂映像：

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

建構與執行：

```bash
docker build -t my-app .
docker run -d my-app
```

## Docker Compose

多容器應用編排：

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
```

## 相關筆記

- [[python-async]] - Python 應用容器化
- [[project-log]] - 專案部署記錄
