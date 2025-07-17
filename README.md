# 🗣️ AI Voice Receptionist  

**A Real-Time Conversational Voice Assistant using AssemblyAI + Gemini + macOS TTS**  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)  
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io)  

Developed by [Sarthak Chauhan](https://github.com/CodeNinjaSarthak)

## 🌟 Overview  

This project implements a **real-time AI-powered voice receptionist** with the following technology stack:  

- 🎙️ **AssemblyAI Streaming API** - Live speech-to-text transcription  
- 🤖 **Gemini 1.5 Flash** - Fast LLM-based response generation  
- 🔊 **macOS `say` command** - Native text-to-speech output  
- 🧵 **Streamlit UI** - Interactive interface with state management  

Ideal for: voice-enabled kiosks, front-desk automation, or hands-free virtual assistants.

## ⚙️ System Architecture  
<img width="1003" height="376" alt="image" src="https://github.com/user-attachments/assets/06032179-268a-4e30-9c05-7593ed8af31a" />


### Core Components  

1. **Speech Input**  
   - Real-time microphone streaming  
   - Uses AssemblyAI's BeginEvent and TurnEvent  
   - Finalizes input after 3 seconds of silence  

2. **LLM Processing**  
   - Gemini Flash with conversation history  
   - Optimized for low-latency responses  

3. **Speech Output**  
   - macOS native `say` command  
   - Instant text-to-speech conversion  

4. **Interruptions**  
   - Dedicated "Interrupt & Ask" button  
   - Cancels ongoing input  
   - Resets conversation state  

## ✨ Key Features  

- ⏱️ Sub-3 second response times  
- 🔁 Real-time streaming transcription  
- ✋ Clean interruption handling  
- 🗨️ Contextual conversation memory  
- 🖥️ Cross-platform compatible (customizable TTS)  

## 🛠️ Installation  

### Prerequisites  
- macOS (for native TTS)  
- Python 3.10+  
- Streamlit  

### Setup  

1. Clone the repository:  
   ```bash
   git clone https://github.com/CodeNinjaSarthak/AI-Powered-Voice-Chatbot.git
   cd AI-Powered-Voice-Chatbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set API keys - Create a .env file in root directory and paste the below:
```bash
ASSEMBLYAI_API_KEY=<YOUR_API_KEY>
GEMINI_API_KEY=<YOUR_API_KEY>
```
4. Run the application:
   ```bash
   streamlit run app.py
   ```
   
