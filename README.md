# Automated Student Performance Analyzer

A simple Flask web app that analyzes student exam data (CSV or XLSX), calculates total marks and subject-wise toppers, and produces per-subject bar charts. Ideal for teachers or small schools that want a quick dashboard from spreadsheet data.

## Stack
- Language: Python 3
- Framework: Flask
- Notable libraries: pandas, numpy, matplotlib, openpyxl
- Deployable with: gunicorn (requirements.txt included)

## Features
- Upload student data (.csv or .xlsx) via web form
- Show uploaded table
- Compute total marks per student
- Produce subject-wise topper list
- Generate and serve bar-chart images for each subject
- Simple HTML templates for dashboard and results

## Quickstart — run locally
1. Clone the repo and change into it:

   git clone https://github.com/govindrkumar/Automated-Student-Performance-Analyzer.git
   cd Automated-Student-Performance-Analyzer

2. Create a virtual environment and install requirements:

   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt

3. Start the app:

   python app.py
   # By default the app runs with debug=True and listens on http://127.0.0.1:5000

4. Open a browser and go to:

   http://127.0.0.1:5000/        (home)
   http://127.0.0.1:5000/dashboard  (upload and analysis entry)

Production (example):

   gunicorn --bind 0.0.0.0:8000 app:app

## Routes / Pages
- GET / — landing page (templates/index.html)
- GET /dashboard — upload form (templates/dashboard.html)
- POST /submit — accepts file upload (CSV or XLSX); saved to uploads/uploaded_data.csv or uploads/uploaded_data.xlsx and shows uploaded table (templates/result.html)
- GET /analyse — computes total marks and shows analysis table (templates/final_dashboard.html)
- GET /subjecttoppers — shows subject-wise topper list (templates/subject_wise_toppers.html)
- GET /graphics — generates bar charts per subject and shows performance dashboard (templates/performance_dashboard.html)

## Expected data format
The app expects the uploaded spreadsheet to include at least the following columns (exact header text is required as used in the code):
- Student Name
- Student ID
- Physics
- Chemistry
- Biology
- Mathematics
- English

Example CSV header and one row:

Student Name,Student ID,Physics,Chemistry,Biology,Mathematics,English
John Doe,12345,78,85,72,90,88

## Notes about file handling and generated files
- Uploaded files are saved to the uploads/ directory (uploads/uploaded_data.csv or uploads/uploaded_data.xlsx).
- Generated graphs are saved under static/graphs/ as PNG files (one per numeric column except Student Name/Student ID).
- The app creates required directories on startup (uploads and static/graphs) if they don't exist.

## How it works (brief)
- app.py implements the Flask app and defines:
  - load_uploaded_data(): loads the saved CSV/XLSX from uploads/
  - marks_cum_statement(df): sums the five subject columns to build Total Marks
  - subject_wise_toppers(df): for each subject finds the max and returns rows for highest scorers
  - graphical_representation(): iterates columns and creates bar-charts using matplotlib, saves images to static/graphs
- Templates render HTML tables returned by pandas.DataFrame.to_html() and show links to other views.

## Repository layout (top-level)
```
app.py                 # Flask app and analysis logic
requirements.txt       # Python dependencies
templates/             # HTML views used by the app
  index.html
  dashboard.html
  result.html
  final_dashboard.html
  performance_dashboard.html
  subject_wise_toppers.html
static/                # static assets (CSS, images, graphs/)
  graphs/              # generated graph PNGs
uploads/               # uploaded spreadsheets are stored here
data/                  # contains data.sql (empty)
LICENSE                # project license file
README.md              # (this is where this content goes)
```

## Limitations & gotchas
- The app expects the specific column names shown above; missing or differently-named columns will cause KeyError or incorrect results.
- No authentication — do not expose to public without adding access controls.
- No large-file protections or input validation (e.g., negative marks, non-numeric cells). Consider adding validation and better error messages.
- For multiple uploads in quick succession the app overwrites previous uploaded_data.* files (only one active dataset at a time).
- The front-end is minimal. Charts are created server-side and saved; adding caching or interactive plotting would be an enhancement.

## Suggested improvements
- Validate uploaded sheets (required columns, numeric marks).
- Allow selecting which columns are subjects dynamically.
- Support multiple datasets and per-upload history.
- Add tests and CI (unit tests for analysis functions).
- Serve graphs without writing to disk (in-memory) for stateless deployments.
- Add input sanitization and file size limits.

## Contributing
- Feel free to open issues or PRs. Key places to start:
  - add tests for marks_cum_statement and subject_wise_toppers
  - improve validation and error handling in submit()
  - make the subject list configurable (instead of hard-coded in app.py)

## License
- See LICENSE file in the repository.

If you'd like, I can:
- Paste this into a README.md in the repo for you,
- Add an example sample CSV file under data/ or uploads/ to make testing easier,
- Or add basic input validation and a small test suite for the analysis functions.
