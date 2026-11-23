---
run_id: 002
operation: dpr_ingest
source: dpr
started_at: 2026-11-23T21:45:23+08:00
input_state: proposed
status: verified
---

# Run 002：DPR ingest

## Human approval

使用者已明確核准 `proposals/dpr.md` 的閱讀方向，DPR 才由 `proposed` 進入
`approved` 並開始正式 ingest。

## Checks before fix

- Proposal 狀態為 `proposed`。
- DPR PDF 已固定為 arXiv v3，SHA-256 與 manifest 一致。
- 正式 paper note、claim-level evidence 與 concept pages 尚不存在。
- 專案只有規則，尚無可執行的 Wiki evidence validator。

## Findings

1. Section 2 將 Top-k retrieval accuracy 定義為「前 k 個 passages 至少有一個含答案」
   的問題比例；因此不能把 Table 2 誤讀成 top-k passages 的 precision。
2. Table 2 的 Natural Questions test／Single／Top-20 結果為 DPR 78.4、BM25 59.1，
   但 SQuAD 在同類設定中是 DPR 63.2、BM25 68.8，不能宣稱全面勝出。
3. Table 4 的 Natural Questions end-to-end Exact Match 為 DPR 41.5、BM25 32.6；
   這是最終 QA 指標，不是 retrieval accuracy。
4. Table 7 顯示 dense retrieval 能處理部分 semantic relation，也可能漏掉罕見、
   關鍵的 exact phrase，適合作為 failure mode，而非整體成效證據。
5. DPR 的範圍是 open-domain extractive QA retriever，不是完整 generative RAG；
   generator 必須等後續 RAG 論文提供證據。

## Action taken

- 將 DPR proposal 標記為 `approved`。
- 建立 `wiki/evidence/dpr.json`，記錄 17 個 claim 與 PDF page／section locator。
- 對六個數字／實驗結果記錄 Table 或 Figure、selection 與 comparison target。
- 建立正式 DPR paper note，採 Introduction／Results 優先，再說明 Method／Experiments。
- 建立 retriever、dense retrieval、embedding、chunk、top-k evaluation 五個概念頁。
- 建立標準函式庫版本的 `scripts/validate_wiki.py`。
- 更新 manifest、README 與 Wiki index 狀態。

## Checks before correction

第一次執行 validator 失敗：`wiki/evidence/README.md` 中的 placeholder citation
被 parser 誤認為真實 citation，回報 unknown paper label `PAPER-ID`。

這是文件範例與 parser pattern 的真實衝突，不是刻意製造的 test fixture。

## Correction

把 README 的示例改成文字描述，不再使用與正式 citation 完全相同的方括號格式；
未放寬 validator，也沒有忽略錯誤。

## Checks after fix

執行：

```text
python3 scripts/validate_wiki.py
Wiki validation passed: 17 verified claims, 17 cited claims, 1 paper.
```

- [x] Evidence JSON 可解析且 ID 不重複。
- [x] 17 個 claims 全部為 `verified` 且至少被引用一次。
- [x] Result claims 具有 Table／Figure locator、selection 與 comparison target。
- [x] Wiki citation IDs 全部存在。
- [x] Wiki Markdown relative links 全部存在。
- [x] 正式 paper page front matter 為 `verified`。
- [x] 正式 Wiki 沒有 `needs_verification`。
- [x] 原始 PDF 仍位於 `.gitignore` 範圍內。

## Files changed

- `proposals/dpr.md`
- `raw/manifest.yaml`
- `README.md`
- `wiki/index.md`
- `wiki/papers/dpr.md`
- `wiki/evidence/README.md`
- `wiki/evidence/dpr.json`
- `wiki/concepts/retriever.md`
- `wiki/concepts/dense-retrieval.md`
- `wiki/concepts/embedding.md`
- `wiki/concepts/chunk.md`
- `wiki/concepts/top-k-evaluation.md`
- `scripts/README.md`
- `scripts/validate_wiki.py`
- `logs/runs/002-dpr-ingest.md`

