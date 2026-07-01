# Prep AI — AI-Powered Placement Preparation Chatbot

**Prep AI** is a premium, commercial-grade placement preparation web application designed for engineering and college students. It provides a suite of tools including interactive practice modules, AI chatbots, ATS resume checks, and live simulated mock interview assessments to help students ace their campus recruitment rounds.

---

## Technical Stack
- **Frontend**: HTML5, CSS3, Bootstrap 5, Javascript, Chart.js (for progress reporting dashboards).
- **Backend**: Python Flask (configured with a modular blueprint-based MVC architecture).
- **Database**: MySQL (supported via SQLAlchemy ORM, including an automated fallback to SQLite `prep_ai.db` in case of offline/local testing).
- **AI Engine**: Google Gemini 1.5 Flash (interfaced through REST API with full conversation context memory and output validation constraints).
- **PDF Extraction**: PyPDF2 (safely reads text blocks from uploaded resume formats).

---

## Folder Structure
```text
prep-ai/
├── app.py                  # Factory app entry point and global error setups
├── config.py               # Configures path variables, upload parameters, and URLs
├── requirements.txt        # PIP dependencies
├── seed.py                 # Core database seeding script (180+ real prep questions)
├── .env                    # System configuration key-value storage (ignored by git)
├── .env.example            # Template for key values
├── database/
│   └── schema.sql          # Raw MySQL database structures
├── models/                 # Declarative SQLAlchemy models (users, chats, reports, etc.)
├── routes/                 # Blueprint endpoints managing site views and API routes
├── static/                 # Stylesheets, JS modules, and image elements
├── templates/              # HTML layout documents
└── uploads/                # Directory containing temporary resume files during parsing
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.8+ installed on your system.
- MySQL server installed (optional, as SQLite fallback is enabled by default in `.env`).

### 2. Install Dependencies
Open your shell terminal in the project root directory and run:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to a new file named `.env`:
```bash
cp .env.example .env
```
Fill out the parameters inside `.env`:
- `SECRET_KEY`: Set a secure random string.
- `DATABASE_URL`: Your MySQL URL (e.g., `mysql+pymysql://username:password@localhost:3306/prep_ai`).
- `USE_SQLITE_FALLBACK`: Set to `True` to test instantly using SQLite without needing to configure a MySQL server.
- `GEMINI_API_KEY`: Input your Gemini API key from Google AI Studio.

### 4. Database Setup

#### Option A: Using SQLite Fallback (Recommended for Instant Testing)
If `USE_SQLITE_FALLBACK=True` in `.env`, the database file `prep_ai.db` will be initialized automatically on the first start of the server. You can skip any MySQL configurations.

#### Option B: Using MySQL Server
1. Start your local MySQL server.
2. Open a SQL console and create a new schema named `prep_ai`:
   ```sql
   CREATE DATABASE prep_ai;
   ```
3. Import the initial structures:
   ```bash
   mysql -u username -p prep_ai < database/schema.sql
   ```

### 5. Seed Placement Material
Run the data seeder to insert all 180+ real aptitude questions, technical Q&A collections, MNC guides, coding problems, and HR interview parameters:
```bash
python seed.py
```

### 6. Run the Application
Start the Flask development server:
```bash
python app.py
```
Open your web browser and navigate to `http://127.0.0.1:5000` to begin.

---

## Features Walkthrough

1. **SaaS Landing Page**: Clean scroll roadmap showing product components.
2. **Onboarding & Auth**: Secure Werkzeug credentials hashing, password strength validations, email checks, and session control.
3. **Interactive Dashboard**: Dynamically computes stats, lists weak/strong subjects based on history, and prints recommended links.
4. **Placement Chatbot**: AI chats focused strictly on engineering categories, supporting full conversation thread context.
5. **Aptitude Practice**: Quantitative, logical, and verbal tests with a countdown timer, auto-submitting at zero.
6. **Technical Accordion**: Guides for OS, DBMS, DSA, OOP, Python, SQL, C++, Java, etc.
7. **HR Interview**: Explains HR questions and lazy-caches dynamic answers.
8. **Company Preparation**: Roadmaps, rounds, and previously asked coding questions for TCS, Infosys, Zoho, Capgemini, etc.
9. **Coding Sandbox**: Filterable code workspace supporting code testing and compiler logs.
10. **Resume Analyzer**: ATS score evaluator pointing out missing keywords and grammar improvements.
11. **Mock Interview Simulator**: Evaluates user answers on communication and confidence indicators.
12. **Analytics Report**: Renders line/bar charts of historical scores using Chart.js.
