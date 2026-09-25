from datetime import datetime, timezone
from typing import get_args
from uuid import UUID

import pytest
from pydantic import ValidationError

from signaldesk_contracts import (
    DiagnosticCompletedV1,
    DiagnosticRequestedV1,
    DiagnosticTerminalV2,
    EmailRequestedV1,
    Event,
    ExportCompletedV1,
    ExportRequestedV1,
    NotificationRequestedV1,
    REDIS_STREAM_BY_EVENT_TYPE,
    parse_event_json,
)


EVENT_ID = UUID("00000000-0000-4000-8000-000000000001")
CORRELATION_ID = UUID("00000000-0000-4000-8000-000000000002")
ORGANIZATION_ID = UUID("00000000-0000-4000-8000-000000000003")
DIAGNOSTIC_JOB_ID = UUID("00000000-0000-4000-8000-000000000004")
EMAIL_DELIVERY_ID = UUID("00000000-0000-4000-8000-000000000005")
EXPORT_JOB_ID = UUID("00000000-0000-4000-8000-000000000006")
NOTIFICATION_ID = UUID("00000000-0000-4000-8000-000000000007")
OCCURRED_AT = datetime(2026, 7, 22, 22, 15, tzinfo=timezone.utc)


def test_diagnostic_requested_round_trips_through_json() -> None:
    event = DiagnosticRequestedV1(
        schema_version=1,
        event_id=EVENT_ID,
        event_type="diagnostic.requested.v1",
        occurred_at=OCCURRED_AT,
        correlation_id=CORRELATION_ID,
        organization_id=ORGANIZATION_ID,
        diagnostic_job_id=DIAGNOSTIC_JOB_ID,
    )

    assert DiagnosticRequestedV1.model_validate_json(event.model_dump_json()) == event


def test_diagnostic_completed_round_trips_through_json() -> None:
    event = DiagnosticCompletedV1(
        schema_version=1,
        event_id=EVENT_ID,
        event_type="diagnostic.completed.v1",
        occurred_at=OCCURRED_AT,
        correlation_id=CORRELATION_ID,
        organization_id=ORGANIZATION_ID,
        diagnostic_job_id=DIAGNOSTIC_JOB_ID,
    )

    assert DiagnosticCompletedV1.model_validate_json(event.model_dump_json()) == event


def test_diagnostic_terminal_round_trips_through_json() -> None:
    event = DiagnosticTerminalV2(
        schema_version=1,
        event_id=EVENT_ID,
        event_type="diagnostic.terminal.v2",
        occurred_at=OCCURRED_AT,
        correlation_id=CORRELATION_ID,
        organization_id=ORGANIZATION_ID,
        diagnostic_job_id=DIAGNOSTIC_JOB_ID,
        status="failed",
    )

    assert DiagnosticTerminalV2.model_validate_json(event.model_dump_json()) == event


def test_email_requested_round_trips_through_json() -> None:
    event = EmailRequestedV1(
        schema_version=1,
        event_id=EVENT_ID,
        event_type="email.requested.v1",
        occurred_at=OCCURRED_AT,
        correlation_id=CORRELATION_ID,
        organization_id=ORGANIZATION_ID,
        email_delivery_id=EMAIL_DELIVERY_ID,
    )

    assert EmailRequestedV1.model_validate_json(event.model_dump_json()) == event


def test_export_requested_round_trips_through_json() -> None:
    event = ExportRequestedV1(
        schema_version=1,
        event_id=EVENT_ID,
        event_type="export.requested.v1",
        occurred_at=OCCURRED_AT,
        correlation_id=CORRELATION_ID,
        organization_id=ORGANIZATION_ID,
        export_job_id=EXPORT_JOB_ID,
    )

    assert ExportRequestedV1.model_validate_json(event.model_dump_json()) == event


def test_export_completed_round_trips_through_json() -> None:
    event = ExportCompletedV1(
        schema_version=1,
        event_id=EVENT_ID,
        event_type="export.completed.v1",
        occurred_at=OCCURRED_AT,
        correlation_id=CORRELATION_ID,
        organization_id=ORGANIZATION_ID,
        export_job_id=EXPORT_JOB_ID,
    )

    assert ExportCompletedV1.model_validate_json(event.model_dump_json()) == event


