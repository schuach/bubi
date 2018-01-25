import pyperclip
import os
import datetime
import easygui

# import variables and values from config file
from conf import *

# check if the directory for the outfiles exists. If not, create it
if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)

def get_sf_delim(instr):
    """Returns the subfield delimiter of instr (string), or None if there is none"""
    # check for the right delimiters
    if "|" in instr:
        return "|"
    elif "$$" in instr:
        return "$$"
    else:
        return ""

def makedict(instr):
    """Returns a dictionary with subfield codes as keys. Values are the subfield
    contents. There's a list for the contents to accomodate to multiple occurences
    one subfield.
    """
    dct = {}
    sf_delim = get_sf_delim(instr)
    inlist = instr.split(sf_delim)
    inlist.pop(0)

    # populate dictionary
    for i in inlist:
        if i[0] in dct.keys():
            sf = i[0]
            cont = i[2:].strip()
            dct[sf].append(cont)
        else:
            sf = i[0]
            cont = i[2:].strip()
            dct[sf] = [cont]

    return dct

def get_instr():
    """Gets contents from clipboard and checks them for validity. Returns a
    string.
    """
    msg = "Bitte den Feldinhalt in die Zwischenablage Kopieren"

    sf_delim = ""

    while True:
        reply = easygui.buttonbox(msg, choices=["OK", "Abbrechen"])

        if reply == "Abbrechen":
            quit()
        else:
            instr = pyperclip.paste()

        # check if data is valid -- if not, ask again
        if "a Universitätsbibliothek" not in instr:
            msg = """Etwas scheint nicht zu stimmen. Bitte versuchen Sie es nocheinmal.

Bitte kopieren Sie den Feldinhalt in die Zwischenablage."""
            continue
        else:
            return instr


def write_output(dct):
    """Writes the contents of the dictionary to a file"""
    call_nr = easygui.enterbox(msg="Bitte die Signatur eingeben")
    outfile_name = OUT_DIR + call_nr.replace(" ", "-") +  "_{:%Y-%m-%d}.txt".format(datetime.datetime.now())

    def write_sf(sf_code, prefix=""):
        """Convenience-Funktion zum schreiben einzelner Subfelder in Datei.
        Nimmt den Subfdcode als String als Argument."""
        subfields = dct.get(sf_code)
        if subfields == None:
            return
        else:
            for sf in subfields:
                outfile.write(prefix + sf + "\n")

    with open(outfile_name, "w", encoding="utf-8") as outfile:
        write_sf("a")
        outfile.write("\n\n")
        write_sf("b")
        write_sf("c")
        write_sf("d", "TITEL: ")
        write_sf("e")
        write_sf("f")
        write_sf("g")
        write_sf("h")
        write_sf("i")
        write_sf("j")
        write_sf("k")
        write_sf("l")
        write_sf("m")
        write_sf("n")
        write_sf("o")
        write_sf("p")
        write_sf("q")
        write_sf("r")

    os.startfile(outfile_name)

def run():
    instr = get_instr()
    dct = makedict(instr)
    write_output(dct)
