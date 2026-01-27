---
tags: [python, async, concurrency]
date: 2024-01-15
status: complete
---

# Python 異步編程

Python 的異步編程主要透過 `asyncio` 模組實現，讓單執行緒程式能處理大量 I/O 操作。

## 基本概念

### Coroutine

使用 `async def` 定義的函數稱為 coroutine：

```python
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### Event Loop

Event Loop 是異步程式的核心，負責調度 coroutines：

```python
import asyncio

async def main():
    result = await fetch_data("https://api.example.com/data")
    print(result)

asyncio.run(main())
```

## 並發執行

### asyncio.gather

同時執行多個 coroutines：

```python
async def fetch_all(urls: list[str]) -> list[dict]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### asyncio.create_task

建立 Task 讓 coroutine 在背景執行：

```python
async def background_work():
    task = asyncio.create_task(long_running_operation())
    # 繼續其他工作
    await task  # 等待完成
```

## 常見陷阱

1. **忘記 await**: Coroutine 不會自動執行，必須 await
2. **阻塞操作**: 不要在 async 函數中使用同步 I/O
3. **共享狀態**: 雖然是單執行緒，但狀態仍需小心處理

## 相關筆記

- [[docker-basics]] - 容器化 Python 應用
- [[system-design]] - 系統設計中的並發考量
