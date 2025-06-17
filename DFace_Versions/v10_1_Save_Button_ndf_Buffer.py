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

###############################################################################
#
#           V_10_1
#           At this point i decided to finish this program with the key
#           functionalities being evaluating just one dataset
#           Not multiple datasets. -> time constraints and Prüfungsphase
#           are slowly creeping up and do not allow crazy modifications which I
#           simply do not have the time to work on. 
#
###############################################################################
#
#       v10_1
#       the SAVE - button in the choose region & normalize window
#       Should add information into the row which describes your datapoints
#       for the fit. 
#       The Save button sould also now save the dataframe in the ndf window
#
###############################################################################



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

def Import_Info_Button():
    filepath = entry_path.get()
    extract_integral_info(filepath)
    import_file_dataframe_text(filepath)
    import_file_integral_info(filepath)
    update_gradient_label_on_import()
    

def import_file_dataframe_text(input_file):
    global df  # Declare that we want to modify the global variable
    #Global will allow me to access this data from anywhere in the script. It is sort of hovering around everything

    filepath = entry_path.get()
    if filepath:
        try:
            df = import_dataframe(filepath)  # <-- Assign globally
            text_output_dataframe.delete("1.0", tk.END)
            text_output_dataframe.insert(tk.END, df.to_string())
        except Exception as e:
            text_output_dataframe.delete("1.0", tk.END)
            text_output_dataframe.insert(tk.END, f"Fehler beim dataframe Import:\n{e}")



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

dynamic_rows = []  # Global list to track added rows
row_counter = 1   # Also global row counter


def add_File():
    global row_counter
    global df

    var_gradient = tk.StringVar(value="gpz6")
    var_isotope = tk.StringVar(value="1H")

    button_gpz6 = tk.Radiobutton(frame_data_import, text="gpz6", variable=var_gradient, value="gpz6")
    button_gpz6.grid(row=row_counter, column=0, padx=5)

    button_p30 = tk.Radiobutton(frame_data_import, text="p30", variable=var_gradient, value="p30")
    button_p30.grid(row=row_counter, column=1, padx=5)

    button_1H = tk.Radiobutton(frame_data_import, text="1H", variable=var_isotope, value="1H")
    button_1H.grid(row=row_counter, column=2, padx=5)

    button_19F = tk.Radiobutton(frame_data_import, text="19F", variable=var_isotope, value="19F")
    button_19F.grid(row=row_counter, column=3, padx=5)

    entry_path_new = tk.Entry(frame_data_import, width=40)
    entry_path_new.grid(row=row_counter, column=4, padx=10)

    def browse_file_new():
        filepath = filedialog.askopenfilename(title="Datei auswählen", filetypes=[("Alle Dateien", "*.*")])
        if filepath:
            entry_path_new.delete(0, tk.END)
            entry_path_new.insert(0, filepath)

    button_browse = tk.Button(frame_data_import, text="Browse", command=browse_file_new)
    button_browse.grid(row=row_counter, column=5, padx=5)

    # Important: Pass the local StringVars to this function via default args
    def Import_databutton_new(local_var_gradient=var_gradient, local_var_isotope=var_isotope):
        filepath = entry_path_new.get()
        if filepath:
            try:
                info = extract_integral_info(filepath)
                text_output_integral_info.delete("1.0", tk.END)
                for line in info:
                    text_output_integral_info.insert(tk.END, line + "\n")
                global df
                df = import_dataframe(filepath)
                text_output_dataframe.delete("1.0", tk.END)
                text_output_dataframe.insert(tk.END, df.to_string())

                # Use local StringVars here!
                gradient = local_var_gradient.get()
                isotope = local_var_isotope.get()
                new_text = f"Variable Gradient: {gradient}\nIsotope: {isotope}"
                Gradient_label.config(text=new_text)

            except Exception as e:
                text_output_integral_info.delete("1.0", tk.END)
                text_output_integral_info.insert(tk.END, f"Fehler:\n{e}")

    button_import = tk.Button(frame_data_import, text="Import info", command=Import_databutton_new)
    button_import.grid(row=row_counter, column=6, padx=5)

    # Rest of your code unchanged...
    def delete_row():
        widgets = [button_gpz6, button_p30, button_1H, button_19F,
                   entry_path_new, button_browse, button_import, button_delete]
        for widget in widgets:
            widget.grid_forget()
        dynamic_rows.remove(widgets)

    button_delete = tk.Button(frame_data_import, text=" - Remove", command=delete_row)
    button_delete.grid(row=row_counter, column=7, padx=5)

    dynamic_rows.append([
        button_gpz6, button_p30, button_1H, button_19F,
        entry_path_new, button_browse, button_import, button_delete,
        var_gradient, var_isotope
    ])

    row_counter += 1




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
frame_data_import = tk.LabelFrame(root)
frame_data_import.grid(row=0, column=0, pady=5, padx=5, sticky="nw")






