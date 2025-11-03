# SecureGuard AI - Cybersecurity Chatbot

An intelligent RAG (Retrieval-Augmented Generation) chatbot specialized in **Cybersecurity Incident Response** and **OWASP Top 10** vulnerabilities. Built with LangChain, Streamlit, and powered by Groq's LLaMA 3.3 70B model.

## Features

- **Smart Document Retrieval**: Uses ChromaDB vector database for semantic search
- **Similarity Score Analysis**: Real-time display of document relevance scores
- **Beautiful UI**: Modern gradient design with glassmorphism effects
- **Export Conversations**: Download chat history as text files
- **Quick Actions**: Pre-defined prompts for common queries
- **Specialized Knowledge**: Focuses on incident response and OWASP Top 10

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Features in Detail](#features-in-detail)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Groq API key (Get it from https://console.groq.com/)

### Setup Instructions

1. Install required dependencies:

```bash
pip install streamlit langchain langchain-community langchain-groq langchain-huggingface
pip install chromadb sentence-transformers pypdf python-dotenv nbformat nbconvert
```

2. Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

3. Prepare your documents:

Create a `data/` folder and add your cybersecurity PDF documents:

```bash
mkdir data
```

**Recommended Documents:**
- NIST Cybersecurity Incident Response Guidelines
- OWASP Top 10 Documentation
- Security Best Practices PDFs
- Incident Response Playbooks

**Recommended Documents:**
- NIST Cybersecurity Incident Response Guidelines
- OWASP Top 10 Documentation
- Security Best Practices PDFs
- Incident Response Playbooks

## Project Structure

```
secureguard-ai/
│
├── app.py                  # Main Streamlit application
├── chatbot.ipynb          # Jupyter notebook with core functions
├── .env                   # Environment variables (create this)
├── README.md             # This file
│
├── data/                 # PDF documents (create this)
│   ├── incident_response.pdf
│   ├── owasp_top10.pdf
│   └── security_guidelines.pdf
│
└── chroma_db/            # Vector database (auto-created)
    └── ...
```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### First Time Setup

1. **Initial Load**: The first time you run the app, it will:
   - Load all PDFs from the `data/` folder
   - Create embeddings using HuggingFace's MiniLM model
   - Store them in ChromaDB (takes 2-5 minutes)

2. **Subsequent Runs**: Will load the existing database instantly

### Example Queries

**In-Scope Queries:**
```
"What is incident prioritization?"
"Explain SQL injection from OWASP Top 10"
"How to respond to a data breach?"
"What are the phases of incident response?"
"Tell me about cross-site scripting (XSS)"
```

**Out-of-Scope Queries:**
```
"What is the weather today?"
"Tell me about machine learning"
"What is neuro fuzzy?"
```

## How It Works

### Architecture Overview

```
User Query
    ↓
1. Embedding Generation (HuggingFace MiniLM)
    ↓
2. Vector Search (ChromaDB)
    ↓
3. Similarity Score Calculation
    ↓
4. Threshold Filtering (0.65)
    ↓
5. Context Retrieval
    ↓
6. LLM Generation (Groq LLaMA 3.3)
    ↓
7. Response Display
```

### Key Components

1. **Document Loading**: `PyPDFLoader` extracts text from PDFs
2. **Text Splitting**: `RecursiveCharacterTextSplitter` with 1000 character chunks and 200 character overlap
3. **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` for vector generation
4. **Vector Store**: ChromaDB with local persistence
5. **LLM**: Groq's LLaMA 3.3 70B Versatile model
6. **Frontend**: Streamlit with custom CSS styling

### Similarity Threshold Logic

The chatbot uses **distance-based similarity** where **lower scores indicate better matches**:

```python
SIMILARITY_THRESHOLD = 0.65

Score < 0.3  → Excellent Match
Score < 0.5  → Good Match
Score < 0.8  → Fair Match
Score >= 0.8 → Poor Match

# Only documents with score <= 0.65 are used for response generation
```

## Features in Detail

### 1. Similarity Analysis Display

Every query shows:
- **Similarity Score**: Numerical distance metric
- **Match Quality**: Visual indicator (Excellent/Good/Fair/Poor)
- **Threshold Status**: Whether document passes the threshold
- **Content Preview**: First 150 characters of matched text

Example output:
```
Similarity Score: 0.5669 - Good Match
WILL USE (Threshold: 0.65)
Preview: Organizations must establish incident response capabilities...
```

### 2. Session Statistics

Sidebar displays:
- Total messages in conversation
- Number of user messages
- Real-time updates

### 3. Quick Actions

- **Clear Chat History**: Reset the entire conversation
- **Export Conversation**: Download chat history as `.txt` file with timestamp
- **Suggested Topics**: Pre-defined prompts for common cybersecurity questions

### 4. Smart Filtering

If no documents match the threshold:
```
Response: "This information is not in our database."
```

This prevents hallucinations and ensures responses are grounded in your provided documents.

## Troubleshooting

### Issue: "No module named 'langchain_huggingface'"

**Solution:**
```bash
pip install -U langchain-huggingface
```

### Issue: Similarity scores not showing in Streamlit

**Solution:** 
The app captures print statements from the notebook. If you still don't see them:
1. Check that `chatbot.ipynb` contains the print statements in `get_relevant_docs()`
2. Restart the Streamlit app completely
3. Clear browser cache and refresh

### Issue: "ChromaDB created and saved" appears multiple times

**Solution:** 
This happens when the vector database is recreated unnecessarily. To fix:
1. Delete the `chroma_db` folder
2. Restart the app to create a fresh database
3. Ensure the database path in code is `./chroma_db` (not `.chroma_db`)

### Issue: Poor response quality or irrelevant answers

**Solutions:**
1. **Increase threshold**: Change `SIMILARITY_THRESHOLD` in `chatbot.ipynb` from 0.65 to 0.8 or higher
2. **Add more documents**: Expand your `data/` folder with more relevant PDFs
3. **Improve chunk size**: Modify `chunk_size` parameter in `RecursiveCharacterTextSplitter`

### Issue: Database loading is slow

**Solution:**
The first load takes time to process PDFs and create embeddings. Subsequent loads are fast because the database is cached. If it's still slow:
1. Reduce PDF file sizes
2. Decrease the number of documents
3. Use smaller chunk sizes

### Issue: "incorrect startxref pointer(1)" warning

**Solution:**
This is a PyPDF warning for malformed PDFs. It doesn't affect functionality. To suppress:
```python
import warnings
warnings.filterwarnings('ignore')
```

## Technical Details

### Notebook Structure (chatbot.ipynb)

**Cell 1**: Load environment variables
```python
import os
from dotenv import load_dotenv
load_dotenv()
```

**Cell 2**: Import required libraries

**Cell 3**: Initialize LLM with Groq

**Cell 4**: Create vector database from PDFs

**Cell 5**: Get relevant documents with similarity filtering

**Cell 6**: Setup QA chain with custom prompts

**Cell 7**: Test queries (commented out for production)

### Streamlit App Structure (app.py)

1. **Load Notebook Functions**: Converts `.ipynb` to Python and executes
2. **Custom CSS**: Applies gradient theme and glassmorphism
3. **Session State**: Manages conversation history
4. **Sidebar**: Displays stats and quick actions
5. **Main Chat**: Handles user input and displays responses
6. **Output Capture**: Redirects print statements to Streamlit UI

## Customization

### Changing the Similarity Threshold

Edit `chatbot.ipynb`, Cell 5:
```python
SIMILARITY_THRESHOLD = 0.85  # Change this value
```

Lower values = stricter matching (fewer false positives)
Higher values = looser matching (more results, potentially less relevant)

### Modifying the Prompt Template

Edit `chatbot.ipynb`, Cell 6:
```python
prompt_template = """
You are a cybersecurity expert chatbot. Answer ONLY using the provided context.
[Customize this instruction...]

Context:
{context}

User: {question}
Chatbot:"""
```

### Changing the LLM Model

Edit `chatbot.ipynb`, Cell 3:
```python
llm = ChatGroq(
    model='llama-3.3-70b-versatile',  # Change model here
    groq_api_key=os.getenv('GROQ_API_KEY'),
    temperature=0.8  # Adjust temperature (0.0 = deterministic, 1.0 = creative)
)
```

Available Groq models:
- `llama-3.3-70b-versatile` (recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

## Best Practices

### Document Preparation

1. **Use high-quality PDFs**: Ensure text is extractable (not scanned images)
2. **Organize by topic**: Separate incident response, OWASP, and general security docs
3. **Remove duplicate content**: Avoid redundant information
4. **Keep documents updated**: Replace outdated security guidelines

### Query Optimization

1. **Be specific**: "Explain SQL injection prevention" instead of "Tell me about security"
2. **Use domain terminology**: "What is incident containment?" instead of "How to stop attacks?"
3. **Ask one question at a time**: Break complex queries into parts

### Performance Optimization

1. **Limit PDF size**: Keep individual files under 10MB
2. **Use fewer documents initially**: Start with 5-10 core documents
3. **Monitor memory usage**: ChromaDB stores embeddings in memory
4. **Restart periodically**: Clear cache if the app becomes sluggish

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution

- Adding support for more document formats (Word, Markdown, HTML)
- Implementing user authentication
- Adding conversation memory across sessions
- Supporting multiple languages
- Improving similarity calculation algorithms
- Adding unit tests and integration tests

## License

This project is licensed under the MIT License.

## Author

**Rishaan Yadav**

---

**Built with care for the cybersecurity community. Stay secure!**
