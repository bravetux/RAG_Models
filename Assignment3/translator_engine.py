import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import uuid

# Language Mapping
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "French": "fr",
    "Arabic": "ar"
}

# Speech Recognition Language Codes (BCP-47)
SR_LANG_CODES = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "French": "fr-FR",
    "Arabic": "ar-SA"
}

def recognize_speech_from_mic(audio_data, language_name):
    """
    Recognizes speech from audio data.
    """
    recognizer = sr.Recognizer()
    lang_code = SR_LANG_CODES.get(language_name, "en-US")
    
    try:
        # Convert audio_data (bytes) to AudioData object if needed
        # In this app, we might valid path or bytes. 
        # For simplicity with streamlit-audiorecorder, we usually save to file first or process bytes.
        # Let's assume we pass a file path for now to be robust.
        with sr.AudioFile(audio_data) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=lang_code)
            return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def translate_text(text, target_language_name):
    """
    Translates text to target language.
    """
    target_code = LANGUAGES.get(target_language_name, "en")
    try:
        translator = GoogleTranslator(source='auto', target=target_code)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        return f"Translation Error: {e}"

def text_to_speech(text, target_language_name):
    """
    Converts text to speech and returns the file path.
    """
    target_code = LANGUAGES.get(target_language_name, "en")
    try:
        tts = gTTS(text=text, lang=target_code, slow=False)
        filename = f"temp_output_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(os.getcwd(), filename)
        tts.save(filepath)
        return filepath
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
