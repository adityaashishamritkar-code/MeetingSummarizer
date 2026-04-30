from typing import List
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline

class TranscriptionEngine:
    def __init__(self, hf_token: str):
        self.whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        
        self.diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=hf_token
        )
    
    def process(self, audio_path: str) -> List[dict]:
        output = self.diarization_pipeline(audio_path)
        
        if hasattr(output, 'speaker_diarization'):
            diarization = output.speaker_diarization
        elif hasattr(output, 'annotation'):
            diarization = output.annotation
        else:
            diarization = output

        segments, _ = self.whisper_model.transcribe(audio_path, beam_size=5)
        transcript_list = list(segments)

        final_segments = []
        for segment in transcript_list:

            if len(segment.text.strip()) < 5: 
                continue

            midpoint = (segment.start + segment.end) / 2
            speaker = "Unknown"

            for turn, _, speaker_label in diarization.itertracks(yield_label=True):
                if turn.start <= midpoint <= turn.end:
                    speaker = speaker_label
                    break
            
            final_segments.append({
                "speaker": speaker,
                "text": segment.text.strip(),
                "start": segment.start,
                "end": segment.end
            })
            
        return final_segments

""
