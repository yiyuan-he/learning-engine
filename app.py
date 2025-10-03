import streamlit as st
from anthropic import Anthropic
import os
from snippets import SNIPPETS

# Page config
st.set_page_config(page_title="Learn Recursion", layout="wide")

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def diagnose_and_help(user_code):
    """Use Claude to diagnose what concept the user is missing"""

    prompt = f"""You are a helpful coding tutor. A student is trying to write a factorial function recursively and is stuck.

Their code:
```python
{user_code}
```

Available learning snippets:
- base_case: Explains why you need a base case to stop recursion
- recursive_case: Explains how to write the recursive call (n * factorial(n-1))
- trust_recursion: Explains the mental model of trusting recursion works

Analyze their code and determine which ONE snippet would help them most right now. Respond with ONLY the snippet key (base_case, recursive_case, or trust_recursion).

If their code is empty or they haven't started, return: base_case
If they have no base case or infinite recursion: base_case
If they have base case but no recursive call: recursive_case
If they have both but seem confused about how it works: trust_recursion"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )

    snippet_key = message.content[0].text.strip()
    return SNIPPETS.get(snippet_key, SNIPPETS["base_case"])

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

        # Get AI diagnosis and snippet
        with st.spinner("Thinking..."):
            snippet = diagnose_and_help(user_code)
            st.session_state.messages.append({
                "role": "assistant",
                "content": snippet
            })
        st.rerun()

with col2:
    st.subheader("AI Tutor")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

st.markdown("---")
st.markdown("**Test cases:**")
st.code("factorial(0) = 1\nfactorial(3) = 6\nfactorial(5) = 120")
