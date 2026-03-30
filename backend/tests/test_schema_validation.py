import pytest
from pydantic import ValidationError

from app.schemas.workflow import WorkflowRequest


def test_workflow_request_rejects_short_title() -> None:
    with pytest.raises(ValidationError):
        WorkflowRequest(
            title='abc',
            objective='This objective is long enough to pass validation constraints.',
            constraints=[],
            output_format='both',
        )


def test_workflow_request_rejects_short_objective() -> None:
    with pytest.raises(ValidationError):
        WorkflowRequest(
            title='Valid workflow title',
            objective='short',
            constraints=[],
            output_format='both',
        )


def test_workflow_request_accepts_valid_payload() -> None:
    payload = WorkflowRequest(
        title='Research student productivity app launch strategy',
        objective='Define a focused and practical 90-day go-to-market plan for student users.',
        constraints=['small team', 'limited budget'],
        output_format='both',
    )

    assert payload.output_format == 'both'
    assert payload.constraints == ['small team', 'limited budget']
