# 🧠 Local RAG 問答系統

本專案為一個本地端運行的 RAG（Retrieval-Augmented Generation）系統，整合 FastAPI、Streamlit、Ollama 與 Qdrant，實現中文/英文語意查詢與回答功能。

---

## 🏗 系統架構

```mermaid
graph TD
    A[使用者輸入問題] --> B[Streamlit 前端]
    B --> C[FastAPI 後端 /query]
    C --> D[Ollama - Embedding 模型]
    C --> E[Qdrant 向量資料庫]
    E --> F[擷取最相關內容]
    F --> G[Ollama - LLM (llama3)]
    G --> H[回答結果]
    H --> B
```

---

## 📦 使用技術與模組

| 元件         | 技術/模型名稱           | 描述                       |
|--------------|--------------------------|----------------------------|
| Backend API  | FastAPI                  | 接收 `/insert`、`/query` 請求並處理邏輯 |
| Frontend     | Streamlit                | 提供使用者圖形化介面       |
| LLM 模型     | `llama3`                 | 回答使用者問題             |
| Embedding    | `nomic-embed-text`       | 將文字轉為向量             |
| 向量資料庫   | Qdrant                   | 儲存與查詢向量資料         |
| 模型平台     | Ollama                   | 提供 embedding 與 LLM 模型推論 |

---

## 🐳 Docker Compose 啟動方式

### 🧾 前置條件
- 已安裝 Docker 與 Docker Compose
- 已手動下載模型（如未使用 entrypoint 自動拉）

### 📁 專案結構
```
rag_ui/
├── app.py                   # FastAPI 程式碼
├── streamlit_app.py         # Streamlit 前端
├── Dockerfile.backend       # Backend 容器建構檔
├── Dockerfile.frontend      # Frontend 容器建構檔
├── docker-compose.yml       # 多容器編排設定
├── requirements.txt         # Python 套件需求
```

### ▶️ 啟動指令
```bash
docker-compose up --build
```

---

## 🔧 API 說明

### 插入資料
```http
POST /insert
Content-Type: application/json
{
  "text": "Python was created by Guido van Rossum."
}
```

### 查詢資料
```http
POST /query
Content-Type: application/json
{
  "query": "Who created Python?"
}
```

---

## 🌍 服務位置

| 服務        | URL                       |
|-------------|----------------------------|
| Streamlit   | [http://localhost:8501](http://localhost:8501) |
| FastAPI     | `http://localhost:8000`    |
| Qdrant UI   | [http://localhost:6333/dashboard](http://localhost:6333/dashboard) |
| Ollama API  | `http://localhost:11434`   |

---

## ✅ 測試範例

```bash
curl -X POST http://localhost:8000/insert   -H "Content-Type: application/json"   -d '{"text": "Python was created by Guido van Rossum."}'

curl -X POST http://localhost:8000/query   -H "Content-Type: application/json"   -d '{"query": "Who created Python?"}'
```

---

## 🚧 常見錯誤排除

| 問題                           | 解法                                                |
|--------------------------------|-----------------------------------------------------|
| ❌ embedding 模型找不到        | 手動執行 `ollama pull nomic-embed-text`            |
| ❌ LLM 模型未載入              | 手動執行 `ollama pull llama3`                      |
| ❌ streamlit 無法呼叫 API      | 確認 `http://rag-app:8000` 是否正確解析             |
| ❌ Qdrant 無法連線             | 確認 container network 正常、或適當延遲啟動         |

---

## 📌 後續可擴充項目

- ✅ 支援 `.env` 管理環境參數
- ✅ 自動拉模型與健康檢查 script
- ☁️ 整合 MinIO 或 PostgreSQL 做 metadata 儲存
- 🔐 加入使用者權限與 Token 驗證
- 📊 加入查詢紀錄分析（如儲存於 SQLite）

---

## 🙌 聯絡與貢獻

若你有想擴充功能或遇到困難，歡迎發 issue 或開 PR，一起讓本地 RAG 系統更強大 💪