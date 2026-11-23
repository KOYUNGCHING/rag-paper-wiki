---
run_id: 003
operation: rag_reading_proposal
source: rag
started_at: 2026-11-23T21:52:42+08:00
input_state: not_started
status: awaiting_user_approval
---

# Run 003：RAG reading proposal

## Checks before fix

- `raw/manifest.yaml` 已選定 RAG，但 version、download date 與 SHA-256 尚未填寫。
- `raw/pdfs/rag.pdf` 尚不存在。
- RAG proposal 與正式 Wiki paper note 均不存在。
- Wiki index 中的 RAG proposal 狀態為 `not_started`。

## Findings

1. arXiv 顯示最新版為 v4，最後修訂日期為 2021-04-12。
2. 下載的 v4 PDF 共 19 頁、未加密、沒有 JavaScript，檔案大小為 885,323 bytes。
3. PDF SHA-256 為
   `23e3249e9a1e75418d82efecab0ea8c4d033b89c93742f63208d47ce01f21233`。
4. 已抽取並閱讀 Introduction、Methods、Experiments、Results、Discussion 與 Broader
   Impact，另渲染檢查 PDF pp. 1–3、6–10。
5. Proposal 階段識別出主要誤讀風險：把原始 RAG 當成所有 RAG、忽略 fine-tuning
   邊界、混合 RAG variants／metrics／splits，以及把較 factual 說成不會 hallucinate。
6. Table 6 的 FEVER 結果顯示 BM25 是重要例外，不能把 learned dense retrieval 寫成
   所有 task 都較好。
7. Broader Impact 明確提醒外部 knowledge source 仍可能不正確、有偏見或不完整。

## Action taken

- 下載 arXiv v4 PDF 至被 Git 忽略的 `raw/pdfs/rag.pdf`。
- 在 manifest 記錄固定版本、下載日期、檔案路徑與 SHA-256。
- 建立 `proposals/rag.md`，只規劃閱讀、圖表選擇與驗證方向。
- 將 README 與 Wiki index 的 RAG proposal 狀態更新為 `proposed`。
- 沒有建立 `wiki/papers/rag.md`，也沒有將任何 RAG claim 標記為 verified。

## Checks after fix

- [x] arXiv ID 與標題一致。
- [x] 固定使用 arXiv v4 URL。
- [x] PDF 可解析，頁數為 19。
- [x] SHA-256 已重新計算並寫入 manifest。
- [x] Figure 1、Tables 1–6、Figures 2–3 與限制段落已進行文字及視覺檢查。
- [x] Proposal 回答研究問題、Introduction、Results、Method、教學用途與誤讀風險。
- [x] 狀態停在 `proposed`／`awaiting_user_approval`。
- [x] 本機 PDF 不會被 Git 追蹤。

## Files changed

- `raw/manifest.yaml`
- `proposals/rag.md`
- `logs/runs/003-rag-proposal.md`
- `README.md`
- `wiki/index.md`

本次沒有修改正式 Wiki claim，因此不會增加 validator 的 verified paper count。

