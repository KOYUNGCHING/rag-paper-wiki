---
run_id: 010
operation: ragchecker_ingest
source: ragchecker
started_at: 2026-11-23T22:41:00+08:00
input_state: proposed
status: verified
---

# Run 010：RAGChecker ingest

## Approval

使用者在 Run 009 proposal 後回覆「下一步」，視為明確核准（`proposed -> approved`）。

## Checks before fix

- Validator 通過：82 verified claims、4 papers。
- `raw/pdfs/ragchecker.pdf` SHA-256 與 manifest 相符（v2）。
- 尚無 RAGChecker paper note、evidence 或概念頁。

## Findings

1. **Table 2 與作者文字不完全一致**：Section 4.2 寫 RAGChecker 在三個面向都有最強
   correlation，但 completeness 的 Spearman 是 RAGAS Answer Similarity 較高
   （61.35 vs 58.11）。Wiki 以表格數字為準，記為 `ragchecker-r03`。
2. **「significantly better」找不到統計檢定**：全文搜尋 significant／p-value／t-test，
   只出現在 Abstract、contributions 與標註選項文字。Wiki 只寫「correlation 較高」。
3. **Table 16 與 Appendix G 文字不完全一致**：作者說 Llama3 RefChecker 在三種 settings
   都勝過最佳 open-source 組合；accuracy 確實都較高，但 noisy context 的 Non-Factual F1
   較低（64.15 vs 64.72）。記為 `ragchecker-r12`。
4. **GPT-4 擴寫的 domains 前後不一**：Table 1 caption 列六個，Figure 2 caption 列七個
   （多 Writing）。記為 `ragchecker-c18`，不判定哪個正確。
5. **Section 4.4 數字無法追溯到明確設定**：正文的 k 5→20、chunk 150→300 等數字沒有
   說明 system／domain 或平均方式；Appendix F 用 3 systems × 3 domains，Figures 6–10
   只給 radar 範圍。依 AGENTS.md 不得猜測，因此**未收錄這些數字**，只收錄設定與作者
   的質性觀察。
6. 標註介面顯示 GPT-4 critiques、部分 ground truth 由 GPT-4 擴寫、checker 為 Llama3-70B；
   在 paper note 的 Limitations 以 `wiki_synthesis` 標註對 GPT-4 比較的潛在影響。
7. 視覺檢查（Run 009 已渲染 pp. 4、7、8）確認 Figure 1、Tables 1–3；本次再以文字抽取
   核對 Appendix B 公式、Tables 5、6、10、16 與 Appendix C、D、F、G、H、I。

以上是閱讀中發現的**論文內部不一致或不可追溯**，不是 validator failure。本次 validator
沒有失敗。

## Action taken

- 建立 `wiki/papers/ragchecker.md`（依 AGENTS.md 的 11 段順序）。
- 建立 `wiki/evidence/ragchecker.json`：31 個一般 claims（c01–c31）與 12 個 result claims
  （r01–r12），result 全部帶 Table／Figure locator、selection 與 comparison target。
- 新增概念頁：claim-level-evaluation、retrieval-diagnostics、generation-diagnostics、
  rag-error-attribution（含明確標記為 `wiki_synthesis` 的自製教學範例）、
  rag-meta-evaluation。
- 更新既有概念頁：retriever、generator、top-k-evaluation、chunk、rag、citation-quality
  （移除 retriever 頁「RAGChecker ingest 後會再補上」的待辦句）。
- 新增 `wiki/comparisons/five-paper-overview.md`。
- 更新 manifest（verified）、proposal（approved）、README、`wiki/index.md`
  （「預定概念」改為「概念」並連結新頁）。
- 刪除暫存 `tmp/pdfs/`。

## Checks after fix

- [x] Validator：125 verified claims、125 cited claims、5 papers。
- [x] 43 個 RAGChecker claims 全部 `verified` 且至少被引用一次。
- [x] 12 個 result claims 都有完整 locator。
- [x] Table 3 引用數字逐格與渲染表格核對。
- [x] Wiki relative links 全部存在；正式 Wiki 不含未驗證標記。
- [x] PDF 仍在 `.gitignore` 範圍內。

## Files changed

- `proposals/ragchecker.md`
- `raw/manifest.yaml`
- `README.md`
- `wiki/index.md`
- `wiki/papers/ragchecker.md`
- `wiki/evidence/ragchecker.json`
- `wiki/concepts/claim-level-evaluation.md`
- `wiki/concepts/retrieval-diagnostics.md`
- `wiki/concepts/generation-diagnostics.md`
- `wiki/concepts/rag-error-attribution.md`
- `wiki/concepts/rag-meta-evaluation.md`
- `wiki/concepts/retriever.md`
- `wiki/concepts/generator.md`
- `wiki/concepts/top-k-evaluation.md`
- `wiki/concepts/chunk.md`
- `wiki/concepts/rag.md`
- `wiki/concepts/citation-quality.md`
- `wiki/comparisons/five-paper-overview.md`
- `logs/runs/010-ragchecker-ingest.md`
