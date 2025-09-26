# Mini Regulatory Report Assistant - Feyti Medical Group

## Project Overview
A full-stack application that processes adverse event reports using AI/NLP techniques. The system extracts structured data from medical reports and provides a user-friendly interface for regulatory compliance.

## Live Demo
- Backend (PythonAnywhere): https://asj234.pythonanywhere.com
- API base (PythonAnywhere): https://asj234.pythonanywhere.com/api
- Admin dashboard (PythonAnywhere) : https://asj234.pythonanywhere.com/admin
- Frontend (Vercel): https://software-intern-ai-project.vercel.app
  - Set `REACT_APP_API_URL=https://asj234.pythonanywhere.com/api` in Vercel Environment Variables (and in `frontend/.env` for local builds).

## Assignment Requirements

### Part 1: Backend (Python - Django REST Framework) ✅ COMPLETED
- [x] **API Endpoint**: POST /api/process-report/
- [x] **Input Processing**: JSON with medical report text
- [x] **NLP Extraction**: 
  - Drug name extraction
  - Adverse events identification
  - Severity classification (mild, moderate, severe)
  - Outcome determination (recovered, ongoing, fatal)
- [x] **Output Format**: Structured JSON response
- [x] **Database**: SQLite integration for report storage
- [x] **Bonus Features**:
  - [x] GET /api/reports/ endpoint for history
  - [x] POST /api/translate/ endpoint for French/Swahili translation
  - [x] GET /api/analytics/ endpoint for data analytics

### Part 2: Frontend (React) ✅ COMPLETED
- [x] **Input Form**: Text area for medical report entry
- [x] **Process Button**: Submit report for analysis
- [x] **Results Display**: Cards/table showing extracted data
- [x] **Bonus Features**:
  - [x] Translation buttons (French/Swahili)
  - [x] History view of processed reports
  - [x] Charts for severity distribution
  - [x] Analytics dashboard with data visualization

### Technical Requirements
- [x] **Backend**: Python with Django REST Framework
- [x] **Frontend**: React application
- [x] **Communication**: JSON API
- [x] **Database**: SQLite for data persistence
- [x] **Folder Structure**: Clear separation (backend/ + frontend/)

## Project Structure
```
Full_stack_Assignment/
├── backend/
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   ├── setup.py           # Setup script
│   ├── test_django_api.py # API testing script
│   ├── regulatory_assistant/
│   │   ├── __init__.py
│   │   ├── settings.py    # Django settings
│   │   ├── urls.py        # Main URL configuration
│   │   ├── wsgi.py        # WSGI configuration
│   │   └── asgi.py        # ASGI configuration
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── models.py      # Database models
│   │   ├── serializers.py # API serializers
│   │   ├── views.py       # API views
│   │   ├── urls.py        # App URL configuration
│   │   ├── admin.py       # Admin interface
│   │   ├── apps.py        # App configuration
│   │   └── nlp_processor.py # NLP processing logic
│   └── db.sqlite3         # SQLite database (auto-created)
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Styling
│   └── package.json       # Node.js dependencies
└── README.md              # This file
```

## Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git (optional)

### Environment Variables
Create a `.env` file in `backend/` for Django settings:

```env
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Optionally, create a `.env` file in `frontend/` for the API base URL (defaults to `http://localhost:8000/api` if not set):

```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Backend Setup (Local)
1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script** (automatically handles migrations and spaCy model):
   ```bash
   python setup.py
   ```

5. **Start the Django server**:
   ```bash
   python manage.py runserver
   ```
   Server will start at: http://localhost:8000
   Admin interface: http://localhost:8000/admin (username: admin, password: admin123)

6. **(Recommended) Create a superuser for admin login**:
   ```bash
   python manage.py createsuperuser
   ```
   Follow prompts to set your own credentials, then use them at `/admin`.

### Frontend Setup (Local)
1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```
   Application will open at: http://localhost:3000
   
   Optional: create `frontend/.env` for local prod-like API endpoint
   ```env
   REACT_APP_API_URL=https://asj234.pythonanywhere.com/api
   ```

## Deployment (PythonAnywhere + Vercel)

### Backend on PythonAnywhere
1. Create a new Web App (Manual configuration) on PythonAnywhere.
2. Set Python version to 3.12.
3. In the virtualenv, install deps:
   ```bash
   pip install -r /home/<username>/Software-Intern-AI-Project/backend/requirements.txt
   ```
