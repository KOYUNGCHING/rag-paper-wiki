---
concept_id: multi-passage-fusion
status: verified
verified_sources:
  - rag
  - fid
  - self-rag
---

# Multi-passage fusion

Multi-passage fusion 指 generator／reader 同時利用多篇 retrieved passages，而不是只
依賴 top-1 passage。

## 原始 RAG

原始 RAG 把 retrieved documents 視為 latent variables，RAG-Sequence 或 RAG-Token
以不同方式 marginalize document-conditioned generation。[RAG:rag-c04]
[RAG:rag-c05]

## FiD

FiD 讓每篇 passage 獨立編碼，再把全部 representations 交給同一 decoder 做 joint
attention。[FID:fid-c03] 作者將 passage-count curve 的提升解讀為模型能整合多篇
evidence 的支持，但這仍是對輸出行為的推論。[FID:fid-c13]

## 共同限制

增加 passages 可能帶來更多 evidence，也增加計算與 distractors。RAG Figure 3 顯示
不同 variants 對 k 的反應不同；FiD 的實驗則在顯示範圍內持續改善。
[RAG:rag-r06] [FID:fid-r03]

## Self-RAG

Self-RAG 在需要 retrieval 的 segment step 對多篇 passages 平行生成候選，再用
IsRel、IsSup、IsUse scores 做 segment-level ranking。[SELF-RAG:self-rag-c05]
[SELF-RAG:self-rag-c10] 這和 FiD 把全部 passage representations 交給同一 decoder
jointly attend 不同：Self-RAG 在候選選擇層融合 passage-conditioned generations。

其 50k-data ablation 中，固定只取 top-1 passage 低於完整設定，但這只支持該實驗
範圍，不能證明所有 tasks 都必須採用相同的 multi-passage strategy。
[SELF-RAG:self-rag-r05]

