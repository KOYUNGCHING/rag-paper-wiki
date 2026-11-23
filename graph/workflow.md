# RAG Paper Wiki workflow

本圖依 `logs/runs/001–011` 的實際執行順序更新（Run 011）。虛線節點是實際發生過的
修正或例外路徑，旁註對應的 run。

## 實際流程

```mermaid
flowchart TD
    A[選擇下一篇核心論文] --> B[查證 arXiv 版本]
    B --> C{Agent 能下載 PDF？}
    C -- 否：proxy 403（Run 009） --> C2[使用者在本機下載]
    C -- 是 --> D[驗證 PDF：hash／頁數／加密／JS]
    C2 --> D
    D --> E[文字抽取 + 關鍵圖表渲染檢查]
    E --> F[寫 proposal、更新 manifest 為 proposed、run log]
    F --> G[停止，等待使用者]
    G --> H{使用者核准？}
    H -- 「下一步」 --> I[approved：建立 paper note、evidence JSON]
    I --> J[新增／更新 concept 與 comparison pages]
    J --> K{validate_wiki.py}
    K -- 失敗（Run 002：README 範例被當成 citation） --> L[修正來源，不放寬 validator]
    L --> K
    K -- 通過 --> M[verified：run log、建議 Git commands，停止]
    M --> N{五篇皆 verified？}
    N -- 否 --> A
    N -- 是 --> O[Milestone A：reconciliation]
    O --> P{validate_project.py}
    P -- 失敗（Run 011：run_id 八進位、rag.md 來源宣告） --> Q[修正 validator 或 Wiki]
    Q --> P
    P -- 通過 --> R[test_fixture 驗證 validator 能抓錯]
    R --> S[術語對照、過時句清理、reflection]
    S --> T[Milestone B：slides-src 大綱 + Wiki mapping]
    T --> U{使用者核准大綱？}
    U -- 修改 --> T
    U -- 核准 --> V[Milestone C：docs/ HTML 簡報]
    V --> W{validators + 導覽／版面／無 JS 檢查}
    W -- 不合格 --> X[回到對應 Wiki、outline 或 slide]
    X --> T
    W -- 通過 --> Y[使用者 commit、push、發布 Pages]

    style C2 stroke-dasharray: 5 5
    style L stroke-dasharray: 5 5
    style Q stroke-dasharray: 5 5
```

T 之後的節點尚未執行，是預定流程。

## 實際 run 順序

| Run | 操作 | 論文 | 狀態轉移 | 真實 failure |
| --- | --- | --- | --- | --- |
| 001 | proposal | DPR | not_started → proposed | — |
| 002 | ingest | DPR | approved → verified | validator：README 範例 citation |
| 003 | proposal | RAG | not_started → proposed | — |
| 004 | ingest | RAG | approved → verified | —（`rag.md` 來源宣告錯誤在此產生，Run 011 才發現） |
| 005 | proposal | FiD | not_started → proposed | — |
| 006 | ingest | FiD | approved → verified | — |
| 007 | proposal | Self-RAG | not_started → proposed | — |
| 008 | ingest | Self-RAG | approved → verified | — |
| 009 | proposal | RAGChecker | not_started → proposed | 環境：arXiv 被 proxy 擋 |
| 010 | ingest | RAGChecker | approved → verified | —（論文內部不一致 4 項） |
| 011 | reconciliation | 全部 | — | validator bug + Wiki 來源宣告錯誤 |

## 三個主要 loop

1. **Ingest loop**（A → N）：逐篇提案、人工核准、ingest，五篇各跑一次。
2. **Validation loop**（K／P）：失敗時修正來源或 validator，再重跑；從未以放寬規則
   來通過。
3. **Slide review loop**（T → W → X）：尚未執行。

## 責任分工

- **Human**：核准每篇 proposal、大綱與最終成果；本專案中也負責在 agent 無法連線時
  下載 PDF，並自行 commit／push。
- **Agent**：閱讀、摘要、跨論文綜合、教學設計與語意修正。
- **Python validators**：`validate_wiki.py`（evidence、citation、link）、
  `validate_project.py`（manifest、lifecycle、來源宣告、slide mapping）、
  `test_validators.py`（test_fixture，證明 validators 會失敗）。
