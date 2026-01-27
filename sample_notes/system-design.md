---
tags: [architecture, system-design, scalability]
date: 2024-03-10
status: in-progress
---

# 系統設計原則

設計大規模系統時需要考量的核心概念與權衡。

## 可擴展性 (Scalability)

### 水平 vs 垂直擴展

```
垂直擴展 (Scale Up)          水平擴展 (Scale Out)
┌─────────────────┐          ┌─────┐ ┌─────┐ ┌─────┐
│                 │          │     │ │     │ │     │
│   更強的機器     │    vs    │ S1  │ │ S2  │ │ S3  │
│                 │          │     │ │     │ │     │
└─────────────────┘          └─────┘ └─────┘ └─────┘
```

水平擴展通常更有彈性，但需要處理分散式系統的複雜性。

### 負載均衡

```
              ┌─────────────────┐
              │  Load Balancer  │
              └────────┬────────┘
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ Server1 │   │ Server2 │   │ Server3 │
    └─────────┘   └─────────┘   └─────────┘
```

常見策略：Round Robin, Least Connections, IP Hash

## 快取策略

### 快取層級

1. **瀏覽器快取**: HTTP Cache-Control
2. **CDN**: 靜態資源
3. **應用層**: Redis, Memcached
4. **資料庫**: Query Cache

### Cache Aside Pattern

```
讀取流程:
1. 檢查快取 → 命中則返回
2. 快取未命中 → 查詢資料庫
3. 寫入快取 → 返回結果

寫入流程:
1. 更新資料庫
2. 刪除快取（非更新）
```

## 資料庫設計

### SQL vs NoSQL

| 需求 | 選擇 |
|------|------|
| 複雜查詢、事務 | PostgreSQL, MySQL |
| 高寫入量、彈性 schema | MongoDB, Cassandra |
| 快取、Session | Redis |
| 搜尋 | Elasticsearch |

### 讀寫分離

```
        ┌──────────┐
        │  Master  │ ← 寫入
        └────┬─────┘
             │ 複製
    ┌────────┼────────┐
    ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐
│Replica│ │Replica│ │Replica│ ← 讀取
└───────┘ └───────┘ └───────┘
```

## 可靠性 (Reliability)

### 單點故障 (SPOF)

每個關鍵元件都需要備援：
- 多個應用伺服器
- 資料庫主從複製
- 多區域部署

### 熔斷器模式

```
CLOSED → 正常運作
   ↓ 失敗達閾值
OPEN → 快速失敗，不呼叫服務
   ↓ 等待時間後
HALF-OPEN → 測試服務
   ↓ 成功則回 CLOSED
```

## 相關筆記

- [[docker-basics]] - 容器化部署
- [[python-async]] - 高並發處理
