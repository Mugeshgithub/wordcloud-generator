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
    wordcloud = WordCloud(width=width, height=height, background_color="white",
                           stopwords=stopwords, contour_color='steelblue', contour_width=1).generate(text)
    return wordcloud

def download_link(object_to_download, download_filename, download_label):
    """Generate a download link for files."""
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_label}</a>'

# ------------------------------
# Streamlit App Setup
# ------------------------------
st.set_page_config(page_title="✨ Word Cloud Generator", layout="wide", page_icon="🌐")

# Header Section with a Hero Image
st.markdown("""
    <style>
        .main-header {
            text-align: center;
            background-color: #4CAF50;
            color: white;
            padding: 30px 0;
            font-size: 2.5em;
            border-radius: 8px;
        }
        .sidebar-header {
            color: #2c3e50;
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .custom-footer {
            text-align: center;
            margin-top: 50px;
            font-size: 1.2em;
            color: #7f8c8d;
        }
        .custom-footer a {
            color: #3498db;
            text-decoration: none;
        }
        .wordcloud-container {
            text-align: center;
            margin: 30px 0;
        }
    </style>
    <div class="main-header">✨ Word Cloud Generator ✨</div>
""", unsafe_allow_html=True)

# Sidebar Header
st.sidebar.markdown("<div class='sidebar-header'>⚙️ Options</div>", unsafe_allow_html=True)

# Sidebar
uploaded_files = st.sidebar.file_uploader("Upload Files (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"], accept_multiple_files=True)
use_default_stopwords = st.sidebar.checkbox("Use Default Stopwords", value=True)
additional_stopwords = st.sidebar.text_area("Add Custom Stopwords (comma-separated)", value="")
show_filtered_text = st.sidebar.checkbox("Preview Filtered Text", value=True)

# Word Cloud Settings
st.sidebar.subheader("🖼️ Word Cloud Settings")
cloud_width = st.sidebar.slider("Cloud Width", 400, 2000, 800, 100)
cloud_height = st.sidebar.slider("Cloud Height", 200, 1000, 400, 50)
max_words = st.sidebar.slider("Max Words", 50, 500, 200, 50)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3>📬 Connect with Me:</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <a href="https://bit.ly/3YYtinf" target="_blank">
        <img src="https://img.icons8.com/?size=40&id=13930&format=png" alt="LinkedIn"/>
    </a>
    <a href="https://bit.ly/3CyOBTZ" target="_blank">
        <img src="https://img.icons8.com/?size=40&id=106567&format=png" alt="GitHub"/>
    </a>
    <a href="https://www.fiverr.com/sellers/mugesh_krish/edit" target="_blank">
        <img src="https://img.icons8.com/?size=40&id=121864&format=png" alt="Fiverr"/>
    </a>
""", unsafe_allow_html=True)

# ------------------------------
# Main Section
# ------------------------------

if uploaded_files:
    st.subheader("📂 Uploaded Files")
    all_text = ""

    for uploaded_file in uploaded_files:
        file_text = read_file(uploaded_file)
        if file_text:
            all_text += " " + file_text
            st.write(f"✅ {uploaded_file.name} successfully processed!")

    # Process Stopwords
    custom_stopwords = set(additional_stopwords.split(",")) if additional_stopwords else set()
    if use_default_stopwords:
        custom_stopwords = STOPWORDS.union(custom_stopwords)

    # Filter Text
    filtered_text = filter_stopwords(all_text, custom_stopwords)

    # Display Filtered Text (Optional)
    if show_filtered_text:
        st.subheader("📝 Filtered Text Preview")
        st.text_area("Preview", value=filtered_text[:1000], height=200)

    # Generate Word Cloud
    st.subheader("☁️ Generated Word Cloud")
    wordcloud = generate_wordcloud(filtered_text, width=cloud_width, height=cloud_height, stopwords=custom_stopwords)
    fig, ax = plt.subplots(figsize=(cloud_width / 100, cloud_height / 100))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Add Attribution
    st.markdown("<p class='wordcloud-container'>🌟 Created by <strong>Mugesh Murugaiyan</strong></p>", unsafe_allow_html=True)

    # Provide Download Links
    st.markdown(download_link(filtered_text, "filtered_text.txt", "📥 Download Filtered Text"), unsafe_allow_html=True)

    # Generate Word Count Table
    words = filtered_text.split()
    word_count_df = pd.DataFrame({"Word": words}).value_counts().reset_index(name="Count").rename(columns={0: "Word"})
    st.subheader("📊 Word Count Analysis")
    st.dataframe(word_count_df)

    # CSV Download Link
    csv_data = word_count_df.to_csv(index=False)
    st.markdown(f'<a href="data:file/csv;base64,{base64.b64encode(csv_data.encode()).decode()}" download="word_count.csv">📥 Download Word Count as CSV</a>', unsafe_allow_html=True)

else:
    st.info("Upload files to generate a Word Cloud!")

# ------------------------------
# Footer
# ------------------------------
st.markdown("""
<div class="custom-footer">
    <p>Built with ❤️ by <strong>Mugesh Murugaiyan</strong></p>
    <p>
        <a href="https://bit.ly/3YYtinf" target="_blank">LinkedIn</a> |
        <a href="https://bit.ly/3CyOBTZ" target="_blank">GitHub</a> |
        <a href="https://www.fiverr.com/sellers/mugesh_krish/edit" target="_blank">Fiverr</a>
    </p>
</div>
""", unsafe_allow_html=True)
