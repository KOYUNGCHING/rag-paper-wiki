# RAG Paper Wiki

一個以正式論文為依據的 Karpathy-style LLM Wiki，並從 Wiki 產生可互動的
RAG 教學型 HTML 簡報。

## 專案目標

- 用五篇具有發展關係的論文建立 RAG 論文知識庫。
- 採用「Introduction 與 Results 優先」的閱讀方法。
- 讓一般概念能追溯到章節與頁碼，讓實驗數字能追溯到圖表與比較欄位。
- 將跨論文知識重新組織成適合「知道 LLM、尚未學過 RAG」資工同學的教材。
- 以實際的 ingest、lint、revision 紀錄說明 workflow、loop 與反思。

## 核心資料

| Paper | Wiki 中的角色 | 初始狀態 |
| --- | --- | --- |
| Dense Passage Retrieval | Dense retriever 與向量檢索基礎 | verified |
| Retrieval-Augmented Generation | Retriever 與 generator 的核心架構 | not_started |
| Fusion-in-Decoder | 多篇檢索內容的整合 | not_started |
| Self-RAG | 按需求檢索與自我反思 | not_started |
| RAGChecker | 分析 retrieval 與 generation 錯誤 | not_started |

詳細來源資料記錄於 [`raw/manifest.yaml`](raw/manifest.yaml)。原始 PDF 只保留
在本機的 `raw/pdfs/`，不會提交至 Git。

## 工作流程

每篇論文都必須依序經過：

```text
not_started → proposed → 使用者確認 → approved → ingested → verified
```

Wiki 完成後才會進行大綱審查、HTML 簡報生成與投影片來源檢查。完整流程見
[`graph/workflow.md`](graph/workflow.md)，Agent 操作規則見 [`AGENTS.md`](AGENTS.md)。

## 目錄

```text
raw/          原始來源 manifest；PDF 僅存本機
proposals/    每篇 ingest 前的閱讀計畫與人工確認狀態
wiki/         正式的論文頁、概念頁與跨論文比較
logs/         執行、檢查、修正與反思紀錄
graph/        實際 workflow 與 loop
scripts/      deterministic validator
slides-src/   簡報大綱與結構化內容
docs/         GitHub Pages 的原生 HTML/CSS/JS 簡報
```

## 目前進度

專案骨架與操作契約已建立。尚未建立任何閱讀計畫、下載 PDF、ingest 論文，
也尚未產生 Wiki 正式內容或簡報。

