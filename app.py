"""
Advanced AI Search Engine
Developed by: Yaswanth Thottempudi
A comprehensive search platform combining multiple AI-powered search tools
"""

import streamlit as st
import os
from datetime import datetime
import json
from typing import List, Dict, Any

# LangChain imports
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🔍 Yaswanth's AI Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    .search-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        flex: 1;
        margin: 0 0.5rem;
    }
    .search-history-item {
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .feature-highlight {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "total_searches" not in st.session_state:
    st.session_state.total_searches = 0
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Welcome to my AI Search Engine! I can help you search across Wikipedia, ArXiv research papers, and the web. What would you like to explore today?"}
    ]

# Header
st.markdown("""
<div class="main-header">
    <h1>🔍 Yaswanth's AI Search Engine</h1>
    <p>Advanced Multi-Source Search Platform | Powered by AI & LangChain</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# API Key Input
api_key = st.sidebar.text_input(
    "🔑 Enter your Groq API Key:", 
    type="password",
    help="Get your free API key from https://console.groq.com/"
)

# Search Options
st.sidebar.markdown("### 🔧 Search Options")
search_sources = st.sidebar.multiselect(
    "Select search sources:",
    ["Wikipedia", "ArXiv", "Web Search"],
    default=["Wikipedia", "ArXiv", "Web Search"],
    help="Choose which sources to include in your search"
)

# Advanced Settings
with st.sidebar.expander("🔬 Advanced Settings"):
    max_results = st.slider("Max results per source:", 1, 5, 2)
    response_length = st.selectbox("Response length:", ["Short", "Medium", "Detailed"], index=1)
    search_timeout = st.slider("Search timeout (seconds):", 10, 60, 30)

# Statistics
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Statistics")
st.sidebar.metric("Total Searches", st.session_state.total_searches)
st.sidebar.metric("Session Duration", f"{len(st.session_state.messages)} interactions")

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    # Search Interface
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.markdown("### 🚀 Start Your Search")
    
    # Search input
    user_input = st.chat_input(
        placeholder="Ask me anything! Try: 'What is quantum computing?' or 'Latest AI research papers'",
        key="search_input"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat Interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Process search
    if user_input and api_key:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Initialize tools based on selection
        tools = []
        
        if "Wikipedia" in search_sources:
            wiki_wrapper = WikipediaAPIWrapper(
                top_k_results=max_results, 
                doc_content_chars_max=300 if response_length == "Short" else 500 if response_length == "Medium" else 800
            )
            wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
            tools.append(wiki_tool)
        
        if "ArXiv" in search_sources:
            arxiv_wrapper = ArxivAPIWrapper(
                top_k_results=max_results, 
                doc_content_chars_max=300 if response_length == "Short" else 500 if response_length == "Medium" else 800
            )
            arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)
            tools.append(arxiv_tool)
        
        if "Web Search" in search_sources:
            web_tool = DuckDuckGoSearchRun(name="WebSearch")
            tools.append(web_tool)
        
        if tools:
            # Initialize LLM
            llm = ChatGroq(
                groq_api_key=api_key,
                model_name="Gemma2-9b-it",
                streaming=True,
                temperature=0.7
            )
            
            # Create agent
            search_agent = initialize_agent(
                tools, 
                llm, 
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True,
                verbose=True
            )
            
            # Generate response
            with st.chat_message("assistant"):
                st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
                
                try:
                    response = search_agent.invoke(
                        {"input": user_input}, 
                        callbacks=[st_callback]
                    )
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response["output"]
                    })
                    
                    # Update statistics
                    st.session_state.total_searches += 1
                    st.session_state.search_history.append({
                        "query": user_input,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "sources": search_sources
                    })
                    
                    st.write(response["output"])
                    
                except Exception as e:
                    error_msg = f"❌ Search failed: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.write(error_msg)
        else:
            st.warning("⚠️ Please select at least one search source!")
    
    elif user_input and not api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to start searching!")

with col2:
    # Features Panel
    st.markdown("### ✨ Features")
    st.markdown("""
    <div class="feature-highlight">
        <h4>🔍 Multi-Source Search</h4>
        <p>Search across Wikipedia, ArXiv, and the web simultaneously</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-highlight">
        <h4>🤖 AI-Powered</h4>
        <p>Advanced AI agent with reasoning capabilities</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-highlight">
        <h4>📊 Smart Analytics</h4>
        <p>Track your search patterns and history</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search History
    if st.session_state.search_history:
        st.markdown("### 📚 Recent Searches")
        for i, search in enumerate(st.session_state.search_history[-5:]):
            st.markdown(f"""
            <div class="search-history-item">
                <strong>{search['query']}</strong><br>
                <small>📅 {search['timestamp']} | 🔍 {', '.join(search['sources'])}</small>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 <strong>Yaswanth's AI Search Engine</strong> | Built with Streamlit & LangChain</p>
    <p>💡 <em>Empowering intelligent search across multiple knowledge sources</em></p>
</div>
""", unsafe_allow_html=True)

# Export functionality
if st.session_state.search_history:
    if st.sidebar.button("📥 Export Search History"):
        history_json = json.dumps(st.session_state.search_history, indent=2)
        st.sidebar.download_button(
            label="Download JSON",
            data=history_json,
            file_name=f"search_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )