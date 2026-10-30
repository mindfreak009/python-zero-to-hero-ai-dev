import streamlit as st
import html
from datetime import datetime

from chatbot_chain import ask_question
from db_service import initialize_database

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Support Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. DATABASE INITIALIZATION
# ============================================================


@st.cache_resource(show_spinner=False)
def setup_database():
    initialize_database()
    return True


try:
    DATABASE_READY = setup_database()
except Exception as error:
    DATABASE_READY = False
    print(f"Database initialization error: {error}")


# ============================================================
# 3. APPLICATION CONFIGURATION
# ============================================================

WELCOME_MESSAGE = """
Hello! 👋 Welcome to Student Support.

I can help you with:

- Course information
- Fee structures
- Admissions and eligibility
- Attendance policies
- Institute guidelines

What would you like to know today?
"""

SAMPLE_QUESTIONS = [
    "What Python courses are available?",
    "What is the fee for Data Science?",
    "Explain Retrieval-Augmented Generation.",
    "What is the attendance policy?",
    "What are the prerequisites for AI?",
    "How can I apply for admission?",
]


# ============================================================
# 4. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
            "time": datetime.now().strftime("%I:%M %p"),
        }
    ]

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# 5. CSS STYLING
# ============================================================

st.markdown(
    """
<style>

/* =========================================
   GLOBAL
========================================= */

.stApp {
    background: #e9edef;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* =========================================
   SIDEBAR
========================================= */

[data-testid="stSidebar"] {
    background: #ffffff;
}

[data-testid="stSidebar"] > div:first-child {
    background: #ffffff;
}

/* Sidebar headings */

.sidebar-title {
    color: #075e54 !important;
    font-size: 23px;
    font-weight: 700;
    margin-bottom: 5px;
}

.sidebar-description {
    color: #475569 !important;
    font-size: 13px;
    line-height: 1.6;
}

.sidebar-section {
    color: #075e54 !important;
    font-size: 16px;
    font-weight: 700;
    margin-top: 12px;
    margin-bottom: 10px;
}

/* Sidebar buttons */

[data-testid="stSidebar"] .stButton > button {
    background: #f8fafc !important;
    color: #202c33 !important;
    border: 1px solid #dce3e7 !important;
    border-radius: 9px !important;
    min-height: 42px;
}

[data-testid="stSidebar"] .stButton > button p {
    color: #202c33 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #e9f5ef !important;
    border-color: #075e54 !important;
}


/* =========================================
   CHAT SECTION
========================================= */

.chat-heading {
    color: #202c33 !important;
    font-size: 18px;
    font-weight: 700;
}

.chat-subheading {
    color: #667781 !important;
    font-size: 12px;
    margin-bottom: 15px;
}

/* Chat canvas */

.chat-canvas {
    background: #e9edef;
    padding: 12px;
    border-radius: 12px;
}

/* =========================================
   MESSAGE BUBBLES
========================================= */

.chat-row {
    display: flex;
    width: 100%;
    margin: 12px 0;
}

.assistant-row {
    justify-content: flex-start;
}

.user-row {
    justify-content: flex-end;
}

.chat-bubble {
    width: fit-content;
    max-width: 76%;
    padding: 12px 15px;
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    overflow-wrap: anywhere;
}

.assistant-bubble {
    background: #ffffff;
    border: 1px solid #dce3e7;
    border-top-left-radius: 3px;
}

.user-bubble {
    background: #d9fdd3;
    border: 1px solid #c5e8bc;
    border-top-right-radius: 3px;
}

.sender-name {
    color: #075e54 !important;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 7px;
}

.message-time {
    color: #8696a0 !important;
    font-size: 10px;
    text-align: right;
    margin-top: 8px;
}

/* =========================================
   MARKDOWN MESSAGE CONTENT
========================================= */

.message-content {
    color: #202c33 !important;
    font-size: 14px;
    line-height: 1.65;
    overflow-wrap: anywhere;
}

.message-content p {
    color: #202c33 !important;
    margin-bottom: 8px;
}

.message-content ul,
.message-content ol {
    color: #202c33 !important;
    padding-left: 22px;
}

.message-content li {
    color: #202c33 !important;
    margin-bottom: 5px;
}

.message-content strong {
    color: #075e54 !important;
}

/* =========================================
   SEARCH INDICATOR
========================================= */

.search-indicator {
    background: #ffffff;
    border: 1px solid #b8ded1;
    border-radius: 12px;
    padding: 14px;
    color: #075e54 !important;
    font-size: 14px;
    margin: 10px 0;
}

.search-indicator small {
    color: #64748b !important;
}

/* =========================================
   CHAT INPUT
========================================= */

[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #dce3e7 !important;
    border-radius: 20px !important;
}

[data-testid="stChatInput"] textarea {
    color: #202c33 !important;
    background: #ffffff !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8696a0 !important;
}

/* =========================================
   FOOTER
========================================= */

.app-footer {
    text-align: center;
    color: #667781 !important;
    font-size: 11px;
    padding: 18px;
    margin-top: 25px;
    border-top: 1px solid #dce3e7;
}

/* =========================================
   RESPONSIVE
========================================= */

@media(max-width: 700px) {

    .block-container {
        padding: 1rem 0.6rem;
    }

    .main-header {
        padding: 15px;
    }

    .header-title {
        font-size: 18px;
    }

    .chat-bubble {
        max-width: 92%;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 6. HEADER
# ============================================================


def render_header():

    with st.container(border=True):

        logo_col, title_col = st.columns([0.7, 5])

        with logo_col:
            st.markdown("# 🎓")

        with title_col:
            st.markdown(
                """
                <h3 style="
                    color: #123b35;
                    font-size: 24px;
                    font-weight: 800;
                    margin-bottom: 5px;
                ">
                    Student Support Assistant
                </h3>

                <p style="
                    color: #334155;
                    font-size: 14px;
                    font-weight: 600;
                    margin-top: 0;
                ">
                    🟢 Online · AI-powered academic support
                </p>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# 7. SIDEBAR
# ============================================================


def render_sidebar():

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-title">🎓 Student Assistant</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-description">'
            "Your assistant for courses and institute policies."
            "</div>",
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown(
            '<div class="sidebar-section">💡 Suggested Questions</div>',
            unsafe_allow_html=True,
        )

        for index, sample in enumerate(SAMPLE_QUESTIONS):

            if st.button(
                sample,
                key=f"suggestion_{index}",
                use_container_width=True,
            ):

                st.session_state.pending_question = sample
                st.rerun()

        st.divider()

        st.markdown(
            '<div class="sidebar-section">⚙️ Chat Settings</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True,
        ):

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": WELCOME_MESSAGE,
                    "time": datetime.now().strftime("%I:%M %p"),
                }
            ]

            st.session_state.pending_question = None
            st.rerun()

        st.divider()

        if DATABASE_READY:
            st.success("Knowledge Base Connected")
        else:
            st.error("Knowledge Base Unavailable")


