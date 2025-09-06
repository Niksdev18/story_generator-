import streamlit as st
from story_engine import generate_story_segments
from image_generator import create_story_images
from export_utils import export_story_pdf
from config import OPENAI_API_KEY

st.set_page_config(page_title="Story Generator", layout="wide")
st.title("📖 AI-Powered Text-to-Image Story Generator")

# CSS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

prompt = st.text_input("Enter your story idea:")
genre = st.selectbox("Select genre:", ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Horror"])
tone = st.selectbox("Select tone:", ["Dark", "Lighthearted", "Epic", "Mysterious"])
audience = st.selectbox("Target audience:", ["Kids", "Teens", "Adults"])
art_style = st.selectbox("Choose art style:", ["Realistic", "Cartoon", "Watercolor", "Anime"])

if st.button("Generate Story"):
    if not prompt.strip():
        st.error("Please enter a story idea.")
    else:
        try:
            with st.spinner("Generating your story..."):
                segments = generate_story_segments(prompt, genre, tone, audience, OPENAI_API_KEY)
            with st.spinner("Generating images..."):
                images = create_story_images(segments, art_style, OPENAI_API_KEY)
            st.balloons()

            for idx, segment in enumerate(segments):
                st.markdown(f"### Scene {idx + 1}")
                st.write(segment)
                st.image(images[idx], use_column_width=True)

            if st.button("Download PDF"):
                pdf_file = export_story_pdf(prompt, segments, images)
                st.download_button("Download Story PDF", pdf_file, file_name="story.pdf", mime="application/pdf")

        except Exception as e:
            st.error(f"An error occurred: {e}")

