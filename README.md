# Meeting & Lecture Synthesizer
### Asynchronous Multi-Modal Audio Intelligence Pipeline

A robust, full-stack processing engine that transforms unstructured audio and video recordings into structured, actionable intelligence. By integrating Speaker Diarization (SD), Speech-to-Text (STT), and LLM Orchestration, this system automates the generation of executive summaries and task boards directly into Notion.

---

## System Architecture

The pipeline is engineered as a sequence of high-latency AI workloads managed by an asynchronous FastAPI backend to ensure system stability and a responsive user experience.

### 1. Diarization & Transcription Engine (The Extraction Layer)
This module decomposes raw multi-modal files into timestamped dialogue sequences.
* **Speaker Identification:** Utilizes Pyannote.audio 3.1 to generate voice-prints and identify distinct speakers in a shared audio space.
* **STT Processing:** Leverages Faster-Whisper (CTranslate2) for high-speed, high-accuracy transcription.
* **Temporal Alignment:** A custom alignment algorithm maps the midpoints of transcribed segments to diarization tracks, ensuring every sentence is attributed to the correct speaker.
* **Signal Filtering:** Implements DSP-inspired logic to prune segments with low character density, removing background noise and "ghost" speaker artifacts.

### 2. Cognitive Synthesis Engine (The Logic Layer)
Transforms raw dialogue into structured intelligence using Llama-3.3-70B.
* **Contextual Analysis:** Generates high-level executive summaries from the raw transcript.
* **Structured Extraction:** Applies complex prompt engineering to isolate action items, assignees, and task priorities.
* **Pydantic Validation:** Uses a strictly typed validation layer with AliasChoices to ensure non-deterministic LLM output perfectly matches the system schema.

### 3. Integration & Exporter Engine (The Delivery Layer)
Bridges local AI processing with professional productivity ecosystems.
* **Notion API Orchestration:** Translates validated JSON into Notion-specific block types (To-Do, Heading, Paragraph).
* **Automated Board Population:** Programmatically creates database entries and nested page content.
* **Asynchronous Dispatch:** Managed by FastAPI BackgroundTasks, allowing for immediate user confirmation while heavy API handshakes occur in the background.

---

## Technical Stack

* **Language:** Python 3.12+
* **AI & Machine Learning:**
    * Pyannote.audio 3.1 (Speaker Diarization)
    * Faster-Whisper (Speech-to-Text)
    * Llama-3.3-70B via Groq (Inference Optimization)
* **Backend:** FastAPI (Asynchronous API Management)
* **Frontend:** Streamlit (Human-Centric UI)
* **Integrations:** Notion SDK (Structured Persistence)
* **Data Validation:** Pydantic V2 (Schema Enforcement)
* **System Tools:** FFmpeg (Multi-modal Stream Decoding)

---

## Module Directory Breakdown

* `app/main.py`: Orchestrates the FastAPI server and handles asynchronous background task dispatching.
* `app/frontend.py`: Provides a Streamlit-based UI for file ingestion and real-time processing feedback.
* `app/models.py`: Defines the strict Pydantic schemas and validation aliases for data integrity.
* `app/services/transcription.py`: Manages ML models for speaker diarization and transcription alignment.
* `app/services/processor.py`: Interfaces with the Groq API for LLM-based summary and task extraction.
* `app/services/exporters.py`: Handles the mapping and transmission of data to the Notion API.

---

## Getting Started

### Prerequisites
* Python 3.12+
* FFmpeg installed on your system
* A Groq API Key and Notion Integration Token

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/MeetingSummarizer.git](https://github.com/your-username/MeetingSummarizer.git)
   cd MeetingSummarizer
2. Create a .env file in the root directory:
  GROQ_API_KEY=your_key_here
  NOTION_TOKEN=your_token_here
  NOTION_DB_ID=your_db_id_here
  HF_TOKEN=your_huggingface_token_here
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

### Running the app
Run the main file and streamlit concurrently, upload a file via teh Streamlit dashboard and check the updated notion database
