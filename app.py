import streamlit as st
from gtts import gTTS
import os

# --- पेजची रचना आणि टायटल ---
st.set_page_config(page_title="Alliwar AI Voice Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Alliwar AI Voice Studio (V2.0)")
st.write("भारतातील १२ प्रमुख भाषांमध्ये एकदम नॅचरल AI आवाज तयार करा! 🚀")

st.markdown("---")

# --- विभाग १: १२ भाषांची निवड ---
st.subheader("🌐 १. भाषा निवडा (Select Language)")

languages = {
    "मराठी (Marathi)": "mr",
    "हिंदी (Hindi)": "hi",
    "इंग्रजी (English - India)": "en",
    "तमिळ (Tamil)": "ta",
    "तेलगू (Telugu)": "te",
    "कन्नड (Kannada)": "kn",
    "मळयाळम (Malayalam)": "ml",
    "गुजराती (Gujarati)": "gu",
    "बंगाली (Bengali)": "bn",
    "पंजाबी (Punjabi)": "pa",
    "उर्दू (Urdu)": "ur",
    "ओडिया (Odia)": "or"
}

selected_lang = st.selectbox("तुमची भाषा निवडा:", list(languages.keys()))
lang_code = languages[selected_lang]

# --- विभाग २: स्क्रिप्ट इनपुट ---
st.markdown("---")
st.subheader("📝 २. तुमची स्क्रिप्ट इथे टाका (Enter Script)")
text_input = st.text_area(
    "खाली तुमची कथा किंवा संवाद पेस्ट करा:",
    placeholder="तुम्ही निवडलेल्या भारतीय भाषेत इथे स्क्रिप्ट लिहा...",
    height=150
)

# --- विभाग ३: ऑडिओ जनरेशन ---
st.markdown("---")
if st.button("🚀 आवाज तयार करा (Generate Audio)"):
    if not text_input.strip():
        st.warning("⚠️ कृपया आधी वरच्या बॉक्समध्ये स्क्रिप्ट लिहा!")
    else:
        with st.spinner("⏳ तुमच्या भाषेत AI आवाज तयार होत आहे, थोडी वाट पाहा..."):
            output_file = "alliwar_v2_voice.mp3"
            
            try:
                tts = gTTS(text=text_input.strip(), lang=lang_code, slow=False)
                tts.save(output_file)
                
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    st.success("🎉 १२ भाषांच्या ब्ल्यूप्रिंटनुसार आवाज यशस्वीरित्या तयार झाला!")
                    
                    with open(output_file, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    st.download_button(
                        label="📥 MP3 फाईल डाऊनलोड करा",
                        data=audio_bytes,
                        file_name=f"alliwar_{lang_code}_voice.mp3",
                        mime="audio/mp3"
                    )
                    os.remove(output_file)
                else:
                    st.error("❌ ऑडिओ फाईल तयार होऊ शकली नाही.")
                
            except Exception as e:
                st.error(f"❌ या भाषेत तांत्रिक अडचण आली: {str(e)}")

# --- विभाग ४: क्रेडिट्स ---
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #f1f1f1; padding: 12px; border-radius: 8px; text-align: center;">
        <p style="margin: 0; color: #333; font-weight: bold;">Created by Son of Alliwar | V2.0 Smart Studio</p>
    </div>
    """,
    unsafe_allow_html=True
)
