from operator import length_hint
import os
from flask import Flask, render_template, url_for, request

# The goal of this app is to show messages sent across space, not across time
# Messages are organized according to the lat/long of where they were sent from (rounded to int)

app = Flask(__name__)

@app.route("/")
@app.route("/geo")
def geo():
    return render_template("geo.html")

@app.route("/makepost")
def makepost():
    return render_template("makepost.html")

@app.route("/seeposts")
def seeposts():
    n = open("markers.txt", "r")
    _markers = n.read()
    n.close()

    return render_template("seeposts.html", map = "https://upload.wikimedia.org/wikipedia/commons/8/83/Equirectangular_projection_SW.jpg", marker = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Roundel_of_Turkey.svg/120px-Roundel_of_Turkey.svg.png", markers = _markers)

@app.route("/writetomarkers", methods=["POST", "GET"])
def writeToMarkers():    
    output = request.form.to_dict()
    text = output["text"]
    lat = output["latitude"]
    long = output["longitude"]
    
    m = open("marker_count.txt", "r")
    n = open("markers.txt", "r")

    current_m = int(m.read())

    message = "M" + str(current_m) + "|" + text + "|" + lat + "|" + long
    
    current_m += 1

    current_n = n.read()

    m.close()
    n.close()

    m = open("marker_count.txt", "w")
    n = open("markers.txt", "w")

    m.write(str(current_m))
    n.write(current_n + "/" + message)

    m.close()
    n.close()

    return render_template("makepost.html")
    
@app.route("/display", methods=["POST", "GET"])
def display():
    marker_index = ""
    if request.method == "POST":
        marker_index = request.form["marker_button"]
        
        n = open("markers.txt", "r")
        ncontent = n.read()
        n.close()

    return render_template("display.html", content = ncontent, index = marker_index)

if __name__ == "__main__":
    app.run()