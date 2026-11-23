# Execution logs

每次 proposal、ingest、lint、revision 或 slides review 都要在 `logs/runs/`
留下可讀紀錄。建議檔名為 `<run-id>-<operation>.md`。

每份 run log 至少包含：

```yaml
run_id: null
operation: null
source: null
started_at: null
input_state: null
checks_before_fix: []
findings: []
action_taken: []
checks_after_fix: []
files_changed: []
status: null
```

只記錄真實執行結果。若使用故意破壞的測試資料，必須明確標記為
`test_fixture`，不得冒充實際 ingest 失敗。

