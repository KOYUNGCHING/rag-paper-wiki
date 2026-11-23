---
title: "RAG 是什麼？讓 LLM 先查資料再回答"
status: approved
approved_at: 2026-11-23
audience: 已懂基本 LLM、尚未學過 RAG 的資工學生
slides: 14
target_minutes: 11.5
---

# 簡報大綱與 Wiki mapping

規則：
- 每張 slide 列出使用的 Wiki pages 與 claim IDs；validator 會檢查每個連結和 claim 是否存在、是否 verified。
- 數字一律附上 paper、Table／Figure、dataset 與比較對象。不同論文的數字不放在同一張圖。
- 「青嶼市」範例是虛構教學資料，畫面上要標示「虛構範例」。
- `wiki_synthesis` 的內容在畫面上標成「整理」，作者的解讀標成「作者觀察」。

時間配置合計 11.5 分鐘（目標 10–12 分鐘）。

---

## Slide 1

**標題：RAG 是什麼？讓 LLM 先查資料再回答**（0.5 分鐘）

- 副標：從五篇論文看 RAG 怎麼找資料、用資料、檢查錯誤。
- 學習目標：
  1. 說出 Retrieve → Augment → Generate 三步驟。
  2. 分辨「沒找到資料」和「找到了卻沒用好」兩種錯誤。
  3. 知道 Self-RAG 與 RAGChecker 各自解決什麼問題。
- 畫面：五篇論文的時間線（DPR → RAG → FiD → Self-RAG → RAGChecker），標成「整理」。

Wiki：[五篇總覽](../wiki/comparisons/five-paper-overview.md)

## Slide 2

**LLM 為什麼需要外部知識？**（0.75 分鐘）

- 模型權重裡的知識（parametric memory）難以直接修改、檢查，也不提供來源。[RAG:rag-c01]
- 把知識全部塞進權重，需要很大的模型，訓練與查詢都貴。[FID:fid-c01]
- RAG 的想法：加一個可檢查、可替換的外部文字記憶（non-parametric memory）。[RAG:rag-c02]
- 但外部資料本身也可能錯誤或有偏見。[RAG:rag-c13]

Wiki：[Parametric memory](../wiki/concepts/parametric-memory.md)、[Non-parametric memory](../wiki/concepts/non-parametric-memory.md)、[RAG paper](../wiki/papers/rag.md)、[FiD paper](../wiki/papers/fid.md)

## Slide 3

**RAG 的三步驟：Retrieve → Augment → Generate**（0.75 分鐘）

- Retrieve：retriever 找出 top-k chunks。[RAG:rag-c03]
- Augment：把 chunks 接在問題後面，成為 generator 的 context。[RAG:rag-c07]
- Generate：generator 根據問題與 context 產生答案，不只是擷取原文片段。[RAG:rag-c10]
- 註明：原始 RAG 是特定架構（DPR retriever + BART + marginalization）；今天說的「RAG」常泛指 retrieval + generation 流程（整理）。
- 畫面：原創三格流程 SVG。

Wiki：[RAG concept](../wiki/concepts/rag.md)、[Retriever](../wiki/concepts/retriever.md)、[Generator](../wiki/concepts/generator.md)、[Context augmentation](../wiki/concepts/context-augmentation.md)

## Slide 4

**DPR：怎麼找到相關的 chunks？**（0.75 分鐘）

- BM25 靠關鍵字比對；dense retrieval 用向量，能連到字面不同但語意相近的文字。[DPR:dpr-c02]
- 兩個 encoder 分別把問題和 passage 變成向量，用內積排序。[DPR:dpr-c05] Passage 向量事先建好索引。[DPR:dpr-c06]
- 評估：Top-k accuracy＝前 k 個結果中至少一個含答案的比例。[DPR:dpr-c09]
- 結果（DPR 論文 Table 2，Single setting，Top-20）：
  - Natural Questions：DPR 78.4 vs BM25 59.1。[DPR:dpr-r01]
  - SQuAD 是例外：DPR 63.2 vs BM25 68.8。[DPR:dpr-r02]
