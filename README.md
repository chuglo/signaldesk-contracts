# SignalDesk Contracts

**Not for production use.**

Strict, versioned event contracts shared by SignalDesk Python 3.11 services.

Every event is a strict Pydantic model (`extra="forbid"`) with a common envelope:
`schema_version` (always `1`), `event_id`, a timezone-aware `occurred_at`,
`correlation_id`, and `organization_id`. Events carry identifiers only; consumers
re-fetch authoritative state from the owning API.

| Event type | Model | Identifier | Redis stream |
|---|---|---|---|
| `diagnostic.requested.v1` | `DiagnosticRequestedV1` | `diagnostic_job_id` | `signaldesk:diagnostics` |
| `diagnostic.completed.v1` | `DiagnosticCompletedV1` | `diagnostic_job_id` | `signaldesk:diagnostic-completions` |
| `diagnostic.terminal.v2` | `DiagnosticTerminalV2` | `diagnostic_job_id`, `status` (`completed` or `failed`) | `signaldesk:diagnostic-terminals` |
| `email.requested.v1` | `EmailRequestedV1` | `email_delivery_id` | `signaldesk:emails` |
| `export.requested.v1` | `ExportRequestedV1` | `export_job_id` | `signaldesk:exports` |
| `export.completed.v1` | `ExportCompletedV1` | `export_job_id` | `signaldesk:export-completions` |
| `notification.requested.v1` | `NotificationRequestedV1` | `notification_id` | `signaldesk:notifications` |

`parse_event_json` validates JSON into the model selected by `event_type`, and
`REDIS_STREAM_BY_EVENT_TYPE` is a read-only map from each event type to its stream.

## License

MIT. See [LICENSE](LICENSE).
