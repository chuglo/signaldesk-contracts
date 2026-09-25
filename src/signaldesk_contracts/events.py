"""Strict, versioned event contracts shared by SignalDesk services."""

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator


class _EventBase(BaseModel):
    """Correlation envelope common to every SignalDesk event."""

    model_config = ConfigDict(extra="forbid", strict=True)

    schema_version: Literal[1]
    event_id: UUID
    occurred_at: datetime
    correlation_id: UUID
    organization_id: UUID

    @field_validator("occurred_at")
    @classmethod
    def require_timezone_aware_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurred_at must be timezone-aware")
        return value


class DiagnosticRequestedV1(_EventBase):
    """A request to process an authoritative diagnostic job."""

    event_type: Literal["diagnostic.requested.v1"]
    diagnostic_job_id: UUID


class DiagnosticCompletedV1(_EventBase):
    """A notice that an authoritative diagnostic job completed."""

    event_type: Literal["diagnostic.completed.v1"]
    diagnostic_job_id: UUID


class EmailRequestedV1(_EventBase):
    """A request to process an authoritative email delivery."""

    event_type: Literal["email.requested.v1"]
    email_delivery_id: UUID


class ExportRequestedV1(_EventBase):
    """A request to process an authoritative export job."""

    event_type: Literal["export.requested.v1"]
    export_job_id: UUID


class ExportCompletedV1(_EventBase):
    """A notice that an authoritative export job completed."""

    event_type: Literal["export.completed.v1"]
    export_job_id: UUID


Event = Annotated[
    DiagnosticRequestedV1
    | DiagnosticCompletedV1
    | EmailRequestedV1
    | ExportRequestedV1
    | ExportCompletedV1,
    Field(discriminator="event_type"),
]

_EVENT_ADAPTER = TypeAdapter(Event)


def parse_event_json(data: str | bytes | bytearray) -> Event:
    """Parse JSON into the event selected by its versioned event type."""

    return _EVENT_ADAPTER.validate_json(data)
