[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Mbf-Zm77)

# Voice AI Assistant

An intelligent AI chatbot with comprehensive voice input and output capabilities, featuring multi-language support, personality modes, and voice command recognition. Built with Streamlit and powered by Google Gemini AI.

## Features

### Core Functionality
- **AI-Powered Conversations**: Intelligent responses powered by Google Gemini 2.5 Flash model
- **Voice Input**: Click-to-record voice input with automatic speech-to-text conversion
- **Voice Output**: Text-to-speech audio playback for all AI responses
- **Multi-Language Support**: Communicate in 5 languages (English, Spanish, French, Chinese, Japanese)
- **Text Input**: Traditional keyboard input with editable transcriptions
- **Chat History**: Persistent conversation history throughout the session

### Voice Commands
Control the assistant hands-free with voice commands:
- **"clear chat"** - Clear conversation history
- **"change personality"** - Switch AI personality mode
- **"speak faster"** - Increase TTS speed to normal
- **"speak slower"** - Decrease TTS speed
- **"help"** - Show all available commands

Supports natural variations like "reset chat", "speed up", etc.

### Personality Modes
Choose from 4 different AI personalities:
- **General Assistant** 🤖 - Helpful AI for general tasks and questions
- **Study Buddy** 📚 - Patient tutor for learning and studying
- **Fitness Coach** 💪 - Motivational fitness and wellness guide
- **Gaming Helper** 🎮 - Gaming companion for tips and strategies

### Multi-Language Support
Full voice input and output support for:
- 🇺🇸 English
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇨🇳 Chinese Mandarin (中文)
- 🇯🇵 Japanese (日本語)

AI responds in your selected language with matching TTS audio.

### User Interface
- Clean, modern design with Streamlit
- Real-time transcription feedback
- Visual language and personality indicators
- Audio playback controls for AI responses
- Collapsible help sections
- Responsive layout

## Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Voice Recording**: audio-recorder-streamlit
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Language**: Python 3.13+

## Installation

### Prerequisites
- Python 3.13 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Microphone access for voice input

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodeCubCA/voice-ai-assistant-TRX9Z.git
   cd voice-ai-assistant-TRX9Z
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser and navigate to: `http://localhost:8501`

## Usage

### Voice Input
1. Select your language from the sidebar (🌍 Choose Language)
2. Click the microphone button 🎤
3. Speak clearly in your selected language
4. Wait for automatic transcription (stops after 2-second pause)
5. Review/edit the transcribed text if needed
6. Click "📤 Send Message"

### Voice Commands
Say commands directly to control the assistant:
- "help" - See all available commands
- "clear chat" - Reset conversation
- "speak slower" - Adjust TTS speed
- "change personality" - Switch AI mode

### Text Input
1. Type your message in the text area
2. Click "📤 Send Message"

### Changing Settings
- **Language**: Use sidebar dropdown (🌍 Choose Language)
- **Personality**: Use sidebar dropdown (Choose Personality)
- **Clear History**: Click "🗑️ Clear Chat History" button

### Audio Playback
- AI responses automatically include audio in your selected language
- Click the play button to listen
- Audio is cached for faster playback

## Project Structure

```
voice-ai-assistant-TRX9Z/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API key) - NOT committed
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## Dependencies

- `streamlit>=1.31.0` - Web application framework
- `google-generativeai>=0.3.2` - Google Gemini API client
- `python-dotenv>=1.0.0` - Environment variable management
- `audio-recorder-streamlit>=0.0.8` - Voice recording component
- `SpeechRecognition>=3.10.0` - Speech-to-text conversion
- `pydub>=0.25.1` - Audio processing
- `gtts>=2.3.0` - Text-to-speech generation

## Key Features Explained

### Voice Command Recognition
The assistant automatically detects when you're giving a command versus having a conversation. Commands are processed immediately without being sent to the AI.

### Multi-Language Intelligence
- Voice recognition adapts to your selected language
- AI responds in the chosen language
- TTS audio matches the language setting
- Audio is cached per language for efficiency

### Personality System
Each personality has its own system prompt that shapes the AI's responses:
- General Assistant: Helpful and informative
- Study Buddy: Patient and educational
- Fitness Coach: Motivating and health-focused
- Gaming Helper: Enthusiastic about games

### TTS Speed Control
Control how fast the AI speaks:
- Normal speed (default): Natural conversation pace
- Slow speed: Better for language learning or complex topics

## Security Notes

- The `.env` file containing your API key is excluded from version control
- Never commit your actual API key to the repository
- Use the provided `.env.example` as a template
- API key is loaded securely using python-dotenv

## Contributing

This is a student project for educational purposes. If you'd like to contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is created for educational purposes as part of a coding assignment.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini API](https://ai.google.dev/)
- Voice input using [audio-recorder-streamlit](https://github.com/Joooohan/audio-recorder-streamlit)
- Speech recognition via [Google Speech Recognition API](https://cloud.google.com/speech-to-text)
- Text-to-speech via [gTTS](https://github.com/pndurette/gTTS)
- Generated with assistance from [Claude Code](https://claude.com/claude-code)

## Troubleshooting

### Common Issues

**Issue**: API key error
- **Solution**: Make sure your `.env` file exists and contains a valid `GEMINI_API_KEY`

**Issue**: Voice input not working
- **Solution**: Ensure your microphone is connected and browser has microphone permissions

**Issue**: Dependencies installation fails
- **Solution**: Make sure you're using Python 3.13+ and try `pip3 install -r requirements.txt`

**Issue**: Speech recognition errors
- **Solution**: Speak clearly and wait for the recording to auto-stop (2-second pause)

**Issue**: TTS audio not playing
- **Solution**: Check browser audio permissions and volume settings

**Issue**: Wrong language recognition
- **Solution**: Verify the correct language is selected in the sidebar before speaking

**Issue**: Voice commands not working
- **Solution**: Say commands clearly in English (e.g., "help", "clear chat")

## Sample Usage Examples

### English Conversation
1. Select "English" from language dropdown
2. Click microphone and say "Hello, how are you?"
3. AI responds in English with audio playback

### Spanish Conversation
1. Select "Español" from language dropdown
2. Click microphone and say "Hola, ¿cómo estás?"
3. AI responds in Spanish with Spanish audio

### Using Voice Commands
1. Say "help" to see all commands
2. Say "speak slower" to adjust TTS speed
3. Say "clear chat" to reset conversation

### Personality Modes
1. Select "Study Buddy" for educational help
2. Ask "Can you explain quantum physics?"
3. Get patient, educational responses

## Future Enhancements

Potential features for future development:
- Additional languages
- Custom personality creation
- Conversation export
- Voice authentication
- Offline mode
- Mobile app version

## Contact

For questions or issues, please open an issue on the GitHub repository.

---

**Built with ❤️ using Python, Streamlit, and Google Gemini AI**
