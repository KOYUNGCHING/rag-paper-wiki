---
concept_id: generator
status: verified
verified_sources:
  - rag
  - fid
---

# Generator

Generator 將 input 與 retrieved context 轉成輸出文字。原始 RAG 使用 BART-large，
做法是把 input sequence 與 retrieved content 串接後交給 seq2seq model。
[RAG:rag-c07]

這與 DPR 的 extractive reader 不同：RAG 可以生成 passage 中沒有逐字出現的答案，
因此 retrieval 只提供 evidence/context，generator 仍負責組織輸出。
[RAG:rag-c10]

Generator 的輸出品質不能只由 retrieval accuracy 推定。需要分別檢查：

1. Retriever 是否找到需要的內容。
2. Generator 是否忠實使用 context。
3. 最終輸出是否正確、相關且有來源。

第三點是本 Wiki 的教學性拆解，標記為 `wiki_synthesis`；後續 RAGChecker 將補上更
完整的診斷分類。

## FiD 的多 passage generator

FiD 把每個 question-passage pair 分開 encode，再讓 decoder attention 所有 encoder
representations。[FID:fid-c03] 這與原始 RAG 對 latent documents 做 marginalization
不同，但兩者都顯示 generator 可以利用 retrieved context，而不是只做 answer span
extraction。