- 畫面：原創長條圖，只放這兩組，標明「DPR Table 2」。

Wiki：[DPR paper](../wiki/papers/dpr.md)、[Dense retrieval](../wiki/concepts/dense-retrieval.md)、[Embedding](../wiki/concepts/embedding.md)、[Top-k evaluation](../wiki/concepts/top-k-evaluation.md)

## Slide 5

**互動範例：一次完整的 RAG**（1.25 分鐘）

虛構範例（青嶼市），資料定義在 Wiki 的 RAG error attribution 頁。

- 互動步驟（按鈕或方向鍵逐步前進）：
  1. **Question**：「青嶼市的捷運何時通車？哪一條線最先開？」
  2. **Retrieve**：從 K1–K5 取出 top-3（K1、K3、K2），相關度分數是示意值，畫面要標「示意」。
  3. **Augment**：顯示組好的 prompt（問題 + 三個 chunks）。
  4. **Generate**：答案「2015 年通車，藍線最先開」，每句標出支持它的 chunk（K1）。
- 重點：答案的每一句都能回指到 chunk。這是「讓 LLM 先查資料再回答」的具體樣子（整理）。
- 無 JS 時：四個步驟以靜態清單完整呈現。

Wiki：[RAG error attribution（虛構資料）](../wiki/concepts/rag-error-attribution.md)、[Chunk](../wiki/concepts/chunk.md)、[Context augmentation](../wiki/concepts/context-augmentation.md)、[RAG concept](../wiki/concepts/rag.md)

## Slide 6

**原始 RAG：兩種記憶一起用**（0.75 分鐘）

- Retriever 由 DPR 初始化，generator 是 BART。[RAG:rag-c06] [RAG:rag-c07]
- 微調時更新 query encoder 和 generator，文件索引不動。[RAG:rag-c08]
- 換掉外部索引，就能改變模型回答的時效性事實，不用重訓 generator（作者主張）。[RAG:rag-c11]
- 結果（RAG 論文 Table 1，Natural Questions test，Exact Match）：RAG-Sequence 44.5 vs DPR 41.5。[RAG:rag-r01]
- 補充一句：RAG-Sequence 和 RAG-Token 決定「整句還是每個 token 用哪份文件」。[RAG:rag-c04] [RAG:rag-c05]

Wiki：[RAG paper](../wiki/papers/rag.md)、[Knowledge update](../wiki/concepts/knowledge-update.md)、[RAG-Sequence 與 RAG-Token](../wiki/concepts/rag-sequence-token.md)

## Slide 7

**FiD：一次融合很多 passages**（0.75 分鐘）

- 每個「問題＋passage」分別 encode，decoder 再一起看全部。[FID:fid-c03]
- 分開 encode，計算量隨 passage 數線性成長。[FID:fid-c04]
- FiD 不是新的 retriever，論文使用 BM25 或 DPR 取得 passages。[FID:fid-c06]
- 在顯示範圍內，passage 越多，Exact Match 越高（FiD Figure 3）。[FID:fid-r03] 但原始 RAG 的 RAG-Token 增加文件數後反而下降。[RAG:rag-r06] 所以 k 越大不一定越好。
- 畫面：原創「多個 encoder → 一個 decoder」示意圖；不放跨論文數字比較。

Wiki：[FiD paper](../wiki/papers/fid.md)、[Fusion-in-Decoder](../wiki/concepts/fusion-in-decoder.md)、[Multi-passage fusion](../wiki/concepts/multi-passage-fusion.md)、[Top-k evaluation](../wiki/concepts/top-k-evaluation.md)

## Slide 8

**Retrieval failure：答錯了，是誰的錯？**（1 分鐘）

虛構範例（同一題）。可切換四種情境：

