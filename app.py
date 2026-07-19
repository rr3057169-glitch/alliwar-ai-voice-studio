import streamlit as st
from elevenlabs.client import ElevenLabs
import os

# १. पेज कॉन्फिगरेशन आणि डिझाईन
st.set_page_config(
    page_title="Alliwar Multilingual Voice Studio 3.5", 
    page_icon="🎙️", 
    layout="wide"
)

# मुख्य टायटल
st.title("🎙️ Alliwar Multilingual Voice Studio 3.5")
st.write("१२+ भारतीय भाषा (मराठी, हिंदी, तमिळ इ.) + ग्लोबल आवाज, व्हॉईस क्लोनिंग आणि ऑटो-व्हॉइस!")

st.markdown("---")
st.header("🔑 ElevenLabs API Key")

# स्क्रीनवर रिकामी स्पेस ठेवली आहे जेणेकरून आधीच एरर येणार नाही
user_api_key = st.text_input(
    "तुमची ElevenLabs API Key इथे पेस्ट करा:", 
    type="password",
    placeholder="इथे sk_... ने सुरू होणारी की पेस्ट करा"
)

# जोपर्यंत युझर स्वतः बटन दाबत नाही, तोपर्यंत बॅकएंडला की जाणार नाही (नो एरर)
client = None
if user_api_key.strip():
    try:
        client = ElevenLabs(api_key=user_api_key.strip())
    except:
        pass

# की आणि बॅलन्स चेक करण्याचे बटन
if st.button("🔍 Check Key & Balance"):
    if client:
        try:
            user_info = client.user.get_subscription()
            character_count = user_info.character_count
            character_limit = user_info.character_limit
            remaining = character_limit - character_count
            st.success(f"🔑 API Key यशस्वीरित्या कनेक्ट झाली! शिल्लक अक्षरे: {remaining}/{character_limit}")
        except Exception as e:
            st.error("❌ चुकीची किंवा एक्सपायर झालेली की! कृपया ElevenLabs वरून पुन्हा कॉपी करा.")
    else:
        st.warning("कृपया आधी बॉक्समध्ये API Key पेस्ट करा.")

st.markdown("---")

# 👥 २. व्हॉईस क्लोनिंग (Voice Cloning)
st.header("👥 Voice Cloning (स्वतःचा आवाज बनवा)")
uploaded_file = st.file_uploader("तुमची सॅम्पल ऑडिओ फाईल अपलोड करा (MP3/WAV):", type=["mp3", "wav"])
cloned_voice_name = st.text_input("क्लोन केलेल्या आवाजाला नाव द्या:", value="My Cloned Voice")

if st.button("👥 Create Cloned Voice"):
    if client:
        if uploaded_file is not None:
            with st.spinner("तुमचा आवाज क्लोन केला जात आहे..."):
                try:
                    with open("temp_sample.wav", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    voice = client.clone(
                        name=cloned_voice_name,
                        description="Cloned via Alliwar Studio",
                        files=["temp_sample.wav"]
                    )
                    st.success(f"🎉 '{cloned_voice_name}' आवाज यशस्वीरित्या तयार झाला!")
                    if os.path.exists("temp_sample.wav"):
                        os.remove("temp_sample.wav")
                except Exception as e:
                    st.error(f"व्हॉईस क्लोनिंग करताना एरर आला: {e}")
        else:
            st.warning("कृपया आधी एक ऑडिओ फाईल अपलोड करा.")
    else:
        st.error("कृपया आधी वरती एक व्हॅलिड API Key टाका.")

st.markdown("---")

# 💬 ३. स्क्रिप्ट आणि व्हॉईस सेटिंग्स
st.header("💬 Script & Voice Settings")
st.subheader("🎭 Dialogue #1")

# आवाज लोड करण्याची सुरक्षित सिस्टीम
selected_voice_id = "21m00Tcm4TlvDq8ikWAM" # डिफॉल्ट (Rachel)
if client:
    try:
        voices_data = client.voices.get_all()
        voice_labels = [f"{v.name} ({v.voice_id})" for v in voices_data.voices]
        selected_voice_label = st.selectbox("आवाज निवडा (#1):", options=voice_labels)
        selected_voice_id = selected_voice_label.split("(")[-1].replace(")", "")
    except:
        st.selectbox("आवाज निवडा (#1):", options=["Default (Rachel)"])
else:
    st.selectbox("आवाज निवडा (#1):", options=["Default (Rachel) - आधी API Key टाका"])

script_text = st.text_area("तुमची स्क्रिप्ट लिहा (मराठी, हिंदी किंवा इंग्लिश मध्ये) (#1):", placeholder="इथे टाईप करा...")

# 🚀 ४. फायनल ऑडिओ जनरेशन
if st.button("Generate Complete Audio File 🚀", type="primary"):
    if client:
        if script_text.strip() != "":
            with st.spinner("ऑडिओ तयार होत आहे..."):
                try:
                    audio = client.generate(
                        text=script_text,
                        voice=selected_voice_id,
                        model="eleven_multilingual_v2"
                    )
                    audio_bytes = b"".join(audio)
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        label="📥 ऑडिओ डाऊनलोड करा", 
                        data=audio_bytes, 
                        file_name="alliwar_studio_output.mp3", 
                        mime="audio/mp3"
                    )
                    st.success("🎉 ऑडिओ यशस्वीरित्या तयार झाला!")
                except Exception as e:
                    st.error(f"ऑडिओ जनरेट करताना एरर आला: {e}")
        else:
            st.warning("कृपया आधी स्क्रिप्ट बॉक्समध्ये काहीतरी लिहा.")
    else:
        st.error("कृपया आधी वरती एक व्हॅलिड API Key टाका.")
