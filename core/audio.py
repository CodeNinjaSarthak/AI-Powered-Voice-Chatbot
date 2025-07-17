import os


class AudioOutput:
    def generate_audio(self, text):
        print(f"\nAI Receptionist: {text}")
        os.system(f'say "{text}"')
