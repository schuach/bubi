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
            raise SystemExit
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
    call_nr = ''

    while call_nr == '':
        call_nr = easygui.enterbox(msg="Bitte die Signatur eingeben")

        if call_nr == None:
            raise SystemExit

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
        outfile.write(HEADER)
        outfile.write("\n\n")
        write_sf("b") # beauftragte Firma
        outfile.write("\n\n")
        write_sf("d", "TITEL: ")
        write_sf("e") # Untertitel
        outfile.write(f"SIGNATUR: {call_nr}\n")
        outfile.write("\n")
        write_sf("f") # Art der Vorlage (Attrappe, Musterband)
        outfile.write("\n")
        write_sf("g", "BINDEART:") # Bindeart
        write_sf("h") # Rückenfarbe
        write_sf("i") # Deckenfarbe
        outfile.write("\n")
        write_sf("j") # Umschläge
        write_sf("k") # Index
        write_sf("l") # Beilagen
        write_sf("m") # Notizen
        outfile.write("\n")
        write_sf("n") # Bandzahl, Jahreszahl, Stückzahl (in je einem SF)
        outfile.write("\n")
        write_sf("o") # Lieferfrist
        outfile.write("\n\n")
        outfile.write(FOOTER)

    os.startfile(outfile_name)

def run():
    instr = get_instr()
    dct = makedict(instr)
    write_output(dct)

run()
