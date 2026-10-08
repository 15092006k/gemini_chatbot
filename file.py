
import streamlit as st
from google import genai


# ==========================================================
# GOOGLE AI STUDIO API KEY
# ==========================================================

API_KEY = "AQ.Ab8RN6I69WJXEYilH2XCyvqcOLePX7K5c9KkgUk2yTxvFZjZPA"


# ==========================================================
# GEMINI MODEL
# ==========================================================

MODEL_NAME = "gemini-3.1-flash-lite"


# ==========================================================
# STREAMLIT PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ==========================================================
# TITLE
# ==========================================================

st.title("🤖 Gemini AI Chatbot")

st.write(
    "Chat with Google's Gemini AI using Python and Streamlit."
)


# ==========================================================
# CHAT HISTORY
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.write("### Model")

    st.info(MODEL_NAME)

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ==========================================================
# DISPLAY CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================================
# USER INPUT
# ==========================================================

user_message = st.chat_input(
    "Type your message here..."
)


# ==========================================================
# SEND MESSAGE
# ==========================================================

if user_message:

    # ------------------------------------------------------
    # Display user's message
    # ------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_message)

    # Save user's message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # ------------------------------------------------------
    # Generate Gemini response
    # ------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🤔 Gemini is thinking..."):

            try:

                # Create a NEW client for this request
                client = genai.Client(
                    api_key=API_KEY
                )


                # --------------------------------------------------
                # Prepare conversation history
                # --------------------------------------------------

                conversation = []

                for message in st.session_state.messages:

                    conversation.append(
                        {
                            "role": message["role"],
                            "parts": [
                                {
                                    "text": message["content"]
                                }
                            ]
                        }
                    )


                # --------------------------------------------------
                # Send conversation to Gemini
                # --------------------------------------------------

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=conversation
                )


                # Get Gemini response
                answer = response.text


                # Display response
                st.markdown(answer)


                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


                # Close client after request
                client.close()


            except Exception as e:

                st.error(
                    "❌ An error occurred:\n\n"
                    + str(e)
                )
