import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Story Generator", page_icon="📖", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False



def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and email and password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.email = email
            st.rerun()
        else:
            st.error("Please enter username, email and password")



def logout():
    st.session_state.logged_in = False
    st.rerun()



def mainpage():
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    st.sidebar.write(f"Email: {st.session_state.email}")
    st.sidebar.button("Logout", on_click=logout)

    st.title("🏠 Main Page")
    st.subheader("🎬 Generate Your Story Plot")

    genre = st.selectbox("Select Genre", ["Fantasy", "Horror", "Sci-fi", "Romance"])
    character = st.text_input("Main Character Name")
    setting = st.text_input("Setting")
    tone = st.selectbox("Tone", ["serious", "funny", "dramatic", "romantic"])
    agegroup = st.selectbox("Age Group", ["kindergarden", "children", "teens", "adults"])

    if st.button("Generate Story Plot"):
        prompt = f"""
        Create a unique and creative story plot.

        Genre: {genre}
        Character: {character}
        Setting: {setting}
        Tone: {tone}
        Age Group: {agegroup}

        Give:
        1. Title
        2. Summary
        3. Main Conflict
        4. Twist
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_completion_tokens=500
        )

        story_plot = response.choices[0].message.content

        st.subheader("📖 Generated Story")
        st.write(story_plot)

        with open("story.txt", "w") as f:
            f.write(story_plot)


if st.session_state.logged_in:
    mainpage()
else:
    login()