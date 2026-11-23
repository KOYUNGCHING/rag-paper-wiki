# Reading proposals

正式 ingest 前，每篇論文都必須先建立一份閱讀計畫並由使用者確認。

檔名使用 `<paper-id>.md`，內容至少包含：

```yaml
paper_id: dpr
status: proposed
proposed_at: YYYY-MM-DD
approved_at: null
```

正文必須回答：

1. 論文想解決什麼問題？
2. Introduction 預計保留哪些重點？
3. 哪些 Results 值得納入 Wiki？
4. 這篇論文對 RAG 教學的用途是什麼？
5. 哪些表格、數字或比較條件最容易讀錯？

建立 `proposed` 版本後必須停止。只有收到使用者明確同意，才能將狀態改為
`approved` 並開始正式 Wiki ingest。

