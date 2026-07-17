import streamlit as st
import asyncio
import edge_tts
import os

# --- पेजची रचना आणि टायटल ---
st.set_page_config(page_title="Alliwar AI Voice Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Alliwar AI Voice Studio (V1.0)")
st.write("भारतातील सर्व प्रमुख भाषांमध्ये एकदम नॅचरल AI आवाज तयार करा! 🔥")

st.markdown("---")

# --- विभाग १: भाषा आणि कॅरेक्टर निवडणे ---
st.subheader("🌐 १. भाषा आणि आवाज निवडा (Select Language & Voice)")

# सर्व भारतीय भाषा आणि त्यांचे अधिकृत AI आवाज (Male/Female)
languages = {
    "मराठी (Marathi)": {
        "👩 काव्या (Kavya - Female)": "mr-IN-KavyaNeural",
        "👨 मधुर (Madhur - Male)": "mr-IN-MadhurNeural"
    },
    "हिंदी (Hindi)": {
        "👩 मधूरम (Madhuram - Female)": "hi-IN-MadhuramNeural",
        "👨 मधुर (Madhur - Male)": "hi-IN-MadhurNeural"
    },
    "इंग्रजी (English - India)": {
        "👩 न्युरा (Neerja - Female)": "en-IN-NeerjaNeural",
        "👨 प्रबात (Prabhat - Male)": "en-IN-PrabhatNeural"
    },
    "तमिळ (Tamil)": {
        "👩 पल्लवी (Pallavi - Female)": "ta-IN-PallaviNeural",
        "👨 वल्लुवर (Valluvar - Male)": "ta-IN-ValluvarNeural"
    },
    "तेलगू (Telugu)": {
        "👩 श्रुती (Shruti - Female)": "te-IN-ShrutiNeural",
        "👨 मोहन (Mohan - Male)": "te-IN-MohanNeural"
    },
    "कन्नड (Kannada)": {
        "👩 सपिना (Sapna - Female)": "kn-IN-SapnaNeural",
        "👨 गगन (Gagan - Male)": "kn-IN-GaganNeural"
    },
    "गुजराती (Gujarati)": {
        "👩 ध्वनी (Dhwani - Female)": "gu-IN-DhwaniNeural",
        "👨 निरंजन (Niranjan - Male)": "gu-IN-NiranjanNeural"
    },
    "बंगाली (Bengali)": {
        "👩 तनिषा (Tanisha - Female)": "bn-IN-TanishaNeural",
        "👨 प्रदिप (Pradeep - Male)": "bn-IN-PradeepNeural"
    },
    "मल्याळम (Malayalam)": {
        "👩 शोभना (Sobhana - Female)": "ml-IN-SobhanaNeural",
        "👨 मिधुन (Midhun - Male)": "ml-IN-MidhunNeural"
    },
    "पंजाबी (Punjabi)": {
        "👩 हरप्रीत (Harpreet - Female)": "pa-IN-HarpreetNeural",
        "👨 बलविंदर (Balwinder - Male)": "pa-IN-AnwarNeural"
    },
    "उर्दू (Urdu - India)": {
        "👩 गुली (Gul - Female)": "ur-IN-GulNeural",
        "👨 सलमान (Salman - Male)": "ur-IN-SalmanNeural"
    }
}

col1, col2 = st.columns(2)

with col1:
    selected_lang = st.selectbox("भाषा निवडा (Select Language):", list(languages.keys()))

with col2:
    available_voices = languages[selected_lang]
    selected_voice_name = st.selectbox("कोणाचा आवाज हवा? (Select Voice Character):", list(available_voices.keys()))

voice_code = available_voices[selected_voice_name]

# --- विभाग २: स्क्रिप्ट इनपुट ---
st.markdown("---")
st.subheader("📝 २. तुमची स्क्रिप्ट इथे टाका (Enter Script)")
text_input = st.text_area(
    "खाली तुमची कथा किंवा संवाद पेस्ट करा (Type or Paste here):",
    placeholder="तुम्ही निवडलेल्या भाषेत इथे स्क्रिप्ट लिहा...",
    height=150
)

# --- विभाग ३: स्पीड CONTROL ---
st.subheader("⚡ ३. आवाजाचा वेग (Speed Control)")
speed_option = st.slider(
    "वेग कमी-जास्त करा:",
    min_value=0.5,
    max_value=1.5,
    value=1.0,
    step=0.1
)

speed_percent = int((speed_option - 1.0) * 100)
speed_str = f"{speed_percent:+d}%" if speed_percent != 0 else "+0%"

# --- ऑडिओ जनरेशनचे फंक्शन ---
async def generate_voice(text, voice, speed, output_filename):
    communicate = edge_tts.Communicate(text, voice, rate=speed)
    await communicate.save(output_filename)

# --- विभाग ४: प्ले आणि डाऊनलोड ---
st.markdown("---")
if st.button("🚀 आवाज तयार करा (Generate Audio)"):
    if not text_input.strip():
        st.warning("⚠️ कृपया आधी वरच्या बॉक्समध्ये स्क्रिप्ट लिहा!")
    else:
        with st.spinner("⏳ AI आवाज तयार होत आहे, थोडी वाट पाहा..."):
            output_file = "alliwar_voice.mp3"
            
            try:
                asyncio.run(generate_voice(text_input, voice_code, speed_str, output_file))
                
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
                
            except Exception as e:
                st.error(f"❌ तांत्रिक अडचण आली: {str(e)}")

# --- विभाग ५: सपोर्ट ---
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center;">
        <h4>☕ Support Alliwar Studio</h4>
        <p>If this tool is helping you in your content creation, feel free to support us!</p>
        <a href="https://payment-link-or-upi" target="_blank" style="text-decoration: none;">
            <div style="background-color: #FF813F; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; display: inline-block;">
                🏆 सपोर्ट करा / Donate UPI
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
