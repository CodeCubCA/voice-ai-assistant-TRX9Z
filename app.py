import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
from gtts import gTTS
from io import BytesIO
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Voice configurations
VOICES = {
    "Female": {
        "name": "Female",
        "icon": "👩",
        "tld": "com",  # US English female voice
        "description": "Female voice"
    },
    "Male": {
        "name": "Male",
        "icon": "👨",
        "tld": "co.uk",  # UK English male-like voice
        "description": "Male voice"
    }
}

# Language configurations
LANGUAGES = {
    "English": {
        "name": "English",
        "flag": "🇺🇸",
        "tts_code": "en",
        "speech_code": "en-US",
        "display_name": "English"
    },
    "Spanish": {
        "name": "Spanish",
        "flag": "🇪🇸",
        "tts_code": "es",
        "speech_code": "es-ES",
        "display_name": "Español"
    },
    "French": {
        "name": "French",
        "flag": "🇫🇷",
        "tts_code": "fr",
        "speech_code": "fr-FR",
        "display_name": "Français"
    },
    "Chinese": {
        "name": "Chinese",
        "flag": "🇨🇳",
        "tts_code": "zh-CN",
        "speech_code": "zh-CN",
        "display_name": "中文"
    },
    "Japanese": {
        "name": "Japanese",
        "flag": "🇯🇵",
        "tts_code": "ja",
        "speech_code": "ja-JP",
        "display_name": "日本語"
    }
}

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

if 'language' not in st.session_state:
    st.session_state.language = "English"

if 'voice' not in st.session_state:
    st.session_state.voice = "Female"

if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""

if 'last_audio_bytes' not in st.session_state:
    st.session_state.last_audio_bytes = None

if 'message_sent' not in st.session_state:
    st.session_state.message_sent = False

if 'tts_audio' not in st.session_state:
    st.session_state.tts_audio = {}

if 'processing_tts' not in st.session_state:
    st.session_state.processing_tts = False

if 'tts_speed' not in st.session_state:
    st.session_state.tts_speed = False  # False = normal speed, True = slow speed

if 'command_feedback' not in st.session_state:
    st.session_state.command_feedback = None

# Function to parse voice commands
def parse_command(text):
    """Parse user input for voice commands and return command type"""
    text_lower = text.lower().strip()

    # Command definitions with aliases
    if any(keyword in text_lower for keyword in ['clear chat', 'clear history', 'reset chat', 'new chat']):
        return 'clear_chat'
    elif any(keyword in text_lower for keyword in ['change personality', 'switch personality', 'change mode']):
        return 'change_personality'
    elif any(keyword in text_lower for keyword in ['speak faster', 'speed up', 'faster', 'talk faster']):
        return 'speak_faster'
    elif any(keyword in text_lower for keyword in ['speak slower', 'slow down', 'slower', 'talk slower']):
        return 'speak_slower'
    elif any(keyword in text_lower for keyword in ['help', 'show commands', 'what can you do', 'commands']):
        return 'help'

    return None  # No command detected

# Function to execute voice commands
def execute_command(command):
    """Execute the parsed voice command and return feedback message"""
    if command == 'clear_chat':
        st.session_state.messages = []
        st.session_state.tts_audio = {}
        return "✅ Chat history cleared!"

    elif command == 'change_personality':
        return "🔄 Please use the sidebar to select a different personality."

    elif command == 'speak_faster':
        st.session_state.tts_speed = False
        return "⚡ TTS speed set to normal (faster)."

    elif command == 'speak_slower':
        st.session_state.tts_speed = True
        return "🐢 TTS speed set to slow."

    elif command == 'help':
        return """📋 **Available Voice Commands:**

- **"clear chat"** - Clear conversation history
- **"change personality"** - Switch AI personality
- **"speak faster"** - Increase TTS speed
- **"speak slower"** - Decrease TTS speed
- **"help"** - Show this command list

You can also use natural variations like "reset chat", "speed up", etc."""

    return None

# Function to convert audio to text
def transcribe_audio(audio_bytes, language_code="en-US"):
    """Convert audio bytes to text using speech recognition"""
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Convert bytes to audio data
        audio_data = sr.AudioData(audio_bytes, sample_rate=16000, sample_width=2)

        # Perform recognition with specified language
        text = recognizer.recognize_google(audio_data, language=language_code)
        return text, None
    except sr.UnknownValueError:
        return None, "Could not understand audio. Please try again."
    except sr.RequestError as e:
        return None, f"Could not request results from speech recognition service: {e}"
    except Exception as e:
        return None, f"Error during transcription: {str(e)}"