####### Radiobuttons for either gpz6 or p30 selection

#Gradient Selection
##################################
#   QUICK INFO REG. Gradient Selection
#  selecting gpz6  implement variable values of gpz6 & fixed p30
# selecting p30 implements variable values of p30 & fixed gpz6 
# Variable values are located in Frame_Valuable 


def update_gradient_label_on_import():
    gradient = Variable_gradient.get()  # "gpz6" or "p30"
    isotope = Isotope_selection.get()   # "1H" or "19F"
    new_text = f"Variable Gradient: {gradient}\nIsotope: {isotope}"
    Gradient_label.config(text=new_text)




Variable_gradient = tk.StringVar(value="gpz6")

button_gpz6 = tk.Radiobutton(frame_data_import, text="gpz6", variable=Variable_gradient, value="gpz6")
button_gpz6.grid(row=0, column=0, padx=5)

button_p30 = tk.Radiobutton(frame_data_import, text="p30", variable=Variable_gradient, value="p30")
button_p30.grid(row=0, column=1, padx=5)

Isotope_selection = tk.StringVar(value="1H")

button_1H = tk.Radiobutton(frame_data_import, text="1H", variable=Isotope_selection, value="1H")
button_1H.grid(row=0, column=2, padx=5)

button_19F = tk.Radiobutton(frame_data_import, text="19F", variable=Isotope_selection, value="19F")
button_19F.grid(row=0, column=3, padx=5)

entry_path = tk.Entry(frame_data_import, width=40)
entry_path.grid(row=0, column=4, padx=10)

button_browse = tk.Button(frame_data_import, text="Browse", command=browse_file)
button_browse.grid(row=0, column=5, padx=5)

button_import = tk.Button(frame_data_import, text="Import Info", command=Import_Info_Button)
button_import.grid(row=0, column=6, padx=5)

button_addFile = tk.Button(frame_data_import, text=" + Add File", command=add_File)
button_addFile.grid(row=0, column=7, padx=5)

# --- FIXED COLUMN for right-hand output section (column 8) ---

frame_Info=tk.LabelFrame(root,text="Integral Information & Dataframe",pady=10,padx=10 )
frame_Info.grid(row=0, column=1, rowspan=2,sticky="n")


text_output_integral_info = scrolledtext.ScrolledText(frame_Info, wrap=tk.WORD, width=85, height=10)
text_output_integral_info.grid(row=0, column=0)


text_output_dataframe = scrolledtext.ScrolledText(frame_Info, wrap=tk.WORD, width=85, height=10)
text_output_dataframe.grid(row=1, column=0)






######################################
#   OPEN CHOOSE AND NORMALIZE WINDOW
######################################
#
# enter region number
# receive normalized column
# continue fitting calculations with this one
# press save and confirm info and dataframe  
#  

# Initialize an empty dictionary to hold buffers indexed by a key (e.g., dataset index)
normalized_data_buffers = {}

#Once I open the n_df window the normalized integral should appear within the window




#n_df = normalized dataframe
# Global variables to hold window, widget, and buffer
ndf_window = None
ndf_result = None
  # Your buffer dict (make sure it matches your save function)

