---
concept_id: reflection-tokens
status: verified
verified_sources:
  - self-rag
---

# Reflection tokens

Reflection tokens 是 Self-RAG 加入 model vocabulary 的特殊 tokens，用來表示 retrieval
與 critique decisions。它們和一般文字一樣由 LM 做 next-token prediction，不是外部
rule engine，也不是模型可靠內省的證明。[SELF-RAG:self-rag-c08]

## 四組 token

- **Retrieve**：判斷何時檢索。
- **IsRel**：判斷 passage 對 input 是否有用。
- **IsSup**：判斷 output 中可驗證敘述受 passage 支持的程度。
- **IsUse**：判斷 response 的整體 utility。

完整值域定義來自 Self-RAG Table 1。[SELF-RAG:self-rag-c04]

## 如何學得？

作者先以 GPT-4 產生 reflection labels，再蒸餾到 Llama2-7B critic；各 token type
約使用 4k–20k supervised examples。[SELF-RAG:self-rag-c06] Critic 離線把 tokens
插入 training corpus，最終 generator 學會自己輸出它們，因此 inference 不必再執行
critic。[SELF-RAG:self-rag-c17]

## 如何驗證？

Reflection-token prediction 仍需外部 evaluation。論文只在 PopQA 與 biography 各
50 筆上做人評；IsRel agreement 為 95.0／90.0，IsSup agreement 為 90.0／85.0。
[SELF-RAG:self-rag-r09] 這是小樣本結果，不能保證每個 token decision 都正確。

相關頁面：[Critique-guided decoding](critique-guided-decoding.md)、
[Citation quality](citation-quality.md)。
