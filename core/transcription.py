import assemblyai as aai
from assemblyai.streaming.v3 import (
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    BeginEvent,
    TurnEvent,
    TerminationEvent,
)
import time
import os


class TranscriptionHandler:
    def __init__(self, assistant):
        self.assistant = assistant
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.client = None

    def start_transcription(self):
        if self.client:
            print("Cleaning up existing client before starting new session")
            self.stop_transcription()

        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=os.getenv("ASSEMBLYAI_API_KEY"),
                api_host="streaming.assemblyai.com",
            )
        )

        # Register event handlers
        self.client.on(StreamingEvents.Begin, self.on_begin)
        self.client.on(StreamingEvents.Turn, self.on_turn)
        self.client.on(StreamingEvents.Termination, self.on_terminated)
        self.client.on(StreamingEvents.Error, self.on_error)

        # Connect with streaming parameters
        try:
            self.client.connect(
                StreamingParameters(
                    sample_rate=16000,
                    format_turns=True,
                )
            )
            print("Please start speaking...")
            self.client.stream(aai.extras.MicrophoneStream(sample_rate=16000))
        except Exception as e:
            print(f"Error starting transcription: {e}")
            self.stop_transcription()

    def stop_transcription(self):
        if self.client:
            try:
                self.client.disconnect(terminate=True)
                print("Streaming client disconnected")
            except Exception as e:
                print(f"Error stopping transcription: {e}")
            finally:
                self.client = None
        time.sleep(0.5)

    def on_begin(self, client: StreamingClient, event: BeginEvent):
        print()

    def on_turn(self, client: StreamingClient, event: TurnEvent):
        if not event.transcript:
            return
        print(event.transcript, end="\r")
        if event.end_of_turn:
            self.assistant.generate_ai_response(event)

    def on_error(self, client: StreamingClient, error: StreamingError):
        print("An error occurred:", error)

    def on_terminated(self, client: StreamingClient, event: TerminationEvent):
        print(
            f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
        )
