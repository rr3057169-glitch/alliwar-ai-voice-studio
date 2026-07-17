
import streamlit as st
import asyncio
import edge_tts
import os
import html  # स्पेशल कॅरेक्टर्स फिक्स करण्यासाठी

# --- पेजची रचना आणि टायटल ---
st.set_page_config(page_title="Alliwar AI Voice Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Alliwar AI Voice Studio (V1.0)")
st.write("भारतातील सर्व प्रमुख भाषांमध्ये एकदम नॅचरल AI आवाज तयार करा! 🔥")

st.markdown("---")

# --- विभाग १: भाषा आणि कॅरेक्टर निवडणे ---
st.subheader("🌐 १. भाषा आणि आवाज निवडा (Select Language & Voice)")

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

# स्पीड स्ट्रिंग एकदम अचूक तयार करणे
speed_percent = int((speed_option - 1.0) * 100)
if speed_percent == 0:
    speed_str = "+0%"
else:
    speed_str = f"{speed_percent:+d}%"

# --- ऑडिओ जनरेशनचे मजबूत फंक्शन ---
async def generate_voice(text, voice, speed, output_filename):
    # १. आधी सर्व प्रकारचे नको असलेले कोड्स आणि अवतरण चिन्हे काढून टाकणे
    clean_text = text.replace('"', '').replace("'", "").replace("“", "").replace("”", "")
    clean_text = clean_text.replace('\n', ' ').replace('\r', ' ').strip()
    
    # २. मायक्रोसॉफ्ट सर्व्हरसाठी टेक्स्ट सुरक्षित (Escape) करणे
    safe_text = html.escape(clean_text)
    
    # ३. ऑडिओ जनरेट करणे
    communicate = edge_tts.Communicate(safe_text, voice, rate=speed)
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
                # सिस्टीमचा इव्हेंट लूप व्यवस्थित हाताळणे
                asyncio.run(generate_voice(text_input, voice_code, speed_str, output_file))
                
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
                    st.error("❌ ऑडिओ फाईल तयार झाली नाही, कृपया स्क्रिप्ट थोडी लहान करून पहा.")
                
            except Exception as e:
                st.error(f"❌ तांत्रिक अडचण आली: {str(e)}")

# --- विभाग ५: सपोर्ट ---
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
