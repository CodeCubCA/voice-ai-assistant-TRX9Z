import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Personality configurations
PERSONALITIES = {
    "General Assistant": {
        "name": "General Assistant",
        "emoji": "🤖",
        "description": "A helpful AI assistant for general tasks and questions",
        "system_prompt": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, concise, and accurate responses to user queries."
    },
    "Study Buddy": {
        "name": "Study Buddy",
        "emoji": "📚",
        "description": "An AI tutor to help with learning and studying",
        "system_prompt": "You are an encouraging and patient study buddy. Help users learn by breaking down complex topics, providing explanations, and asking questions to reinforce understanding. Use analogies and examples to make concepts clearer."
    },
    "Fitness Coach": {
        "name": "Fitness Coach",
        "emoji": "💪",
        "description": "A motivational fitness and wellness coach",
        "system_prompt": "You are an enthusiastic and motivating fitness coach. Provide workout advice, nutrition tips, and encouragement. Be positive, supportive, and focus on healthy, sustainable habits. Always remind users to consult healthcare professionals for medical advice."
    },
    "Gaming Helper": {
        "name": "Gaming Helper",
        "emoji": "🎮",
        "description": "A gaming companion for tips, strategies, and game discussions",
        "system_prompt": "You are a knowledgeable and enthusiastic gaming companion. Help users with game strategies, tips, walkthroughs, and general gaming discussions. Be friendly and share in their excitement about games."
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot with Gemini",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'personality' not in st.session_state:
    st.session_state.personality = "General Assistant"

if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""

if 'last_audio_bytes' not in st.session_state:
    st.session_state.last_audio_bytes = None

if 'message_sent' not in st.session_state:
    st.session_state.message_sent = False

# Function to convert audio to text
def transcribe_audio(audio_bytes):
    """Convert audio bytes to text using speech recognition"""
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Convert bytes to audio data
        audio_data = sr.AudioData(audio_bytes, sample_rate=16000, sample_width=2)

        # Perform recognition
        text = recognizer.recognize_google(audio_data)
        return text, None
    except sr.UnknownValueError:
        return None, "Could not understand audio. Please try again."
    except sr.RequestError as e:
        return None, f"Could not request results from speech recognition service: {e}"
    except Exception as e:
        return None, f"Error during transcription: {str(e)}"

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot Settings")
    st.markdown("---")

    # Personality selector
    st.subheader("Choose Personality")
    selected_personality = st.selectbox(
        "Select AI Personality:",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality),
        key='personality_selector'
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history on personality change
        st.rerun()

    # Display current personality info
    current_personality = PERSONALITIES[st.session_state.personality]
    st.markdown(f"### {current_personality['emoji']} {current_personality['name']}")
    st.markdown(f"*{current_personality['description']}*")

    st.markdown("---")
    st.subheader("How to Use Voice Input")
    st.markdown("""
    1. 🎤 Click the microphone button
    2. 🗣️ Speak your message clearly
    3. 🔴 Recording stops automatically after pause
    4. ✏️ Edit transcribed text if needed
    5. 📤 Click Send to submit
    """)

    st.markdown("---")
    st.subheader("About")
    st.markdown("""
    This chatbot uses:
    - **Streamlit** for the interface
    - **Google Gemini API** (gemini-2.5-flash)
    - **Voice Input** via speech recognition
    - Personalized AI personalities

    Clear the chat history by changing the personality!
    """)

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title(f"{PERSONALITIES[st.session_state.personality]['emoji']} AI Chatbot")
st.markdown(f"*Currently chatting with: **{st.session_state.personality}***")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice Input Section
st.markdown("### 💬 Send a Message")

# Voice Input Button
col_voice, col_status = st.columns([1, 3])

with col_voice:
    st.markdown("**🎤 Voice Input**")
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="2x",
        pause_threshold=2.0,
        sample_rate=16000
    )

with col_status:
    # Check if we have new audio (different from last processed)
    if audio_bytes and audio_bytes != st.session_state.last_audio_bytes:
        with st.spinner("🎙️ Transcribing audio..."):
            text, error = transcribe_audio(audio_bytes)
            if text:
                st.session_state.voice_text = text
                st.session_state.last_audio_bytes = audio_bytes
                st.success(f"✅ Transcribed: '{text}'")
            elif error:
                st.session_state.last_audio_bytes = audio_bytes
                st.error(f"❌ {error}")

    # Show current transcription if available
    if st.session_state.voice_text:
        st.info(f"📝 Ready to send: {st.session_state.voice_text}")

# Text Input Section
st.markdown("**⌨️ Type or Edit Your Message:**")

# Initialize the text input key dynamically
if 'input_counter' not in st.session_state:
    st.session_state.input_counter = 0

# Display the transcribed text in an editable text area
# The key changes with each send, forcing a new empty widget
user_input = st.text_area(
    "Message:",
    value=st.session_state.voice_text,
    height=100,
    key=f"message_input_{st.session_state.input_counter}",
    label_visibility="collapsed",
    placeholder="Type your message here or use the microphone button above..."
)

# Send button
send_clicked = st.button("📤 Send Message", type="primary", use_container_width=True)

# Handle send button
if send_clicked:
    if user_input.strip():
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        # Clear state and increment counter
        st.session_state.voice_text = ""
        st.session_state.last_audio_bytes = None
        st.session_state.input_counter += 1
        st.rerun()
    else:
        st.warning("⚠️ Please enter a message before sending.")

# Process AI response if there's a new user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Get the last user message
    prompt = st.session_state.messages[-1]["content"]

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Initialize the model with system instruction
            model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=PERSONALITIES[st.session_state.personality]['system_prompt']
            )

            # Build conversation history for context
            conversation_history = []
            for msg in st.session_state.messages[:-1]:  # Exclude the last message (current prompt)
                conversation_history.append({
                    "role": msg["role"],
                    "parts": [msg["content"]]
                })

            # Start chat with history
            chat = model.start_chat(history=conversation_history)

            # Get response
            response = chat.send_message(prompt)
            full_response = response.text

            # Display response
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "model", "content": full_response})
            st.rerun()

        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "model", "content": error_message})
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Powered by Google Gemini 2.5 Flash</div>",
    unsafe_allow_html=True
)
