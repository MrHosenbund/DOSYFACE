import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
from scipy.optimize import curve_fit
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



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
# Function to import a dataframe from a given file and display it in the GUI text field
def import_file_dataframe(input_file):
    # Get the filepath from the entry field (GUI input field)
    filepath = entry_path.get()

    # Check if a filepath was actually provided
    if filepath:
        try:
            # Call function to load and return the cleaned dataframe from the file
            dataframe = import_dataframe(filepath)

            # Clear any previous content in the dataframe output text field
            text_output_dataframe.delete("1.0", tk.END)

            # Insert the entire dataframe (as string) into the text widget (just once)
            text_output_dataframe.insert(tk.END, dataframe.to_string())

        # Handle exceptions if an error occurs during file loading or parsing
        except Exception as e:
            # Clear any old content in the text field
            text_output_dataframe.delete("1.0", tk.END)

            # Display the error message in the text field
            text_output_dataframe.insert(tk.END, f"Fehler beim dataframe Import:\n{e}")

    else:
        # If no filepath was entered, inform the user
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


############################################
#
#
#   ADD FILE FUNCTION
#
#
###########################################

# Global variables
row_counter = 1  # Start counting from row 1 (since row 0 is used by the static UI)
dynamic_rows = []  # List to store all widget groups for later deletion or reference

def add_File():
    global row_counter  # Make sure we use the global row counter

    # --- Checkbuttons for experiment flags ---
    button_gpz6 = tk.Checkbutton(frame_buttons, text="gpz6")
    button_gpz6.grid(row=row_counter, column=0, padx=5)  # Place in column 0 of current row

    button_p30 = tk.Checkbutton(frame_buttons, text="p30")
    button_p30.grid(row=row_counter, column=1, padx=5)  # Column 1

    button_1H = tk.Checkbutton(frame_buttons, text="1H")
    button_1H.grid(row=row_counter, column=2, padx=5)  # Column 2

    button_19F = tk.Checkbutton(frame_buttons, text="19F")
    button_19F.grid(row=row_counter, column=3, padx=5)  # Column 3

    # --- Entry widget to display the file path ---
    entry_path_new = tk.Entry(frame_buttons, width=40)
    entry_path_new.grid(row=row_counter, column=4, padx=10)  # Column 4

    # --- Browse button for selecting file ---
    def browse_file_new():  # Local function tied to this row's entry field
        filepath = filedialog.askopenfilename(
            title="Datei auswählen", filetypes=[("Alle Dateien", "*.*")]
        )
        if filepath:  # If user selected a file
            entry_path_new.delete(0, tk.END)  # Clear current entry
            entry_path_new.insert(0, filepath)  # Insert new path

    button_browse = tk.Button(frame_buttons, text="Durchsuchen", command=browse_file_new)
    button_browse.grid(row=row_counter, column=5, padx=5)  # Column 5

    # --- Import button that processes the selected file ---
       # --- Updated Import button (with live output) ---
    def Import_databutton_new():
        filepath = entry_path_new.get()
        if filepath:
            try:
                # --- Integral Info ---
                info = extract_integral_info(filepath)
                text_output_integral_info.delete("1.0", tk.END)
                for line in info:
                    text_output_integral_info.insert(tk.END, line + "\n")

                # --- DataFrame ---
                df = import_dataframe(filepath)
                text_output_dataframe.delete("1.0", tk.END)
                text_output_dataframe.insert(tk.END, df.to_string())

            except Exception as e:
                text_output_integral_info.delete("1.0", tk.END)
                text_output_integral_info.insert(tk.END, f"Fehler:\n{e}")

    button_import = tk.Button(frame_buttons, text="Import Info", command=Import_databutton_new)
    button_import.grid(row=row_counter, column=6, padx=5)

    # --- Delete button to remove this row of widgets ---
    def delete_row():  # Destroys/hides all widgets of this row
        widgets = [button_gpz6, button_p30, button_1H, button_19F,
                   entry_path_new, button_browse, button_import, button_delete]
        for widget in widgets:
            widget.grid_forget()  # Hides the widget from the grid
        dynamic_rows.remove(widgets)  # Remove from tracking list

    button_delete = tk.Button(frame_buttons, text=" - Remove", command=delete_row)
    button_delete.grid(row=row_counter, column=7, padx=5)  # Column 7

    # --- Save the entire row for potential later reference or cleanup ---
    dynamic_rows.append([
        button_gpz6, button_p30, button_1H, button_19F,
        entry_path_new, button_browse, button_import, button_delete
    ])

    row_counter += 1  # Prepare for the next row to be added below



