from flask import Flask, render_template, request
import pandas

app = Flask(__name__)
DATA_PATH = "data/patient_tb.csv"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        firstName = request.form['firstName']
        fullData = pandas.read_csv(DATA_PATH)
        data = fullData[fullData['PatientFirstName'] == firstName]
        data = data.drop_duplicates(subset=['PatientID', 'MostRecentTestDate', 'TestName'])
        data_html = data.to_html(classes="table col-sm-10") if data.size > 0 else "No results found for that name."
        
        return render_template("search.html", data_html = data_html, firstName = firstName)
    else:
        return render_template("search.html")