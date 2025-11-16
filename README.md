[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Mbf-Zm77)

# Voice AI Assistant Chatbot

A simple yet powerful AI chatbot web application built with Streamlit and Google Gemini API, featuring voice input capability for hands-free interaction.

## Features

### Core Functionality
- **AI-Powered Conversations**: Uses Google Gemini 2.5 Flash model for intelligent responses
- **Voice Input**: Click-to-record voice input with automatic speech-to-text conversion
- **Text Input**: Traditional keyboard input option
- **Editable Transcriptions**: Review and edit voice transcriptions before sending
- **Chat History**: Complete conversation history maintained throughout the session

### Personality Modes
Choose from 4 different AI personalities:
- **General Assistant**: Helpful AI for general tasks and questions
- **Study Buddy**: Patient tutor for learning and studying
- **Fitness Coach**: Motivational fitness and wellness guide
- **Gaming Helper**: Gaming companion for tips and strategies

### User Interface
- Clean, modern design with Streamlit
- Real-time transcription feedback
- Visual indicators for recording status
- Responsive layout

## Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Voice Recording**: audio-recorder-streamlit
- **Speech Recognition**: Google Speech Recognition API
- **Language**: Python 3.13+

## Installation

### Prerequisites
- Python 3.13 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

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
1. Click the microphone button
2. Speak your message clearly
3. Wait for automatic transcription (stops after 2-second pause)
4. Review/edit the transcribed text if needed
5. Click "Send Message"

### Text Input
1. Type your message in the text area
2. Click "Send Message"

### Changing Personality
- Use the sidebar dropdown to select different AI personalities
- Chat history clears when switching personalities

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

## Security Notes

- The `.env` file containing your API key is excluded from version control
- Never commit your actual API key to the repository
- Use the provided `.env.example` as a template

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

## Contact

For questions or issues, please open an issue on the GitHub repository.
