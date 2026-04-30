import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, BackgroundTasks
from app.services.transcription import TranscriptionEngine
from app.services.processor import AIProcessor
from app.services.exporters import NotionExporter

app = FastAPI()

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")


# Initialize Services
engine = TranscriptionEngine(HF_TOKEN)
processor = AIProcessor(GROQ_KEY)
exporter = NotionExporter(NOTION_TOKEN, NOTION_DB_ID)

@app.post("/process-lecture")
async def process_lecture(file: UploadFile, background_tasks: BackgroundTasks):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    temp_path = os.path.join(upload_dir, file.filename)
    
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(full_pipeline, temp_path, file.filename)
    return {"message": "Processing started."}

def full_pipeline(path: str, filename: str):
    try:
        print(f"Starting transcription for {filename}...")
        utterances = engine.process(path)
        
        print("Extracting action items...")
        analysis = processor.analyze(utterances)
        
        print("Exporting to Notion...")
        page_url = exporter.export(analysis, title=f"Notes: {filename}")
        
        print(f"Success! View here: {page_url}")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)