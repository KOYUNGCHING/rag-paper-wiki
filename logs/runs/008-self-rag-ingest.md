---
run_id: 008
operation: self_rag_ingest
source: self-rag
started_at: 2026-11-23T22:22:23+08:00
input_state: proposed
status: verified
---

# Run 008：Self-RAG ingest

## Human approval

使用者在完成 Self-RAG reading proposal 後指示「下一步」，授權由 `proposed` 進入
`approved` 並開始正式 ingest。

## Checks before fix

- Proposal 狀態為 `proposed`。
- Self-RAG PDF 已固定為 arXiv v1，SHA-256 與 manifest 一致。
- 正式 Self-RAG paper note、evidence record 與 Self-RAG-specific concepts 尚不存在。
- Wiki validator 當時涵蓋 3 papers、56 verified claims。

## Findings

1. Self-RAG 的 self-reflection 是學得的 Retrieve、IsRel、IsSup、IsUse token
   predictions，不是 prompt-only self-check 或可靠內省的證明。
2. Critic labels 由 GPT-4 產生並蒸餾至 Llama2-7B critic；critic 離線擴充訓練資料，
   正式 generator inference 不需再執行 critic。
3. Retrieval 可由 Retrieve token 或 probability threshold 觸發；threshold 對 PopQA 與
   PubHealth 的 accuracy 影響不同。
4. Table 2 同時涵蓋六項 tasks 與 accuracy、FactScore、ROUGE、MAUVE、citation
   precision／recall 等指標，不可合成單一總分。
5. ASQA 上 Self-RAG 13B 的 citation precision 高於 Ret-ChatGPT，但 recall 較低，
   不能寫成全面勝出。
6. Figure 3(a) 的 ablation 使用 50k training instances，Table 2 final model 使用
   150k；兩者數字不能直接互換。
7. 提高 IsSup decoding weight 會提高 citation precision、降低 MAUVE，顯示 evidence
   support 與 fluency 的 trade-off。
8. Figure 4(d) 的 human evaluation 只抽樣 PopQA 與 biography 各 50 筆，不能當作
   reflection tokens 全面可靠的證明。

## Action taken

- 將 Self-RAG proposal 標記為 `approved`。
- 建立 `wiki/evidence/self-rag.json`，記錄 26 個 verified claims。
- 對九個 result claims 記錄 Table／Figure、selection 與 comparison target。
- 建立 Self-RAG paper note，採 Introduction／Results 優先，再說明 Method、Experiments、
  Ablations 與 Limitations。
- 新增 adaptive retrieval、reflection tokens、critique-guided decoding 與 citation
  quality 四個概念頁。
- 以 Self-RAG 證據擴充 RAG、retriever、generator、context augmentation 與
  multi-passage fusion 既有概念頁。
- 建立四篇論文的發展比較，明確區分 retrieval、fusion、timing 與 critique。
- 更新 manifest、README 與 Wiki index 狀態。

## Checks after fix

首次執行 validator 即通過：

```text
python3 scripts/validate_wiki.py
Wiki validation passed: 82 verified claims, 82 cited claims, 4 paper.
```

- [x] Self-RAG evidence JSON 可解析且 claim IDs 不重複。
- [x] 新增 26 個 Self-RAG claims，全部為 `verified` 且至少被引用一次。
- [x] 九個 result claims 都有 Table／Figure locator、selection 與 comparison target。
- [x] DPR、RAG、FiD、Self-RAG citation IDs 全部存在。
- [x] Wiki Markdown relative links 全部存在。
- [x] 四篇正式 paper pages 的 front matter 均為 `verified`。
- [x] 正式 Wiki 沒有 `needs_verification`。
- [x] YAML/front matter 與 JSON 均可解析。
- [x] Self-RAG PDF hash 與 manifest 相符，且仍位於 `.gitignore` 範圍內。

本次沒有 validator failure；沒有為了作業刻意製造錯誤。

## Files changed

- `proposals/self-rag.md`
- `raw/manifest.yaml`
- `README.md`
- `wiki/index.md`
- `wiki/papers/self-rag.md`
- `wiki/evidence/self-rag.json`
- `wiki/concepts/adaptive-retrieval.md`
- `wiki/concepts/reflection-tokens.md`
- `wiki/concepts/critique-guided-decoding.md`
- `wiki/concepts/citation-quality.md`
- `wiki/concepts/retriever.md`
- `wiki/concepts/generator.md`
- `wiki/concepts/context-augmentation.md`
- `wiki/concepts/multi-passage-fusion.md`
- `wiki/concepts/rag.md`
- `wiki/comparisons/dpr-rag-fid-self-rag.md`
- `logs/runs/008-self-rag-ingest.md`
