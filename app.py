from operator import length_hint
import os
import pickle
import json
from flask import Flask, render_template, url_for, request

# CHANGES TO MAKE:
# - geo.html is fine. maybe should be renamed, but otherwise the way it's organized here and its relations to other files are at least ok for now.
# - makepost.html is also fine. again maybe should be renamed, but it works ok.
# - writetomarkers has to be changed. specifically, it should both be renamed and should be reconfigured to use JSON to write unique classes (maybe? ideally?)  of characters to the list. this is the most important part by far
# - seeposts.html is fine, but should be renamed.
# - display.html has to be slightly changed, to give an int index instead of index read as it is now.

class Character:
    def __init__(self, name, image, bio, r1, r2):
        self.name = name
        self.image = image
        self.bio = bio
        self.r1 = r1
        self.r2 = r2

app = Flask(__name__)

@app.route("/")
@app.route("/landing")
def geo():
    return render_template("landing.html")

@app.route("/makepost")
def makepost():
    return render_template("makepost.html")

@app.route("/seeposts")
def seeposts():
    filename = "characters_pickled"
    infile = open(filename, "rb")

    oldCharacters = pickle.load(infile)

    infile.close

    return render_template("seeposts.html", characters = oldCharacters)

@app.route("/writetomarkers", methods=["POST", "GET"])
def writeToMarkers():    
    output = request.form.to_dict()
    
    # Get each element from the form as a unique string
    name = output["name"]
    image = output["image"]
    bio = output["bio"]
    r1 = output["r1"]
    r2 = output["r2"]

    # OPTION 1:
    # Define a new class, and create a new instance of it using the form elements as constructor parameters
    newCharacter = Character(name, image, bio, r1, r2)
    teststring = "bo"

    # OPTION 2:
    # Get multiple lists (either in a single file or in multiple files), each list storing a certain element (name, image src, etc.), and write each form element to these lists at the same index

    # Write the new stuff to the appropriate file(s)
    filename = "characters_pickled"
    
    thisfile = open(filename, "rb")
    temp = pickle.load(thisfile)
    temp += teststring
    thisfile.close()

    thisfile = open(filename, "wb")
    pickle.dump(temp, thisfile)
    thisfile.close()

    # seems to work fine so far
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