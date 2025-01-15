import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import PyPDF2
from docx import Document
from io import BytesIO
import base64

# ------------------------------
# Functions
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

def generate_wordcloud(text, width, height, stopwords, color_palette):
    """Generate a Word Cloud image."""
    wordcloud = WordCloud(width=width, height=height, background_color="white",
                           stopwords=stopwords, colormap=color_palette).generate(text)
    return wordcloud

def get_download_link(data, filename, label):
    """Generate a download link for the filtered text."""
    b64 = base64.b64encode(data.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'

# ------------------------------
# Streamlit App Setup
# ------------------------------
st.set_page_config(page_title="✨ InsightCloud", layout="wide", page_icon="☁️")

# Header Section with a Hero Image
st.markdown("""
    <style>
        .main-header {
            background-color: #f7f7f7;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .main-header h1 {
            color: #2E4053;
            font-family: 'Roboto', sans-serif;
        }
        .main-header p {
            color: #2E4053;
            font-family: 'Open Sans', sans-serif;
            font-size: 18px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #7f8c8d;
        }
        .footer a {
            color: #3498db;
            text-decoration: none;
        }
    </style>
    <div class="main-header">
        <h1>✨ InsightCloud ✨</h1>
        <p>Visualize, Analyze, and Unlock the Power of Your Words.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Options")
uploaded_files = st.sidebar.file_uploader("Upload Files (txt, pdf, docx)", type=["txt", "pdf", "docx"], accept_multiple_files=True)
use_default_stopwords = st.sidebar.checkbox("Use Default Stopwords", value=True)
additional_stopwords = st.sidebar.text_area("Add Custom Stopwords (comma-separated)", value="")
dark_mode = st.sidebar.checkbox("Enable Dark Mode")
cloud_width = st.sidebar.slider("Cloud Width", 400, 1200, 800)
cloud_height = st.sidebar.slider("Cloud Height", 300, 800, 400)
max_words = st.sidebar.slider("Max Words", 50, 300, 150)
color_palette = st.sidebar.selectbox("Color Palette", ["coolwarm", "viridis", "plasma", "magma", "cividis"])

# ------------------------------
# Main Section
# ------------------------------
if uploaded_files:
    st.subheader("📂 Uploaded Files")
    all_text = ""

    for uploaded_file in uploaded_files:
        file_content = read_file(uploaded_file)
        if file_content:
            all_text += file_content
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")

    # Process Stopwords
    custom_stopwords = set(additional_stopwords.split(",")) if additional_stopwords else set()
    if use_default_stopwords:
        custom_stopwords = STOPWORDS.union(custom_stopwords)

    # Filter Text
    filtered_text = filter_stopwords(all_text, custom_stopwords)

    # Word Cloud Preview
    st.subheader("☁️ Generated Word Cloud")
    wordcloud = generate_wordcloud(filtered_text, cloud_width, cloud_height, custom_stopwords, color_palette)
    fig, ax = plt.subplots(figsize=(cloud_width / 100, cloud_height / 100))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Add Attribution
    st.markdown("<p style='text-align: center;'>🌟 Created by <strong>Mugesh Murugaiyan</strong></p>", unsafe_allow_html=True)

    # Provide Download Links
    st.markdown(get_download_link(filtered_text, "filtered_text.txt", "📥 Download Filtered Text"), unsafe_allow_html=True)

    # Word Count Analysis
    st.subheader("📊 Word Count Analysis")
    words = filtered_text.split()
    word_count_df = pd.DataFrame({"Word": words}).value_counts().reset_index(name="Count").rename(columns={0: "Word"})
    st.dataframe(word_count_df)

    # CSV Download Link
    csv = word_count_df.to_csv(index=False)
    st.markdown(f'<a href="data:file/csv;base64,{base64.b64encode(csv.encode()).decode()}" download="word_count.csv">📥 Download Word Count as CSV</a>', unsafe_allow_html=True)

else:
    st.info("Upload files to start generating word clouds!")

# ------------------------------
# Footer
# ------------------------------
st.markdown("""
    <div class="footer">
        <p>Built with ❤️ by <strong>Mugesh Murugaiyan</strong></p>
        <p>
            <a href="https://bit.ly/3YYtinf" target="_blank">LinkedIn</a> |
            <a href="https://bit.ly/3CyOBTZ" target="_blank">GitHub</a> |
            <a href="https://www.fiverr.com/sellers/mugesh_krish/edit" target="_blank">Fiverr</a>
        </p>
    </div>
""", unsafe_allow_html=True)