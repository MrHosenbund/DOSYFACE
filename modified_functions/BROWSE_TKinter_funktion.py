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


#   Defining a function solely for Text_extraction
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




### Importing the file into the text field function!
def import_file():
    # Holt den Pfad aus dem Eingabefeld (entry_path)
    filepath = entry_path.get()
    
    # Prüft, ob überhaupt ein Pfad eingegeben wurde
    if filepath:
        try:
            # Extrahiert die "integral info"-Daten aus der Datei
            integral_information = extract_integral_info(filepath)
            
            # Löscht alten Text im Ausgabefeld (Textfeld für Integral Info)
            text_output_integral_Info.delete("1.0", tk.END)
            
            # Fügt Zeile für Zeile den extrahierten Inhalt in das Textfeld ein
            for line in integral_information:
                text_output_integral_Info.insert(tk.END, line + "\n")

        # Fehlerbehandlung: Wenn z. B. Datei nicht gefunden oder nicht lesbar
        except Exception as e:
            # Vorherigen Inhalt löschen
            text_output_integral_Info.delete("1.0", tk.END)
            # Fehlermeldung ins Textfeld schreiben
            text_output_integral_Info.insert(tk.END, f"Fehler beim Import:\n{e}")
    else:
        # Falls kein Pfad angegeben ist: Hinweis anzeigen
        text_output_integral_Info.delete("1.0", tk.END)
        text_output_integral_Info.insert(tk.END, "Kein Pfad angegeben.")

# Fenster
root = tk.Tk()
root.title("Dateiimport")
root.geometry("800x400")

# Rahmen für obere Zeile
frame_top = tk.Frame(root)
frame_top.pack(pady=10, padx=10)

# Eingabefeld für Pfad
entry_path = tk.Entry(frame_top, width=60)
entry_path.pack(side="left", padx=(0, 10))

# Button: Durchsuchen
button_browse = tk.Button(frame_top, text="Durchsuchen", command=browse_file)
button_browse.pack(side="left", padx=(0, 10))

# Button: Import
button_import = tk.Button(frame_top, text="Import file", command=import_file)
button_import.pack(side="left")

# # Scrollbares Textfeld für Ausgabe von Integral Information
# text_output_integral_Info = scrolledtext.ScrolledText(root, width=95, height=15, wrap=tk.WORD)
# text_output_integral_Info.pack(pady=10, padx=10)


# LabelFrame erzeugt einen Rahmen mit Titel
frame_Integral_Info = tk.LabelFrame(root, text="Integral Info", padx=10, pady=10)
frame_Integral_Info.pack(padx=10, pady=10, fill="both", expand=True)

# Scrollbares Textfeld innerhalb des beschrifteten Rahmens
text_output_integral_Info = scrolledtext.ScrolledText(frame_Integral_Info, wrap=tk.WORD, width=70, height=10)
text_output_integral_Info.pack(fill="both", expand=True)


# Second Frame for second textbox
frame_dataframe = tk.LabelFrame(root, text="Dataframe",padx=10, pady=10)
frame_dataframe.pack(padx=10, pady=10, fill="both",expand=True)

#second textfield for dataframe
text_output_dataframe = scrolledtext.ScrolledText(frame_dataframe,wrap=tk.WORD, width=70, height=10 )
text_output_dataframe.pack(padx=10, pady=10, fill="both",expand=True)


# GUI starten
root.mainloop()
