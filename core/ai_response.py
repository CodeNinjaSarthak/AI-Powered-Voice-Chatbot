import google.generativeai as genai
import os


class AIResponseGenerator:
    def __init__(self, assistant):
        self.assistant = assistant
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_ai_response(self, transcript):
        self.assistant.stop_transcription()

        self.assistant.full_transcript.append(
            {"role": "user", "content": transcript.transcript}
        )
        print(f"\nClient: {transcript.transcript}\n")

        prompt_text = "Respond concisely while being clear and helpful:\n"
        for msg in self.assistant.full_transcript:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt_text += f"[System Instruction]: {content}\n"
            elif role == "user":
                prompt_text += f"Client: {content}\n"
            elif role == "assistant":
                prompt_text += f"{content}\n"

        try:
            response = self.model.generate_content(prompt_text)
            ai_response = response.text.strip()
        except genai.exceptions.GenerationError as e:
            if "429" in str(e):
                print(f"Gemini API quota exceeded: {e}")
                print(
                    "Please check your plan at https://ai.google.dev/gemini-api/docs/rate-limits or wait for the quota to reset."
                )
                ai_response = "I'm sorry, I've reached my request limit. Please try again later or contact the clinic directly."
            else:
                print(f"Error generating response from Gemini API: {e}")
                ai_response = (
                    "I'm sorry, I couldn't process your request. Please try again."
                )
        except Exception as e:
            print(f"Unexpected error from Gemini API: {e}")
            ai_response = (
                "I'm sorry, I couldn't process your request. Please try again."
            )

        self.assistant.generate_audio(ai_response)
        self.assistant.full_transcript.append(
            {"role": "assistant", "content": ai_response}
        )

        print("\nReal-time transcription:\n")
        self.assistant.start_transcription()