def n_df():
    global ndf_window, ndf_result, normalized_data_buffers

    # If window already exists, just bring it to front
    if ndf_window and ndf_window.winfo_exists():
        ndf_window.lift()
        return

    ndf_window = tk.Toplevel(root)
    ndf_window.title("Normalized Dataframe")
    ndf_window.geometry("600x400")

    ndf_result = scrolledtext.ScrolledText(ndf_window, wrap=tk.WORD, width=60, height=30)
    ndf_result.grid(row=0, column=0, padx=10, pady=10)

    # Combine all buffered normalized data into one string
    full_text = "\n".join(normalized_data_buffers.values())

    # Insert buffer content into the text widget
    ndf_result.insert(tk.END, full_text)
#SAVE Button in Choose_window    
# Place this once at the top level of your script (not inside the function)
 # key: datapoint_name, value: accumulated normalized text

def open_ChsANorm_Window():
    global normalized_data_buffers

    ChooseANorm_window = tk.Toplevel(root)
    ChooseANorm_window.title("Choose and Normalize Region")
    ChooseANorm_window.geometry("500x300")

    saved = False  # local flag

    def on_close():
        # just destroy window, flag reset next time you open
        ChooseANorm_window.destroy()

    ChooseANorm_window.protocol("WM_DELETE_WINDOW", on_close)

    frame_buttons = tk.Frame(ChooseANorm_window)
    frame_buttons.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

    Label_Region_entry = tk.Label(frame_buttons, text="Region: ")
    Label_Region_entry.grid(row=0, column=0, sticky="n")

    Region_entry = tk.Entry(frame_buttons, width=10)
    Region_entry.grid(row=0, column=1, sticky="n")

    Normalized_Integral = scrolledtext.ScrolledText(ChooseANorm_window, wrap=tk.WORD, width=40, height=20)
    Normalized_Integral.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

    def normalize():
        global df
        try:
            region_index = int(Region_entry.get()) - 1
            normalized = df.iloc[:, region_index] / df.iloc[:, region_index].max()
            Normalized_Integral.delete("1.0", tk.END)
            Normalized_Integral.insert(tk.END, normalized.to_string())
        except Exception as e:
            Normalized_Integral.delete("1.0", tk.END)
            Normalized_Integral.insert(tk.END, f"Fehler bei der Normalisierung:\n{e}")

    button_normalize = tk.Button(frame_buttons, text="Normalize", command=normalize)
    button_normalize.grid(row=1, column=0, sticky="w", pady=10)

    def save():
        global datapoint_row_count
        global normalized_data_buffers
        try:
            gradient = Variable_gradient.get()
            isotope = Isotope_selection.get()
            region_n = Region_entry.get()

            datapoint_name = f"{gradient}_{isotope}_Region_{region_n}"

            if dataset_count.get() == "one":
                # Update only fixed 0. Datapoints entry
                Entry_filename.delete(0, tk.END)
                Entry_filename.insert(0, datapoint_name)
            else:
                # Add new dynamic datapoint row
                add_datapoint_row(datapoint_name)

            # Get normalized text
            normalized_text = Normalized_Integral.get("1.0", tk.END).strip()
            append_text = f"{normalized_text}"

            # Append normalized text to dictionary buffer keyed by datapoint_name
            if datapoint_name not in normalized_data_buffers:
                normalized_data_buffers[datapoint_name] = ""
            normalized_data_buffers[datapoint_name] += append_text

            # Prepare full text from all buffers concatenated
            full_text = "\n".join(normalized_data_buffers.values())

            # Update the n_df window content if open
            if ndf_result and ndf_result.winfo_exists():
                ndf_result.delete("1.0", tk.END)
                ndf_result.insert(tk.END, full_text)
            else:
                # Open n_df window and load full buffer content
                n_df()
                ndf_result.delete("1.0", tk.END)
                ndf_result.insert(tk.END, full_text)

        except Exception as e:
            print(f"Error updating filename: {e}")

    button_save = tk.Button(frame_buttons, text="Save", command=save)
    button_save.grid(row=2, column=0, sticky="s", pady=10)


