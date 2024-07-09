import streamlit as st
from langchain.vectorstores import Cassandra
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
import cassio
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

# --- Configuration ---
# (Preferably store these as secrets in Streamlit Cloud or a .env file)
ASTRA_DB_TOKEN = st.secrets["astra_db_token"]
ASTRA_DB_ID = st.secrets["astra_db_id"]
OPENAI_API_KEY = st.secrets["openai_api_key"]
TABLE_NAME = "qa_mini_demo"

# --- Initialization (Outside Streamlit for efficiency) ---
try:
    cassio.init(token=ASTRA_DB_TOKEN, database_id=ASTRA_DB_ID)
    llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)  # Temperature for creativity
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vector_store = Cassandra(embedding=embedding, table_name=TABLE_NAME)
    index = VectorstoreIndexCreator().from_vectorstore(vector_store)  # Build the index
except Exception as e:
    st.error(f"Error during initialization: {e}")
    st.stop()

# --- Helper Functions ---
def load_pdf(uploaded_file):
    """Extract raw text from an uploaded PDF."""
    raw_text = ""
    pdfreader = PdfReader(uploaded_file)
    for page in pdfreader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text


def add_to_vector_store(raw_text):
    """Split text and add it to the vector store."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,  # Adjust for your documents
        chunk_overlap=200,
    )
    texts = text_splitter.split_text(raw_text)
    vector_store.add_texts(texts)


# --- Streamlit App ---
st.title("DataScience:GPT - PDF Q&A Chatbot")

# File Upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    with st.spinner("Processing PDF..."):
        raw_text = load_pdf(uploaded_file)
        add_to_vector_store(raw_text)
    st.success("PDF processed and added to the vector store!")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Ask me questions about your uploaded PDF!"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = index.query(prompt, llm=llm)  # Using the pre-built index
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