def test_notification_requested_round_trips_through_json() -> None:
    event = NotificationRequestedV1(
        schema_version=1,
        event_id=EVENT_ID,
        event_type="notification.requested.v1",
        occurred_at=OCCURRED_AT,
        correlation_id=CORRELATION_ID,
        organization_id=ORGANIZATION_ID,
        notification_id=NOTIFICATION_ID,
    )

    assert NotificationRequestedV1.model_validate_json(event.model_dump_json()) == event


def test_naive_timestamp_is_rejected() -> None:
    with pytest.raises(ValidationError, match="timezone-aware"):
        DiagnosticRequestedV1(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="diagnostic.requested.v1",
            occurred_at=datetime(2026, 7, 22, 22, 15),
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            diagnostic_job_id=DIAGNOSTIC_JOB_ID,
        )


def test_python_input_is_validated_strictly() -> None:
    with pytest.raises(ValidationError, match="UUID"):
        DiagnosticRequestedV1.model_validate(
            {
                "schema_version": 1,
                "event_id": str(EVENT_ID),
                "event_type": "diagnostic.requested.v1",
                "occurred_at": OCCURRED_AT,
                "correlation_id": CORRELATION_ID,
                "organization_id": ORGANIZATION_ID,
                "diagnostic_job_id": DIAGNOSTIC_JOB_ID,
            }
        )


def test_extra_field_is_rejected() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        DiagnosticRequestedV1.model_validate(
            {
                "schema_version": 1,
                "event_id": EVENT_ID,
                "event_type": "diagnostic.requested.v1",
                "occurred_at": OCCURRED_AT,
                "correlation_id": CORRELATION_ID,
                "organization_id": ORGANIZATION_ID,
                "diagnostic_job_id": DIAGNOSTIC_JOB_ID,
                "unexpected": "not envelope metadata",
            }
        )


@pytest.mark.parametrize(
    "event",
    [
        DiagnosticRequestedV1(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="diagnostic.requested.v1",
            occurred_at=OCCURRED_AT,
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            diagnostic_job_id=DIAGNOSTIC_JOB_ID,
        ),
        DiagnosticCompletedV1(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="diagnostic.completed.v1",
            occurred_at=OCCURRED_AT,
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            diagnostic_job_id=DIAGNOSTIC_JOB_ID,
        ),
        DiagnosticTerminalV2(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="diagnostic.terminal.v2",
            occurred_at=OCCURRED_AT,
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            diagnostic_job_id=DIAGNOSTIC_JOB_ID,
            status="completed",
        ),
        EmailRequestedV1(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="email.requested.v1",
            occurred_at=OCCURRED_AT,
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            email_delivery_id=EMAIL_DELIVERY_ID,
        ),
        ExportRequestedV1(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="export.requested.v1",
            occurred_at=OCCURRED_AT,
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            export_job_id=EXPORT_JOB_ID,
        ),
        ExportCompletedV1(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="export.completed.v1",
            occurred_at=OCCURRED_AT,
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            export_job_id=EXPORT_JOB_ID,
        ),
        NotificationRequestedV1(
            schema_version=1,
            event_id=EVENT_ID,
            event_type="notification.requested.v1",
            occurred_at=OCCURRED_AT,
            correlation_id=CORRELATION_ID,
            organization_id=ORGANIZATION_ID,
            notification_id=NOTIFICATION_ID,
        ),
    ],
)
def test_parse_event_json_discriminates_supported_events(event: Event) -> None:
    parsed = parse_event_json(event.model_dump_json())

    assert parsed == event
    assert type(parsed) is type(event)


def diagnostic_requested_data() -> dict[str, object]:
    return {
        "schema_version": 1,
        "event_id": EVENT_ID,
        "event_type": "diagnostic.requested.v1",
        "occurred_at": OCCURRED_AT,
        "correlation_id": CORRELATION_ID,
        "organization_id": ORGANIZATION_ID,
        "diagnostic_job_id": DIAGNOSTIC_JOB_ID,
    }


def test_unsupported_schema_version_is_rejected() -> None:
    event = DiagnosticRequestedV1.model_validate(diagnostic_requested_data())
    unsupported_json = event.model_dump_json().replace(
        '"schema_version":1', '"schema_version":2'
    )

    with pytest.raises(ValidationError, match="schema_version"):
        parse_event_json(unsupported_json)


def test_unsupported_event_type_is_rejected() -> None:
    event = DiagnosticRequestedV1.model_validate(diagnostic_requested_data())
    unsupported_json = event.model_dump_json().replace(
        '"event_type":"diagnostic.requested.v1"',
        '"event_type":"diagnostic.requested.v2"',
    )

    with pytest.raises(ValidationError, match="diagnostic.requested.v2"):
        parse_event_json(unsupported_json)


