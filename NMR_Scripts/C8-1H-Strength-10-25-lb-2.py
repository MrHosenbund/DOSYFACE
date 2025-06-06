
import numpy as np           # NumPy: Efficient numerical computations and array operations: np.array 
import pandas as pd          # Pandas: Data analysis and manipulation using DataFrames: Reading .csv Files
from io import StringIO      # StringIO: Allows string data to be used as file-like objects
import matplotlib.pyplot as plt  # Matplotlib: Plotting library for creating graphs and visualizations
from scipy.optimize import curve_fit  # SciPy: Function fitting and optimization tools
import os                   # OS module: Interact with the file system (paths, directories, environment)
import matplotlib.cm as cm 
import cmcrameri.cm as cmc

###################################
#
#          DEFINE FUNCTIONS
#
###################################



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
    #dataframe = dataframe.iloc[1:].reset_index(drop=True) #removes the first row as this one is empty and corrects index
    dataframe.index = range(len(dataframe))
    #dataframe = dataframe.replace("", np.nan).dropna(how='all') #removes completely empty rows

    return dataframe



def cov2corr(covalence_matrix):
    std_devs = np.sqrt(np.diag(covalence_matrix))
    correlation_matrix = covalence_matrix / np.outer(std_devs, std_devs)
    return std_devs





def stejskal_tanner(gradient_strength, D):              # Steijskal tanner equation (unabhängige Variable g_strength/ abhängige variable D)
    return np.exp(- y**2 * gradient_strength**2 * gradient_length**2 * D * ( t - gradient_length/3) * (2/np.pi)**2)


######################
#
#   Define Variables
#
######################

y = 2.67*10**8  #SI-unit: rad/s*T #gyromagnetic ratio C
gradient_length = (500/10**6)*2        # 1871.0000  us /// SI-unit: Sekunden / 10**6 In Sekunden - p30 Angabe in Mikrosekunden (usec)
t = 0.1  # SI-unit: In Sekunden: 100 ms 


#



#########################
#
#   IMPORT DATA
#
#########################


df_DOSY = import_data(r"C:\Users\bruno\Documents\Studium\MP_Kovermann\Processing\Global_Diff\Integrale-LB-2\C8-1H-G-10-25-LB-2") #absolute path to dataH
print(df_DOSY)   #check if import has worked properly 




############## STRENGTH 13C ###############


gradient_strength_percentage = np.array([0.05, 0.11, 0.17, 0.23, 0.29, 0.35, 0.41, 0.47, 0.53, 0.59, 0.65, 0.71, 0.77, 0.83, 0.89, 0.95])  # relative percentage (%)
gradient_strength = gradient_strength_percentage*0.593   # Percentages * 100 % T/m: SI-unit: T/m 

print("gradient strength shape:", np.shape(gradient_strength))


###############################
###############################
#
#         INITATE LOOPING
#
###############################
###############################


  #iloc = wir greifen auf bestimmte Teile im dataframe zu, : = alle Reihen, , = eine Spalten, 0 = Erste Spalte (Spalte 1)
#[:,0]1 Spalte nicht normieren ,[:,1] 2 Spalte muss normiert s

colors = cm.get_cmap('jet', 7)(np.linspace(0, 1, 7)) 

Fitted_Curve = ["H1 - 4.13"]


for i, col_name in enumerate(df_DOSY.columns[:7]):  
    color = colors[i]
    
    label_data = f"{Fitted_Curve[i]} (Data)"
    label_fit = f"{Fitted_Curve[i]}"


    df_peak1_DOSY = df_DOSY.iloc[:,i]
    df_peak1_DOSY = df_peak1_DOSY/df_peak1_DOSY.max()     # Normalize data from each column


    D_popt_13C_DOSY, D_pcov_13C_DOSY = curve_fit(stejskal_tanner, gradient_strength, df_peak1_DOSY, p0=10**-9) # fitting
    stdev_13C_DOSY = cov2corr(D_pcov_13C_DOSY)  # St. Deviation
    
    x_fit_13C_DOSY= np.linspace(min(gradient_strength), max(gradient_strength), 100)
    y_fit_13C_DOSY= stejskal_tanner(x_fit_13C_DOSY, D_popt_13C_DOSY)

     

    plt.scatter(gradient_strength, df_peak1_DOSY, marker= "s", color=color  ) #label=label_data
    plt.plot(x_fit_13C_DOSY, y_fit_13C_DOSY, color=color, label=label_fit )

    print({i} ,*D_popt_13C_DOSY, "+/-",*stdev_13C_DOSY)


# Fitting Plot
plt.title("C8 1H Lb 2 Fit")
plt.xlabel("Gradient Strength / [Tm⁻¹]")
plt.ylabel("Norm. Integral / [a.u.]")
plt.ylim(0,1.1)
plt.legend(title="Legend", loc="best", fontsize="x-large")

# ========================
# Residuals Plot
# ========================
plt.figure(figsize=(10, 5))
plt.axhline(0, color='black', linestyle='--', linewidth=1)

for i, col_name in enumerate(df_DOSY.columns[:7]):  
    color = colors[i]
    label_res = f"{Fitted_Curve[i]}"

    df_peak1_DOSY = df_DOSY.iloc[:,i]
    df_peak1_DOSY = df_peak1_DOSY / df_peak1_DOSY.max()

    D_popt_13C_DOSY, _ = curve_fit(stejskal_tanner, gradient_strength, df_peak1_DOSY, p0=10**-9)
    y_fit_data_points = stejskal_tanner(gradient_strength, D_popt_13C_DOSY)

    residuals = df_peak1_DOSY - y_fit_data_points

    plt.plot(gradient_strength, residuals, marker='o', linestyle='-', color=color, label=label_res)

plt.title("Residuals C8 1H Lb 2")
plt.xlabel("Gradient Strength / [Tm⁻¹]")
plt.ylabel("Residuals [a.u]")
plt.legend(title="Legend", loc="best", fontsize="medium")
plt.grid(True)
plt.tight_layout()
plt.show()

##############################
##############################
#
#       END LOOPING
#
##############################
##############################