#Frame for normalizing and saving settings
frame_button_choose =tk.Frame(frame_Info)
frame_button_choose.grid(row=2,column=0, sticky="w")
button_choose = tk.Button(frame_button_choose, text="Open Choose & Normalize Window", command=open_ChsANorm_Window)
button_choose.grid(row=0,column=0)


#Frame for Infomration Label: Variable Gradient and Isotope Information
frame_Gradient_Label =tk.Frame(frame_Info)
frame_Gradient_Label.grid(row=2, column=0)
Gradient_label = tk.Label(frame_Gradient_Label, text="Select a variable Gradient and Isotope")
Gradient_label.grid(row=0,column=0)


###############################
#   ADD DATA IN FIT SETTINGS
###############################



# Global variables to track rows and frames
dynamic_row_frames = []
datapoint_row_count = 1  # assuming fixed row 0 exists

def reindex_rows():
    global dynamic_row_frames

    for i, frame in enumerate(dynamic_row_frames, start=1):
        for widget in frame.grid_slaves(row=0, column=3):
            if isinstance(widget, tk.Label):
                widget.config(text=f"{i}. Datapoints: ")
                break

def add_datapoint_row(filename_text=""):
    global datapoint_row_count
    global dynamic_row_frames

    frame = tk.Frame(frame_Data_row)
    frame.grid(row=datapoint_row_count, column=0, sticky="w")

    def remove_row():
        frame.destroy()
        dynamic_row_frames.remove(frame)
        reindex_rows()
        global datapoint_row_count
        datapoint_row_count = len(dynamic_row_frames) + 1

    Button_checkmark_row = tk.Button(frame, text=u"\u2713")
    Button_checkmark_row.grid(row=0, column=0)

    Button_Cross_row = tk.Button(frame, text=u"\u2717")
    Button_Cross_row.grid(row=0, column=1)

    button_remove_row = tk.Button(frame, text=u"\u2013", command=remove_row)
    button_remove_row.grid(row=0, column=2)

    Label_Datapoint = tk.Label(frame, text=f"{datapoint_row_count}. Datapoints: ")
    Label_Datapoint.grid(row=0, column=3, columnspan=2)

    entry_filename = tk.Entry(frame, width=30)
    entry_filename.grid(row=0, column=5)
    entry_filename.insert(0, filename_text)

    Label_Label = tk.Label(frame, text="Label: ")
    Label_Label.grid(row=0, column=6)

    entry_label = tk.Entry(frame, width=10)
    entry_label.grid(row=0, column=7)

    Label_Color = tk.Label(frame, text="Color: ")
    Label_Color.grid(row=0, column=8)

    color_var = tk.StringVar(frame)
    color_var.set("black")
    Dropdown_color = tk.OptionMenu(frame, color_var, "black", "red")
    Dropdown_color.grid(row=0, column=9)

    Label_Symbol = tk.Label(frame, text="Symbol: ")
    Label_Symbol.grid(row=0, column=10)

    symbol_var = tk.StringVar(frame)
    symbol_var.set("ᨔ")
    Dropdown_symbol = tk.OptionMenu(frame, symbol_var, "ᨔ", "ᨖ", "为")
    Dropdown_symbol.grid(row=0, column=11)

    Analyzed_dataframe = tk.Button(frame, text="df",command=n_df)
    Analyzed_dataframe.grid(row=0, column=12)

    # Add the frame reference for later removal or management
    dynamic_row_frames.append(frame)

    datapoint_row_count += 1  # increment for next row



######################################
#   FITTING SETTINGS FRAME
######################################
# Necessary to be on top so add_data function can acces that.

frame_Fit_settings = tk.LabelFrame(root,text="Fit-Settings", padx=10, pady=10 )
frame_Fit_settings.grid(row=2, column=1, sticky="n")

frame_Data_row = tk.Frame(frame_Fit_settings)
frame_Data_row.grid(row=0, column=0, columnspan=9)

############################################
#   ORIGINAL BUTTONS IN FRAME _ DATA _ ROW
############################################

