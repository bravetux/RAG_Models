import streamlit as st
import os
import time
import numpy as np
from collections import deque
import sounddevice as sd
import io
import wave
from translator_engine import recognize_speech_from_mic, translate_text, text_to_speech, LANGUAGES

st.set_page_config(page_title="Voice Translator", page_icon="🎙️")

st.title("🎙️ Voice to Voice Translator")
st.markdown("Speak in one language and hear it in another!")

def record_audio(max_duration_seconds=15):
    """Records audio from the microphone for a specified duration with progress indication."""
    
    sample_rate = 16000  # Sample rate in Hz
    channels = 1       # Number of audio channels

    # --- UI Elements ---
    st.info(f"Recording for a maximum of {max_duration_seconds} seconds...")
    progress_bar = st.progress(0)
    
    # --- Recording Logic ---
    audio_data = deque()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            st.warning(f"Input status: {status}")
        audio_data.extend(indata[:, 0])
        
    try:
        with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback, dtype='float32'):
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                progress_value = min(1.0, elapsed_time / max_duration_seconds)
                progress_bar.progress(progress_value)

                if elapsed_time >= max_duration_seconds:
                    break
                time.sleep(0.1) # Update progress bar every 100ms
                
    except Exception as e:
        st.error(f"An error occurred during recording: {e}")
        return None

    st.success("Recording complete!")
    
    # --- Convert to WAV bytes ---
    if audio_data:
        audio_np = np.array(audio_data)
        # Normalize and convert to 16-bit PCM
        audio_int16 = (audio_np * 32767).astype(np.int16)
        
        wav_io = io.BytesIO()
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())
        
        wav_io.seek(0)
        return wav_io.getvalue()
        
    return None

# Sidebar for Language Selection
with st.sidebar:
    st.header("Settings")
    input_lang = st.selectbox("Input Language", list(LANGUAGES.keys()), index=0)
    output_lang = st.selectbox("Output Language", list(LANGUAGES.keys()), index=1)

# Audio Recorder
st.subheader("1. Record your Voice")
if st.button("Start Recording"):
    audio_bytes = record_audio()

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        # Save temp file for processing
        temp_input_path = "temp_input.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_bytes)

        # 2. Transcribe
        with st.spinner(f"Transcribing {input_lang}..."):
            text_input = recognize_speech_from_mic(temp_input_path, input_lang)
            
        if text_input:
            st.success("Transcription Complete!")
            st.text_area("Original Text", value=text_input, height=100, disabled=True)

            # 3. Translate
            with st.spinner(f"Translating to {output_lang}..."):
                translated_text = translate_text(text_input, output_lang)
                
            st.text_area("Translated Text", value=translated_text, height=100, disabled=True)

            # 4. Text to Speech
            if translated_text and not translated_text.startswith("Translation Error"):
                with st.spinner("Generating Audio..."):
                    output_audio_path = text_to_speech(translated_text, output_lang)
                    
                if output_audio_path:
                    st.subheader("Result Audio")
                    st.audio(output_audio_path, format="audio/mp3")
                    
        else:
            st.error("Could not understand audio. Please try again.")

        # Cleanup input
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
