import streamlit as st
from gtts import gTTS
import os
from audiorecorder import audiorecorder

# --- पेजची रचना आणि प्रीमियम लुक ---
st.set_page_config(page_title="Alliwar AI Voice Studio", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #FF4B4B; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 16px; text-align: center; color: #555555; margin-bottom: 25px; }
    .studio-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎙️ Alliwar AI Voice Studio (Ultimate V4.0)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">१२ भारतीय भाषा, एआय व्हॉईस जनरेटर आणि लाईव्ह स्क्रिप्ट रेकॉर्डर! 🚀</div>', unsafe_allow_html=True)

# --- मुख्य स्क्रिप्ट इनपुट विभाग ---
st.subheader("📝 १. तुमची स्क्रिप्ट इथे लिहा (Enter Your Script)")

if 'saved_script' not in st.session_state:
    st.session_state.saved_script = ""

use_saved = st.checkbox("💾 माझी आधीची सेव्ह केलेली स्क्रिप्ट लोड करा")
default_text = st.session_state.saved_script if (use_saved and st.session_state.saved_script) else ""

text_input = st.text_area(
    "खाली तुमची कथा, संवाद किंवा व्हिडिओ स्क्रिप्ट लिहा:",
    value=default_text,
    placeholder="इथे स्क्रिप्ट टाईप करा, हीच स्क्रिप्ट खाली वाचून रेकॉर्ड करता येईल किंवा AI आवाज बनवता येईल...",
    height=120
)

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    if st.button("💾 स्क्रिप्ट सेव्ह करा"):
        if text_input.strip():
            st.session_state.saved_script = text_input.strip()
            st.success("सेव्ह झाली!")
        else:
            st.warning("आधी काहीतरी लिहा!")

st.markdown("---")

# --- दोन कॉलम्सची रचना ---
col1, col2 = st.columns(2)

# --- डावा कॉलम: AI व्हॉईस जनरेटर ---
with col1:
    st.markdown('<div class="studio-box">', unsafe_allow_html=True)
    st.subheader("🤖 गुगल AI आवाज तयार करा")
    
    languages = {
        "मराठी (Marathi)": "mr", "हिंदी (Hindi)": "hi", "इंग्रजी (English - India)": "en",
        "तमिळ (Tamil)": "ta", "तेलगू (Telugu)": "te", "कन्नड (Kannada)": "kn",
        "मळयाळम (Malayalam)": "ml", "गुजराती (Gujarati)": "gu", "बंगाली (Bengali)": "bn",
        "पंजाबी (Punjabi)": "pa", "उर्दू (Urdu)": "ur", "ओडिया (Odia)": "or"
    }
    selected_lang = st.selectbox("भाषा निवडा:", list(languages.keys()))
    lang_code = languages[selected_lang]
    
    speed_option = st.radio("वेग (Speed):", ("हळू (Slow)", "नॉर्मल (Normal)"), index=1, horizontal=True)
    is_slow = True if speed_option == "हळू (Slow)" else False
    
    if st.button("🚀 AI आवाज बनवा"):
        if not text_input.strip():
            st.warning("⚠️ कृपया आधी वर स्क्रिप्ट लिहा!")
        else:
            with st.spinner("⏳ AI आवाज तयार होत आहे..."):
                output_file = "alliwar_ai.mp3"
                try:
                    tts = gTTS(text=text_input.strip(), lang=lang_code, slow=is_slow)
                    tts.save(output_file)
                    
                    with open(output_file, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(label="📥 AI MP3 डाऊनलोड", data=audio_bytes, file_name=f"ai_{lang_code}.mp3", mime="audio/mp3")
                    os.remove(output_file)
                except Exception as e:
                    st.error(f"एरर: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- उजवा कॉलम: लाईव्ह व्हॉईस रेकॉर्डर ---
with col2:
    st.markdown('<div class="studio-box">', unsafe_allow_html=True)
    st.subheader("🎙️ स्वतःचा आवाज रेकॉर्ड करा")
    st.info("💡 वर लिहिलेली स्क्रिप्ट पाहून खालील बटण दाबून स्वतःच्या आवाजात रेकॉर्डिंग सुरू करा!")
    
    # लाईव्ह रेकॉर्डर कॉम्पोनंट
    audio = audiorecorder("🔴 रेकॉर्डिंग सुरू करा (Record)", "⏹️ रेकॉर्डिंग थांबवा (Stop)")
    
    if len(audio) > 0:
        st.success("✅ रेकॉर्डिंग पूर्ण झाले आहे!")
        st.audio(audio.export().read(), format="audio/wav")
        st.download_button(
            label="📥 तुमचे रेकॉर्डिंग डाऊनलोड करा (WAV)",
            data=audio.export().read(),
            file_name="my_recorded_voice.wav",
            mime="audio/wav"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# --- विभाग ५: क्रेडिट्स ---
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #FF4B4B;">
        <p style="margin: 0; color: #FFFFFF; font-weight: bold; letter-spacing: 1px;">⚡ Powered by Son of Alliwar | Ultimate Studio V4.0 ⚡</p>
    </div>
    """,
    unsafe_allow_html=True
)
