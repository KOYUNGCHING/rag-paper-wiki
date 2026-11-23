---
concept_id: rag-error-attribution
status: verified
verified_sources:
  - ragchecker
---

# RAG error attribution：是沒找到，還是沒用好？

RAGChecker 把 response 錯誤分成兩類：

- **Retrieval errors**：retriever 沒有找回完整、相關的 context。
- **Generator errors**：context 裡有相關資訊，但 generator 沒有辨認或利用。
  [RAGCHECKER:ragchecker-c05]

對應的使用者也不同：要選系統的 user 需要單一 F1；要修系統的 developer 需要模組化指標。
[RAGCHECKER:ragchecker-c05]

## 教學範例（`wiki_synthesis`）

以下是本 Wiki 為教學自行設計的範例，用來說明指標如何對應，不是論文中的實例。
正式定義見 [Retrieval diagnostics](retrieval-diagnostics.md) 與
[Generation diagnostics](generation-diagnostics.md)。

「青嶼市」是**虛構城市**，以下內容全部是教學用假資料，不是事實，也不是論文資料。

問題：「青嶼市的捷運何時通車？哪一條線最先開？」ground truth 有兩個 claims：
A（2015 年通車）與 B（藍線最先開）。

虛構知識庫（chunks）：

| Chunk | 內容 | 相對於問題 |
| --- | --- | --- |
| K1 | 青嶼市捷運於 2015 年通車，首條營運路線為藍線。 | relevant（含 A、B） |
| K2 | 青嶼市捷運原計畫 2012 年完工，因工程延誤延後通車。 | relevant（含 A 的背景，也含可誤導的「2012」） |
| K3 | 藍線連接青嶼車站與港區，全長 12 公里。 | relevant（含 B 的路線資訊） |
| K4 | 綠線於 2019 年加入營運。 | irrelevant（不含 A、B） |
| K5 | 青嶼市公車路網於 1998 年重整。 | irrelevant |

這份假資料用於簡報的完整互動 RAG 範例與 retrieval-failure 範例。

| 情境 | 現象 | 主要反映的指標 |
| --- | --- | --- |
| Chunks 只含 A | B 根本沒被找回 | Claim recall 低（retrieval error） |
| Chunks 含 A 與 B，但回答只寫 A | 有資料卻沒用 | Context utilization 低（generator error） |
| 含 A 的 chunk 也提到錯誤的「計畫年份」，回答採用了它 | 被同 chunk 雜訊帶偏 | Relevant noise sensitivity |
| 回答寫了 chunks 裡都沒有的錯誤路線 | 無來源的錯誤 | Hallucination |

## 邊界

- 分類依賴 LLM extractor／checker 的判斷。[RAGCHECKER:ragchecker-c16]
- RAGChecker 不區分 Neutral 與 Contradiction。[RAGCHECKER:ragchecker-c22]

相關頁面：[RAG](rag.md)、[Retriever](retriever.md)、[Generator](generator.md)。
