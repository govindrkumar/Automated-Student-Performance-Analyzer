# Automated Student Performance Analyzer

A small Flask web app to analyze student exam data (CSV / XLSX), compute per-student total marks, identify subject-wise toppers, and generate per-subject bar charts.

The project is intended as a lightweight tool for teachers or small schools to get quick insights from student score sheets.

**Live Demo:** https://automated-student-performance-analyzer.onrender.com

## Status

**Basic working prototype**

Core features implemented:

- Upload CSV / XLSX files
- View uploaded student data
- Calculate total marks for each student
- Find subject-wise toppers
- Generate subject-wise performance graphs

No automated tests or CI are currently configured. The application also does not include authentication or advanced input sanitization.

## Tech Stack

- Python 3
- Flask
- Pandas
- NumPy
- Matplotlib
- OpenPyXL
- Gunicorn

## Quickstart — Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/govindrkumar/Automated-Student-Performance-Analyzer.git
cd Automated-Student-Performance-Analyzer
````

### 2. Create a virtual environment and install requirements

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
python app.py
```

By default, the application runs on:

```text
http://127.0.0.1:5000
```

### 4. Open the application

Home page:

```text
http://127.0.0.1:5000/
```

Dashboard:

```text
http://127.0.0.1:5000/dashboard
```

## Production Example

The application can also be run using Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

## Docker

There is currently no Dockerfile in the repository.

If Docker support is needed, a Dockerfile can be added to install Python, copy the application, install the requirements, and expose the required port.

## Routes / Pages

| Route             | Method | Description                                             |
| ----------------- | ------ | ------------------------------------------------------- |
| `/`               | GET    | Landing page                                            |
| `/dashboard`      | GET    | Upload and analysis entry page                          |
| `/submit`         | POST   | Accepts CSV/XLSX uploads and displays the uploaded data |
| `/analyse`        | GET    | Calculates total marks and displays the analysis        |
| `/subjecttoppers` | GET    | Displays subject-wise toppers                           |
| `/graphics`       | GET    | Generates and displays subject-wise performance graphs  |

## Expected Data Format

The uploaded spreadsheet should contain the following columns:

* Student Name
* Student ID
* Physics
* Chemistry
* Biology
* Mathematics
* English

### Example CSV

```csv
Student Name,Student ID,Physics,Chemistry,Biology,Mathematics,English
John Doe,12345,78,85,72,90,88
```

## File Handling

Uploaded files are stored in the `uploads/` directory.

Examples:

```text
uploads/uploaded_data.csv
uploads/uploaded_data.xlsx
```

Generated graphs are stored in:

```text
static/graphs/
```

The application automatically creates the required directories when they do not exist.

## How It Works

The main application logic is contained in `app.py`.

Important functions include:

### `load_uploaded_data()`

Loads the uploaded CSV or XLSX file from the `uploads/` directory.

### `marks_cum_statement(df)`

Calculates the total marks for each student using the configured subject columns.

### `subject_wise_toppers(df)`

Finds the highest-scoring student(s) in each subject.

### `graphical_representation()`

Creates subject-wise bar charts using Matplotlib and saves them as PNG files.

The Flask templates display the processed data and analysis results.

## Current Limitations

* The application expects specific column names.
* Invalid or missing data may cause errors.
* Non-numeric marks are not currently validated.
* Negative marks or values outside the expected range are not validated.
* Only one active dataset is maintained at a time.
* A new upload overwrites the previous uploaded dataset.
* Generated graphs are stored on disk.
* There is no authentication or rate limiting.
* No automated tests or CI are currently configured.

## Future Improvements

Some possible improvements include:

1. Add validation for uploaded files and required columns.
2. Validate that marks are numeric and within valid ranges.
3. Make the subject list configurable.
4. Add automated tests for the analysis functions.
5. Support multiple datasets instead of overwriting the previous upload.
6. Improve file handling for stateless deployments.
7. Add file size limits and better input sanitization.
8. Improve the front-end and add interactive visualizations.

## Contributing

Contributions are welcome!

Some useful areas for contribution:

* Adding tests for the analysis logic
* Improving validation and error handling
* Making the subject list configurable
* Improving the user interface
* Adding Docker support
* Adding GitHub Actions / CI

## Repository Structure

```text
Automated-Student-Performance-Analyzer/
│
├── app.py
├── requirements.txt
├── templates/
│   └── HTML templates
├── static/
│   ├── CSS and other static assets
│   └── graphs/
├── uploads/
├── LICENSE
└── README.md
```

## License

See the `LICENSE` file for license information.

