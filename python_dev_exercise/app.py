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
        firstName = request.form['firstName']
        fullData = pandas.read_csv(DATA_PATH)

        # for a substring of a patient's name to work to find them, use:
        # data = fullData[fullData['PatientFirstName'].str.contains(firstName, case=False, regex=False)]

        data = fullData[fullData['PatientFirstName'].str.lower() == firstName.lower()]
        data = data.drop_duplicates(subset=['PatientID', 'MostRecentTestDate', 'TestName'])

        # set class for bootstrap formatting, handle case when no results
        data_html = data.to_html(classes="table col-sm-10") if data.size > 0 else "No results found for that name."
        
        return render_template("search.html", data_html = data_html, firstName = firstName)
    else:
        return render_template("search.html")