from notion_client import Client
from app.models import MeetingAnalysis

class NotionExporter:
    def __init__(self, auth_token: str, database_id: str):
        self.notion = Client(auth=auth_token)
        self.database_id = database_id

    def export(self, analysis: MeetingAnalysis, title: str):
        new_page = self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
                "Category": {"select": {"name": "Lecture/Meeting Summary"}}
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Summary"}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": analysis.summary}}]}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Action Items"}}]}
                }
            ]
        )

        todo_blocks = []
        for item in analysis.action_items:
            content = f"{item.task} (Assignee: {item.assignee or 'Unassigned'})"
            todo_blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": content}}],
                    "checked": False
                }
            })

        self.notion.blocks.children.append(block_id=new_page["id"], children=todo_blocks)
        return new_page["url"]
    
    ""