def plot_into_frame(target_frame):
    # Create a Matplotlib figure
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Example data to plot
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 15, 30, 25]
    ax.plot(x, y, label="Example Curve")
    ax.set_title("My Plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()

    # Embed the plot into the tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=target_frame)  # target_frame is a tk.Frame
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

############################################
#
#       NMR VARIABLE ASSIGNMENT
#
############################################

gyro_mag_Ratio_1H = (2.675 * 10**8) #gyromagnetic ratio proton (s-1T-1)
gyro_mag_Ratio_19F = (2.516 * 10**8) #gyromagnetic ratio proton (s-1T-1)



###########################################
#
#        WINDOW COSMETICS / DESIGN
#
###########################################


# Fenster
root = tk.Tk()
root.title("DOSYFACE")
root.geometry("9000x700")


# ----------- frame_buttons (alle Bedienelemente) -----------
frame_buttons = tk.LabelFrame(root)
frame_buttons.grid(row=0, column=0, pady=5, padx=5, sticky="nw")

# Checkbuttons & Buttons nebeneinander platzieren
button_gpz6 = tk.Checkbutton(frame_buttons, text="gpz6")                    #COMMAND MISSING
button_gpz6.grid(row=0, column=0, padx=5)

button_p30 = tk.Checkbutton(frame_buttons, text="p30")                      #COMMAND MISSING
button_p30.grid(row=0, column=1, padx=5)

button_1H = tk.Checkbutton(frame_buttons, text="1H")                        #COMMAND MISSING
button_1H.grid(row=0, column=2, padx=5)

button_19F = tk.Checkbutton(frame_buttons, text="19F")                      #COMMAND MISSING
button_19F.grid(row=0, column=3, padx=5)

entry_path = tk.Entry(frame_buttons, width=40)  
entry_path.grid(row=0, column=4, padx=10)

button_browse = tk.Button(frame_buttons, text="Durchsuchen", command=browse_file)
button_browse.grid(row=0, column=5, padx=5)

button_import = tk.Button(frame_buttons, text="Import Info", command=Import_databutton)
button_import.grid(row=0, column=6, padx=5)

button_addFile = tk.Button(frame_buttons, text=" + Add File", command=add_File)
button_addFile.grid(row=0, column=7, padx=5)

# --- FIXED COLUMN for right-hand output section (column 8) ---

frame_Info=tk.LabelFrame(root,text="Integral Information & Dataframe",pady=10,padx=10 )
frame_Info.grid(row=0, column=1, rowspan=3,sticky="n")


text_output_integral_info = scrolledtext.ScrolledText(frame_Info, wrap=tk.WORD, width=85, height=10)
text_output_integral_info.grid(row=0, column=0)


text_output_dataframe = scrolledtext.ScrolledText(frame_Info, wrap=tk.WORD, width=85, height=10)
text_output_dataframe.grid(row=1, column=0)

##################################
# VAR. ASSIGNMENT - BOTTOM RIGHT
##################################

#variable Assignment - Frame
frame_input = tk.LabelFrame(root, text="Variables", padx=10, pady=10)
frame_input.grid(row=2, column=1)

#Fixed Values - Frame 
frame_Fixed_Values = tk.Frame(frame_input,padx=2, pady=2)
frame_Fixed_Values.grid(row=0, column=0)

label_Fixed_values = tk.Label(frame_Fixed_Values, text="Fixd Values")
label_Fixed_values.grid(row=0, column=0)

#Label for fixed gpz6 - fixed gradient strength for gradient length variation experiments
label_gpz6 = tk.Label(frame_Fixed_Values, text="gpz6 [%]")
label_gpz6.grid(row=1,column=0)
#Input field for gpz6 - tk.Entry = allows everything to be entered => I need to convert the string to float, 
# In this case: String - to float ( precent number )
entry_gpz6 = tk.Entry(frame_Fixed_Values,width=5 )                  # CONVERT STRING TO FLOAT
entry_gpz6.grid(row=2, column=1)

#Label for p30 - fixed gradient length for gpz6 variation experiments
label_p30 = tk.Label(frame_Fixed_Values, text=r"p30 [μS]") #tkinter - does not present LaTeX style greek letters
label_p30.grid(row=2, column=0)
#Input field for fixed p30
entry_p30 = tk.Entry(frame_Fixed_Values, width=5)                   #CONVERT STRING INTO FLOAT
entry_p30.grid(row=1, column=1)

#Label for initial guess regarding fit
label_initial_guess = tk.Label(frame_Fixed_Values, text="in. guess")
label_initial_guess.grid(row=3, column=0)
#entry for initual guess   
entry_initial_guess = tk.Entry(frame_Fixed_Values, width=5)         #CONVERT STRING INTO FLOAT - ALLOW 10^x == 10**9
entry_initial_guess.grid(row=3,column=1)                            #Two ways of entering an exponent
                                                                    #implement info which shows how to enter what exactly



#SEPARATOR SHOULD SEPARATE FOLLOWING FRAMES FROM EACH OTHER:
# FRAME - LEFT = frame_Fixed_Values  | FRAME RIGHT = frame_Variable_Values
#Sticky"ns" is important to make it visible 

ttk.Separator(frame_input,orient="vertical").grid(column=1,row=0,rowspan=4, sticky="ns") 

#FRAME 2 - Variable p30 & gpz6
frame_Variable_Values = tk.Frame(frame_input, padx=2, pady=2)
frame_Variable_Values.grid(row=0, column=2)

#Variable p30 Entry 
label_p30_var = tk.Label(frame_Variable_Values, text="Var. p30 in:  ")
label_p30_var.grid(row=0, column=0)

p30_microSeconds = tk.Checkbutton(frame_Variable_Values, text="μS")
p30_microSeconds.grid(row=0, column=1)

p30_milliSeconds= tk.Checkbutton(frame_Variable_Values, text="mS")
p30_milliSeconds.grid(row=0,column=2)

p30_Seconds = tk.Checkbutton(frame_Variable_Values, text="S")
p30_Seconds.grid(row=0,column=3)


#Graph Frame for Graph
frame_Graph = tk.LabelFrame(root, text="Graphical Results",padx=0, pady=5 )
frame_Graph.grid(row=1,column=0)

# Frame for Matplotlib plot, below the button frame
frame_plot = tk.Frame(root)
frame_plot.grid(row=1, column=0, padx=10, pady=10, sticky="n")
plot_into_frame(frame_plot)

#Frame for results
frame_results = tk.LabelFrame(root, text="Diffusion Coefficient",padx=0, pady=5)
frame_results.grid(row=2,column=0)

#textbox for results
text_output_results = scrolledtext.ScrolledText(frame_results, wrap=tk.WORD, width=60, height=0.5)
text_output_results.grid(row=0, column=0)







# GUI starten
root.mainloop()
