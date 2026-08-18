# Import required libraries
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


# Create Flask application
app = Flask(__name__)


# --------------------------------------------------
# FILE STORAGE
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static/graphs", exist_ok=True)


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def load_uploaded_data():

    csv_path = os.path.join(UPLOAD_FOLDER, "uploaded_data.csv")
    xlsx_path = os.path.join(UPLOAD_FOLDER, "uploaded_data.xlsx")

    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)

    elif os.path.exists(xlsx_path):
        return pd.read_excel(xlsx_path)

    return None


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

@app.route("/submit", methods=["POST"])
def submit():

    file_type = request.form["file_type"]
    file = request.files["myfile"]

    # Make sure a file was selected
    if file.filename == "":
        return "No file selected."

    # Remove old uploaded files
    old_csv = os.path.join(UPLOAD_FOLDER, "uploaded_data.csv")
    old_xlsx = os.path.join(UPLOAD_FOLDER, "uploaded_data.xlsx")

    if os.path.exists(old_csv):
        os.remove(old_csv)

    if os.path.exists(old_xlsx):
        os.remove(old_xlsx)


    # Save new file
    if file_type == "csv":

        filepath = os.path.join(
            UPLOAD_FOLDER,
            "uploaded_data.csv"
        )

        file.save(filepath)

        df = pd.read_csv(filepath)


    elif file_type == "xlsx":

        filepath = os.path.join(
            UPLOAD_FOLDER,
            "uploaded_data.xlsx"
        )

        file.save(filepath)

        df = pd.read_excel(filepath)


    else:
        return "Unsupported file type."


    # Show uploaded data
    return render_template(
        "result.html",
        table=df.to_html(index=False)
    )


# --------------------------------------------------
# TOTAL MARKS
# --------------------------------------------------

def marks_cum_statement(df):

    subjects = [
        "Physics",
        "Chemistry",
        "Biology",
        "Mathematics",
        "English"
    ]

    return df[subjects].sum(axis=1)


# --------------------------------------------------
# SUBJECT-WISE TOPPERS
# --------------------------------------------------

def subject_wise_toppers(df):

    subjects = [
        "Physics",
        "Chemistry",
        "Biology",
        "Mathematics",
        "English"
    ]

    topper_data = []

    for subject in subjects:

        highest_marks = df[subject].max()

        toppers = df.loc[
            df[subject] == highest_marks
        ]

        for _, student in toppers.iterrows():

            topper_data.append({
                "Subject": subject,
                "Student Name": student["Student Name"],
                "Student ID": student["Student ID"],
                "Marks": highest_marks
            })

    return pd.DataFrame(topper_data)


# --------------------------------------------------
# ANALYSIS PAGE
# --------------------------------------------------

@app.route("/analyse")
def analyse():

    # Load saved file
    df = load_uploaded_data()

    if df is None:
        return "Please upload a file first."


    # Calculate total marks
    total_marks = marks_cum_statement(df)


    # Create analysis DataFrame
    analysis_df = pd.DataFrame({
        "Student Name": df["Student Name"],
        "Student ID": df["Student ID"],
        "Total Marks": total_marks
    })


    # Convert analysis table to HTML
    table = analysis_df.to_html(index=False)


    # Calculate subject toppers
    toppers_df = subject_wise_toppers(df)


    # Convert topper table to HTML
    topper_table = toppers_df.to_html(index=False)


    # Send both tables to dashboard
    return render_template(
        "final_dashboard.html",
        table=table,
        topper_table=topper_table
    )


# --------------------------------------------------
# SUBJECT TOPPERS PAGE
# --------------------------------------------------

@app.route("/subjecttoppers")
def topper_list():
    # Load saved file
    df = load_uploaded_data()

    if df is None:
        return "Please upload a file first."


    # Calculate toppers
    toppers_df = subject_wise_toppers(df)


    # Convert to HTML
    topper_table = toppers_df.to_html(index=False)


    return render_template(
        "subject_wise_toppers.html",
        topper_table=topper_table
    )


# --------------------------------------------------
# GRAPHICAL REPRESENTATION
# --------------------------------------------------

@app.route("/graphics")
def graphical_representation():
    # Load saved file
    df = load_uploaded_data()
    if df is None:
        return "Please upload a file first."


    # Student names
    x = df["Student Name"]
    y = ['Student Name', 'Student ID']
    graphs = []
    

    for col in df.columns:
        if col not in y:
            y = df[col]
            plt.figure(figsize=(12,7))
            colors = plt.cm.viridis(np.linspace(0, 1, len(x)))
            plt.bar(x,y, color = colors)
            plt.title(f'{col} Performance')
            plt.xlabel('students')
            plt.ylabel('Marks')
            plt.xticks(rotation=45, ha = 'right')
            plt.tight_layout()
            plt.savefig(f'static/graphs/{col}.png')
            plt.close()
            graphs.append(f'graphs/{col}.png')

    return render_template('performance_dashboard.html', graphs = graphs)




# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)