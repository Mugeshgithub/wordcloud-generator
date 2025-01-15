import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import PyPDF2
from docx import Document
from io import BytesIO
import base64

# ------------------------------
# Functions for File Reading
# ------------------------------
def read_file(file):
    """Read uploaded file content based on file type."""
    if file.type == "text/plain":
        return file.getvalue().decode("utf-8")
    elif file.type == "application/pdf":
        pdf = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in pdf.pages])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file format!")
        return None

def filter_stopwords(text, custom_stopwords):
    """Filter out stopwords from the text."""
    words = text.split()
    all_stopwords = STOPWORDS.union(set(custom_stopwords))
    filtered_words = [word for word in words if word.lower() not in all_stopwords]
    return " ".join(filtered_words)

def generate_wordcloud(text, width, height, stopwords):
    """Generate a Word Cloud image."""
    wordcloud = WordCloud(width=width, height=height, background_color="white", stopwords=stopwords).generate(text)
    return wordcloud

def download_link(data, filename, label):
    """Generate a download link for files."""
    b64 = base64.b64encode(data.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'

# ------------------------------
# Streamlit App Setup
# ------------------------------
st.set_page_config(page_title="Word Cloud Generator", layout="wide")
st.markdown("<h1 style='text-align: center; color: steelblue;'>✨ Word Cloud Generator ✨</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Options")
uploaded_files = st.sidebar.file_uploader("Upload Files (txt, pdf, docx)", type=["txt", "pdf", "docx"], accept_multiple_files=True)
use_default_stopwords = st.sidebar.checkbox("Use Default Stopwords", value=True)
additional_stopwords = st.sidebar.text_area("Custom Stopwords (comma-separated)", value="")
preview_text = st.sidebar.checkbox("Preview Filtered Text", value=True)

# Word Cloud Settings
st.sidebar.subheader("Word Cloud Settings")
cloud_width = st.sidebar.slider("Cloud Width", 400, 2000, 800, 100)
cloud_height = st.sidebar.slider("Cloud Height", 200, 1000, 400, 50)
max_words = st.sidebar.slider("Max Words", 50, 500, 200, 50)
color_palette = st.sidebar.selectbox("Color Palette", ["Monochrome", "Vibrant", "Cool"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Connect with Me:**")
st.sidebar.markdown("""
[![LinkedIn](https://img.icons8.com/?size=24&id=13930&format=png)](https://bit.ly/3YYtinf)
[![GitHub](https://img.icons8.com/?size=24&id=106567&format=png)](https://bit.ly/3CyOBTZ)
[![Fiverr](https://img.icons8.com/?size=24&id=121864&format=png)](https://www.fiverr.com/sellers/mugesh_krish/edit)
""", unsafe_allow_html=True)

# ------------------------------
# Main Section
# ------------------------------
if uploaded_files:
    st.subheader("Uploaded Files")
    all_text = ""

    for uploaded_file in uploaded_files:
        file_text = read_file(uploaded_file)
        if file_text:
            all_text += " " + file_text
            st.write(f"✅ {uploaded_file.name} successfully read!")

    # Process Stopwords
    custom_stopwords = set(additional_stopwords.split(",")) if additional_stopwords else set()
    if use_default_stopwords:
        custom_stopwords = STOPWORDS.union(custom_stopwords)

    # Filter Text
    filtered_text = filter_stopwords(all_text, custom_stopwords)

    # Preview Filtered Text
    if preview_text:
        st.subheader("Filtered Text Preview")
        st.text_area("Preview", value=filtered_text[:1000], height=150)

    # Generate Word Cloud
    st.subheader("Word Cloud")
    wordcloud = generate_wordcloud(filtered_text, cloud_width, cloud_height, custom_stopwords)
    fig, ax = plt.subplots(figsize=(cloud_width / 70, cloud_height / 70))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Download Filtered Text
    st.markdown(download_link(filtered_text, "filtered_text.txt", "📥 Download Filtered Text"), unsafe_allow_html=True)

    # Word Count Analysis
    words = filtered_text.split()
    word_count_df = pd.DataFrame({"Word": words}).value_counts().reset_index(name="Count").rename(columns={0: "Word"})
    st.subheader("Word Count Table")
    st.dataframe(word_count_df)

    # Download Word Count as CSV
    csv_data = word_count_df.to_csv(index=False)
    b64_csv = base64.b64encode(csv_data.encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{b64_csv}" download="word_count.csv">📥 Download Word Count as CSV</a>',
                unsafe_allow_html=True)

else:
    st.info("Upload files to start generating word clouds!")