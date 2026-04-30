from groq import Groq
from typing import List
from app.models import MeetingAnalysis
import json

class AIProcessor:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def analyze(self, utterances: List[dict]) -> MeetingAnalysis:
        formatted_transcript = "\n".join([f"{u['speaker']}: {u['text']}" for u in utterances])

        prompt = f"""
        Analyze the following transcript. 
        Return ONLY a JSON object with this exact structure:
        {{
        "summary": "A detailed overview of the meeting",
        "action_items": [
            {{"task": "The specific thing to do", "assignee": "Name", "priority": "High/Medium/Low"}}
        ]
        }}
        
        Transcript:
        {formatted_transcript}
        """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return MeetingAnalysis.model_validate_json(response.choices[0].message.content)
        
""