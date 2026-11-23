# RAG Paper Wiki workflow

## 完整流程

```mermaid
flowchart TD
    A[與使用者確認專案規格] --> B[選擇下一篇核心論文]
    B --> C[保存來源資訊與本機 PDF]
    C --> D[Agent 提出閱讀計畫]
    D --> E{使用者核准？}
    E -- 修改 --> D
    E -- 核准 --> F[抽取 Introduction / Gap / Contributions / Results]
    F --> G{Evidence Validator}
    G -- 缺來源或定位 --> F
    G -- 通過 --> H[抽取 Method / Experiments / Limitations]
    H --> I[更新 paper note 與 concept pages]
    I --> J{Wiki lint}
    J -- 衝突、缺漏、壞連結 --> F
    J -- 通過 --> K{已驗證五篇？}
    K -- 否 --> B
    K -- 是 --> L[Query verified Wiki]
    L --> M[Agent 產生教學大綱]
    M --> N{Outline review}
    N -- 不合格 --> L
    N -- 使用者核准 --> O[產生 HTML 簡報]
    O --> P{內容、引用、導覽與版面檢查}
    P -- 不合格 --> Q[回到對應 Wiki、outline 或 slide 節點]
    Q --> L
    P -- 通過 --> R[完成紀錄與反思]
```

## 三個主要 loop

1. **Ingest loop**：逐篇提案、人工確認與 ingest，直到五篇皆完成。
2. **Wiki lint loop**：證據缺漏、概念矛盾或連結錯誤時回到原始論文修正。
3. **Slide review loop**：大綱或投影片未通過時重新查詢 Wiki，只重做受影響內容。

## 責任分工

- **Human**：核准每篇閱讀計畫、大綱與最終成果。
- **Agent**：閱讀、摘要、跨論文綜合、教學設計與語意修正。
- **Python validator**：schema、狀態、連結、引用、證據欄位及 slide mapping。

