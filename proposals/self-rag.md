---
paper_id: self-rag
title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
status: approved
proposal_version: 1
proposed_at: 2026-11-23
approved_at: 2026-11-23
source_version: arXiv v1
source_sha256: d9eaa1398abac0df67a9d0933a5bf8b6d9d83d2e72da2a486073cd842dd52978
---

# Self-RAG 閱讀計畫

這份文件只定義 Self-Reflective Retrieval-Augmented Generation（Self-RAG）的正式
ingest 方向，尚不是 Wiki 內容。所有方法敘述與結果數字都要在使用者核准後建立
evidence records，才可標記為 `verified`。

## 1. 論文想解決什麼問題？

一般 RAG 往往不論問題是否需要外部知識，都先檢索固定數量的 passages；檢索內容可能
不相關，而 generator 也不保證遵循 passages。Self-RAG 的研究問題是：能否訓練同一個
language model（LM），讓它在生成過程中決定何時檢索、判斷 passage 是否相關、檢查
回答是否受 evidence 支持，並以這些判斷控制解碼？

這裡的「self-reflection」是模型生成預先定義的特殊 token，不應解讀成模型具有可驗證
的內省能力。

## 2. Introduction 預計保留的重點

1. **固定檢索的限制**：不分需求檢索固定數量 passages，可能降低模型在非知識型任務的
   彈性，也可能把不相關內容帶入生成。
2. **Grounding 並非自動成立**：即使 passage 相關，既有 RAG 的輸出仍不保證與 evidence
   一致。
3. **按需檢索**：Self-RAG 先生成 retrieval token，決定是否呼叫 retriever。
4. **平行候選與批判**：需要檢索時，模型平行處理多篇 passages，再用 critique tokens
   評估 passage relevance、answer support 與整體 utility。
5. **可控制解碼**：reflection-token probabilities 可作為 segment-level beam search 的
   分數或 hard constraints，調整檢索頻率與輸出偏好。
6. **訓練而非單次 prompting**：critic 先離線標註訓練資料，generator 再學習同時生成
   text 與 reflection tokens；推論時不需要另外執行 critic model。

預定證據範圍：PDF pp. 1–2，Abstract、Section 1 與 Figure 1。

## 3. Results 預計保留的重點

### 3.1 適合簡報的核心結果

- **六項任務的整體結果**：Table 2 涵蓋 PopQA、TriviaQA、PubHealth、
  ARC-Challenge、biography generation 與 ASQA。Self-RAG 7B／13B 在表中所有任務上
  取得 non-proprietary models 的最佳表現，但各欄使用 accuracy、FactScore、string
  exact match、ROUGE、MAUVE 與 citation precision／recall 等不同指標，不能合併成
  單一「總分」。
- **長文引用的具體比較**：ASQA 上，Self-RAG 13B 的 citation precision／recall 為
  70.3／71.3；Ret-ChatGPT 為 65.1／76.6。這支持 precision 與 recall 必須分開解讀，
  不能簡化成全面勝過 proprietary baseline。
- **按需檢索與 critique 的消融**：Figure 3(a) 的 50k-data ablation 顯示，拿掉 critic、
  停用 retrieval、永遠只用 top-1 passage，或拿掉 IsSup score，會在不同任務造成不同
  程度的下降。正式 Wiki 會保留資料規模、task 與 metric，避免把單一消融外推到所有
  RAG 場景。
- **可控制性是 trade-off**：Figure 3(b) 顯示提高 IsSup 權重時，ASQA citation
  precision 上升而 MAUVE 下降；Figure 3(c) 則顯示 retrieval threshold 同時改變
  retrieval frequency 與 accuracy。這比單純宣稱「更多自我檢查一定更好」更準確。

### 3.2 適合 Wiki、未必放入簡報的結果

- Table 2 同時包含 proprietary、non-proprietary、with-retrieval 與 without-retrieval
  baselines，粗體規則也分組；比較時必須保留 baseline 類別。
- PopQA 使用 1,399 個 rare-entity queries；TriviaQA 使用既有工作定義的 11,313-query
  split，並以答案是否包含在生成文字中評估，而非嚴格 exact match。
- Biography 使用 FactScore；ASQA 同時報 correctness、fluency 與 citation metrics。
- Figure 3(a) 使用 50k training instances，並非 Table 2 最終模型的 150k 設定；ASQA
  消融只取樣 150 instances。
- Figure 4 的 human evaluation 只抽樣 PopQA 與 biography 各 50 筆，不能視為大規模
  人工驗證。

預定證據範圍：PDF pp. 6–10，Sections 4–5、Table 2、Figures 3–4。

## 4. Method 預計如何整理？

正式 ingest 時會在 Results 之後補上：

1. **四組 reflection tokens**：Retrieve 決定是否檢索；IsRel 判斷 passage 是否有用；
   IsSup 判斷可驗證敘述受 passage 支持的程度；IsUse 評估回答整體 utility。
2. **Critic data construction**：以 GPT-4 產生各 token 類型的監督訊號，再蒸餾到
   Llama2-7B critic；每個 token 類型收集約 4k–20k supervised examples。
3. **Offline augmentation**：critic 與 retriever 把 reflection tokens、相關 passages
   插入原始 instruction-output corpus，形成 generator training data。
4. **Generator learning**：Llama2 7B／13B 以標準 next-token objective 學習 text 與
   reflection tokens；retrieved chunks 在 loss 計算中被 mask。
5. **Adaptive retrieval**：模型可直接依 Retrieve token 決定是否檢索，也可用 normalized
   probability threshold 觸發 retrieval。
6. **Segment-level decoding**：需要檢索時，對多篇 passages 平行生成候選，再以
   IsRel、IsSup、IsUse probabilities 的加權和做 beam search 或 hard filtering。
7. **實驗中的 retrieval setup**：預設使用 Contriever-MS MARCO；不同任務另有 web
   search 或 GTR-XXL passages，必須在結果比較中保留。

預定證據範圍：PDF pp. 3–7，Section 3、Table 1、Algorithm 1、Figure 2 與
Section 4.3。

## 5. 對 RAG 教學的用途

Self-RAG 將補上目前 Wiki 缺少的「是否檢索」與「生成後如何評估」：

- DPR、原始 RAG 與 FiD 主要說明如何找 passages、把 retrieval 接到 generation，以及
  如何融合多篇 evidence；Self-RAG 進一步把 retrieval timing 與 evidence-based critique
  放進模型的生成流程。
- 它提供一個可操作的 RAG control loop：判斷是否檢索 → 檢索 → 逐 passage 生成 →
  評估 relevance/support/utility → 選擇候選 → 視需要重複。
- Citation quality 不是單一維度；citation precision、recall、completeness 與 fluency
  可能互相拉扯。
- 「自我反思」可以實作成可觀察的控制 token 與 decoding score，但 token prediction
  本身仍可能錯誤，需要外部 evaluation。

簡報會自行用 HTML／CSS／SVG 重畫控制流程，不直接複製論文 Figure 1。

## 6. 容易讀錯的圖表與比較

1. **不是 prompt-only self-check**：Self-RAG 的 reflection tokens、critic data 與
   generator 都經過專門訓練。
2. **「self-reflection」不是可靠內省的證明**：它是模型對特殊 token 的機率預測，
   仍需人工與 task metrics 驗證。
3. **Critic 的監督並非純人工標註**：主要由 GPT-4 產生，再蒸餾到本地 critic；這也
   帶來 proprietary teacher 與重現性限制。
4. **推論時沒有外接 critic，不等於訓練時不需要 critic**：offline data augmentation
   是方法的重要部分。
5. **Retrieve token 不保證需求判斷正確**：threshold 是可調超參數，且效果依任務而異。
6. **不是所有實驗都用完全相同的 passages**：biography、open-domain QA 與 ASQA 有
   額外 retrieval sources；比較時要保留設定。
7. **Table 2 指標不能橫向相加**：accuracy、FactScore、ROUGE、MAUVE 與 citation
   precision／recall 衡量不同面向。
8. **「outperforms ChatGPT」有範圍**：只適用論文所列任務、當時版本與特定 metrics；
   在 ASQA citation recall 上 Ret-ChatGPT 仍較高。
9. **7B 不一定全面低於 13B**：例如 biography FactScore 與 ASQA MAUVE，Self-RAG 7B
   在 Table 2 高於 13B；作者也指出較小模型可能較短但更精確地 grounding。
10. **Figure 3(a) 不是完整訓練設定**：使用 50k instances，不能直接和 Table 2 的
    150k final model 數字互換。
11. **Human evaluation 樣本很小**：Figure 4(d) 每個任務 50 筆，不能代表所有輸出。
12. **SOTA 有時間性**：論文是 2023 年 arXiv v1，結論只反映當時 baselines。

## 7. 核准後的預定輸出

- `wiki/papers/self-rag.md`
- Self-RAG claim-level evidence，包含 Figure 1、Table 1、Algorithm 1、Table 2、
  Figures 3–4 locators
- 新增 adaptive retrieval、reflection tokens、citation precision／recall 與
  critique-guided decoding 概念頁
- 更新 retriever、generator、context augmentation、multi-passage fusion 等既有頁面
- 建立 DPR → RAG → FiD → Self-RAG 的跨論文比較與連結
- Self-RAG ingest run log 與 deterministic checks

## 8. 核准結果

使用者在本 proposal 里程碑後指示進行「下一步」，授權正式 ingest。驗證結果記錄於
[`logs/runs/008-self-rag-ingest.md`](../logs/runs/008-self-rag-ingest.md)。
