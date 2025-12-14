import streamlit as st
from services.ai_assistant import AIAssistant

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

st.title("🤖 AI Assistant")
st.markdown("---")

# Check if user is logged in
if st.session_state.get("current_user") is None:
    st.error("❌ Please log in first!")
    st.stop()

# Initialize AI Assistant in session state
if "ai_assistant" not in st.session_state:
    st.session_state.ai_assistant = AIAssistant(
        system_prompt="You are a helpful cybersecurity and data analysis expert assistant for the Multi-Domain Intelligence Platform."
    )

ai = st.session_state.ai_assistant

# Sidebar for settings
with st.sidebar:
    st.subheader("⚙️ AI Settings")
    
    st.write("**System Prompt:**")
    new_prompt = st.text_area(
        "Customize the AI behavior:",
        value=ai.get_system_prompt(),
        height=150,
        key="system_prompt"
    )
    
    if st.button("Update Prompt"):
        ai.set_system_prompt(new_prompt)
        st.success("✅ System prompt updated!")
    
    if st.button("Clear History"):
        ai.clear_history()
        st.success("✅ Conversation history cleared!")

# Main chat interface
st.subheader("💬 Conversation")

# Display chat history
history = ai.get_history()
if history:
    for message in history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
else:
    st.info("👋 Start a conversation with the AI assistant!")

# Input for new message
user_input = st.chat_input("Ask me anything about cybersecurity, data analysis, or IT operations...")

if user_input:
    # Display user message
    st.chat_message("user").write(user_input)
    
    # Get AI response
    with st.spinner("🤖 Thinking..."):
        response = ai.send_message(user_input)
    
    # Display AI response
    st.chat_message("assistant").write(response)
    st.rerun()

st.markdown("---")

# Display conversation stats
history = ai.get_history()
if history:
    col1, col2, col3 = st.columns(3)
    with col1:
        message_count = len(history)
        st.metric("Messages", message_count)
    with col2:
        user_messages = sum(1 for m in history if m["role"] == "user")
        st.metric("Your Messages", user_messages)
    with col3:
        ai_messages = sum(1 for m in history if m["role"] == "assistant")
        st.metric("AI Responses", ai_messages)

