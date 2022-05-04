from email import charset
from enum import unique
from imghdr import tests
from operator import length_hint
import os
import pickle
from flask import Flask, render_template, url_for, request

# CHANGES TO MAKE:
# - geo.html is fine. maybe should be renamed, but otherwise the way it's organized here and its relations to other files are at least ok for now.
# - makepost.html is also fine. again maybe should be renamed, but it works ok.
# - writetomarkers has to be changed. specifically, it should both be renamed and should be reconfigured to use JSON to write unique classes (maybe? ideally?)  of characters to the list. this is the most important part by far
# - seeposts.html is fine, but should be renamed.
# - display.html has to be slightly changed, to give an int index instead of index read as it is now.

class Character:
    def __init__(self, name, image, bio, bios, rels, relsID, UniqueID):
        self.name = name
        self.image = image
        self.bio = bio
        self.bios = bios
        self.rels = rels
        self.relsID = relsID
        self.UniqueID = UniqueID

app = Flask(__name__)

@app.route("/")
@app.route("/landing")
def geo():
    return render_template("landing.html")

@app.route("/makepost")
def makepost():
    filename = "characters_pickled"
    countfile = "character_count.txt"

    infcontent = "0"
    pnames = ["None"]
    pids = ["None"]

    cfile = open(countfile, "r")

    if int(cfile.read()) != 0:
        infile = open(filename, "rb")
        pcontent = pickle.load(infile)
        infile.close()

        infcontent = pcontent

        for n in range(len(pcontent)):
            pnames.append(pcontent[n].name)
            pids.append(pcontent[n].UniqueID)

    cfile.close()

    return render_template("makepost.html", content = infcontent, names = pnames, ids = pids)

@app.route("/seeposts")
def seeposts():
    filename = "characters_pickled"
    countfile = "character_count.txt"

    infile = open(filename, "rb")
    oldCharacters = pickle.load(infile)
    infile.close

    cfile = open(countfile, "r")
    currentcount = int(cfile.read())
    cfile.close()

    return render_template("seeposts.html", characters = oldCharacters, charcount = currentcount)

@app.route("/writetochars", methods=["POST", "GET"])
def writeToCharacters():    
    output = request.form.to_dict()
    filename = "characters_pickled"

    # Get each element from the form as a unique string
    name = output["name"]
    image = output["image"]
    bio = output["bio"]
    
    bios = ["temp"]
    biocount = int(output["numofnewbios"])

    for i in range(biocount):
        bios.append(output[f"nb{i}"])

    rels = ["temp"]
    relcount = int(output["numofnewrels"])

    relsID = ["temp"]

    for i in range(relcount):
        rel1 = output[f"r{i}"]
        rel2 = output[f"s{i}"]

        tempfile = open(filename, "rb")
        tempchars = pickle.load(tempfile)
        tempfile.close()

        rels.append(rel1 + ": " + rel2 + ": " + str(tempchars[rel1].name))
        relsID.append(rel2)

    # Write the new stuff to the appropriate file(s)
    countfile = "character_count.txt"

    f1 = open(countfile, "r")
    charcount = int(f1.read())
    
    # Define a new class, and create a new instance of it using the form elements as constructor parameters
    newCharacter = Character(name, image, bio, bios, rels, relsID, charcount)

    if charcount == 0: # Indicates that this is the first character
        f1.close()

        f1 = open(countfile, "w")
        f1.write("1")
        f1.close()

        f2 = open(filename, "wb")
        initarray = [newCharacter]
        pickle.dump(initarray, f2)
        f2.close()
    
    else: # Indicates that this is not the first character
        f1.close()

        f1 = open(countfile, "w")
        f1.write(str(charcount + 1))
        f1.close()

        f2 = open(filename, "rb")
        currentlist = pickle.load(f2)
        f2.close()

        currentlist.append(newCharacter)

        f2 = open(filename, "wb")
        pickle.dump(currentlist, f2)
        f2.close()

    infcontent = "0"
    pnames = ["None"]
    pids = ["None"]

    cfile = open(countfile, "r")

    if int(cfile.read()) != 0:
        infile = open(filename, "rb")
        pcontent = pickle.load(infile)
        infile.close()

        infcontent = pcontent

        for n in range(len(pcontent)):
            pnames.append(pcontent[n].name)
            pids.append(pcontent[n].UniqueID)

    cfile.close()

    # Done
    return render_template("makepost.html", content = infcontent, names = pnames, ids = pids)
    
@app.route("/display", methods=["POST", "GET"])
def display():
    index = ""
    filename = "characters_pickled"

    if request.method == "POST":
        index = request.form["character_input_button"]

        infile = open(filename, "rb")
        oldCharacters = pickle.load(infile)
        infile.close

        selectCharacter = oldCharacters[int(index)]
        selectBios = selectCharacter.bios
        selectBiosLength = len(selectCharacter.bios)

        selectRels = selectCharacter.rels
        selectRelsLength = len(selectCharacter.rels)

    return render_template("display.html", character = selectCharacter, bios = selectBios, bioslength = selectBiosLength, rels = selectRels, relslength = selectRelsLength)

if __name__ == "__main__":
    app.run()