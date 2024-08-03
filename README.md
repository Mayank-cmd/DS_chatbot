DocuBot

Welcome to DocuBot, an interactive Q&A application that lets you upload PDF documents and ask questions about their contents. This project is built using Streamlit, LangChain, and OpenAI's language model.

Demo

You can try the live demo of the application here.

Features
PDF Upload: Upload PDF files to the app.
Text Extraction: Extracts text from the uploaded PDF.
Vector Store: Stores the extracted text as embeddings using LangChain's vector store with Cassandra.
Interactive Q&A: Ask questions about the uploaded document, and get answers based on the content.
Installation
Prerequisites
Python 3.8+
Streamlit
PyPDF2
OpenAI API key
Astra DB credentials for Cassandra
Setup
Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/DocuBot.git
cd DocuBot
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set up your environment variables:

ASTRA_DB_TOKEN: Token for Astra DB.
ASTRA_DB_ID: Database ID for Astra DB.
OPENAI_API_KEY: API key for OpenAI.
You can store these in a .env file or directly in Streamlit Cloud secrets.

Run the application:

bash
Copy code
streamlit run app.py
Usage
Upload PDF: Use the file uploader to upload a PDF document. The text from the document will be extracted and stored in a vector store.
Ask Questions: Type in your questions about the uploaded document. The assistant will provide answers based on the extracted content.
Project Structure
app.py: Main Streamlit application file.
requirements.txt: List of Python dependencies.
Technologies Used
Streamlit: For the web interface.
LangChain: For handling the language model and vector store.
OpenAI: For generating embeddings and handling Q&A.
Cassandra: For storing vectorized text data.
Contributing
Contributions are welcome! Please feel free to submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Special thanks to the developers of Streamlit, LangChain, and OpenAI for providing the tools and APIs that made this project possible.
