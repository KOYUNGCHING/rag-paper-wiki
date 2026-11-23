---
run_id: 001
operation: dpr_reading_proposal
source: dpr
started_at: 2026-11-23T21:40:32+08:00
input_state: not_started
status: awaiting_user_approval
---

# Run 001：DPR reading proposal

## Checks before fix

- `raw/manifest.yaml` 已選定 DPR，但 version、download date 與 SHA-256 尚未填寫。
- `raw/pdfs/dpr.pdf` 尚不存在。
- DPR proposal 與正式 Wiki paper note 均不存在。
- Wiki index 中的 DPR proposal 狀態為 `not_started`。

## Findings

1. arXiv 顯示最新版為 v3，最後修訂日期為 2020-09-30。
2. 下載的 v3 PDF 共 13 頁、未加密、沒有 JavaScript，檔案大小為 383,508 bytes。
3. PDF SHA-256 為
   `3e67fc1a9977715acf722d85f0b7d124b03715e975f6310a4d6c12094190912f`。
4. 已抽取並閱讀全文，另渲染檢查 PDF pp. 1–2、5–8、12–13。
5. Proposal 階段識別出四類主要誤讀風險：metric、dataset split、Single/Multi
   training setting，以及 retrieval 與 end-to-end QA 結果混用。
6. Table 2 顯示 SQuAD 是重要例外，不能將論文結論簡化為 DPR 在所有資料集均
   勝過 BM25。

## Action taken

- 下載 arXiv v3 PDF 至被 Git 忽略的 `raw/pdfs/dpr.pdf`。
- 在 manifest 記錄固定版本、下載日期、檔案路徑與 SHA-256。
- 建立 `proposals/dpr.md`，只規劃閱讀與驗證方向。
- 將 README 與 Wiki index 的 DPR proposal 狀態更新為 `proposed`。
- 沒有建立 `wiki/papers/dpr.md`，也沒有將任何 claim 標記為 verified。

## Checks after fix

- [x] arXiv ID 與標題一致。
- [x] 固定使用 arXiv v3 URL。
- [x] PDF 可解析，頁數為 13。
- [x] SHA-256 已重新計算並寫入 manifest。
- [x] 重要表格與 Introduction 已進行文字及視覺檢查。
- [x] Proposal 回答研究問題、Introduction、Results、教學用途與誤讀風險。
- [x] 狀態停在 `proposed`／`awaiting_user_approval`。
- [x] 本機 PDF 不會被 Git 追蹤。

## Files changed

- `raw/manifest.yaml`
- `proposals/dpr.md`
- `logs/runs/001-dpr-proposal.md`
- `README.md`
- `wiki/index.md`

本次沒有修正正式 Wiki 內容，因此沒有 claim-level validation 結果。

