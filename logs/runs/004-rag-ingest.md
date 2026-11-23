---
run_id: 004
operation: rag_ingest
source: rag
started_at: 2026-11-23T21:56:25+08:00
input_state: proposed
status: verified
---

# Run 004：RAG ingest

## Human approval

使用者在完成 RAG reading proposal 後指示「下一步」，授權由 `proposed` 進入
`approved` 並開始正式 ingest。

## Checks before fix

- Proposal 狀態為 `proposed`。
- RAG PDF 已固定為 arXiv v4，SHA-256 與 manifest 一致。
- 正式 RAG paper note、evidence record 與 RAG-specific concepts 尚不存在。
- Wiki validator 當時涵蓋 1 paper、17 verified claims。

## Findings

1. 原始 RAG 是 DPR retriever、Wikipedia dense index、BART generator 與
   latent-document marginalization 的特定架構，不能直接等同所有現代 RAG。
2. Task fine-tuning 更新 query encoder 與 generator，但 document encoder/index
   保持固定；「end-to-end」有明確邊界。
3. Table 1 的 Natural Questions test Exact Match 為 RAG-Sequence 44.5、DPR 41.5。
4. Table 6 支援 learned retrieval 對 Natural Questions 的價值，但 FEVER 由 BM25
   replacement 略勝，是不能忽略的例外。
5. Figure 3 顯示增加 retrieved documents 對不同 RAG variants 的效果不同，不能
   假設 k 越大越好。
6. Index hot-swapping 可以更新模型可取得的知識，但 Broader Impact 明確指出外部
   corpus 仍可能錯誤、有偏見或不完整。

## Action taken

- 將 RAG proposal 標記為 `approved`。
- 建立 `wiki/evidence/rag.json`，記錄 20 個 verified claims。
- 對六個數字／實驗結果記錄 Table／Figure、selection 與 comparison target。
- 建立 RAG paper note，採 Introduction／Results 優先，再說明 Method／Experiments。
- 新增 RAG、parametric memory、non-parametric memory、generator、context
  augmentation、RAG variants 與 knowledge update 概念頁。
- 以 RAG 證據擴充 retriever、dense retrieval、embedding、chunk 與 top-k pages。
- 建立 `comparisons/dpr-to-rag.md`，明確連接兩篇論文的角色與範圍。
- 更新 manifest、README 與 Wiki index 狀態。

## Checks after fix

首次執行 validator 即通過：

```text
python3 scripts/validate_wiki.py
Wiki validation passed: 37 verified claims, 37 cited claims, 2 paper.
```

- [x] RAG evidence JSON 可解析且 claim IDs 不重複。
- [x] 新增 20 個 RAG claims，全部為 `verified` 且至少被引用一次。
- [x] Result claims 具有 Table／Figure locator、selection 與 comparison target。
- [x] DPR 與 RAG citation IDs 全部存在。
- [x] Wiki Markdown relative links 全部存在。
- [x] 兩篇正式 paper pages 的 front matter 均為 `verified`。
- [x] 正式 Wiki 沒有 `needs_verification`。
- [x] RAG PDF hash 與 manifest 相符，且仍位於 `.gitignore` 範圍內。

本次沒有 validator failure；沒有為了作業刻意製造錯誤。先前 Run 002 已保存一筆
真實 parser conflict，可供後續反思統計。

## Files changed

- `proposals/rag.md`
- `raw/manifest.yaml`
- `README.md`
- `wiki/index.md`
- `wiki/papers/rag.md`
- `wiki/evidence/rag.json`
- `wiki/concepts/rag.md`
- `wiki/concepts/parametric-memory.md`
- `wiki/concepts/non-parametric-memory.md`
- `wiki/concepts/generator.md`
- `wiki/concepts/context-augmentation.md`
- `wiki/concepts/rag-sequence-token.md`
- `wiki/concepts/knowledge-update.md`
- `wiki/concepts/retriever.md`
- `wiki/concepts/dense-retrieval.md`
- `wiki/concepts/embedding.md`
- `wiki/concepts/chunk.md`
- `wiki/concepts/top-k-evaluation.md`
- `wiki/comparisons/dpr-to-rag.md`
- `logs/runs/004-rag-ingest.md`

