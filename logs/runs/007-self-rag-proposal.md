---
run_id: 007
operation: self_rag_reading_proposal
source: self-rag
started_at: 2026-11-23T22:18:23+08:00
input_state: not_started
status: awaiting_user_approval
---

# Run 007：Self-RAG reading proposal

## Checks before fix

- `raw/manifest.yaml` 已選定 Self-RAG，但 version、download date 與 SHA-256 尚未填寫。
- `raw/pdfs/self-rag.pdf` 尚不存在。
- Self-RAG proposal 與正式 Wiki paper note 均不存在。
- Wiki index 中的 Self-RAG proposal 狀態為 `not_started`。

## Findings

1. arXiv 僅有 v1，提交日期為 2023-10-17。
2. 下載的 v1 PDF 共 30 頁、未加密、沒有 JavaScript，檔案大小為 1,405,127 bytes。
3. PDF SHA-256 為
   `d9eaa1398abac0df67a9d0933a5bf8b6d9d83d2e72da2a486073cd842dd52978`。
4. 已抽取並閱讀主要本文，另渲染檢查 PDF pp. 2、4–5、7–10，包括 Figures 1–4、
   Table 1、Algorithm 1 與 Table 2。
5. Self-RAG 使用 Retrieve、IsRel、IsSup、IsUse 四組 reflection tokens；它是訓練過的
   control mechanism，不是只在既有 RAG 後加 self-check prompt。
6. Critic supervision 由 GPT-4 labels 蒸餾而來，critic 在資料建構時離線使用；正式
   generator 推論時不需要另外執行 critic。
7. Table 2 混合多種任務與 metrics；Figure 3 的消融使用 50k training instances，
   不能與 150k final model 結果直接互換。
8. 主要誤讀風險包括：把 reflection 當可靠內省、泛化「勝過 ChatGPT」、忽略不同
   retrieval sources、混淆 citation precision／recall，以及把 threshold 效果外推到
   所有任務。

## Action taken

- 下載 arXiv v1 PDF 至被 Git 忽略的 `raw/pdfs/self-rag.pdf`。
- 在 manifest 記錄固定版本、下載日期、檔案路徑與 SHA-256。
- 建立 `proposals/self-rag.md`，只規劃閱讀、圖表選擇與驗證方向。
- 將 README 與 Wiki index 的 Self-RAG proposal 狀態更新為 `proposed`。
- 沒有建立 `wiki/papers/self-rag.md`，也沒有將任何 Self-RAG claim 標記為 verified。

## Checks after fix

- [x] arXiv ID 與標題一致。
- [x] 固定使用 arXiv v1 URL。
- [x] PDF 可解析，頁數為 30。
- [x] SHA-256 已重新計算並寫入 manifest。
- [x] Introduction、Method、Results、Tables 1–2、Algorithm 1 與 Figures 1–4 已完成
  文字檢查，核心圖表已完成視覺檢查。
- [x] Proposal 回答研究問題、Introduction、Results、Method、教學用途與誤讀風險。
- [x] 狀態停在 `proposed`／`awaiting_user_approval`。
- [x] 本機 PDF 不會被 Git 追蹤。

## Files changed

- `raw/manifest.yaml`
- `proposals/self-rag.md`
- `logs/runs/007-self-rag-proposal.md`
- `README.md`
- `wiki/index.md`

本次沒有修改正式 Wiki claim，因此 validator 的 verified paper count 維持不變。
