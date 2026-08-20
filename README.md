# Automated Student Performance Analyzer

**It's a simple flask app made for teachers for following purpose :**
- Know total marks
- Know subject-wise toppers
- Compare performance of students in each subject among their classmate / peers.

## Tech Stack

- Python 3.13.0
- Flask
- Pandas
- Matplotlib
- OpenPyXL
- HTML5 / CSS

## How to run it locally on your system ?

### 1. Clone the repository

```bash
git clone https://github.com/govindrkumar/Automated-Student-Performance-Analyzer.git
cd Automated-Student-Performance-Analyzer
````

### 2. Install Requirements
```bash
pip install -r requirements.txt
````

### 3. Run it
````bash
python3 app.py
````

## Project Architecture 
(Credit : Google Slide)

<img width="1350" height="900" alt="ChatGPT Image Aug 19, 2026, 09_10_46 PM" src="https://github.com/user-attachments/assets/7d399f3f-840d-4408-bc06-8033536abe45" />


## How my project Works ?
So, as it can be seen from above architecture diagram that it follows two system :

**i. Manual Entry**

**ii. Automatic Analysis**

So, let's start :
### 1. Manual Entry

- So, it starts with you entering the no. of subject and no. of students on my page. (`index.html`)

<img width="698" height="757" alt="quickshot_260820_121425" src="https://github.com/user-attachments/assets/71d716a3-63a4-48f9-87f4-be96db472c73" />

- When you click `submit` button the result is sent to backend in `/result_calc` route.
- Here, I turn the submitted input in int format.
- Afterwards, I send you to `subject_selection.html` to collect the data of what subjects you are going to evaluate. (Contains 150 subjects in 8 different field) (Credit : Google Gemini for providing me list of 150 subjects.)

- <img width="1741" height="916" alt="quickshot_260820_122743" src="https://github.com/user-attachments/assets/d81d873d-7131-412b-a19c-f2eebbedc3c5" />


- You scroll down and click submit.
- I collect your returned input in my global `selected_subject` list using `request.form.getlist()` function which is looped to make keys in `my_dict`.
- Then, it is redirect to `/student_data`.
- `student_data_pushed.html` uses Jinga2 to make a loop and fill the values.

  <img width="1428" height="454" alt="quickshot_260820_123545" src="https://github.com/user-attachments/assets/adf012e7-208f-41e5-80b9-da17c8ecb343" />

- From now on, `Pandas DataFrame` will be used.
- Your data is saved in `uploaded_data.csv` format on `result.html` page.

  <img width="804" height="534" alt="quickshot_260820_123936" src="https://github.com/user-attachments/assets/dbbea547-02c3-4558-8c4c-0e97cd858024" />

### 2. Automatic Upload
Before you get excited 🥳 , let me tell you one thing. The project has a hard limitation which you will need to follow to properly use it. 
The project expects the great `Homo Sapiens` to follow specific file format :

- Student ID
- Student Name
- (Your list of subjects)

Note : Make sure you don't put your DOB, Father's Name or any extra detail against this format. Okay ? Am I clear ?

<img width="706" height="764" alt="quickshot_260820_105749" src="https://github.com/user-attachments/assets/1ddd0604-e005-4e0d-a032-adabd63a77fc" />

i. Click on Upload Existing students marks button.

ii. Now, choose your file format. ( `.csv` or `.xlsx` supported)

<img width="693" height="567" alt="quickshot_260820_124605" src="https://github.com/user-attachments/assets/8b9b7720-37a0-45e2-b76d-06fc37ac92fa" />


- Click on submit. Now, when you press `Submit` where, I take it in my backroom 💀.
- Highly classified operation 🕵️‍♀️ of converting and saving it `df` variable is conducted inside it. (I already told you before.)
- On `result.html`

  <img width="741" height="815" alt="quickshot_260820_125230" src="https://github.com/user-attachments/assets/b93fa053-2dea-4427-ad01-c73fdf417fa4" />


## Hah, So, both ways are completed. 
Thank you for your patience gentleman. 😚 

<img width="480" height="422" alt="Cinema Cat Reaction GIF" src="https://github.com/user-attachments/assets/e5c1114f-a1ad-4588-b48b-a8f976a04fe8" />

So, you! Yes, I am talking to you. 
Did you find anything common point in both ways ? Or, your **attention span** made you scroll the cool part.
Let me show you. 
See, these three warriors ? 👑


<img width="548" height="168" alt="quickshot_260820_125950" src="https://github.com/user-attachments/assets/2c356662-3620-41f8-adde-fd3cb5fcf9d2" />

## Let's talk now :
### i. Analyse Results

-It's to know total marks of each student in one go. No, excel required. Yeah, seriously. 

<img width="1112" height="894" alt="quickshot_260820_130531" src="https://github.com/user-attachments/assets/ed464fd1-7dea-4ac2-9fda-e0722a01f73e" />


**Tech Details for Nerdy Readers :**
- This part uses `marks_cum_statement` function and sends it to `/analyse` which will display result on `final_dashboard.html`. (was it final ? No, you dork!)
- It says 'Hey Fella! If my file has anything other than `Student Name` or `Student ID` just add it using `df.sum(axis = 1)` (row-wise) and tell our total gang number. 💰🥷'

### ii. Subject-Wise Topper List

- It's know subject wise topper in your class. Who is performing in which subject and recognise their value in class. 🥺 (Not one single topper. )

  <img width="679" height="460" alt="quickshot_260820_131553" src="https://github.com/user-attachments/assets/1cd1966c-e023-4405-b17d-cf76ad538eaa" />

**Study time :**
- It uses `subject_wise_toppers` function, uses loop to know which one is subject (Just, excludes `Student Name & Student ID`. No, biggie!)
- Then, uses `iterrows` to merge the max marks (created using df.max()), student names, student id and subject name in a for loop.
- Rendered on `subject_wise_toppers.html`.

### iii. Graphical Representation

<img width="1799" height="897" alt="quickshot_260820_132643" src="https://github.com/user-attachments/assets/ac3d0eb5-2f9d-421c-99de-816b6fea0d34" />

**Details :**
- It picks up your df which you prepared.
- Plots bar graph using matplotlib.pyplot in a for loop of each subject, comparing each student performance in a graph. (A bar graph 😂)

Thank you for keeping up with me in this explanation. 
Hope you liked it!

<img width="480" height="480" alt="Cat Meme GIF" src="https://github.com/user-attachments/assets/5940b5dd-d135-4775-a421-0065d20ad465" />



## Contribution
No one helps single man 🥺😢😭

Commit a PR and help me out grow features in this project. 

## License
See the `LICENSE` file for license information.


## One Last thing 
If you really read this....

<img width="480" height="406" alt="Five Nights At Freddys GIF" src="https://github.com/user-attachments/assets/1d751f03-e259-4a97-8e5a-dadacbe84e63" />

Bye, Bye! Love you all!! 😘