4. WSGI config: point to Django wsgi module `backend/regulatory_assistant/wsgi.py`.
   Example in the WSGI file:
   ```python
   import sys, os
   project_path = '/home/<username>/Software-Intern-AI-Project/backend'
   if project_path not in sys.path:
       sys.path.append(project_path)
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regulatory_assistant.settings')
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
5. Collect static files in a Bash console:
   ```bash
   cd /home/<username>/Software-Intern-AI-Project/backend
   python manage.py collectstatic --noinput
   ```
6. Environment variables (PythonAnywhere Web app → Environment):
   - `SECRET_KEY` (secure value)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=asj234.pythonanywhere.com`
   - Optionally: `CSRF_TRUSTED_ORIGINS=https://asj234.pythonanywhere.com,https://<your-vercel-app>.vercel.app`
7. Reload the web app. Visit `https://asj234.pythonanywhere.com/admin`.

### Frontend on Vercel
1. Import the GitHub repo into Vercel.
2. Root Directory: `frontend`
3. Build Command: `npm run build`
4. Output Directory: `build`
5. Environment Variable:
   - `REACT_APP_API_URL=https://asj234.pythonanywhere.com/api`
6. Deploy. Your site will be available at `https://<your-vercel-app>.vercel.app`.

### CORS/CSRF configuration
In `backend/regulatory_assistant/settings.py`, ensure:
```python
CORS_ALLOWED_ORIGINS = [
    "https://software-intern-ai-project.vercel.app",
]
CSRF_TRUSTED_ORIGINS = [
    "https://asj234.pythonanywhere.com",
    "https://software-intern-ai-project.vercel.app",
]
ALLOWED_HOSTS = [
    'localhost', '127.0.0.1', '0.0.0.0', 'asj234.pythonanywhere.com'
]
```

If your backend runs elsewhere, set `REACT_APP_API_URL` in `frontend/.env` accordingly.

## Admin UI (Jazzmin)
The Django admin uses Jazzmin for a modern UI. Key configuration lives in `backend/regulatory_assistant/settings.py` under `JAZZMIN_SETTINGS` and `JAZZMIN_UI_TWEAKS`.

- Current theme: `cosmo` (light) with `darkly` (dark mode)
- Branding: site title/header set to "Regulatory Assistant"
- Icons and top menu links for quick navigation

### Customize the look
1. Open `backend/regulatory_assistant/settings.py`
2. Edit `JAZZMIN_UI_TWEAKS['theme']` to any Bootswatch theme, e.g.: `flatly`, `minty`, `yeti`, `journal`, `cyborg` (dark)
3. Optionally adjust `navbar`, `sidebar`, and `accent` classes
4. Save and hard refresh the admin (Ctrl+F5)

Example snippet to change theme:
```python
JAZZMIN_UI_TWEAKS = {
    'theme': 'flatly',
    'dark_mode_theme': 'darkly',
}
```

## API Endpoints

### GET /api/
**Output**: API information and available endpoints

### POST /api/process-report/
**Input**:
```json
{
  "report": "Patient experienced severe nausea and headache after taking Drug X. Patient recovered."
}
```

**Output**:
```json
{
  "drug": "Drug X",
  "adverse_events": ["nausea", "headache"],
  "severity": "severe",
  "outcome": "recovered"
}
```

### GET /api/reports/
**Output**:
```json
{
  "reports": [
    {
      "id": 1,
      "original_report": "Patient experienced...",
      "drug": "Drug X",
      "adverse_events": ["nausea", "headache"],
      "severity": "severe",
      "outcome": "recovered",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### GET /api/reports/{id}/
**Output**: Single report details

### POST /api/translate/
**Input**:
```json
{
  "text": "recovered",
  "target_language": "french"
}
```

**Output**:
```json
{
  "translated_text": "rétabli",
  "original_text": "recovered",
  "target_language": "french"
}
```

### GET /api/analytics/
**Output**:
```json
{
  "total_reports": 25,
  "severity_distribution": {"mild": 10, "moderate": 8, "severe": 7},
  "outcome_distribution": {"recovered": 20, "ongoing": 3, "fatal": 2},
  "common_adverse_events": {"nausea": 15, "headache": 12, "dizziness": 8},
  "common_drugs": {"Drug X": 10, "Aspirin": 8, "Penicillin": 5}
}
```

## Features Implemented

### Backend Features ✅
- **Django REST Framework**: Robust API framework with built-in features
- **NLP Processing**: Uses spaCy and regex patterns for text extraction
- **Drug Extraction**: Identifies drug names using NER and pattern matching
- **Adverse Event Detection**: Keyword-based identification of medical symptoms
- **Severity Classification**: Rule-based severity assessment
- **Outcome Analysis**: Determines patient outcome from report text
- **Database Storage**: SQLite integration with Django ORM
- **Translation Support**: Basic translation for French and Swahili
- **Analytics API**: Data aggregation and statistics
- **Admin Interface**: Django admin for data management
- **CORS Support**: Configured for frontend integration

### Frontend Features ✅
- **Modern UI**: Clean, responsive design with medical theme
- **Report Input**: Large text area for medical report entry
- **Results Display**: Card-based layout for extracted data
- **Loading States**: User feedback during processing
- **Error Handling**: Graceful error display
- **Responsive Design**: Mobile-friendly interface
- **Tabbed Interface**: Process, History, and Analytics tabs
- **Translation Features**: French and Swahili translation buttons
- **Data Visualization**: Charts for severity and outcome distribution
- **Analytics Dashboard**: Statistics and data insights

## Testing the Application

### Sample Test Cases
1. **Basic Report**:
   ```
   "Patient experienced severe nausea and headache after taking Drug X. Patient recovered."
   ```

2. **Multiple Adverse Events**:
   ```
   "Patient reported mild dizziness, fatigue, and skin rash after taking Aspirin 500mg. Symptoms are ongoing."
   ```

3. **Fatal Outcome**:
   ```
   "Patient experienced severe allergic reaction to Penicillin injection. Patient died."
   ```

## Deployment Options

### Backend (Django) on Render
1. Push your repo to GitHub.
2. Create a new Web Service on Render, connect the repo.
3. Environment:
   - Runtime: Python 3.12
   - Build Command:
     ```bash
     pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput
     ```
   - Start Command:
     ```bash
     gunicorn regulatory_assistant.wsgi:application --chdir backend --bind 0.0.0.0:10000
     ```
4. Add Environment Variables:
   - `SECRET_KEY` (generate a secure value)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=<your-render-host>.onrender.com`
   - `CSRF_TRUSTED_ORIGINS=https://<your-render-host>.onrender.com`
