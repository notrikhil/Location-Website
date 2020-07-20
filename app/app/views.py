from app import app
from flask import render_template
from flask import request, redirect
import requests
from flask import send_file

#from plotly.offline import plot
#from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from flask import Markup


@app.route("/")
def about():
    return render_template("public/index.html")

@app.route("/charts", methods = ["GET", "POST"])
def charts():
    if request.method == "POST":
        CovidData = []
        req = request.form
        
        zipcode = int(req.get('Location'))

        json_data = requests.get('https://opendata.arcgis.com/datasets/854d7e48e3dc451aa93b9daf82789089_0.geojson')
        data = json_data.json()
        for x in range(len(data['features'])):
            if zipcode == data['features'][x]["properties"]['zipcode_zip']:
                if not str(data['features'][x]['properties']['case_count']) == "null":
                    d = []
                    d.append(data['features'][x]['properties']['updatedate'])
                    d.append(data['features'][x]['properties']['case_count'])
                    CovidData.append(d)

        x_data = []
        y_data = []

            
        for value in CovidData:
            date = value[0]
            caseCount = value[1]

            justDay = date.split()[0]

            x_data.append(caseCount)
            y_data.append(justDay)
        
        #my_plot_div = plot([bar(x= y_data, y = x_data)], output_type='div')
        my_plot_div = go.Figure([go.Bar(x = y_data, y = x_data, name = "Test Graph")])
        my_plot_div.update_layout(
            title="Covid Case Count By Date",
            xaxis_title="Date",
            yaxis_title="Case Count",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        
        my_plot_div.show()
        return render_template('public/index.html')

        #return render_template("public/chart.html", CovidData = CovidData)

    

