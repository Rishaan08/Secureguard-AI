import streamlit as st
import os
import nbformat
from nbconvert import PythonExporter
import sys
from datetime import datetime
import time
from io import StringIO
import contextlib

# Load and execute the notebook to get its functions
def load_notebook_functions():
    # Read the notebook
    with open('chatbot.ipynb', 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Convert to Python code
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)
    
    # Execute the notebook code to get functions
    exec(source, globals())

# Load functions from notebook
load_notebook_functions()

# Custom CSS for beautiful styling
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom header styling */
    .custom-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        text-align: center;
    }
    
    .custom-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .custom-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Chat container styling */
    .chat-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
    }
    
    /* Message styling */
    .stChatMessage {
        background: rgba(255,255,255,0.8);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Input styling */
    .stChatInputContainer {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102,126,234,0.9) 0%, rgba(118,75,162,0.9) 100%);
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 4px 16px 0 rgba(31, 38, 135, 0.2);
    }
    
    .stats-card h3 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stats-card p {
        color: rgba(255,255,255,0.8);
        margin: 0.5rem 0 0 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: white !important;
    }
    
    /* Similarity info box */
    .similarity-box {
        background: rgba(255,255,255,0.1);
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .score-display {
        font-size: 1.1rem;
        font-weight: 600;
        color: #667eea;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    st.markdown("""
    <div class="custom-header">
        <h1>🛡️ SecureGuard AI</h1>
        <p>Your intelligent companion for security and support</p>
    </div>
    """, unsafe_allow_html=True)

def display_stats_sidebar():
    with st.sidebar:
        st.markdown("### 📊 Session Stats")
        
        # Calculate stats
        total_messages = len(st.session_state.history)
        user_messages = sum(1 for speaker, _ in st.session_state.history if speaker == "You")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{total_messages}</h3>
                <p>Total Messages</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{user_messages}</h3>
                <p>Your Messages</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Clear Chat History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        
        if st.button("💾 Export Conversation", use_container_width=True):
            export_conversation()
        
        st.markdown("---")
        
        # Suggested prompts
        st.markdown("### 💡 Suggested Topics")
        suggestions = [
            "Tell me about cybersecurity best practices",
            "How can I protect my personal data?",
            "What are common security threats?",
            "Explain two-factor authentication"
        ]
        
        for suggestion in suggestions:
            if st.button(f"📌 {suggestion[:30]}...", key=suggestion, use_container_width=True):
                st.session_state.pending_input = suggestion
                st.rerun()

def export_conversation():
    if not st.session_state.history:
        st.sidebar.warning("No conversation to export!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content = f"SecureGuard AI Conversation - {timestamp}\n\n"
    
    for speaker, msg in st.session_state.history:
        content += f"{speaker}: {msg}\n\n"
    
    st.sidebar.download_button(
        label="⬇️ Download as TXT",
        data=content,
        file_name=f"secureguard_chat_{timestamp}.txt",
        mime="text/plain"
    )

def display_welcome_message():
    if not st.session_state.history:
        st.markdown("""
        <div class="chat-container">
            <h3>Welcome to SecureGuard AI!</h3>
            <p>I'm here to help you with:</p>
            <ul>
                <li>Cybersecurity guidance and best practices</li>
                <li>Threat detection and prevention</li>
                <li>Security recommendations</li>
                <li>Educational resources</li>
            </ul>
            <p><strong>Ask me anything to get started!</strong></p>
        </div>
        """, unsafe_allow_html=True)

@contextlib.contextmanager
def capture_output():
    """Capture stdout to display print statements in Streamlit"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        yield captured_output
    finally:
        sys.stdout = old_stdout

def parse_similarity_output(output_text):
    """Parse the similarity score output from the notebook prints"""
    lines = output_text.strip().split('\n')
    similarity_info = []
    
    for line in lines:
        if 'Score:' in line:
            # Extract score and preview
            parts = line.split('|')
            if len(parts) >= 2:
                score_part = parts[0].strip()
                preview_part = parts[1].strip() if len(parts) > 1 else ""
                
                # Extract numeric score
                try:
                    score = float(score_part.split('Score:')[1].strip())
                    preview = preview_part.replace('Content Preview:', '').strip()
                    similarity_info.append({'score': score, 'preview': preview})
                except:
                    pass
    
    return similarity_info

def display_similarity_info(similarity_data, threshold=0.65):
    """Display similarity information in a nice format"""
    if not similarity_data:
        return
    
    for item in similarity_data:
        score = item['score']
        preview = item['preview']
        
        # Determine quality
        if score < 0.3:
            quality = "✅ Excellent Match"
            color = "#2ed573"
        elif score < 0.5:
            quality = "✔️ Good Match"
            color = "#34d399"
        elif score < 0.8:
            quality = "⚠️ Fair Match"
            color = "#fbbf24"
        else:
            quality = "❌ Poor Match"
            color = "#ef4444"
        
        # Check if passes threshold
        passes = score <= threshold
        pass_text = "✅ WILL USE" if passes else "❌ FILTERED OUT"
        pass_color = "#2ed573" if passes else "#ef4444"
        
        st.markdown(f"""
        <div class="similarity-box">
            <div class="score-display" style="color: {color};">
                🔍 Similarity Score: <strong>{score:.4f}</strong> - {quality}
            </div>
            <div style="color: {pass_color}; font-weight: 600; margin: 0.5rem 0;">
                {pass_text} (Threshold: {threshold})
            </div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.5rem;">
                Preview: {preview}
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="SecureGuard AI",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Display header
    display_header()
    
    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if "pending_input" not in st.session_state:
        st.session_state.pending_input = None
    
    # Initialize LLM & DB only once
    if "qa_chain" not in st.session_state:
        with st.spinner("🔧 Initializing SecureGuard AI..."):
            llm = initialize_llm()
            db_path = "./chroma_db"

            if not os.path.exists(db_path):
                with st.spinner("📚 Creating knowledge base for the first time..."):
                    vector_db = create_vector_db()
            else:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                from langchain_community.vectorstores import Chroma
                embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
                vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)

            st.session_state.qa_chain = setup_qa_chain(vector_db, llm)
            st.session_state.vector_db = vector_db
    
    # Display sidebar stats
    display_stats_sidebar()
    
    # Main chat area
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # Display welcome message if no history
        display_welcome_message()
        
        # Display chat history
        for speaker, msg in st.session_state.history:
            if speaker == "You":
                with st.chat_message("user", avatar="👤"):
                    st.write(msg)
            else:
                with st.chat_message("assistant", avatar="🛡️"):
                    st.write(msg)
        
        # Handle user input
        user_input = st.chat_input("💬 Type your message here...", key="chat_input")
        
        # Handle pending input from sidebar buttons
        if st.session_state.pending_input:
            user_input = st.session_state.pending_input
            st.session_state.pending_input = None
        
        if user_input:
            if user_input.lower() == "exit":
                goodbye_msg = "🌙 Whenever you need a listening ear, a gentle reminder, or a little light — I'll be here. Goodbye for now 🤍"
                st.session_state.history.append(("You", user_input))
                st.session_state.history.append(("Bot", goodbye_msg))
                st.rerun()
            else:
                # Show user message immediately
                with st.chat_message("user", avatar="👤"):
                    st.write(user_input)
                
                # Show bot response with typing indicator
                with st.chat_message("assistant", avatar="🛡️"):
                    # Capture the output from the chatbot (including print statements)
                    with capture_output() as captured:
                        try:
                            # Get response from chatbot (this will print similarity scores)
                            if callable(st.session_state.qa_chain):
                                response = st.session_state.qa_chain(user_input)
                            elif hasattr(st.session_state.qa_chain, 'invoke'):
                                response = st.session_state.qa_chain.invoke({"query": user_input})
                            else:
                                response = st.session_state.qa_chain({"query": user_input})
                            
                            # Extract result based on response type
                            if isinstance(response, dict):
                                result = response.get('result', response.get('answer', str(response)))
                            else:
                                result = str(response)
                            
                        except Exception as e:
                            st.error(f"Error generating response: {str(e)}")
                            result = "I apologize, but I encountered an error processing your request. Please try again."
                    
                    # Get the captured output (print statements)
                    output_text = captured.getvalue()
                    
                    # Parse and display similarity information
                    if output_text:
                        similarity_data = parse_similarity_output(output_text)
                        if similarity_data:
                            st.markdown("### 🔍 Similarity Analysis")
                            display_similarity_info(similarity_data, threshold=0.65)
                            st.markdown("---")
                    
                    # Display the final response
                    st.markdown("### 💬 Response")
                    st.write(result)
                
                # Update history
                st.session_state.history.append(("You", user_input))
                st.session_state.history.append(("Bot", result))
                st.rerun()

if __name__ == "__main__":
    main()