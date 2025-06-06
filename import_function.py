import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
from scipy.optimize import curve_fit
from tkinter import *

################################################
#
#   Import function is a modified version of the initial input_data function
#   this system here includes two functions which isolate integral info, which is important for region selection
#   as well as a function which presents the imported data in a clean manner
#
##############################################


def import_data(input_file): #imports data to dataframe, filters out all lines starting with # or empty lines
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



# Extracts the section starting from '# --- Integral info ---' up to (but not including)
# the line that starts with '# Spectrum#; Integral 0; Integral 1;'.
#
# Extracts only the lines from '# --- Integral info ---'
# up to (but NOT including) the line starting with '# Spectrum#;'
#  

def extract_integral_info(input_file):
   
    integral_info = []                 # Liste zur Speicherung der gewünschten Zeilen
    inside_section = False            # Steuerflag: "Sind wir im interessierenden Abschnitt?"

    with open(input_file, 'r') as infile:      # Öffnet die Datei zum Lesen
        for line in infile:                    # Zeile für Zeile durchgehen
            stripped_line = line.strip()       # Entfernt führende und nachfolgende Leerzeichen

            if stripped_line.startswith('# --- Integral info ---'):
                inside_section = True          # Startsignal: Wir sind jetzt im Zielabschnitt

            if stripped_line.startswith('# Spectrum#;'):
                break                          # Abbruch: Wir wollen nicht bis zur Tabelle mitlesen

            if inside_section:
                integral_info.append(stripped_line)  # Nur dann Zeile speichern

    return integral_info


# Displays the integral info block cleanly, especially for region lines
# with aligned columns: low field | high field | bias | slope | region
def display_integral_info_clean(lines):
    
    for line in lines:
        if "# for region" in line:
            # Extrahiere und formatiere die numerischen Spalten + Kommentar
            parts = line.strip("#").strip().split()
            if len(parts) >= 7:
                low = float(parts[0])
                high = float(parts[1])
                bias = float(parts[2])
                slope = float(parts[3])
                region = " ".join(parts[4:])  # z. B. "# for region 1"
                print(f"{low:>12.6f}  {high:>12.6f}  {bias:>6.2f}  {slope:>6.2f}    {region}")
        else:
            print(line)

#extract lines and display these in a beautiful manner

######################################################################################################
#
#                  IMPLEMENT THIS FUNCTION INTO DOSYFACE
#           Integral info extraction and clean displaying of that
#
######################################################################################################


def extract_and_display_integral_info(input_file):
    extracted_integral_info_lines = []
    inside_section = False

    with open(input_file, 'r') as infile:
        for line in infile:
            stripped_line = line.strip()

            if stripped_line.startswith('# --- Integral info ---'):
                inside_section = True

            if stripped_line.startswith('# Spectrum#;'):
                break

            if inside_section:
                extracted_integral_info_lines.append(stripped_line)
                if "# for region" in stripped_line:
                    parts = stripped_line.strip("#").strip().split()
                    if len(parts) >= 7:
                        try:
                            low = float(parts[0])
                            high = float(parts[1])
                            bias = float(parts[2])
                            slope = float(parts[3])
                            region = " ".join(parts[4:])
                            print(f"{low:>12.6f}  {high:>12.6f}  {bias:>6.2f}  {slope:>6.2f}    {region}")
                        except ValueError:
                            print(stripped_line)
                else:
                    print(stripped_line)

    return extracted_integral_info_lines



df_DOSY = import_data(r"DOSYFACE\NMR_data\C8_19F_global_G_Length_DOSY-150-165")
info_DOSY_raw = extract_and_display_integral_info(r"DOSYFACE\NMR_data\C8_19F_global_G_Length_DOSY-150-165")

print(df_DOSY) #prints DOSY_data in a clean and simple manner.
print(info_DOSY_raw) #prints extracted integral info directly, ugly
print(display_integral_info_clean(info_DOSY_raw))  #prints extracted integral info in a beautiful manner


