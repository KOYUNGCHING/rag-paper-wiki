---
run_id: 006
operation: fid_ingest
source: fid
started_at: 2026-11-23T22:08:44+08:00
input_state: proposed
status: verified
---

# Run 006：FiD ingest

## Human approval

使用者在完成 FiD reading proposal 後指示「下一步」，授權由 `proposed` 進入
`approved` 並開始正式 ingest。

## Checks before fix

- Proposal 狀態為 `proposed`。
- FiD PDF 已固定為 arXiv v2，SHA-256 與 manifest 一致。
- 正式 FiD paper note、evidence record 與 FiD-specific concepts 尚不存在。
- Wiki validator 當時涵蓋 2 papers、37 verified claims。

## Findings

1. FiD 的核心是 independent passage encoding 與 decoder-side joint fusion，不是新的
   retriever。
2. FiD 可使用 DPR 或 BM25，且不同 datasets 的 retriever 設定不同；跨 dataset 結果
   不能只歸因於 decoder architecture。
3. Table 1 的 Natural Questions test Exact Match 為 FiD-large 51.4、FiD-base 48.2、
   RAG 44.5、DPR 41.5，但這不是單變量 architecture ablation。
4. Figure 3 在顯示範圍內隨 retrieved passages 增加而改善，支持 multi-passage fusion，
   但不可外推為 passages 無限增加都有效。
5. Table 2 顯示較少 training passages 會降低 dev EM，追加多-passage fine-tuning 可
   縮小差距，呈現品質與運算成本 trade-off。
6. Retriever 沒有和 FiD generator joint-train；整合 retrieval 與提升 large-passage
   efficiency 都被作者列為 future work。

## Action taken

- 將 FiD proposal 標記為 `approved`。
- 建立 `wiki/evidence/fid.json`，記錄 19 個 verified claims。
- 對五個結果 claims 記錄 Table／Figure、selection 與 comparison target。
- 建立 FiD paper note，採 Introduction／Results 優先，再說明 Method／Experiments。
- 新增 Fusion-in-Decoder、multi-passage fusion、encoder/decoder scaling 概念頁。
- 以 FiD 證據擴充 generator、context augmentation、chunk、top-k、retriever 與 RAG
  variants 等既有頁面。
- 建立 `comparisons/dpr-rag-fid.md`，比較三篇論文的角色、fusion 與 training boundary。
- 更新 manifest、README 與 Wiki index 狀態。

## Checks after fix

首次執行 validator 即通過：

```text
python3 scripts/validate_wiki.py
Wiki validation passed: 56 verified claims, 56 cited claims, 3 paper.
```

- [x] FiD evidence JSON 可解析且 claim IDs 不重複。
- [x] 新增 19 個 FiD claims，全部為 `verified` 且至少被引用一次。
- [x] Result claims 具有 Table／Figure locator、selection 與 comparison target。
- [x] DPR、RAG、FiD citation IDs 全部存在。
- [x] Wiki Markdown relative links 全部存在。
- [x] 三篇正式 paper pages 的 front matter 均為 `verified`。
- [x] 正式 Wiki 沒有 `needs_verification`。
- [x] FiD PDF hash 與 manifest 相符，且仍位於 `.gitignore` 範圍內。

本次沒有 validator failure；沒有為了作業刻意製造錯誤。

## Files changed

- `proposals/fid.md`
- `raw/manifest.yaml`
- `README.md`
- `wiki/index.md`
- `wiki/papers/fid.md`
- `wiki/evidence/fid.json`
- `wiki/concepts/fusion-in-decoder.md`
- `wiki/concepts/multi-passage-fusion.md`
- `wiki/concepts/encoder-decoder-scaling.md`
- `wiki/concepts/generator.md`
- `wiki/concepts/context-augmentation.md`
- `wiki/concepts/chunk.md`
- `wiki/concepts/top-k-evaluation.md`
- `wiki/concepts/retriever.md`
- `wiki/concepts/rag-sequence-token.md`
- `wiki/comparisons/dpr-rag-fid.md`
- `logs/runs/006-fid-ingest.md`

