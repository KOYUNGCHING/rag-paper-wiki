---
concept_id: encoder-decoder-scaling
status: verified
verified_sources:
  - fid
---

# Encoder／decoder scaling

FiD 的核心 scaling 設計是把多 passage interaction 從 encoder 移到 decoder。

## Encoder side

每個 question-passage pair 獨立編碼，因此 encoder self-attention 只在單一 context
內計算。增加 passages 時，encoder computation 對 passage count 近似線性增加，而非
把所有 passages 串成一段後產生 quadratic self-attention。[FID:fid-c04]

## Decoder side

所有 encoder outputs 會串接，decoder attention 完整 representations，負責跨 passage
fusion。[FID:fid-c03] 所以 FiD 沒有消除多 context 成本，只是改變成本分布。

## 品質與成本

Table 2 顯示較少 training passages 會降低 dev EM，而追加多-passage fine-tuning 可以
縮小差距。[FID:fid-r04] [FID:fid-r05] 作者仍把大 passage count 的效率列為 future
work。[FID:fid-c14]

