---
run_id: 009
operation: ragchecker_reading_proposal
source: ragchecker
started_at: 2026-11-23T22:36:00+08:00
input_state: not_started
status: awaiting_user_approval
---

# Run 009：RAGChecker reading proposal

## Checks before fix

- Validator 通過：82 verified claims、82 cited claims、4 papers；工作樹乾淨，與
  `origin/main` 同步。
- `raw/manifest.yaml` 已選定 RAGChecker，但 version、download date 與 SHA-256 尚未填寫，
  `pdf_url` 未帶版本。
- `raw/pdfs/ragchecker.pdf` 尚不存在。

## Findings

1. arXiv 有 v1（2024-08-15）與 v2（2024-08-17）；固定使用最新的 v2。
2. **真實環境問題**：agent 的兩個執行環境都無法連到 arxiv.org（proxy 回 HTTP 403，
   網域不在 allowlist）。改由使用者在本機執行 `curl` 下載 v2 PDF。這是下載路徑的限制，
   不是 validator failure。
3. PDF 第 1 頁標示 `arXiv:2408.08067v2 [cs.CL] 17 Aug 2024`；共 27 頁、未加密、沒有
   JavaScript（OpenAction 僅為 GoTo），檔案 2,553,412 bytes。
4. PDF SHA-256 為
   `1034bf8f0b909895540e093f2d42d6d81f1dfae51711fcf1b0379dc834c084c2`。
5. 已抽取全文並閱讀 Sections 1–5，以及 Appendix 結構；渲染檢查 PDF pp. 4、7、8
   （Figure 1、Table 1、Table 2、Table 3），表格數字與文字抽取一致。
6. RAGChecker 是外部評估框架：以 Llama3-70B 做 claim extraction 與 entailment checking，
   將錯誤拆成 retriever 指標（claim recall、chunk-level context precision）與六項 generator
   指標。
7. 主要誤讀風險：metric direction 混合、評估者本身是 LLM、部分 ground truth 由 GPT-4
   擴寫、meta evaluation 僅 280 pairs、Table 3 為 10 datasets 平均、Section 4.4 數字設定需
   回 Appendix F 確認。

## Action taken

- 使用者下載 v2 PDF 至被 Git 忽略的 `raw/pdfs/ragchecker.pdf`。
- 在 manifest 記錄 v2 URL、版本、下載日期與 SHA-256，狀態改為 `proposed`。
- 建立 `proposals/ragchecker.md`。
- 將 README 與 Wiki index 的 RAGChecker proposal 狀態更新為 `proposed`。
- 刪除暫存 render 與文字抽取檔 `tmp/pdfs/`。
- 沒有建立 `wiki/papers/ragchecker.md` 或 `wiki/evidence/ragchecker.json`。

## Checks after fix

- [x] arXiv ID、標題與 v2 版本一致。
- [x] PDF 可解析，頁數 27，未加密，無 JavaScript。
- [x] SHA-256 已重新計算並寫入 manifest。
- [x] Proposal 回答研究問題、Introduction、Results、錯誤拆分、評估範圍、教學用途與誤讀風險。
- [x] 狀態停在 `proposed`／`awaiting_user_approval`。
- [x] 本機 PDF 不會被 Git 追蹤。
- [x] Validator 維持 82 verified claims／4 papers。

## Files changed

- `raw/manifest.yaml`
- `proposals/ragchecker.md`
- `logs/runs/009-ragchecker-proposal.md`
- `README.md`
- `wiki/index.md`
