# Import required libraries
from flask import Flask, render_template, request, redirect, url_for
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

df = 0
@app.route("/submit", methods=["POST"])
def submit():

    file_type = request.form["file_type"]
    file = request.files["myfile"]
    global df 

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
    col = ['Student ID', 'Student Name']

    subjects = [x for x in df.columns if x not in col]

    return df[subjects].sum(axis=1)


# --------------------------------------------------
# SUBJECT-WISE TOPPERS
# --------------------------------------------------

def subject_wise_toppers(df):
    global selected_subject
    col = ['Student ID', 'Student Name']
    

    subjects = [x for x in df.columns if x not in col]
    


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


# ---------------------------------------------------
# BUILIDING READER
# ---------------------------------------------------

#declaring for global
student_no = 0
subject_no = 0

@app.route('/result_calc',methods = ['POST'])
def result_calc():
    # Save the form counts for the next subject and student screens.
    global student_no
    global subject_no
    student_no = int(request.form['student_no'])
    subject_no = int(request.form['subject_no'])

    print(student_no)
    print(subject_no)

    # Subject options are grouped so the selection page stays organised.
    subjects = [
    "English",
    "Hindi",
    "Sanskrit",
    "Urdu",
    "Bengali",
    "Tamil",
    "Telugu",
    "Marathi",
    "Gujarati",
    "Kannada",
    "Malayalam",
    "Punjabi",
    "Assamese",
    "Odia",
    "French",
    "German",
    "Spanish",
    "Japanese",
    "Chinese",
    "Arabic",]

    subjects2 = ["Mathematics",
    "Applied Mathematics",
    "Statistics",
    "Physics",
    "Chemistry",
    "Biology",
    "Environmental Science",
    "Earth Science",
    "Geology",
    "Astronomy",
    "Astrophysics",
    "Geography",
    "Geology and Mineralogy",
    "Oceanography",
    "Meteorology",]

    subjects3 = ["History",
    "Political Science",
    "Civics",
    "Economics",
    "Sociology",
    "Psychology",
    "Philosophy",
    "Anthropology",
    "Archaeology",
    "Public Administration",
    "International Relations",
    "Human Geography",
    "Social Work",
    "Gender Studies",
    "Cultural Studies",]

    subjects4 = ["Computer Science",
    "Informatics Practices",
    "Information Technology",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Data Analytics",
    "Cyber Security",
    "Computer Applications",
    "Software Engineering",
    "Web Development",
    "Database Management",
    "Computer Networks",
    "Operating Systems",
    "Computer Architecture",
    "Programming",
    "Python Programming",
    "Java Programming",
    "C Programming",
    "C++ Programming",
    "Algorithms",
    "Data Structures",
    "Cloud Computing",
    "Internet of Things",
    "Blockchain Technology",
    "Robotics",
    "Human-Computer Interaction",]


    subjects5 = ["Accountancy",
        "Business Studies",
        "Commerce",
        "Financial Management",
        "Marketing",
        "Business Economics",
        "Entrepreneurship",
        "Management",
        "Operations Management",
        "Human Resource Management",
        "Organizational Behaviour",
        "Financial Accounting",
        "Cost Accounting",
        "Taxation",
        "Auditing",
        "Banking",
        "Insurance",
        "Business Law",
        "Corporate Finance",]

    
    subjects6 = ["Biochemistry",
        "Microbiology",
        "Biotechnology",
        "Genetics",
        "Molecular Biology",
        "Cell Biology",
        "Ecology",
        "Zoology",
        "Botany",
        "Marine Biology",
        "Neuroscience",
        "Immunology",
        "Bioinformatics",
        "Biomedical Science",
        "Food Science",
        "Forensic Science",]

    subjects7 = ["Political Theory",
        "Constitutional Studies",
        "Legal Studies",
        "Criminal Law",
        "Contract Law",
        "Civil Law",
        "Corporate Law",
        "International Law",
        "Human Rights",
        "Environmental Law",]

    subjects8 = ["Mechanical Engineering",
        "Civil Engineering",
        "Electrical Engineering",
        "Electronics Engineering",
        "Computer Engineering",
        "Chemical Engineering",
        "Aerospace Engineering",
        "Biomedical Engineering",
        "Environmental Engineering",
        "Industrial Engineering",]

    subjects9 = ["Fine Arts",
        "Visual Arts",
        "Painting",
        "Drawing",
        "Sculpture",
        "Music",
        "Hindustani Classical Music",
        "Carnatic Music",
        "Western Music",
        "Dance",
        "Drama",
        "Theatre",
        "Film Studies",
        "Photography",
        "Graphic Design",
        "Fashion Design",
        "Architecture",
        "Interior Design",
        "Physical Education",
        "Health Education"]

    return render_template('subject_selection.html',
                            my_list = subjects,
                            my_list2 = subjects2,
                            my_list3 = subjects3,
                            my_list4 = subjects4,
                            my_list5 = subjects5,
                            my_list6 = subjects6,
                            my_list7 = subjects7,
                            my_list8 = subjects8,
                            my_list9 = subjects9
                            )



# Temporary in-memory data used by the manual-entry workflow.
my_dict = {}
selected_subject = []
@app.route('/subject_selection', methods = ['POST'])
def subject_selection():
    global my_dict
    global selected_subject
    # Keep only the subjects selected by the user.
    selected_subject = request.form.getlist('selected_items')
    my_dict = {'Student ID':[],
               'Student Name': []}
    for key in selected_subject: #added keys now
        my_dict[key] = []
    return redirect('/student_data')


@app.route('/student_data')
def student_data():
    # Build an empty input table for every student and subject.
    return render_template(
        'student_data_pushed.html',
        student_no=student_no,
        subjects= selected_subject
    )

@app.route('/collect_data', methods=['POST'])
def collect_data():

    global my_dict
    my_dict["Student ID"] = []

    # Read each table cell and place it into a column-based dictionary

    my_dict['Student Name'] = []

    for i in range(student_no):
        my_dict["Student ID"].append(request.form[f'student_id_{i}'])

        my_dict['Student Name'].append(
            request.form[f'name_{i}']
        )

        for subject in selected_subject:

            my_dict[subject].append(
                request.form[f'{subject}_{i}']
            )

    print(my_dict)

    return redirect('/results')

@app.route('/results')
def results():
    # Convert manual entries to the same CSV format used by file uploads.
    print(my_dict)
    df = pd.DataFrame(my_dict)


    UPLOAD_FOLDER = "uploads"
    filepath = os.path.join(UPLOAD_FOLDER, "uploaded_data.csv")
    df.to_csv(filepath, index = False)
    table = df.to_html()
    return render_template('result.html',table = table)



# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)