frame_0 = tk.Frame(frame_Data_row)
frame_0.grid(row=0, column=0, sticky="w", pady=2)

Button_checkmark = tk.Button(frame_0, text=u"\u2713")
Button_checkmark.grid(row=0, column=0)

Button_Cross = tk.Button(frame_0, text=u"\u2717")
Button_Cross.grid(row=0, column=1)

# Spacer to replace missing minus button, same column=2
Spacer = tk.Label(frame_0, text="    ").grid(row=0, column=2)  # Empty label for spacing - simply for cosmetic perfect alignment

Label_filename = tk.Label(frame_0, text="0. Datapoints: ")
Label_filename.grid(row=0, column=3, columnspan=2)

Entry_filename = tk.Entry(frame_0, width=30)
Entry_filename.grid(row=0, column=5)

Label_Legendlabel = tk.Label(frame_0, text="Label: ")
Label_Legendlabel.grid(row=0, column=6)

Entry_Label = tk.Entry(frame_0, width=10)
Entry_Label.grid(row=0, column=7)

Label_Color = tk.Label(frame_0, text="Color: ")
Label_Color.grid(row=0, column=8)

Color = tk.StringVar(frame_0)
Color.set("black")

color_selection = tk.OptionMenu(frame_0, Color, "black", "red")
color_selection.grid(row=0, column=9)

Label_Symbol = tk.Label(frame_0, text="Symbol: ")
Label_Symbol.grid(row=0, column=10)

Symbol = tk.StringVar(frame_0)
Symbol.set("ᨔ")

Symbol_selection = tk.OptionMenu(frame_0, Symbol, "ᨔ", "ᨖ", "为")
Symbol_selection.grid(row=0, column=11)

#Analyzed_dataframe button should open a window which simply shows the normalized dataframe, 
#which in turn will be used to create a fit using it. 



Analyzed_dataframe = tk.Button(frame_0, text="df",command=n_df).grid(row=0, column=12)


#################
# GEN FIT BUTTON   # Initiate Calculations and plots everything
#################

# Frame for Generate Fit button (left)
Frame_Generate_Fit_Button = tk.Frame(frame_Fit_settings)
Frame_Generate_Fit_Button.grid(row=1, column=0, padx=5, pady=5)
Button_gen_fit = tk.Button(Frame_Generate_Fit_Button, text="Generate Fit")  # Add command as needed
Button_gen_fit.grid(row=0, column=0)

# Frame for Add Data button (right)
Frame_Add_Data_Button = tk.Frame(frame_Fit_settings)
Frame_Add_Data_Button.grid(row=1, column=1, padx=5, pady=5)

#Radiobutton which decides if you proceed evaluation with just one dataset or multiple
dataset_count = tk.StringVar(value="one")
Button_One = tk.Radiobutton(Frame_Add_Data_Button, text="One", variable=dataset_count, value="one").grid(row=0,column=0)
button_multiple = tk.Radiobutton(Frame_Add_Data_Button, text="Multi", variable=dataset_count, value="Multiple").grid(row=0,column=1)


#################################################################################
#    DATAFRAME KLASSIFIZIERUNG
#
#   Bestimmt, ob Dataframe als var_p30 oder var_gpz6 weiter verarbeitet wird
#   Das ist abhängig von den dazu ausgesuchten Radiobuttons
#
#################################################################################




####################################
#   VARIABLE FUNCTIONALITIES
####################################

###############################
#   GPZ6 Increment Calculator
###############################

def compute_gpz6_increments():
    try:
        max_t = float(entry_Max_TpM.get())  # Max T/m absolute value
        max_percent = float(entry_Max_TpM_Percent.get()) / 100.0  # convert percent to fraction
        min_percent = float(entry_Min_TpM_Percent.get()) / 100.0
        increments = int(entry_Increments.get())

        # Calculate min and max absolute values
        max_val = max_t * max_percent
        min_val = max_t * min_percent

        # Generate equidistant increments
        gpz6_values = np.linspace(min_val, max_val, increments)

        # Format output as a comma-separated string (or space-separated)
        output_str = ", ".join(f"{v:.6f}" for v in gpz6_values)

        # Clear the output entry and insert new values
        entry_gpz6_var.delete(0, tk.END)
        entry_gpz6_var.insert(0, output_str)

        return gpz6_values

    except Exception as e:
        entry_gpz6_var.delete(0, tk.END)
        entry_gpz6_var.insert(0, f"Error: {e}")
        return None
