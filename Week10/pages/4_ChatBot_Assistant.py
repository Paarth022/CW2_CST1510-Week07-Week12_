import streamlit as st
import os
from datetime import datetime
import json

# Try to import OpenAI - handle gracefully if not installed
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

st.set_page_config(
    page_title="ChatBot Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# AUTHENTICATION CHECK
# ============================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

# ============================================
# SIDEBAR - USER INFO & SETTINGS
# ============================================

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")
    st.divider()
    
    st.subheader("⚙️ Assistant Settings")
    
    # Get API key from secrets
    api_key = st.secrets.get("openai_api_key", None)
    
    if not api_key:
        st.warning("⚠️ OpenAI API Key not found in secrets.toml")
        st.info("Add your API key to `.streamlit/secrets.toml`:")
        st.code('openai_api_key = "sk-..."', language="toml")
    
    # Model selection
    model_choice = st.selectbox(
        "Select Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        help="Choose the AI model for responses"
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )
    
    # System prompt customization
    st.subheader("System Prompt")
    default_system = "You are a helpful AI assistant for an Intelligence Platform. Provide clear, concise, and professional responses."
    system_prompt = st.text_area(
        "Custom System Prompt",
        value=default_system,
        height=100,
        help="Define the assistant's behavior and personality"
    )
    
    st.divider()
    
    # Clear chat history button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.success("Chat history cleared!")
        st.rerun()
    
    # Session info
    st.subheader("📊 Session Info")
    st.info(f"Messages: {st.session_state.get('chat_count', 0)}")
    st.info(f"Model: {model_choice}")
    st.info(f"Temperature: {temperature}")

# ============================================
# MAIN CHAT INTERFACE
# ============================================

st.title("🤖 ChatBot Assistant")

st.markdown("""
---
**Welcome to your AI Assistant!** This intelligent chatbot helps you with:
- Data analysis and insights
- Technical questions and troubleshooting
- Security recommendations
- General intelligence platform support

---
""")

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

# ============================================
# DISPLAY CHAT HISTORY
# ============================================

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ============================================
# USER INPUT & RESPONSE
# ============================================

user_input = st.chat_input(
    "Type your message here...",
    key="user_input"
)

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    st.session_state.chat_count += 1
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # ============================================
    # GET AI RESPONSE
    # ============================================
    
    if not OPENAI_AVAILABLE:
        with st.chat_message("assistant"):
            st.error("❌ OpenAI library not installed. Install with: `pip install openai`")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "❌ OpenAI library not installed."
        })
    
    elif not api_key:
        with st.chat_message("assistant"):
            st.error("❌ OpenAI API Key not configured. Check your secrets.toml file.")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "❌ API Key not configured."
        })
    
    else:
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=api_key)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Create messages list for API
                api_messages = [
                    {"role": "system", "content": system_prompt}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
                
                # Stream response from OpenAI
                with st.spinner("🤔 Thinking..."):
                    stream = client.chat.completions.create(
                        model=model_choice,
                        messages=api_messages,
                        temperature=temperature,
                        stream=True,
                        max_tokens=2000
                    )
                    
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })
        
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"❌ Error: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}"
            })

# ============================================
# FOOTER - QUICK PROMPTS
# ============================================

st.divider()

st.subheader("💡 Quick Prompts")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Analyze Data", use_container_width=True):
        st.session_state.quick_prompt = "Help me analyze a dataset"

with col2:
    if st.button("🔒 Security Tips", use_container_width=True):
        st.session_state.quick_prompt = "What are the best cybersecurity practices?"

with col3:
    if st.button("🐍 Python Help", use_container_width=True):
        st.session_state.quick_prompt = "How do I optimize my Python code?"

# Handle quick prompts
if "quick_prompt" in st.session_state and st.session_state.quick_prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": st.session_state.quick_prompt
    })
    st.session_state.quick_prompt = None
    st.rerun()

# ============================================
# INFO BOX
# ============================================

st.markdown("""
---
### ℹ️ About This Assistant
- **Powered by**: OpenAI GPT Models
- **Purpose**: Support for intelligence platform tasks
- **Features**: Streaming responses, custom prompts, chat history
- **Privacy**: All conversations are stored locally in your session

**Note**: This is a demonstration. For production use, implement proper logging and security measures.
""")