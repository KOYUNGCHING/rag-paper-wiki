---
concept_id: retrieval-diagnostics
status: verified
verified_sources:
  - ragchecker
---

# Retrieval diagnostics

RAGChecker 的 retriever 指標回答：「生成正確答案所需的資訊，有沒有被找回來？找回來的
chunks 有多少是有用的？」

| 指標 | 單位 | 定義 | 方向 |
| --- | --- | --- | --- |
| Claim recall | claim | ground-truth claims 被 retrieved chunks entail 的比例 | 越高越好 |
| Context precision | chunk | 含任一 ground-truth claim 的 chunks ÷ k | 越高越好 |

[RAGCHECKER:ragchecker-c09]

兩者分母不同：一個數 claims，一個數 chunks。作者選 chunk-level precision，是因為固定
大小的 chunk 本來就可能混入無關內容，claim-level precision 不可能到 100%。
[RAGCHECKER:ragchecker-c10]

## 和 DPR top-k accuracy 的差別

DPR 的 [top-k evaluation](top-k-evaluation.md) 檢查 top-k 中是否出現含答案的
passage；RAGChecker 則不依賴人工標註的 relevant chunks，而是用 ground-truth claims
是否被 chunks entail 來判斷。作者認為傳統 recall@k／MRR 依賴標註 chunks 與固定切分。
[RAGCHECKER:ragchecker-c01]（此對照為 `wiki_synthesis`。）

## 實驗中的觀察

固定 GPT-4，BM25 → E5-Mistral 讓 claim recall 74.0 → 83.5、context precision
52.3 → 61.8。[RAGCHECKER:ragchecker-r05] 這個提升因 domain 而差很多。
[RAGCHECKER:ragchecker-r11] 作者也承認 retriever 指標不如 generator 指標細緻。
[RAGCHECKER:ragchecker-c22]

相關頁面：[Retriever](retriever.md)、[Chunk](chunk.md)、
[RAG error attribution](rag-error-attribution.md)。
