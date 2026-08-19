# Automated Student Performance Analyzer

A small Flask web app to analyze student exam data (CSV / XLSX), compute per-student total marks, identify subject-wise toppers, and generate per-subject bar charts. The project is intended as a lightweight tool for teachers or small schools to get quick insights from score sheets.

Live demo: https://automated-student-performance-analyzer.onrender.com

Status: Basic working prototype
- Core features implemented and runnable locally: upload, view table, compute totals, list subject toppers, and generate static PNG charts per subject.
- No automated tests or CI configured. No authentication or input sanitization.

Tech stack
- Python 3
- Flask
- pandas, numpy, matplotlib, openpyxl
- Deployable with gunicorn

Quickstart — run locally
1. Clone the repo and change into it:

   git clone https://github.com/govindrkumar/Automated-Student-Performance-Analyzer.git
   cd Automated-Student-Performance-Analyzer

2. Create a virtual environment and install requirements:

   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. Start the app for development:

   python app.py

   By default the app runs with debug=True and listens on http://127.0.0.1:5000

4. Open a browser and visit:

   http://127.0.0.1:5000/        (home)
   http://127.0.0.1:5000/dashboard  (upload and analysis entry)

Production example (Gunicorn):

   gunicorn --bind 0.0.0.0:8000 app:app

Docker (optional)
- There is no Dockerfile in the repo currently. To run in Docker, create a small Dockerfile that installs Python, copies the app, installs requirements, and exposes the port.

Routes / Pages
- GET / — landing page (templates/index.html)
- GET /dashboard — upload form (templates/dashboard.html)
- POST /submit — accepts file upload (CSV or XLSX); saved to uploads/uploaded_data.csv or uploads/uploaded_data.xlsx and shows uploaded table (templates/result.html)
- GET /analyse — computes total marks and shows analysis table (templates/final_dashboard.html)
- GET /subjecttoppers — shows subject-wise topper list (templates/subject_wise_toppers.html)
- GET /graphics — generates bar charts per subject and shows performance dashboard (templates/performance_dashboard.html)

Expected data format
The app expects the uploaded spreadsheet to include at least the following columns (exact header text as used in the code):
- Student Name
- Student ID
- Physics
- Chemistry
- Biology
- Mathematics
- English

Example CSV header and a sample row:

Student Name,Student ID,Physics,Chemistry,Biology,Mathematics,English
John Doe,12345,78,85,72,90,88

File handling and generated files
- Uploaded files are saved to the `uploads/` directory (uploads/uploaded_data.csv or uploads/uploaded_data.xlsx).
- Generated graphs are saved under `static/graphs/` as PNG files (one per numeric subject column).
- The app creates required directories on startup (uploads and static/graphs) when missing.

How it works (brief)
- `app.py` contains the Flask app and analysis logic including:
  - `load_uploaded_data()` — loads the saved CSV/XLSX from `uploads/`
  - `marks_cum_statement(df)` — sums configured subject columns to build `Total Marks`
  - `subject_wise_toppers(df)` — finds highest scorer(s) per subject
  - `graphical_representation()` — creates bar charts with matplotlib and saves PNGs to `static/graphs/`
- Templates render HTML tables from `pandas.DataFrame.to_html()` and link to analysis views.

Current limitations and risks
- Strict column names: the code expects specific headers and will raise KeyError for different headers.
- No input validation: non-numeric values, negative marks, missing cells, or malformed sheets may cause errors.
- Single active dataset: each upload overwrites `uploads/uploaded_data.*` — no versioning or history.
- Server-side file writes: graphs are written to disk which is not ideal for stateless platforms unless using ephemeral storage.
- No authentication or rate-limiting — do not expose to public without adding access controls.
- No unit tests or CI. Consider adding tests for the analysis functions.

Suggested improvements (prioritized)
1. Add validation for uploaded sheets (required columns, numeric marks, valid ranges).
2. Make the subject list configurable (detect numeric columns or allow user selection on upload).
3. Add unit tests for `marks_cum_statement` and `subject_wise_toppers` and configure CI (GitHub Actions).
4. Support multiple datasets (per-upload history) instead of a single file overwrite.
5. Serve graphs in-memory (Flask send_file with BytesIO) to avoid writing to disk for stateless deployments.
6. Add input sanitization, file size limits, and basic auth for deployments.
7. Improve front-end and add client-side interactivity (plotly/dash or embedding base64 images).

Contributing
- Contributions welcome. Helpful first PRs:
  - Add tests covering analysis logic
  - Improve validation and error handling in `submit()`
  - Make subject list configurable and/or auto-detected
  - Add a Dockerfile and GitHub Actions workflow

Repository layout (top-level)
```
app.py                 # Flask app and analysis logic
requirements.txt       # Python dependencies
templates/             # HTML views used by the app
static/                # static assets (CSS, images, graphs/)
  graphs/              # generated graph PNGs
uploads/               # uploaded spreadsheets are stored here
LICENSE                # project license file
README.md              # (this file)
```

License
- See LICENSE file in the repository.
