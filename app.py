# app.py
import streamlit as st
import edge_tts
import asyncio
import tempfile

# ---------------- Setup ---------------- #
st.set_page_config(page_title="Emotion TTS 🎙️", layout="centered")
st.title("🎤 Microsoft Edge TTS with Emotions")
st.write("Choose gender, emotion, and enter your text to generate emotional speech.")

# ---------------- Voice & Style Options ---------------- #
VOICE_MAP = {
    "Female": {
        "voice": "en-US-JennyNeural",
        "styles": ["cheerful", "sad", "angry", "excited", "hopeful", "empathetic", "shouting", "whispering", "terrified"]
    },
    "Male": {
        "voice": "en-US-GuyNeural",
        "styles": ["cheerful", "sad", "angry", "excited", "shouting", "terrified"]
    }
}

# ---------------- User Input ---------------- #
gender = st.radio("Choose Voice Gender", ["Female", "Male"], index=0)
voice = VOICE_MAP[gender]["voice"]
style_options = ["general"] + VOICE_MAP[gender]["styles"]
style = st.selectbox("Choose Emotion Style", style_options)
rate = st.slider("Speech Rate (%)", min_value=50, max_value=150, value=100)
text = st.text_area("Enter the text you want to convert to speech:", height=150)

# ---------------- Generate Button ---------------- #
if st.button("Generate Audio"):
    if not text:
        st.warning("Please enter some text.")
    else:
        async def generate():
            temp_path = tempfile.mktemp(suffix=".mp3")
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=f"{rate - 100}%",
                style=None if style == "general" else style
            )
            await communicate.save(temp_path)
            return temp_path

        try:
            audio_path = asyncio.run(generate())
            st.success(f"Voice: {voice}, Style: {style}")
            st.audio(audio_path, format="audio/mp3")
        except Exception as e:
            st.error(f"Error generating audio: {e}")