| 情境 | 取回的 chunks | 回答 | 問題出在 |
| --- | --- | --- | --- |
| 沒找到 | K4、K5 | 「不確定」或亂猜 | Retriever（claim recall 低） |
| 找到沒用 | K1、K3 | 只答「2015 年」 | Generator（context utilization 低） |
| 被雜訊帶偏 | K2、K3 | 「2012 年通車」 | Generator（relevant noise sensitivity） |
| 無中生有 | K1 | 「紅線最先開」 | Generator（hallucination） |

- 真實論文的例子：dense retrieval 可能漏掉罕見關鍵詞，BM25 反而找得到。[DPR:dpr-c10]
- 無 JS 時：顯示完整表格。

Wiki：[RAG error attribution](../wiki/concepts/rag-error-attribution.md)、[Retrieval diagnostics](../wiki/concepts/retrieval-diagnostics.md)、[Generation diagnostics](../wiki/concepts/generation-diagnostics.md)、[DPR paper](../wiki/papers/dpr.md)

## Slide 9

**為什麼要分開評估 retrieval 與 generation？**（0.75 分鐘）

- 檢索分數：Top-k accuracy 只問「有沒有找到含答案的 passage」。[DPR:dpr-c09]
- 最終答案分數：Exact Match 只問「答案字串對不對」。[FID:fid-c09]
- 兩者不同：DPR 在 Natural Questions 的 end-to-end Exact Match 是 41.5 vs BM25 32.6（DPR Table 4），和 Slide 4 的 Top-20 accuracy 不是同一個指標。[DPR:dpr-r04]
- 只看 end-to-end 分數，無法知道錯在哪一步。RAGChecker 以此為研究動機。[RAGCHECKER:ragchecker-c01]

Wiki：[Top-k evaluation](../wiki/concepts/top-k-evaluation.md)、[Claim-level evaluation](../wiki/concepts/claim-level-evaluation.md)、[DPR paper](../wiki/papers/dpr.md)

## Slide 10

**Self-RAG：決定何時找，並檢查自己的回答**（1 分鐘）

- 問題：每次都固定檢索，可能帶進不需要或離題的內容。[SELF-RAG:self-rag-c01] 找到相關資料，也不保證回答會忠於它。[SELF-RAG:self-rag-c03]
- 四種 reflection tokens：Retrieve（要不要找）、IsRel（相關嗎）、IsSup（有支持嗎）、IsUse（有用嗎）。[SELF-RAG:self-rag-c04]
- 這些 tokens 是訓練出來的預測，推論時不需要另外的 critic。[SELF-RAG:self-rag-c17] **不是可靠的內省。**
- 結果（Self-RAG Table 2，ASQA citation）：Self-RAG 13B 的 precision 70.3／recall 71.3，Ret-ChatGPT 是 65.1／76.6。precision 較高，recall 較低。[SELF-RAG:self-rag-r03]
- 畫面：原創 Decide → Retrieve → Generate → Critique → Select loop。

Wiki：[Self-RAG paper](../wiki/papers/self-rag.md)、[Adaptive retrieval](../wiki/concepts/adaptive-retrieval.md)、[Reflection tokens](../wiki/concepts/reflection-tokens.md)、[Citation quality](../wiki/concepts/citation-quality.md)

## Slide 11

**RAGChecker：用 claims 診斷錯誤**（1 分鐘）

- 把回答與標準答案拆成 claims，逐一檢查是否被 chunks 支持。[RAGCHECKER:ragchecker-c03]
- Retriever 指標：claim recall、context precision。[RAGCHECKER:ragchecker-c09]
- Generator 指標：faithfulness、noise sensitivity、hallucination 等。[RAGCHECKER:ragchecker-c12]
- 結果（RAGChecker Table 3，10 datasets 平均，固定 GPT-4）：BM25 → E5-Mistral，claim recall 74.0 → 83.5，F1 50.3 → 52.7。[RAGCHECKER:ragchecker-r05]
- 但同樣換 retriever 後，四個 generators 的 relevant noise sensitivity 都上升。[RAGCHECKER:ragchecker-r09]
- 可信度：與人類判斷的 Pearson correlation（overall）61.93，人類之間是 70.09。[RAGCHECKER:ragchecker-r01] 並非每一欄都勝過 baseline。[RAGCHECKER:ragchecker-r03]
- 畫面：原創 claim 分類圖；一張小長條圖只放 Table 3 的 GPT-4 兩列。

