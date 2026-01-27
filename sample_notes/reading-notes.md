---
tags: [reading, book, software-engineering]
date: 2024-01-28
status: complete
book: "A Philosophy of Software Design"
author: "John Ousterhout"
---

# A Philosophy of Software Design 讀書筆記

John Ousterhout 的軟體設計哲學，探討如何降低複雜度。

## 核心論點

> 軟體設計的首要目標是降低複雜度 (Complexity)。

複雜度的來源：
1. **變更放大 (Change Amplification)**: 小改動需要修改多處
2. **認知負擔 (Cognitive Load)**: 需要知道太多東西才能完成任務
3. **未知的未知 (Unknown Unknowns)**: 不知道需要知道什麼

## 深模組 vs 淺模組

### 深模組 (Deep Modules)

```
┌─────────────────────────────────┐
│     簡單的介面 (Small API)       │
├─────────────────────────────────┤
│                                 │
│                                 │
│     複雜的實作                   │
│     (Hidden Complexity)         │
│                                 │
│                                 │
└─────────────────────────────────┘
```

好例子：Unix 檔案 I/O（5 個系統呼叫，隱藏大量複雜度）

### 淺模組 (Shallow Modules)

```
┌─────────────────────────────────┐
│     複雜的介面 (Large API)       │
├─────────────────────────────────┤
│     簡單的實作                   │
└─────────────────────────────────┘
```

壞例子：Java I/O（需要組合多個類別才能讀檔案）

## 實用建議

### Define Errors Out of Existence

與其處理錯誤，不如設計成不會發生錯誤：

```python
# 差：呼叫者需要處理 KeyError
def get_user(user_id):
    return users[user_id]

# 好：永不拋出異常
def get_user(user_id):
    return users.get(user_id, None)
```

### 註解的價值

好的註解描述「為什麼」而非「做什麼」：

```python
# 差：描述程式碼做什麼
# 將 x 加 1
x += 1

# 好：解釋為什麼需要這樣做
# 補償 API 回傳的 0-indexed 結果
x += 1
```

## 我的反思

這本書改變了我對「簡單」的理解。簡單不是程式碼行數少，而是：
- 介面簡單，隱藏複雜度
- 修改時不需要理解太多上下文
- 降低認知負擔

應用到 [[project-log]] 中的 RAG 專案設計。

## 相關筆記

- [[system-design]] - 系統層級的設計考量
- [[project-log]] - 應用這些原則的專案
