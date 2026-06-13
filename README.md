# Voice Assisted KidzAgent

A privacy-first, voice-based reading buddy for kids ages 5–8 to practice reading aloud at home.

## 🎯 Project Overview

**Voice Assisted KidzAgent** helps early readers (ages 5–8) practice reading aloud in short, supportive sessions. The AI listens in real time, offers gentle corrections, explains unfamiliar words in kid-friendly language, and provides encouraging feedback.

### Key Features

- 🎤 **Real-Time Speech Recognition**: Listen and respond to children's reading
- 💡 **Kid-Friendly Explanations**: Explain words in language designed for young learners
- 🎉 **Encouraging Feedback**: Positive, supportive messages to build confidence
- 🔒 **Privacy-First**: Minimal data collection, child-safe by design
- 📊 **Progress Tracking**: Parental dashboard to monitor reading improvements
- ⏱️ **Short Sessions**: 5–15 minute sessions fit busy family schedules

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository** (or extract the project files)

```bash
cd VoiceAssistedKidZAI
```

2. **Create a virtual environment**

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your configuration
# Add your Azure OpenAI credentials
```

5. **Initialize the database**

```bash
python run.py init-db
```

6. **Seed sample data** (optional)

```bash
python run.py seed-db
```

### Running the Application

```bash
python run.py
```

The application will start at `http://localhost:5000`

## 📁 Project Structure

```
VoiceAssistedKidZAI/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   └── __init__.py             # Database models
│   ├── routes/
│   │   ├── __init__.py             # Route blueprints
│   │   ├── main.py                 # Main routes
│   │   ├── session.py              # Reading session routes
│   │   └── api.py                  # API endpoints
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── llm_helper.py           # Azure LLM integration
│   │   ├── speech_helper.py        # Speech-to-text utilities
│   │   └── content_filter.py       # Child-safe content filtering
│   ├── templates/                  # Jinja2 HTML templates
│   └── static/
│       ├── css/
│       │   ├── style.css           # Main styles
│       │   └── session.css         # Reading session styles
│       └── js/
│           ├── main.js             # Main JavaScript
│           └── session.js          # Session-specific JS
├── config.py                       # Flask configuration
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

## 🛠️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_API_KEY=your-api-key
AZURE_DEPLOYMENT_NAME=gpt-4
```

### Database

The app uses SQLite by default. To switch databases:

Edit `config.py` and change `SQLALCHEMY_DATABASE_URI` in the `Config` class.

## 📖 Usage

### For Children

1. Select "Start Reading Session" on the home page
2. Choose your name from the list
3. Pick a story to read
4. Click on each word and read it aloud
5. Get instant feedback and encouragement
6. See your results when finished

### For Parents

1. Visit the Dashboard at `/dashboard`
2. View each child's reading progress
3. See accuracy scores and sessions completed
4. Monitor reading level improvements

## 🔐 Safety & Privacy

- **Content Filtering**: All AI responses are checked for age-appropriateness
- **Minimal Data Collection**: Only stores reading session data needed for progress tracking
- **No Third-Party Tracking**: No ads, analytics, or external data sharing
- **Parental Controls**: Parents have full visibility into child progress
- **Audio Processing**: Speech audio is processed securely and not stored permanently

## 🧠 AI Integration

### Azure OpenAI / Copilot

The app uses Azure OpenAI to generate:
- **Corrections**: How to pronounce words correctly
- **Explanations**: Kid-friendly definitions of unfamiliar words
- **Encouragement**: Positive, age-appropriate feedback

All responses are filtered to ensure they're safe for children ages 5–8.

### Speech Recognition

- **Frontend**: Uses Web Speech API for real-time listening
- **Backend**: Integrates with Google Cloud Speech-to-Text for accurate transcription

## 🧪 Testing

To run tests (if implemented):

```bash
pytest
```

## 📊 Database Models

### User
Represents parents/guardians managing reading sessions

### Child
Represents a child learner with age and reading level

### ReadingPassage
Pre-curated stories appropriate for different age groups

### ReadingSession
A single reading practice session with performance metrics

### SessionFeedback
Word-level feedback during a session

### ProgressMetric
Aggregate progress tracking for each child

## 🚨 Troubleshooting

### Speech Recognition Not Working

- Ensure browser supports Web Speech API (Chrome, Edge, Safari)
- Check microphone permissions
- Verify HTTPS on production (required for audio)

### Azure API Errors

- Verify `AZURE_API_KEY` and `AZURE_ENDPOINT` in `.env`
- Check API quota in Azure portal
- Ensure deployment name matches configuration

### Database Issues

- Delete `kidzagent.db` to reset
- Run `python run.py init-db` to reinitialize

## 📝 License

Privacy-first educational technology. See LICENSE file for details.

## 🤝 Contributing

To contribute improvements:

1. Create a feature branch
2. Make your changes
3. Ensure child safety is maintained
4. Submit a pull request

## 📞 Support

For questions or issues, please check the documentation or reach out to the development team.

---

**Made with ❤️ for young readers everywhere**
