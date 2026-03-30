class WorkflowError(Exception):
    """Base domain exception for workflow execution failures."""


class AgentExecutionError(WorkflowError):
    """Raised when a workflow agent cannot complete its task."""
