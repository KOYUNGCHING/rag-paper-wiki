---
concept_id: claim-level-evaluation
status: verified
verified_sources:
  - ragchecker
---

# Claim-level evaluation

傳統 response-level 指標（例如 ROUGE 或 Exact Match）把整段回答當成一個單位。RAGChecker
改成先把文字拆成 **claims**，再逐一檢查每個 claim 是否被某段參考文字 entail。
[RAGCHECKER:ragchecker-c03]

## 兩個元件

1. **Text-to-claim extractor**：把 response、ground-truth answer 拆成 claims。
2. **Claim-entailment checker**：判斷 claim 是否被 reference text 支持。

一個回答因此可同時包含 correct claims、incorrect claims，並漏掉部分 ground-truth claims。
[RAGCHECKER:ragchecker-c07]

## Overall precision／recall／F1

- **Precision**：response claims 中被 ground truth 支持的比例。
- **Recall**：ground-truth claims 中被 response 涵蓋的比例。
- **F1**：兩者的調和平均。[RAGCHECKER:ragchecker-c08]

## 注意

Extractor 與 checker 本身是 LLM（RAGChecker 使用 Llama3-70B），所以分數也帶有評估
模型的錯誤。[RAGCHECKER:ragchecker-c16] 這種 claim-level F1 與 FiD 的 Exact Match、
DPR 的 top-k retrieval accuracy 是不同尺度，不能放在同一張排行榜（`wiki_synthesis`）。

相關頁面：[Retrieval diagnostics](retrieval-diagnostics.md)、
[Generation diagnostics](generation-diagnostics.md)、[RAGChecker](../papers/ragchecker.md)。