#es ist kein problem output aus rechnungen auch in entry field hinzuzufügen. 

###################################
#       VAR P30 CONVERTER
###################################

def  p30_converter():
    try:
        entry_p30_input = entry_var_p30.get()
        str_values = [s.strip() for s in entry_p30_input.split(",")]
        float_values = [float(val) for val in str_values]

        unit = p30_selection.get()

        if unit == "μs":
            conversion_factor = 1e-6
        elif unit == "ms":
            conversion_factor = 1e-3
        elif unit == "s":
            conversion_factor = 1
        else:
            raise ValueError("Unknown unit selected") #Gibt es sowieso nicht, aber If funtkion muss so enden
        

        converted_p30 = [v * conversion_factor for v in float_values]
        output_str = ", ".join(f"{v:.6f}" for v in converted_p30)

        entry_var_p30.delete(0, tk.END)
        entry_var_p30.insert(0, output_str)

        return converted_p30

    except Exception as e:         
        entry_var_p30.delete(0, tk.END)
        entry_var_p30.insert(0, f"Error: {e}")
        return None

##################################
# VAR. ASSIGNMENT - BOTTOM RIGHT
##################################
######################################
# VARIBALE FRAME
######################################

#variable Assignment - Frame
frame_input = tk.LabelFrame(root, text="Variables", padx=10, pady=10)
frame_input.grid(row=3, column=1)

#Fixed Values - Frame 
frame_Fixed_Values = tk.Frame(frame_input,padx=10, pady=10)
frame_Fixed_Values.grid(row=0, column=0)

# Label and entry for p30 1H
label_p30_1H = tk.Label(frame_Fixed_Values, text=r"p30 1H [μS]")  # tkinter does not present LaTeX style greek letters
label_p30_1H.grid(row=1, column=0)
entry_p30_1H = tk.Entry(frame_Fixed_Values, width=5)  # CONVERT STRING INTO FLOAT
entry_p30_1H.grid(row=1, column=1)

# Label and entry for p30 19F (new, directly below 1H)
label_p30_19F = tk.Label(frame_Fixed_Values, text=r"p30 19F [μS]")
label_p30_19F.grid(row=2, column=0)
entry_p30_19F = tk.Entry(frame_Fixed_Values, width=5)  # CONVERT STRING INTO FLOAT
entry_p30_19F.grid(row=2, column=1)

# Label and entry for gpz6 1H
label_gpz6_1H = tk.Label(frame_Fixed_Values, text="gpz6 1H [%]")
label_gpz6_1H.grid(row=3, column=0)
entry_gpz6_1H = tk.Entry(frame_Fixed_Values, width=5)  # CONVERT STRING TO FLOAT
entry_gpz6_1H.grid(row=3, column=1)

# Label and entry for gpz6 19F (new, directly below 1H)
label_gpz6_19F = tk.Label(frame_Fixed_Values, text="gpz6 19F [%]")
label_gpz6_19F.grid(row=4, column=0)
entry_gpz6_19F = tk.Entry(frame_Fixed_Values, width=5)  # CONVERT STRING TO FLOAT
entry_gpz6_19F.grid(row=4, column=1)

# Label and entry for initial guess (keep the same)
label_initial_guess = tk.Label(frame_Fixed_Values, text="in. guess")
label_initial_guess.grid(row=5, column=0)
entry_initial_guess = tk.Entry(frame_Fixed_Values, width=5)  # CONVERT STRING INTO FLOAT - ALLOW 10^x == 10**9
entry_initial_guess.grid(row=5, column=1)
                      #Two ways of entering an exponent                          #Two ways of entering an exponent
                                                                    #implement info which shows how to enter what exactly












