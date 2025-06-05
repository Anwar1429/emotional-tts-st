import streamlit as st
import edge_tts
import asyncio
import tempfile

st.set_page_config(page_title="Emotion TTS 🎙️", layout="centered")
st.title("🎤 Microsoft Edge TTS with Emotions")

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

gender = st.radio("Choose Voice Gender", ["Female", "Male"], index=0)
voice = VOICE_MAP[gender]["voice"]
style_options = ["general"] + VOICE_MAP[gender]["styles"]
style = st.selectbox("Choose Emotion Style", style_options)
rate = st.slider("Speech Rate (%)", min_value=50, max_value=150, value=100)
text = st.text_area("Enter the text you want to convert to speech:", height=150)

if st.button("Generate Audio"):
    if not text:
        st.warning("Please enter some text.")
    else:

        # Build SSML input:
        if style == "general":
            ssml_text = text
        else:
            ssml_text = f"""
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="{voice}">
    <express-as style="{style}">
      {text}
    </express-as>
  </voice>
</speak>
"""

        async def generate():
            temp_path = tempfile.mktemp(suffix=".mp3")
            communicate = edge_tts.Communicate(ssml_text, voice=voice, rate=f"{rate-100}%")
            await communicate.save(temp_path)
            return temp_path

        try:
            audio_path = asyncio.run(generate())
            st.success(f"Voice: {voice}, Style: {style}")
            st.audio(audio_path, format="audio/mp3")
        except Exception as e:
            st.error(f"Error generating audio: {e}")
