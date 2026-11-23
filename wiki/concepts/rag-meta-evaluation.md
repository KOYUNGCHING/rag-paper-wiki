---
concept_id: rag-meta-evaluation
status: verified
verified_sources:
  - ragchecker
---

# RAG meta evaluation：評估指標本身可信嗎？

Meta evaluation 是「評估評估指標」：比較自動指標的判斷與人類判斷是否一致。作者認為
既有 RAG 指標的這種可靠性少有檢驗。[RAGCHECKER:ragchecker-c02]

## RAGChecker 的做法

- 280 組 pairwise instances（10 domains × 28 system pairs），每組 2 位 annotators，
  評 correctness、completeness、overall assessment。[RAGCHECKER:ragchecker-c20]
- 標註介面會顯示 GPT-4 產生的 critiques 協助判斷。[RAGCHECKER:ragchecker-c21]

## 結果與解讀邊界

| 面向（Pearson） | RAGChecker | RAGAS Answer Similarity | Human |
| --- | --- | --- | --- |
| Correctness | 49.66 | 41.07 | 63.67 |
| Overall assessment | 61.93 | 48.31 | 70.09 |

[RAGCHECKER:ragchecker-r02] [RAGCHECKER:ragchecker-r01]

- Completeness 的 Spearman 是 RAGAS Answer Similarity 較高。[RAGCHECKER:ragchecker-r03]
- 自動指標仍低於人類之間的一致性上界。
- Checker 本身也要驗證：Llama3 版 RefChecker 的 accuracy 較高，但並非每個欄位都勝出。
  [RAGCHECKER:ragchecker-r12]

相關頁面：[Claim-level evaluation](claim-level-evaluation.md)、
[RAGChecker](../papers/ragchecker.md)。
