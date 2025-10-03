import streamlit as st

# Page config
st.set_page_config(page_title="Learn Recursion", layout="wide")

st.title("Learn Recursion by Doing")
st.markdown("**Your goal:** Write a function `factorial(n)` that returns n!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Two columns: code editor and chat
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Your Code")
    user_code = st.text_area(
        "Write your factorial function here:",
        height=300,
        placeholder="def factorial(n):\n    # Your code here\n    pass"
    )

    if st.button("I'm stuck! Help me"):
        st.session_state.messages.append({
            "role": "user",
            "content": f"I'm stuck. Here's my code:\n```python\n{user_code}\n```"
        })

with col2:
    st.subheader("AI Tutor")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

st.markdown("---")
st.markdown("**Test cases:**")
st.code("factorial(0) = 1\nfactorial(3) = 6\nfactorial(5) = 120")
