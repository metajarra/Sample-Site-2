from imghdr import tests
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

    # Define a new class, and create a new instance of it using the form elements as constructor parameters
    newCharacter = Character(name, image, bio, r1, r2)
    teststring = 4

    # Write the new stuff to the appropriate file(s)
    filename = "characters_pickled"
    countfile = "character_count.txt"

    f1 = open(countfile, "r")
    charcount = int(f1.read())

    if charcount == 0: # Indicates that this is the first character
        f1.close()

        f1 = open(countfile, "w")
        f1.write("1")
        f1.close()

        f2 = open(filename, "wb")
        testinitarray = [teststring]
        pickle.dump(testinitarray, f2)
        f2.close()
    
    else: # Indicates that this is not the first character
        f1.close()

        f2 = open(filename, "rb")
        currentlist = pickle.load(f2)
        f2.close()

        currentlist.append(teststring)

        f2 = open(filename, "wb")
        pickle.dump(currentlist, f2)
        f2.close()

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