#SEPARATOR SHOULD SEPARATE FOLLOWING FRAMES FROM EACH OTHER:
# FRAME - LEFT = frame_Fixed_Values  | FRAME RIGHT = frame_Variable_Values
#Sticky"ns" is important to make it visible 

ttk.Separator(frame_input,orient="vertical").grid(column=1,row=0,rowspan=4, sticky="ns") 

#FRAME 2 - Variable p30 & gpz6
frame_Variable_Values = tk.Frame(frame_input, padx=10, pady=10)
frame_Variable_Values.grid(row=0, column=2)


#p30 Variable _ based on Radiobuttons which only allows one selection of these three

p30_selection = tk.StringVar(value="μs")

#Variable p30 Entry 
label_p30_var = tk.Label(frame_Variable_Values, text="Var. p30 increments: ")
label_p30_var.grid(row=0, column=0)

p30_microSeconds = tk.Radiobutton(frame_Variable_Values, text="μS", variable=p30_selection, value="μs")
p30_microSeconds.grid(row=0, column=1)

p30_milliSeconds= tk.Radiobutton(frame_Variable_Values, text="ms", variable=p30_selection, value="ms")
p30_milliSeconds.grid(row=0,column=2)

p30_Seconds = tk.Radiobutton(frame_Variable_Values, text="S", variable=p30_selection, value="s")
p30_Seconds.grid(row=0,column=3)

Button_Converter = tk.Button(frame_Variable_Values, text="convert into S", command= p30_converter)        
Button_Converter.grid(row=1, column=4)


#Entry Field - paste values into here
entry_var_p30 = tk.Entry(frame_Variable_Values, width=40)
entry_var_p30.grid(row=1, column=0, columnspan=4)



#label for gpz6 var
Label_gpz6_var = tk.Label(frame_Variable_Values, text="Var. gpz6 increments:")
Label_gpz6_var.grid(row=2, column=0)

entry_gpz6_var = tk.Entry(frame_Variable_Values, width=40)
entry_gpz6_var.grid(row=3, column=0, columnspan=4)

Label_entry_gpz6 =tk.Label(frame_Variable_Values, text="[T/m]")
Label_entry_gpz6.grid(row=3, column=4)

ttk.Separator(frame_input,orient="vertical").grid(column=3,row=0,rowspan=4, sticky="ns") 


#Frame 3 within Variable_frame. 
#This now contains Max T/m strength of the NMr device

frame_NMR_settings = tk.Frame(frame_input, padx=10, pady=10)
frame_NMR_settings.grid(row=0, column=4)

label_Max_TpM = tk.Label(frame_NMR_settings, text= "Max T/m")
label_Max_TpM.grid(row=0, column=0)

entry_Max_TpM = tk.Entry(frame_NMR_settings, width=10)
entry_Max_TpM.grid(row=0, column=1)

label_Max_TpM_Percent = tk.Label(frame_NMR_settings, text="Max [%]")
label_Max_TpM_Percent.grid(row=1, column=0)

entry_Max_TpM_Percent = tk.Entry(frame_NMR_settings, width=10)
entry_Max_TpM_Percent.grid(row=1, column=1) 

label_Min_TpM_Percent = tk.Label(frame_NMR_settings, text="Min [%]")
label_Min_TpM_Percent.grid(row=2, column=0)

entry_Min_TpM_Percent = tk.Entry(frame_NMR_settings, width=10)
entry_Min_TpM_Percent.grid(row=2, column=1)

Label_Increments = tk.Label(frame_NMR_settings, text="#Increments")
Label_Increments.grid(row=3, column=0)

entry_Increments = tk.Entry(frame_NMR_settings, width=10)
entry_Increments.grid(row=3, column=1)


Button_Compute_Increments = tk.Button(frame_NMR_settings, text="Compute",command=compute_gpz6_increments)
Button_Compute_Increments.grid(row=4, column=1)









#######################################
#       GRAPH & RESULTS
######################################


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
