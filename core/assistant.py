from dotenv import load_dotenv
import os
from .transcription import TranscriptionHandler
from .ai_response import AIResponseGenerator
from .audio import AudioOutput


class AI_Assistant:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Initialize components
        self.transcription_handler = TranscriptionHandler(self)
        self.response_generator = AIResponseGenerator(self)
        self.audio_output = AudioOutput()

        # Transcript history
        self.full_transcript = [
            {
                "role": "system",
                "content": "You are a chatbot. Provide concise, direct, and efficient responses to user queries, using few words.",
            },
        ]

    def start_transcription(self):
        self.transcription_handler.start_transcription()

    def stop_transcription(self):
        self.transcription_handler.stop_transcription()

    def generate_audio(self, text):
        self.audio_output.generate_audio(text)

    def generate_ai_response(self, transcript):
        self.response_generator.generate_ai_response(transcript)
