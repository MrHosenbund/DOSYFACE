import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
from scipy.optimize import curve_fit
from tkinter import *



#Button definition, Browsing function
# Funktion zum Durchsuchen und Auswählen einer Datei
def browse_file():
    # Öffnet Dateiauswahl-Dialog
    filepath = filedialog.askopenfilename(
        title="Datei auswählen",
        filetypes=[("Alle Dateien", "*.*")],  # Datei-Filter (z. B. nur .txt)
    )
    # Wenn eine Datei ausgewählt wurde → Pfad ins Textfeld einfügen
    if filepath:
        entry_path.delete(0, tk.END)          # Vorherigen Inhalt im Textfeld löschen
        entry_path.insert(0, filepath)        # Neuen Pfad einfügen



####################################
#   COMBINE Functions 
#   def extract_integral_info
#   def import_dataframe
#####################################


################################################
#   ASSIGNING MULTIPLE FUNCTIONS TO ONE BUTTON
################################################
def Import_databutton():
    filepath = entry_path.get()
    extract_integral_info(filepath)
    import_file_dataframe(filepath)
    import_file_integral_info(filepath)


################################################
#   EXTRACTS DATAFRAME FROM TEXT 
#################################################
# 




###################################################
#   EXTRACT DATAFRAME FROM TEXTFIELD
###################################################

def import_dataframe(input_file): #imports data to dataframe, filters out all lines starting with # or empty lines
#removes the last column of dataframe as it appears to be empty
   
    valid_lines = []  # Create list to store valid lines

    with open(input_file, 'r') as infile: # rad the file
        for line in infile:
            if line.strip() and not line.startswith('#'): # Check if the line is not empty and does not start with '#'
                valid_lines.append(line.strip())

    # to use read.csv() (and all the benefits) a file like object has to be created. This is done with StringIO
    valid_data = "\n".join(valid_lines) #Join the valid lines into a single string with newline characters
    data_io = StringIO(valid_data)  # Use StringIO to create a file-like object from the string

    df = pd.read_csv(data_io, header=None, index_col=0, sep=";")  # Read the data into a DataFrame
    # maybe has to be customized
    dataframe = df.iloc[:, :-1] #removes last column, as this one is empty
    dataframe = dataframe.iloc[0:] #removes the first row as this one is empty
    #dataframe = dataframe.replace("", np.nan).dropna(how='all') #removes completely empty rows

    return dataframe



######################################
#   IMPORT DATAFRAME INTO TEXT FIELD
######################################
def import_file_dataframe(input_file):
    # Holt den Pfad aus dem Eingabefeld (entry_path)
    filepath = entry_path.get()
    
    # Prüft, ob überhaupt ein Pfad eingegeben wurde
    if filepath:
        try:
            # Extrahiert die "integral info"-Daten aus der Datei
            dataframe = import_dataframe(filepath)
                        
            # Löscht alten Text im Ausgabefeld (Textfeld für Integral Info)
            text_output_dataframe.delete("1.0", tk.END)
            
            # Fügt Zeile für Zeile den extrahierten Inhalt in das Textfeld ein
            for line in dataframe:
                text_output_dataframe.insert(tk.END, dataframe.to_string())
       # Fehlerbehandlung: Wenn z. B. Datei nicht gefunden oder nicht lesbar
        except Exception as e:
            # Vorherigen Inhalt löschen
            text_output_dataframe.delete("1.0", tk.END)
            # Fehlermeldung ins Textfeld schreiben
            text_output_dataframe.insert(tk.END, f"Fehler beim dataframe Import:\n{e}")
    else:
        # Falls kein Pfad angegeben ist: Hinweis anzeigen
        text_output_dataframe.delete("1.0", tk.END)
        text_output_dataframe.insert(tk.END, "Kein Pfad angegeben.")





###########################################
#
#       INTEGRAL INFO IMPORT
#
###########################################


