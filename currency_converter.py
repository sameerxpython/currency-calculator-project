import streamlit as st
import requests
import speech_recognition as sr

st.set_page_config(page_title="Currency Converter", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #C0C9EE;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("\U0001f4b1 Currency Converter")

if "amount_val" not in st.session_state:
    st.session_state.amount_val = 1.0
if "base_val" not in st.session_state:
    st.session_state.base_val = "USD"
if "target_val" not in st.session_state:
    st.session_state.target_val = "INR"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... (say something like 'Convert 100 USD to INR')")
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError:
            st.error("Speech recognition service unavailable.")
        return ""


if st.button("Use Voice Input"):
    spoken_text = recognize_speech()
    if "convert" in spoken_text.lower():
        words = spoken_text.upper().split()
        try:
            idx = words.index("CONVERT")
            amount = float(words[idx + 1])
            base = words[idx + 2]
            to_idx = words.index("TO")
            target = words[to_idx + 1]

            st.session_state.amount_val = amount
            st.session_state.base_val = base
            st.session_state.target_val = target
        except Exception:
            st.warning("Could not parse your input. Try saying: 'Convert 100 USD to INR'.")

amount = st.number_input("Enter amount: ", min_value=0.0, step=1.0, key="amount_val")
base = st.selectbox("From Currency:", ["USD", "EUR", "INR", "GBP", "JPY", "CAD"], key="base_val")
target = st.selectbox("To Currency:", ["USD", "EUR", "INR", "GBP", "JPY", "CAD"], key="target_val")

if st.button("Convert"):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{st.session_state.base_val}"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"].get(st.session_state.target_val)

        if rate:
            result = round(st.session_state.amount_val * rate, 2)
            st.success(f"{st.session_state.amount_val} {st.session_state.base_val} = {result} {st.session_state.target_val}")
        else:
            st.error("Currency not supported.")
    except Exception as e:
        st.error("Something went wrong while fetching exchange rates.")
