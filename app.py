from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim
import pandas
import requests

app = Flask(__name__)

@app.route("/") # only "/"= Home page
def index():
    return render_template("index.html")

@app.route("/data-show", methods=['POST']) # only "/"= Home page
def data_show():

    if request.method=="POST":
        #try:
        my_api = request.form["url1"]
        #print(str(my_api))
        # r = requests.get('http://dummy.restapiexample.com/api/v1/employees')
        # print(r.json())
        r = requests.get(my_api)
        myRespond = r.json()
        print(myRespond)
        return render_template("index.html", myRespond=myRespond)
        # except Exception as e:
        #     return render_template("index.html")

@app.route("/success-table", methods=["POST"])
def success_table():
    if request.method=="POST":
        global filename
        try:
            file = request.files['file']
            df = pandas.read_csv(file) # reading data using pandas dataFrame

            gc = Nominatim() # created object fo Nominatim() = gc
            df["coordinates"] = df["Address"].apply(gc.geocode)
            df["Latitude"] = df["coordinates"].apply(lambda x: x.latitude if x!=None else None)
            df["Longitude"] = df["coordinates"].apply(lambda x: x.longitude if x!=None else None)
            df = df.drop("coordinates", 1)
            df.to_csv("uploads/geocoded.csv", index=None)

            return render_template("index.html", text=df.to_html(), btn="download.html")
        except Exception as e:
            return render_template("index.html", text=str(e))

@app.route("/download-file/")
def download():
    return send_file("uploads/geocoded.csv", attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == "__main__":
    app.debug=True
    app.run() # app.run(port=5001)... Here we can set any port. but default port=5000
