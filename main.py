import langchain_helper as lch
import streamlit as st
import textwrap

# Page Configuration
st.set_page_config(page_title="YouTube Assistant", page_icon="🎥", layout="centered")

# Custom CSS for Styling
st.markdown(
    """
    <style>
    /* Center the input fields */
    div[data-testid="stVerticalBlock"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Input Field Styling */
    .stTextInput, .stTextArea {
        border-radius: 10px;
        border: 1px solid #ccc;
        width: 100%;
    }

    /* Submit Button */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        
        color: white;
        font-weight: bold;
        padding: 10px;
        transition: 0.3s;
    }

    

    /* Chat Response Styling */
    .chat-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        color: black !important;
    }

    /* Resize Video */
    iframe {
    display: block;  /* Ensures it behaves like a block element */
    width: 600px !important;
    height: 340px !important;
    margin: 0 auto;  /* Centers it horizontally */
}

    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.title("🎥 YouTube Assistant")
st.write("Ask questions about any YouTube video based on its transcript!")

# Initialize session state for conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stack to store question-answer pairs

# Input Fields (Centered)
video_url = st.text_input("🔗 Enter YouTube Video URL", placeholder="Paste URL here...", key="video_input")
query = st.text_area("💬 Ask a Question", placeholder="Type your question here...", key="query_input")

# Submit Button
submit = st.button("Submit 🚀")

# Process Input
if submit:
    if not video_url or not query:
        st.warning("⚠️ Please enter both a YouTube URL and a question.")
    else:
        # Display Video (Smaller Size)
        st.markdown(f'<iframe src="https://www.youtube.com/embed/{video_url.split("=")[-1]}" frameborder="0"></iframe>', unsafe_allow_html=True)

        # Loading Indicator
        with st.spinner("🔍 Analyzing video transcript... Please wait."):
            db = lch.CreateVectorDbFromYoutube(video_url)
            response = lch.GetResponseFromQuery(db, query)
        
        # Save to session state stack
        st.session_state.chat_history.append({"question": query, "answer": response})

# Display Chat History
if st.session_state.chat_history:
    st.subheader("💡 AI Response:")
    for chat in reversed(st.session_state.chat_history):  # Show newest first
        st.markdown(f'<div class="chat-box"><b>Q:</b> {chat["question"]}<br><b>A:</b> {textwrap.fill(chat["answer"], width=80)}</div>', unsafe_allow_html=True)