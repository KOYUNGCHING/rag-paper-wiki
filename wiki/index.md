# RAG 論文知識庫

本 Wiki 將五篇正式論文整理成互相連結的論文頁、概念頁與比較頁。目前 DPR、
原始 RAG、FiD 與 Self-RAG 已完成驗證；以下狀態不得超前於實際流程。

## 論文狀態

| Paper | Proposal | Ingest | Evidence |
| --- | --- | --- | --- |
| [DPR](papers/dpr.md) | approved | ingested | verified |
| [RAG](papers/rag.md) | approved | ingested | verified |
| [FiD](papers/fid.md) | approved | ingested | verified |
| [Self-RAG](papers/self-rag.md) | approved | ingested | verified |
| RAGChecker | proposed | not_started | not_started |

## 預定概念

- [RAG（Retrieval-Augmented Generation）](concepts/rag.md)
- [Dense retrieval](concepts/dense-retrieval.md)
- [Embedding 與相似度](concepts/embedding.md)
- [Retriever](concepts/retriever.md)、[generator](concepts/generator.md) 與
  [context augmentation](concepts/context-augmentation.md)
- [Chunk 與 retrieval unit](concepts/chunk.md)
- [Top-k retrieval evaluation](concepts/top-k-evaluation.md) 與 generation 評估
- [Parametric memory](concepts/parametric-memory.md) 與
  [non-parametric memory](concepts/non-parametric-memory.md)
- [RAG-Sequence 與 RAG-Token](concepts/rag-sequence-token.md)
- [Knowledge update](concepts/knowledge-update.md)
- [Fusion-in-Decoder](concepts/fusion-in-decoder.md)
- [Multi-passage fusion](concepts/multi-passage-fusion.md)
- [Encoder／decoder scaling](concepts/encoder-decoder-scaling.md)
- [Adaptive retrieval](concepts/adaptive-retrieval.md)
- [Reflection tokens](concepts/reflection-tokens.md)
- [Critique-guided decoding](concepts/critique-guided-decoding.md)
- [Citation quality](concepts/citation-quality.md)
- Hallucination 與來源忠實度

有連結的項目已由 DPR／RAG／FiD／Self-RAG 證據驗證；其他項目仍是預定架構，在取得
後續論文證據前不得填入實質 claim。

## 跨論文比較

- [從 DPR 到 RAG：由找資料到用資料生成](comparisons/dpr-to-rag.md)
- [DPR → RAG → FiD：檢索、生成與多篇融合](comparisons/dpr-rag-fid.md)
- [DPR → RAG → FiD → Self-RAG：從檢索到可控制的生成](comparisons/dpr-rag-fid-self-rag.md)