@pytest.mark.parametrize(
    "field_name",
    [
        "target",
        "recipient",
        "rendered_body",
        "export_data",
        "object_key",
        "object_path",
        "credential",
        "credentials",
        "token",
        "secret",
    ],
)
def test_authoritative_or_sensitive_fields_are_rejected(field_name: str) -> None:
    event_data = diagnostic_requested_data()
    event_data[field_name] = "must be re-fetched from the authoritative service"

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        DiagnosticRequestedV1.model_validate(event_data)


def diagnostic_terminal_data() -> dict[str, object]:
    return {
        "schema_version": 1,
        "event_id": EVENT_ID,
        "event_type": "diagnostic.terminal.v2",
        "occurred_at": OCCURRED_AT,
        "correlation_id": CORRELATION_ID,
        "organization_id": ORGANIZATION_ID,
        "diagnostic_job_id": DIAGNOSTIC_JOB_ID,
        "status": "failed",
    }


@pytest.mark.parametrize("status", ["completed", "failed"])
def test_diagnostic_terminal_accepts_terminal_statuses(status: str) -> None:
    event_data = diagnostic_terminal_data()
    event_data["status"] = status

    assert DiagnosticTerminalV2.model_validate(event_data).status == status


@pytest.mark.parametrize("status", ["pending", "running", "FAILED", ""])
def test_diagnostic_terminal_rejects_non_terminal_status(status: str) -> None:
    event_data = diagnostic_terminal_data()
    event_data["status"] = status

    with pytest.raises(ValidationError, match="status"):
        DiagnosticTerminalV2.model_validate(event_data)


def test_diagnostic_terminal_requires_status() -> None:
    event_data = diagnostic_terminal_data()
    del event_data["status"]

    with pytest.raises(ValidationError, match="status"):
        DiagnosticTerminalV2.model_validate(event_data)


@pytest.mark.parametrize("field_name", ["outcome", "error_code", "result", "recipient"])
def test_diagnostic_terminal_rejects_result_data(field_name: str) -> None:
    event_data = diagnostic_terminal_data()
    event_data[field_name] = "must be re-fetched from the authoritative service"

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        DiagnosticTerminalV2.model_validate(event_data)


def test_notification_requested_rejects_recipient_data() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        NotificationRequestedV1.model_validate(
            {
                "schema_version": 1,
                "event_id": EVENT_ID,
                "event_type": "notification.requested.v1",
                "occurred_at": OCCURRED_AT,
                "correlation_id": CORRELATION_ID,
                "organization_id": ORGANIZATION_ID,
                "notification_id": NOTIFICATION_ID,
                "recipient": "must be re-fetched from the authoritative service",
            }
        )


def test_event_type_versions_are_distinct_contracts() -> None:
    terminal_json = DiagnosticTerminalV2.model_validate(
        diagnostic_terminal_data()
    ).model_dump_json()

    with pytest.raises(ValidationError, match="diagnostic.terminal.v1"):
        parse_event_json(
            terminal_json.replace(
                '"event_type":"diagnostic.terminal.v2"',
                '"event_type":"diagnostic.terminal.v1"',
            )
        )


def test_redis_stream_mapping_covers_exactly_the_supported_events() -> None:
    (event_union, _discriminator) = get_args(Event)
    supported_event_types = {
        get_args(model.model_fields["event_type"].annotation)[0]
        for model in get_args(event_union)
    }

    assert set(REDIS_STREAM_BY_EVENT_TYPE) == supported_event_types
    assert dict(REDIS_STREAM_BY_EVENT_TYPE) == {
        "diagnostic.requested.v1": "signaldesk:diagnostics",
        "diagnostic.completed.v1": "signaldesk:diagnostic-completions",
        "diagnostic.terminal.v2": "signaldesk:diagnostic-terminals",
        "email.requested.v1": "signaldesk:emails",
        "export.requested.v1": "signaldesk:exports",
        "export.completed.v1": "signaldesk:export-completions",
        "notification.requested.v1": "signaldesk:notifications",
    }
    assert len(set(REDIS_STREAM_BY_EVENT_TYPE.values())) == len(
        REDIS_STREAM_BY_EVENT_TYPE
    )


def test_redis_stream_mapping_is_read_only() -> None:
    with pytest.raises(TypeError):
        REDIS_STREAM_BY_EVENT_TYPE["unknown.v1"] = "signaldesk:unknown"  # type: ignore[index]
