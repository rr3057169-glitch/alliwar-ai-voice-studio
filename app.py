import streamlit as st
from gtts import gTTS
import os

# --- पेजची रचना आणि टायटल ---
st.set_page_config(page_title="Alliwar AI Voice Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Alliwar AI Voice Studio (V1.0)")
st.write("गुगल एआय इंजिनद्वारे भारतातील सर्व प्रमुख भाषांमध्ये आवाज तयार करा! 🔥")

st.markdown("---")

# --- विभाग १: भाषा निवडणे ---
st.subheader("🌐 १. भाषा निवडा (Select Language)")

# गुगल व्हॉईससाठी सोपी भाषा रचना
languages = {
    "मराठी (Marathi)": "mr",
    "हिंदी (Hindi)": "hi",
    "इंग्रजी (English - India)": "en"
}

selected_lang = st.selectbox("भाषा निवडा (Select Language):", list(languages.keys()))
lang_code = languages[selected_lang]

# --- विभाग २: स्क्रिप्ट इनपुट ---
st.markdown("---")
st.subheader("📝 २. तुमची स्क्रिप्ट इथे टाका (Enter Script)")
text_input = st.text_area(
    "खाली तुमची कथा किंवा संवाद पेस्ट करा (Type or Paste here):",
    placeholder="तुम्ही निवडलेल्या भाषेत इथे स्क्रिप्ट लिहा...",
    height=150
)

# --- विभाग ३: प्ले आणि डाऊनलोड ---
st.markdown("---")
if st.button("🚀 आवाज तयार करा (Generate Audio)"):
    if not text_input.strip():
        st.warning("⚠️ कृपया आधी वरच्या बॉक्समध्ये स्क्रिप्ट लिहा!")
    else:
        with st.spinner("⏳ गुगल AI आवाज तयार होत आहे, थोडी वाट पाहा..."):
            output_file = "alliwar_google_voice.mp3"
            
            try:
                # गुगल टीटीएस इंजिन (एकदम सरळ आणि सोपं)
                tts = gTTS(text=text_input.strip(), lang=lang_code, slow=False)
                tts.save(output_file)
                
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    st.success("🎉 आवाज यशस्वीरित्या तयार झाला आहे!")
                    
                    with open(output_file, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    st.download_button(
                        label="📥 MP3 फाईल डाऊनलोड करा",
                        data=audio_bytes,
                        file_name="alliwar_ai_voice.mp3",
                        mime="audio/mp3"
                    )
                    os.remove(output_file)
                else:
                    st.error("❌ ऑडिओ फाईल तयार होऊ शकली नाही. कृपया पुन्हा प्रयत्न करा.")
                
            except Exception as e:
                st.error(f"❌ तांत्रिक अडचण आली: {str(e)}")

# --- विभाग ४: सपोर्ट ---
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center;">
        <h4>☕ Support Alliwar Studio</h4>
        <p>If this tool is helping you in your content creation, feel free to support us!</p>
    </div>
    """,
    unsafe_allow_html=True
)