Wiki：[RAGChecker paper](../wiki/papers/ragchecker.md)、[Claim-level evaluation](../wiki/concepts/claim-level-evaluation.md)、[Retrieval diagnostics](../wiki/concepts/retrieval-diagnostics.md)、[Generation diagnostics](../wiki/concepts/generation-diagnostics.md)、[RAG meta evaluation](../wiki/concepts/rag-meta-evaluation.md)

## Slide 12

**設計取捨：什麼時候不該多找？**（0.75 分鐘）

- 更多 context：claim recall 和 faithfulness 上升，但雜訊也變多（RAGChecker 作者觀察）。[RAGCHECKER:ragchecker-c27]
- 檢索門檻：Self-RAG 提高 retrieval threshold 時，PubHealth 的準確率變化小，PopQA 下降較多（Self-RAG Figure 3(c)）。[SELF-RAG:self-rag-r07]
- 不能同時最佳化：prompt 要求更忠實時，context utilization 上升，noise sensitivity 卻變差。[RAGCHECKER:ragchecker-c28]
- 成本：passage 很多時的效率仍是 FiD 作者列出的未解問題。[FID:fid-c14]
- 結論（整理）：沒有一組「最佳 k」；要看任務、資料和你在意的指標。

Wiki：[Adaptive retrieval](../wiki/concepts/adaptive-retrieval.md)、[Generation diagnostics](../wiki/concepts/generation-diagnostics.md)、[Top-k evaluation](../wiki/concepts/top-k-evaluation.md)、[Chunk](../wiki/concepts/chunk.md)

## Slide 13

**小測驗（3 題）**（1 分鐘）

1. 某次回答漏了重要資訊，而且 claim recall 很低。最可能是哪個模組的問題？
   - 答案：Retriever。需要的資訊根本沒被找回。[RAGCHECKER:ragchecker-c05]
2. DPR 在所有資料集都比 BM25 好？
   - 答案：不是。SQuAD 的 Top-20 accuracy 是 BM25 較高。[DPR:dpr-r02]
3. Self-RAG 的 IsSup token 代表模型「確實知道」回答有證據支持？
   - 答案：不是。它是訓練出來的 token 預測，標註來自 GPT-4 蒸餾，仍需外部評估。[SELF-RAG:self-rag-c06] [SELF-RAG:self-rag-c02]
- 互動：選項點擊後顯示對錯與解釋；無 JS 時答案放在可展開區塊。

Wiki：[RAG error attribution](../wiki/concepts/rag-error-attribution.md)、[DPR paper](../wiki/papers/dpr.md)、[Reflection tokens](../wiki/concepts/reflection-tokens.md)

## Slide 14

**總結與 sources**（0.5 分鐘）

- DPR 找 evidence → RAG 用 evidence → FiD 融合更多 → Self-RAG 決定何時找並自我檢查 → RAGChecker 診斷錯在哪（整理，不代表後者全面勝過前者）。
- 帶走一句話：RAG 答錯時，先問「是沒找到，還是沒用好？」
- 可展開的 sources：五篇 arXiv 連結（DPR v3、RAG v4、FiD v2、Self-RAG v1、RAGChecker v2）與 Wiki 連結。

Wiki：[五篇總覽](../wiki/comparisons/five-paper-overview.md)、[DPR paper](../wiki/papers/dpr.md)、[RAG paper](../wiki/papers/rag.md)、[FiD paper](../wiki/papers/fid.md)、[Self-RAG paper](../wiki/papers/self-rag.md)、[RAGChecker paper](../wiki/papers/ragchecker.md)
