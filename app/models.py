from pydantic import BaseModel, Field, AliasChoices
from typing import List, Optional

class DialogueUtterance(BaseModel):
    speaker: str
    text: str
    start: float
    end: float

class ActionItem(BaseModel):
    task: str = Field(validation_alias=AliasChoices('task', 'item', 'description'))
    assignee: Optional[str] = Field(default="Unassigned", validation_alias=AliasChoices('assignee', 'owner', 'person'))
    priority: str = Field(default="Medium", validation_alias=AliasChoices('priority', 'urgency'))

class MeetingAnalysis(BaseModel):
    summary: str = Field(validation_alias=AliasChoices('summary', 'overview', 'executive_summary', 'description'))
    action_items: List[ActionItem] = Field(validation_alias=AliasChoices('action_items', 'tasks', 'todo_list'))
    full_transcript: Optional[List[dict]] = None

    ""