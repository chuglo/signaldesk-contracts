from datetime import datetime, timezone
from uuid import UUID

import pytest
from pydantic import ValidationError

from signaldesk_contracts import (
    DiagnosticCompletedV1,
    DiagnosticRequestedV1,
    EmailRequestedV1,
    Event,
    ExportCompletedV1,
    ExportRequestedV1,
    parse_event_json,
)


EVENT_ID = UUID("00000000-0000-4000-8000-000000000001")
CORRELATION_ID = UUID("00000000-0000-4000-8000-000000000002")
ORGANIZATION_ID = UUID("00000000-0000-4000-8000-000000000003")
DIAGNOSTIC_JOB_ID = UUID("00000000-0000-4000-8000-000000000004")
EMAIL_DELIVERY_ID = UUID("00000000-0000-4000-8000-000000000005")
EXPORT_JOB_ID = UUID("00000000-0000-4000-8000-000000000006")
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