# ============================================================
# 8. MESSAGE RENDERER
# ============================================================


def render_message(message):

    role = message["role"]
    content = message["content"]
    timestamp = html.escape(message.get("time", ""))

    if role == "assistant":
        row_class = "assistant-row"
        bubble_class = "assistant-bubble"
        sender = "🎓 Student Assistant"
    else:
        row_class = "user-row"
        bubble_class = "user-bubble"
        sender = "You"

    safe_sender = html.escape(sender)

    # Escape content before placing it inside HTML.
    # Markdown is rendered separately by Streamlit where possible.

    escaped_content = html.escape(content)

    st.markdown(
        f"""
        <div class="chat-row {row_class}">
            <div class="chat-bubble {bubble_class}">
                <div class="sender-name">{safe_sender}</div>
                <div class="message-content">
                    {escaped_content.replace(chr(10), '<br>')}
                </div>
                <div class="message-time">{timestamp}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 9. CHAT HISTORY
# ============================================================


def render_chat_history():

    for message in st.session_state.messages:

        render_message(message)


# ============================================================
# 10. PROCESS QUESTION
# ============================================================


def process_question(question):

    question = question.strip()

    if not question:
        return

    if not DATABASE_READY:
        st.error("Knowledge Base is unavailable.")
        return

    user_message = {
        "role": "user",
        "content": question,
        "time": datetime.now().strftime("%I:%M %p"),
    }

    st.session_state.messages.append(user_message)

    with st.chat_message("assistant", avatar="🎓"):

        with st.spinner("Searching the knowledge base..."):

            try:

                answer = ask_question(question)

                if not answer:
                    answer = (
                        "I couldn't find a relevant answer "
                        "in the institute knowledge base."
                    )

                assistant_message = {
                    "role": "assistant",
                    "content": str(answer),
                    "time": datetime.now().strftime("%I:%M %p"),
                }

                st.session_state.messages.append(assistant_message)

            except Exception as error:

                print(f"Chatbot error: {error}")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "Sorry, something went wrong while "
                            "processing your question. Please try again."
                        ),
                        "time": datetime.now().strftime("%I:%M %p"),
                    }
                )


# ============================================================
# 11. FOOTER
# ============================================================


def render_footer():

    st.markdown(
        """
        <div class="app-footer">
            Student Support Assistant
            <br>
            Powered by AI and Retrieval-Augmented Generation
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 12. MAIN APPLICATION
# ============================================================


def main():

    render_header()

    render_sidebar()

    st.markdown(
        """
        <div class="chat-heading">💬 Academic Support Chat</div>
        <div class="chat-subheading">
            Ask questions about courses, fees, admissions and policies.
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_chat_history()

    question = st.chat_input("Type a message...")

    if st.session_state.pending_question:

        question = st.session_state.pending_question
        st.session_state.pending_question = None

    if question:
        process_question(question)
        st.rerun()

    render_footer()


# ============================================================
# 13. APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
