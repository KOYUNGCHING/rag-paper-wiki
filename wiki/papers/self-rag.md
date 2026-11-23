---
paper_id: self-rag
title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
status: verified
source_version: arXiv v1
ingested_at: 2026-11-23
verified_at: 2026-11-23
proposal: ../../proposals/self-rag.md
evidence: ../evidence/self-rag.json
---

# Self-RAG

## 基本資料

- **作者**：Akari Asai、Zeqiu Wu、Yizhong Wang、Avirup Sil、Hannaneh Hajishirzi
- **全名**：Self-Reflective Retrieval-Augmented Generation
- **版本**：[arXiv:2310.11511v1](https://arxiv.org/abs/2310.11511v1)
- **一句話摘要**：Self-RAG 訓練同一個 language model（LM）按需求檢索，並以
  reflection tokens 評估 passage relevance、output support 與整體 utility，再用這些
  訊號控制生成。[SELF-RAG:self-rag-c02] [SELF-RAG:self-rag-c04]

## Introduction 與研究動機

一般 RAG 常在每次生成前取回固定數量的 passages，不論問題是否真的需要外部知識。
作者指出，不必要或離題 passages 可能降低模型的彈性或輸出品質。
[SELF-RAG:self-rag-c01]

另一個缺口是 **retrieval 不等於 grounding**：即使 passage 與問題相關，也不能保證
generator 的輸出與 passage 一致。[SELF-RAG:self-rag-c03] 因此 Self-RAG 不只問
「找到什麼」，還把「現在需不需要找」「這篇是否相關」「這句是否有 evidence 支持」
納入生成流程。

## Research gap

原始 RAG 與 FiD 都會把 retrieved context 提供給 generator，但通常由系統預先決定
何時及取回多少 passages。Self-RAG 的研究問題是：能否讓 LM 本身在生成過程中選擇
是否檢索，並以可觀察的特殊 token 評估 evidence 與自身輸出？

這裡的 self-reflection 應理解為**學得的 token prediction 與 decoding control**，
不是模型具有可靠內省能力的證明。

## Contributions

1. 用 Retrieve token 支援 [adaptive retrieval](../concepts/adaptive-retrieval.md)，而不是
   每次都檢索固定 passages。[SELF-RAG:self-rag-c09]
2. 定義 IsRel、IsSup、IsUse 等 [reflection tokens](../concepts/reflection-tokens.md)，
   將 relevance、support 與 utility 變成生成序列的一部分。
   [SELF-RAG:self-rag-c04]
3. 以離線 critic 建立 augmented training corpus，再讓最終 generator 自己生成
   reflection tokens；推論時不必另外執行 critic。[SELF-RAG:self-rag-c17]
4. 以 [critique-guided decoding](../concepts/critique-guided-decoding.md) 調整 evidence
   support、utility 與 retrieval frequency。[SELF-RAG:self-rag-c10]

## Main results

### 六項任務

| 範圍 | Self-RAG 7B | Self-RAG 13B | 解讀 |
| --- | --- | --- | --- |
| PopQA accuracy | 54.9 | 55.8 | short-form QA |
| TriviaQA accuracy | 66.4 | 69.3 | short-form QA |
| PubHealth accuracy | 72.4 | 74.5 | fact verification |
| ARC accuracy | 67.3 | 73.1 | scientific reasoning |

以上數字來自 Table 2，但四欄代表不同 datasets，不能相加成單一總分。
[SELF-RAG:self-rag-r01]

長文結果也必須逐 metric 解讀。Biography FactScore 是 7B 81.2、13B 80.2；ASQA 的
string exact match／ROUGE／MAUVE 分別是 7B 30.0／35.7／74.3、13B
31.7／37.0／71.6。[SELF-RAG:self-rag-r02] 參數較多的 13B 並非每個 metric 都較高。

### Citation precision 與 recall 不能混為一談

ASQA 上，Self-RAG 13B 的 citation precision／recall 是 70.3／71.3；
retrieval-augmented ChatGPT 是 65.1／76.6。[SELF-RAG:self-rag-r03] 前者 precision
較高、後者 recall 較高，因此不能簡化成「Self-RAG 的引用全面勝過 ChatGPT」。詳見
[Citation quality](../concepts/citation-quality.md)。

### Ablations 與控制 trade-off

Figure 3(a) 的 50k training-instance 消融中，完整 Self-RAG 在 PopQA／PubHealth／
ASQA 的結果為 45.5／73.5／32.1；拿掉 critic 後是 42.6／72.0／18.1。
[SELF-RAG:self-rag-r04]

同一設定下，固定只用 top-1 passage 的 PopQA／ASQA 為 41.8／28.6，拿掉 IsSup
score 為 44.1／30.6，低於完整模型的 45.5／32.1。
[SELF-RAG:self-rag-r05] 這支持 adaptive retrieval 與 support-aware ranking 在該消融
設定有幫助，但不能外推為每個 RAG task 都有相同幅度。

提高 IsSup 權重時，ASQA citation precision 上升、MAUVE 下降，呈現 evidence support
與 fluency 的 trade-off。[SELF-RAG:self-rag-r06] Retrieval threshold 的效果也依任務
而異：threshold 增加時兩個 tasks 的 retrieval frequency 都下降，但 PopQA accuracy
下降幅度比 PubHealth 明顯。[SELF-RAG:self-rag-r07]

## Method

### 四組 reflection tokens

| Token group | 判斷內容 | 論文中的輸出值 |
| --- | --- | --- |
| Retrieve | 何時檢索 | yes／no／continue |
| IsRel | passage 是否對 input 有用 | relevant／irrelevant |
| IsSup | 可驗證敘述是否受 passage 支持 | fully／partially／no support |
| IsUse | response 對 input 是否有用 | 5 到 1 |

這四組定義來自 Table 1。[SELF-RAG:self-rag-c04] Reflection token 是模型對預先定義
類別的預測，不能當成輸出正確性的保證。

### Inference control loop

```text
input + preceding output
  → 預測 Retrieve
  ├─ no  → 直接生成 segment → 預測 IsUse
  └─ yes → retrieve passages
           → 對各 passage 預測 IsRel 並平行生成候選
           → 預測 IsSup、IsUse
           → 排序並選出 segment
           → 繼續下一輪
```

這是 Algorithm 1 的教學性重畫。[SELF-RAG:self-rag-c05] 每個 retrieved passage
產生一個候選 segment，再由 segment-level beam search 選擇，不是把所有 passages
原封不動塞進同一個 prompt。

### Critic 與 generator training

作者先用 GPT-4 為各類 reflection tokens 建立監督訊號，每個 token type 收集約
4k–20k examples，再蒸餾到 Llama2-7B critic。[SELF-RAG:self-rag-c06] 這個 critic
在大部分 reflection-token categories 上與 GPT-4 labels 的 agreement 超過 90%。
[SELF-RAG:self-rag-c07]

接著 critic 與 retriever 離線擴充 instruction-output corpus。Generator 使用標準
next-token objective 學習 text 與 reflection tokens，retrieved chunks 不計入 loss。
[SELF-RAG:self-rag-c08] 資料建立完成後，推論只需要 generator 與 retriever，不需要
再執行 critic。[SELF-RAG:self-rag-c17]

### Adaptive retrieval 與 critique-guided decoding

Self-RAG 可直接依 Retrieve token 的輸出決定是否檢索，也可對其 normalized
probability 設定 threshold。[SELF-RAG:self-rag-c09]

需要檢索時，segment score 結合 generation probability 與 IsRel、IsSup、IsUse 的
加權機率。權重可在推論時調整，也可把不想要的 critique outcome 設成 hard filter。
[SELF-RAG:self-rag-c10]

## Experiments、datasets、metrics 與 baselines

實驗共六項 tasks，涵蓋 PopQA、TriviaQA、PubHealth、ARC-Challenge、biography
generation 與 ASQA，並同時使用 correctness、factuality、fluency、citation precision
和 citation recall。[SELF-RAG:self-rag-c11]

PopQA 使用 1,399 個 rare-entity queries，TriviaQA 使用 11,313-query split；兩者的
accuracy 是檢查 gold answer 是否出現在 generated text，不是 strict exact match。
[SELF-RAG:self-rag-c14]

最終訓練使用 150k instruction-output pairs；generator 以 Llama2 7B／13B 初始化，
critic 以 Llama2-7B 初始化。[SELF-RAG:self-rag-c12]

Retrieval source 並非所有任務都相同：預設是 Contriever-MS MARCO；biography 與
open-domain QA 另加 web-search passages；ASQA 則讓所有 baselines 使用作者提供的
GTR-XXL passages。[SELF-RAG:self-rag-c13] 因此跨 task 數字不能只歸因於
reflection mechanism。

## Ablations

Figure 3 的 ablation 只使用 50k training instances，並非 Table 2 final model 的
150k 設定。[SELF-RAG:self-rag-r04] Figure 4 的 training-scale 分析顯示 PopQA 與
ASQA citation precision 整體隨資料量上升，PubHealth 則較不一致。
[SELF-RAG:self-rag-r08]

這表示資料規模也是 performance 的一部分；不能把 Table 2 的全部差異都歸因於
reflection tokens。

## Limitations 與批判性筆記

1. **Reflection 不是正確性保證**：IsRel／IsSup 是模型預測，仍可能與人工判斷不一致。
2. **Proprietary teacher 依賴**：critic supervision 由 GPT-4 產生；作者也指出這會帶來
   API 成本與重現性問題。[SELF-RAG:self-rag-c16]
3. **人評樣本很小**：只抽樣 PopQA 與 biography 各 50 筆。
   [SELF-RAG:self-rag-c15] Figure 4(d) 的 plausibility-and-support、IsRel agreement、
   IsSup agreement 分別是 PopQA 92.5／95.0／90.0 與 biography 70.0／90.0／85.0，
   不能當成全面可靠性的證明。[SELF-RAG:self-rag-r09]
4. **指標有 trade-off**：提高 IsSup 權重改善 citation precision，卻降低 MAUVE；
   「更 grounded」不等於所有品質面向都提高。[SELF-RAG:self-rag-r06]
5. **比較設定不完全一致**：不同 tasks 使用不同 retrieval sources，proprietary
   baselines 的訓練資料也不可見。[SELF-RAG:self-rag-c13]
6. **結果具有時間邊界**：Table 2 的 SOTA／ChatGPT 比較只適用 2023 年論文採用的
   model versions、tasks 與 metrics。

## 與 DPR、RAG、FiD 的關係

DPR 解決「如何找 passages」；原始 RAG 解決「如何讓 generation 使用 retrieved
passages」；FiD 解決「如何融合更多 passages」；Self-RAG 再加入「是否需要檢索」與
「如何評估 passage／output」。這是跨論文的 `wiki_synthesis`，完整比較見
[DPR → RAG → FiD → Self-RAG](../comparisons/dpr-rag-fid-self-rag.md)。

## Related concepts

- [Adaptive retrieval](../concepts/adaptive-retrieval.md)
- [Reflection tokens](../concepts/reflection-tokens.md)
- [Critique-guided decoding](../concepts/critique-guided-decoding.md)
- [Citation quality](../concepts/citation-quality.md)
- [Retriever](../concepts/retriever.md)
- [Generator](../concepts/generator.md)
- [Multi-passage fusion](../concepts/multi-passage-fusion.md)

## Source evidence

- [Self-RAG reading proposal](../../proposals/self-rag.md)
- [Self-RAG structured evidence](../evidence/self-rag.json)