# ###############################################
#   EXTRACT INTEGRAL INFORMATION FROM TEXT
#################################################
def extract_integral_info(input_file):
    # Liste zum Speichern der relevanten Zeilen (aus dem gewünschten Abschnitt)
    integral_info = []
    
    # Steuerflag, um zu wissen, ob wir uns im interessanten Abschnitt befinden
    inside_section = False

    # Öffnet die Datei im Lesemodus
    with open(input_file, 'r') as infile:
        # Geht jede Zeile der Datei einzeln durch
        for line in infile:
            # Entfernt führende und nachfolgende Leerzeichen (inkl. \n)
            stripped_line = line.strip()

            # Wenn der Start des gewünschten Abschnitts erreicht ist
            if stripped_line.startswith('# --- Integral info ---'):
                inside_section = True  # Wir befinden uns nun im interessanten Block

            # Sobald die Tabelle mit "Spectrum" beginnt, wird abgebrochen
            if stripped_line.startswith('# Spectrum#;'):
                break  # Der gewünschte Abschnitt endet hier – abbrechen

            # Nur wenn wir im gewünschten Abschnitt sind, speichern wir die Zeile
            if inside_section:
                integral_info.append(stripped_line)

    # Gibt die gesammelten Zeilen (aus dem Integral-Info-Block) zurück
    return integral_info
 

#############################################
#   IMPORT INTEGRAL INFO INTO TEXT FIELD
#############################################
def import_file_integral_info(input_file):
    # Holt den Pfad aus dem Eingabefeld (entry_path)
    filepath = entry_path.get()
    
    # Prüft, ob überhaupt ein Pfad eingegeben wurde
    if filepath:
        try:
            # Extrahiert die "integral info"-Daten aus der Datei
            integral_information = extract_integral_info(filepath)
                        
            # Löscht alten Text im Ausgabefeld (Textfeld für Integral Info)
            text_output_integral_info.delete("1.0", tk.END)
            
            # Fügt Zeile für Zeile den extrahierten Inhalt in das Textfeld ein
            for line in integral_information:
                text_output_integral_info.insert(tk.END, line + "\n")

        # Fehlerbehandlung: Wenn z. B. Datei nicht gefunden oder nicht lesbar
        except Exception as e:
            # Vorherigen Inhalt löschen
            text_output_integral_info.delete("1.0", tk.END)
            # Fehlermeldung ins Textfeld schreiben
            text_output_integral_info.insert(tk.END, f"Fehler beim Import:\n{e}")
    else:
        # Falls kein Pfad angegeben ist: Hinweis anzeigen
        text_output_integral_info.delete("1.0", tk.END)
        text_output_integral_info.insert(tk.END, "Kein Pfad angegeben.")


#############################
# #   PACK vs. FILL
# | Option       | `pack()` | `grid()` | Bedeutung                         |
# | ------------ | -------- | -------- | --------------------------------- |
# | `side`       | ✅        | ❌        | Position im Container             |
# | `fill`       | ✅        | ❌        | Widget füllt den Raum aus         |
# | `expand`     | ✅        | ❌        | Widget dehnt sich mit Fenster     |
# | `sticky`     | ❌        | ✅        | Ausrichtung innerhalb einer Zelle |
# | `row/column` | ❌        | ✅        | Gitterposition                    |


# Fenster
root = tk.Tk()
root.title("Dateiimport")
root.geometry("9000x700")

# Rahmen für obere Zeile
frame_top = tk.Frame(root)
frame_top.grid(row=0, column=0,pady=10, padx=10)

# Eingabefeld für Pfad
entry_path = tk.Entry(frame_top, width=60)
entry_path.grid(row=0, column=0,  padx=(0, 10))

# Button: Durchsuchen
button_browse = tk.Button(frame_top, text="Durchsuchen", command=browse_file)
button_browse.grid(row=0, column=1, padx=(0, 10))

# Button: Import # Combined command : Import data & IMport INtegral information 
button_import = tk.Button(frame_top, text="Import Data", command=Import_databutton)
button_import.grid(row=0, column=2)

# LabelFrame erzeugt einen Rahmen mit Titel
frame_Integral_Info = tk.LabelFrame(root, text="Integral Info", padx=10, pady=10)
frame_Integral_Info.grid(row=2, column=2, padx=10, pady=10  )

# Scrollbares Textfeld innerhalb des beschrifteten Rahmens für Integral Info
text_output_integral_info = scrolledtext.ScrolledText(frame_Integral_Info, wrap=tk.WORD, width=70, height=10)
text_output_integral_info.grid(row=2, column=2, padx=10, pady=10 )


# Second Frame for second textbox
frame_dataframe = tk.LabelFrame(root, text="Dataframe",padx=10, pady=10)
frame_dataframe.grid(row=3, column=2, padx=10, pady=10)

#second textfield for dataframe
text_output_dataframe = scrolledtext.ScrolledText(frame_dataframe,wrap=tk.WORD, width=70, height=10 )
text_output_dataframe.grid(row=3, column=2, padx=10, pady=10)


# GUI starten
root.mainloop()
