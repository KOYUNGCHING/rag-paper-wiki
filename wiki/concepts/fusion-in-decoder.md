---
concept_id: fusion-in-decoder
status: verified
verified_sources:
  - fid
---

# Fusion-in-Decoder

Fusion-in-Decoder 是一種 multi-passage generative reader：每個 question-passage pair
分開進 encoder，encoder representations 串接後，再由同一 decoder 共同 attention
並生成答案。[FID:fid-c03]

## Fusion 發生在哪裡？

- **Encoder**：passages 彼此獨立，不做跨 passage self-attention。
- **Decoder**：一次看到所有 concatenated representations，在 generation 時融合資訊。
  [FID:fid-c05]

## 它不包含什麼？

FiD 沒有提出新的 retriever；論文使用 BM25 或 DPR。[FID:fid-c06] Retriever 也沒有
由 answer loss joint-train，end-to-end integration 被保留為 future work。[FID:fid-c10]

相關頁面：[Multi-passage fusion](multi-passage-fusion.md)、
[Encoder／decoder scaling](encoder-decoder-scaling.md)。