5. Save and deploy. After first deploy, create a superuser via Render shell:
   ```bash
   python manage.py migrate && python manage.py createsuperuser --noinput
   ```
   Or use an interactive shell without `--noinput`.

Notes:
- Static files are served with WhiteNoise (`STATICFILES_STORAGE` configured).
- If you see 403 CSRF errors from your frontend, ensure the site URL is added to `CSRF_TRUSTED_ORIGINS`.

### Frontend (React) on Vercel or Netlify

Vercel:
1. Import the GitHub repo in Vercel.
2. Framework preset: React.
3. Environment Variables:
   - `REACT_APP_API_URL=https://<your-render-host>.onrender.com/api`
4. Build Command: `npm run build` (defaults ok)
5. Output Directory: `frontend/build`
6. Root Directory: `frontend`

Netlify:
1. New site from Git, select the repo.
2. Base directory: `frontend`
3. Build command: `npm run build`
4. Publish directory: `build`
5. Environment variable: `REACT_APP_API_URL=https://<your-render-host>.onrender.com/api`

Local production build test:
```bash
cd frontend && npm run build && npx serve -s build
```
Visit `http://localhost:3000` (port may vary) and verify API calls hit your Render URL.

## Evaluation Criteria Checklist

### Core Requirements ✅
- [x] Working backend API with correct extraction
- [x] Functional frontend UI integrated with backend
- [x] Code clarity & organization
- [x] Documentation (README + examples)
- [x] Database integration
- [x] Translation support
- [x] Charts implementation
- [ ] Live deployment

### Bonus Features
- [x] SQLite database for report storage
- [x] GET /api/reports/ endpoint for history
- [x] Translation support for French/Swahili
- [x] Charts for severity distribution
- [x] Analytics dashboard
- [x] Django admin interface
- [ ] Live demo deployment

## Next Steps

### Immediate Tasks
1. **Testing & Debugging**:
   - Test all Django API endpoints
   - Verify frontend-backend integration
   - Test with various report formats
   - Ensure responsive design
   - Run the test script: `python test_django_api.py`

2. **Documentation**:
   - Add API documentation
   - Create setup screenshots
   - Document deployment process

3. **Deployment**:
   - Deploy Django backend to cloud platform (Railway, Render, Heroku)
   - Deploy React frontend to hosting service (Vercel, Netlify)
   - Test live application
   - Update README with live URLs

## Technical Notes

### NLP Processing
- Uses spaCy for named entity recognition
- Fallback regex patterns for drug extraction
- Keyword-based adverse event detection
- Rule-based severity and outcome classification

### Database Schema
Django ORM automatically creates the following table structure:
```sql
CREATE TABLE reports_report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_report TEXT NOT NULL,
    drug VARCHAR(255),
    adverse_events JSON,
    severity VARCHAR(20),
    outcome VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Security Considerations
- CORS configured for development and production
- Input validation using Django serializers
- SQL injection prevention with Django ORM
- Error handling without sensitive data exposure
- Django's built-in security features

## Contact & Support
For questions about this implementation, please refer to the code comments and API documentation above.

---
**Assignment Deadline**: 2 days from assignment receipt
**Submission**: GitHub repository with live demo URL
