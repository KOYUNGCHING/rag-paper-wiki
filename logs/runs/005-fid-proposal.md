---
run_id: 005
operation: fid_reading_proposal
source: fid
started_at: 2026-11-23T22:06:16+08:00
input_state: not_started
status: awaiting_user_approval
---

# Run 005：FiD reading proposal

## Checks before fix

- `raw/manifest.yaml` 已選定 FiD，但 version、download date 與 SHA-256 尚未填寫。
- `raw/pdfs/fid.pdf` 尚不存在。
- FiD proposal 與正式 Wiki paper note 均不存在。
- Wiki index 中的 FiD proposal 狀態為 `not_started`。

## Findings

1. arXiv 顯示最新版為 v2，最後修訂日期為 2021-02-03。
2. 下載的 v2 PDF 共 6 頁、未加密、沒有 JavaScript，檔案大小為 326,612 bytes。
3. PDF SHA-256 為
   `f1ee7e927c3fb31beb2146f8c205692a91b40dadd65d80e025c6686e4d430953`。
4. 已抽取並閱讀全文，另渲染檢查 PDF pp. 1–5，包括 Figures 1–3 與 Tables 1–2。
5. Proposal 階段識別出主要誤讀風險：把 FiD 當新 retriever、誤稱 joint retriever
   training、混合 test/dev 與 TriviaQA splits，以及將 passage-scaling 曲線無限外推。
6. FiD 的核心貢獻是 independent passage encoding 與 decoder-side joint fusion；它與
   原始 RAG 的 latent-document marginalization 不同。
7. 論文結論明確把 retrieval integration 與 end-to-end learning 列為 future work。

## Action taken

- 下載 arXiv v2 PDF 至被 Git 忽略的 `raw/pdfs/fid.pdf`。
- 在 manifest 記錄固定版本、下載日期、檔案路徑與 SHA-256。
- 建立 `proposals/fid.md`，只規劃閱讀、圖表選擇與驗證方向。
- 將 README 與 Wiki index 的 FiD proposal 狀態更新為 `proposed`。
- 沒有建立 `wiki/papers/fid.md`，也沒有將任何 FiD claim 標記為 verified。

## Checks after fix

- [x] arXiv ID 與標題一致。
- [x] 固定使用 arXiv v2 URL。
- [x] PDF 可解析，頁數為 6。
- [x] SHA-256 已重新計算並寫入 manifest。
- [x] Introduction、Method、Tables 1–2、Figures 1–3 與 Conclusion 已完成文字及視覺檢查。
- [x] Proposal 回答研究問題、Introduction、Results、Method、教學用途與誤讀風險。
- [x] 狀態停在 `proposed`／`awaiting_user_approval`。
- [x] 本機 PDF 不會被 Git 追蹤。

## Files changed

- `raw/manifest.yaml`
- `proposals/fid.md`
- `logs/runs/005-fid-proposal.md`
- `README.md`
- `wiki/index.md`

本次沒有修改正式 Wiki claim，因此 validator 的 verified paper count 維持不變。

