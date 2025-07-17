import streamlit as st
from core.assistant import AI_Assistant
import asyncio
import time


def main():
    st.title("AI-Powered Receptionist")
    st.markdown(
        "Welcome to our AI-powered receptionist. Click 'Start Interaction' to begin a voice conversation."
    )

    if "assistant" not in st.session_state:
        st.session_state.assistant = AI_Assistant()
        st.session_state.transcribing = False
        st.session_state.last_speech_time = None
        st.session_state.query_sent = False

    assistant = st.session_state.assistant

    history_container = st.empty()
    question_container = st.empty()
    answer_container = st.empty()

    if st.button("Start Interaction", key="start_interaction"):
        if not st.session_state.transcribing:
            st.session_state.transcribing = True
            st.session_state.query_sent = False
            assistant.start_transcription()
            question_container.markdown("**Listening...** Please speak your query.")
            answer_container.markdown("")
        else:
            st.session_state.transcribing = False
            assistant.stop_transcription()
            question_container.markdown(
                "**Interaction stopped.** Click 'Start Interaction' to begin again."
            )
            answer_container.markdown("")

    if st.session_state.transcribing:
        # Show real-time transcript if available
        current_transcript = (
            assistant.transcription_handler.client.transcript
            if assistant.transcription_handler.client
            else ""
        )
        if current_transcript:
            st.session_state.last_speech_time = time.time()
            question_container.markdown(f"**Current Question**: {current_transcript}")
        else:
            if (
                st.session_state.last_speech_time
                and time.time() - st.session_state.last_speech_time > 3
                and not st.session_state.query_sent
            ):
                st.session_state.query_sent = True
                st.session_state.transcribing = False
                assistant.stop_transcription()
                question_container.markdown("**Finalizing question...**")

    if assistant.full_transcript:
        latest_assistant_message = next(
            (
                msg
                for msg in reversed(assistant.full_transcript)
                if msg["role"] == "assistant"
            ),
            None,
        )
        if latest_assistant_message and st.session_state.query_sent:
            answer_container.markdown(
                f"**Answer**: {latest_assistant_message['content']}"
            )

    if st.button("Interrupt and Ask New Question", key="interrupt"):
        if st.session_state.transcribing:
            assistant.stop_transcription()
        st.session_state.transcribing = True
        st.session_state.query_sent = False
        st.session_state.last_speech_time = None
        assistant.current_transcript = ""
        assistant.start_transcription()
        question_container.markdown(
            "**Interrupted. Listening for new query...** Please speak your question or topic."
        )
        answer_container.markdown("")

    with history_container.container():
        st.subheader("Conversation History")
        if assistant.full_transcript:
            for message in assistant.full_transcript:
                if message["role"] == "user":
                    st.markdown(f"**You**: {message['content']}")
                elif message["role"] == "assistant":
                    st.markdown(f"**AI Receptionist**: {message['content']}")
                    st.markdown("---")
        else:
            st.markdown("No conversation history yet.")


if __name__ == "__main__":
    main()
