from flask import Flask, render_template, request
import pandas

app = Flask(__name__)
DATA_PATH = "data/patient_tb.csv"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    # this can be a request to display the first name form (with GET) or submitting the form (with POST)
    if request.method == 'POST':
        searchQuery = request.form['name']
    else:
        searchQuery = ''
    fullData = pandas.read_csv(DATA_PATH)

    patients = fullData.drop_duplicates(subset=['PatientID'])[['PatientID', 'PatientLastName', 'PatientFirstName', 'Gender']]
    patients = add_full_name(patients)

    # filter patients to match query
    patients = patients[patients['fullname'].str.contains(searchQuery, case=False, regex=False)]

    # set class for bootstrap formatting, handle case when no results
    data_html=patients.to_html(classes="table col-sm-10")
    
    return render_template("search.html", patients = patients, searchQuery = searchQuery)
    
@app.route('/tests/<int:patientId>', methods=['GET'])    
def tests_by_patient(patientId):
    fullData = pandas.read_csv(DATA_PATH)

    tests = fullData[fullData['PatientID']==patientId]
    if len(tests) == 0:
        return render_template("tests.html", data_html="<p>No test results found for this id</p>")
    tests = tests.drop_duplicates(subset=['PatientID', 'MostRecentTestDate', 'TestName'])
    
    fullname = add_full_name(tests).iloc[0]['fullname']
    data_html = tests[['PatientID','PatientLastName','PatientFirstName','Gender','MostRecentTestDate','TestName',
                       'MostRecentLabResult']].to_html(classes="table col-sm-10", index=False, border=0)
    return render_template("tests.html", data_html=data_html, fullname=fullname)


def add_full_name(frame):
    result = frame.assign(fullname=frame["PatientLastName"] + ', ' + frame["PatientFirstName"])
    return result[['PatientID', 'fullname', 'Gender']]