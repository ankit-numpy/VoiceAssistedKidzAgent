<!-- Use this file to provide workspace-specific custom instructions to Copilot -->

# Voice Assisted KidzAgent - Development Guide

## Project Context

This is a **Flask-based web application** for a privacy-first, voice-based reading buddy designed for kids ages 5–8.

### Tech Stack
- **Backend**: Flask with SQLAlchemy ORM
- **Frontend**: Jinja2 templates with HTML/CSS/JavaScript
- **Database**: SQLite
- **LLM**: Azure OpenAI / Copilot
- **Speech**: Google Cloud Speech-to-Text (backend) + Web Speech API (frontend)

## Project Structure

```
app/
├── __init__.py          # Flask app factory
├── models/              # Database models (User, Child, ReadingSession, etc.)
├── routes/              # Route handlers (main, session, api)
├── utils/               # Utilities (LLM, speech, content filtering)
├── templates/           # Jinja2 HTML templates
└── static/              # CSS, JavaScript
config.py              # Flask configuration
run.py                 # Application entry point
requirements.txt       # Python dependencies
```

## Development Workflow

### Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your Azure credentials
```

### Running Locally

```bash
python run.py
```

Visit `http://localhost:5000`

### Database Management

```bash
python run.py init-db    # Initialize database
python run.py seed-db    # Populate with sample data
```

## Key Features

- **Real-time Speech Recognition**: Uses Web Speech API + backend transcription
- **AI-Powered Feedback**: Azure Copilot generates corrections and explanations
- **Content Safety**: All responses filtered for child-appropriateness
- **Progress Tracking**: Parental dashboard with reading metrics
- **Privacy-First**: Minimal data collection, no third-party tracking

## Important Guidelines

### Child Safety
- All AI responses must be checked for age-appropriateness
- Use `content_filter.py` to sanitize responses
- Never include adult content, violence, or scary themes
- Keep language simple (K–3 reading level)

### Privacy
- Store minimal user data (no personal tracking)
- Session audio processed but not stored permanently
- Parents have full visibility into child progress
- Compliance with COPPA (Children's Online Privacy Protection Act)

### Code Organization
- Place database models in `app/models/`
- Route handlers in `app/routes/` (use blueprints)
- Utility functions in `app/utils/`
- HTML templates in `app/templates/`
- Stylesheets and JS in `app/static/`

## Common Tasks

### Adding a New Reading Passage
1. Create a new `ReadingPassage` in the database with appropriate age group
2. Verify content is child-safe
3. Set difficulty level (easy, medium, hard)

### Adding a New Child
1. Use the `Child` model with parent_id, name, and age
2. Set initial reading_level (beginner, intermediate, advanced)

### Creating New Routes
1. Define blueprint in `app/routes/`
2. Register in `app/__init__.py`
3. Create corresponding templates in `app/templates/`

### Modifying LLM Prompts
1. Edit prompts in `app/utils/llm_helper.py`
2. Keep language simple and kid-friendly
3. Test responses for safety

## Environment Variables

See `.env.example` for all required variables. Key ones:
- `AZURE_ENDPOINT`: Your Azure OpenAI endpoint
- `AZURE_API_KEY`: Your API key
- `AZURE_DEPLOYMENT_NAME`: Model deployment name (e.g., gpt-4)

## Testing Checklist

- [ ] Application starts without errors
- [ ] Database initializes properly
- [ ] Reading sessions can be created
- [ ] AI feedback is generated correctly
- [ ] Progress is tracked in database
- [ ] Parental dashboard displays data
- [ ] Content is child-safe

## Next Steps

- [ ] Implement user authentication
- [ ] Add parental controls
- [ ] Expand reading passage library
- [ ] Integrate real Google Cloud Speech-to-Text
- [ ] Deploy to Azure
- [ ] Add analytics (privacy-respecting)
- [ ] Create admin panel for content management

---

**For detailed information, see README.md**