# Function to generate text-to-speech audio
def generate_tts_audio(text, message_index, language_code="en", voice_tld="com"):
    """Generate TTS audio for the given text with progress feedback"""
    try:
        # Create unique cache key with language and voice
        cache_key = f"{message_index}_{language_code}_{voice_tld}"

        # Check if audio already exists for this message, language, and voice
        if cache_key in st.session_state.tts_audio:
            return st.session_state.tts_audio[cache_key], None

        # Truncate very long messages for TTS (>1000 chars)
        if len(text) > 1000:
            text = text[:1000] + "..."
            warning_msg = "⚠️ Message truncated to 1000 characters for audio generation."
        else:
            warning_msg = None

        # Show warning for long messages
        if len(text) > 500 and warning_msg is None:
            warning_msg = "⏳ Long message - audio generation may take a moment..."

        # Generate TTS audio with spinner
        with st.spinner("🎵 Generating audio..."):
            # Add small delay to avoid rate limiting
            time.sleep(0.5)

            # Use session state speed setting, selected language, and voice
            tts = gTTS(text=text, lang=language_code, slow=st.session_state.tts_speed, tld=voice_tld)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_bytes = audio_buffer.read()

            # Store in session state with language and voice-specific key
            st.session_state.tts_audio[cache_key] = audio_bytes

        return audio_bytes, warning_msg

    except Exception as e:
        # Handle specific rate limit errors
        if "429" in str(e) or "Too Many Requests" in str(e):
            error_msg = "⚠️ TTS rate limit reached. Please wait a moment before generating more audio."
        else:
            error_msg = f"❌ Audio generation failed: {str(e)}"
        return None, error_msg

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot Settings")
    st.markdown("---")

    # Language selector
    st.subheader("🌍 Choose Language")
    selected_language = st.selectbox(
        "Select Language:",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language),
        format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['display_name']}",
        key='language_selector'
    )

    # Update language if changed
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

    # Display current language info
    current_language = LANGUAGES[st.session_state.language]
    st.markdown(f"**Current:** {current_language['flag']} {current_language['display_name']}")

    st.markdown("---")

    # Voice selector
    st.subheader("🎤 Choose Voice")
    selected_voice = st.selectbox(
        "Select Voice:",
        options=list(VOICES.keys()),
        index=list(VOICES.keys()).index(st.session_state.voice),
        format_func=lambda x: f"{VOICES[x]['icon']} {VOICES[x]['name']}",
        key='voice_selector'
    )

    # Update voice if changed
    if selected_voice != st.session_state.voice:
        st.session_state.voice = selected_voice
        # Clear TTS cache when voice changes
        st.session_state.tts_audio = {}
        st.rerun()

    # Display current voice info
    current_voice = VOICES[st.session_state.voice]
    st.markdown(f"**Current:** {current_voice['icon']} {current_voice['name']}")

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

    # Voice Commands in expandable section
    with st.expander("🎤 Voice Commands", expanded=False):
        st.markdown("""
        **Say these commands to control the assistant:**

        - 🗑️ **"clear chat"** - Reset conversation
        - 🔄 **"change personality"** - Switch mode
        - ⚡ **"speak faster"** - Normal speed
        - 🐢 **"speak slower"** - Slow speed
        - ❓ **"help"** - Show all commands

        **Tip:** You can also use variations like "reset chat", "speed up", etc.
        """)

    # Voice & Audio Features in expandable section
    with st.expander("🎙️ Voice & Audio Features", expanded=False):
        st.markdown("**Voice Input:**")
        st.markdown("""
        1. 🎤 Click microphone button
        2. 🗣️ Speak in your selected language
        3. Auto-stops after 2s pause
        4. ✏️ Edit text if needed
        5. 📤 Send message
        """)

        st.markdown("**Audio Playback:**")
        st.markdown("""
        - 🔊 AI responses include audio in selected language
        - Click play to listen
        - Audio cached for speed
        - Long messages may be truncated
        """)

    st.markdown("---")

    # About section in expandable
    with st.expander("ℹ️ About", expanded=False):
        st.markdown("""
        **Technologies:**
        - Streamlit UI
        - Google Gemini 2.5 Flash
        - Speech Recognition
        - Text-to-Speech (gTTS)

        **Tip:** Change personality to clear chat!
        """)

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
current_lang = LANGUAGES[st.session_state.language]
st.title(f"{PERSONALITIES[st.session_state.personality]['emoji']} AI Chatbot {current_lang['flag']}")
st.markdown(f"*Currently chatting with: **{st.session_state.personality}** • Language: **{current_lang['display_name']}***")

# Show command feedback if available
if st.session_state.command_feedback:
    st.success(st.session_state.command_feedback)
    st.session_state.command_feedback = None  # Clear after displaying

# Show helpful tip if no messages yet
if len(st.session_state.messages) == 0:
    st.info("💡 **Quick Start:** Type a message or click the microphone to speak. Try saying 'help' to see voice commands!")

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Display audio player for AI messages (outside chat_message container)
    if message["role"] == "model":
        # Generate audio and get any warnings/errors
        tts_lang_code = LANGUAGES[st.session_state.language]['tts_code']
        voice_tld = VOICES[st.session_state.voice]['tld']
        audio_result = generate_tts_audio(message["content"], idx, tts_lang_code, voice_tld)

        if audio_result:
            audio_bytes, feedback_msg = audio_result

            # Show warning or error message if any
            if feedback_msg:
                if "failed" in feedback_msg.lower():
                    st.error(feedback_msg)
                else:
                    st.warning(feedback_msg)

            # Display audio player with improved layout
            if audio_bytes:
                # Add divider for visual separation
                st.markdown("---")

                # Use columns for better layout
                col_audio_label, col_audio_player = st.columns([1, 4])

                with col_audio_label:
                    st.markdown("**🔊 Listen:**")

                with col_audio_player:
                    st.audio(audio_bytes, format='audio/mp3')

                # Add spacing after audio
                st.markdown("")

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
            # Get current language code for speech recognition
            lang_code = LANGUAGES[st.session_state.language]['speech_code']
            text, error = transcribe_audio(audio_bytes, lang_code)
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
        # Check if input is a voice command
        command = parse_command(user_input.strip())

        if command:
            # Execute the command
            feedback = execute_command(command)
            st.session_state.command_feedback = feedback

            # Clear input state
            st.session_state.voice_text = ""
            st.session_state.last_audio_bytes = None
            st.session_state.input_counter += 1
            st.rerun()
        else:
            # Not a command, add as regular message to chat history
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
            # Get current language
            current_lang = LANGUAGES[st.session_state.language]

            # Build system instruction with personality and language
            base_prompt = PERSONALITIES[st.session_state.personality]['system_prompt']
            language_instruction = f"\n\nIMPORTANT: Please respond in {current_lang['display_name']}."

            # Initialize the model with system instruction
            model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=base_prompt + language_instruction
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
