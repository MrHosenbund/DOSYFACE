
import numpy as np                          # NumPy: Efficient numerical computations and array operations: np.array 
import pandas as pd                         # Pandas: Data analysis and manipulation using DataFrames: Reading .csv Files
from io import StringIO                     # StringIO: Allows string data to be used as file-like objects
import matplotlib.pyplot as plt             # Matplotlib: Plotting library for creating graphs and visualizations
from scipy.optimize import curve_fit        # SciPy: Function fitting and optimization tools
import os                                   # OS module: Interact with the file system (paths, directories, environment)
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





def stejskal_tanner(gradient_length, D):              # Steijskal tanner equation (unabhängige Variable g_strength/ abhängige variable D)
    return np.exp(- y_gyro**2 * gradient_strength**2 * gradient_length**2 * D * ( t - gradient_length/3) * (2/np.pi)**2)


######################
#
#   Define Variables
#
######################

#Konstanten

y_gyro = 2.51*10**8 #SI-unit: rad/s*T #gyromagnetic ratio C
gradient_strength = 0.128*0.593       #  us /// SI-unit: Sekunden / 10**6 In Sekunden - p30 Angabe in Mikrosekunden (usec)
t = 0.1  # SI-unit: In Sekunden: 100 ms 
sample_name = "C3_19F_Global_Length_DOSY_14.05_Fit"








#########################
#
#   IMPORT DATA
#
#########################


df_DOSY = import_data(r"C:\Users\bruno\Documents\Studium\MP_Kovermann\Processing\Global_Diff\Integrale-LB-var\C3_19F_global_G_Length_DOSY-150-165") #absolute path to dataH
print("data shape", np.shape(df_DOSY))   #check if import has worked properly 


gradient_length_us= np.array([195.35, 429.77, 664.19, 898.60, 1133.02, 1367.44, 1601.86, 1830.26,2070.70, 2305.12, 2539.53, 2773.95, 3008.37, 3242.79, 3477.21, 3711.63])  # relative percentage (%)
gradient_length = (gradient_length_us/1000000) * 2   #Convert Microseconds to Seconds // *2, da 2 Pulse notwendig sind. Wieso das aber?


print("gradient strength shape:", np.shape(gradient_length))


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

Fitted_Curve = ["-82.97", "-122.11"  ] # Fit Legend Beschriftung

fig, ax =plt.subplots()  #Figure mit als subplot kategorisiert

results = []   #Liste mit REsults


for i, col_name in enumerate(df_DOSY.columns[:7]):  
    color = colors[i]
    
    label_data = f"{Fitted_Curve[i]} (Data)"
    label_fit = f"{Fitted_Curve[i]}"


    df_peak1_DOSY = df_DOSY.iloc[:,i]
    df_peak1_DOSY = df_peak1_DOSY/df_peak1_DOSY.max()     # Normalize data from each column


    D_popt_DOSY, D_pcov_DOSY = curve_fit(stejskal_tanner, gradient_length, df_peak1_DOSY, p0=10**-9) # fitting
    stdev_DOSY = cov2corr(D_pcov_DOSY)  # St. Deviation
    
    x_fit_DOSY= np.linspace(min(gradient_length), max(gradient_length), 100)
    y_fit_DOSY= stejskal_tanner(x_fit_DOSY, D_popt_DOSY)

    results.append({
        "Column": col_name,
        "Diffusion Coefficient": D_popt_DOSY,
        "Uncertainty": stdev_DOSY
    }) 

    ax.scatter(gradient_length, df_peak1_DOSY, marker= "s", color=color, label=f"{Fitted_Curve[i]}") #label=label_data
    ax.plot(x_fit_DOSY, y_fit_DOSY, color=color ) # label=f"{Fitted_Curve[i]} (Fit)"

    print({i} ,*D_popt_DOSY, "+/-",*stdev_DOSY)
    
print("this is your results::", results)
# Ensure the figure is fully drawn before saving
#fig.canvas.draw()

ax.set_title(sample_name)
ax.set_xlabel("Gradient Length / s")
ax.set_ylabel("Norm. Integral / a.u.")
ax.set_ylim(0, 1.1)
ax.legend(loc="best", fontsize="medium")


# Define the save path # ADJUST SAVING FILE
save_dir = "Global_Diff/results/C3"
name = sample_name  # Use the sample name as the base for filenames

# Save fit results as a text file
results_file = f"{save_dir}/{name}_fit_results.txt"
with open(results_file, "w") as f:
    f.write("Column\tDiffusion Coefficient\tUncertainty\n")
    for result in results:
        f.write(f"{result['Column']}\t{result['Diffusion Coefficient']}\t{result['Uncertainty']}\n")

# Save the plot using the figure handle
plot_file = f"{save_dir}/{name}_fitted_plot.png"
fig.savefig(plot_file, dpi=300, bbox_inches='tight')

# Close the figure to free memory
plt.show()







# ========================
# Residuals Plot
# ========================


fig_res, ax =plt.subplots() 

for i, col_name in enumerate(df_DOSY.columns[:7]):  
    color = colors[i]
    label_res = f"{Fitted_Curve[i]}"

    df_peak1_DOSY = df_DOSY.iloc[:,i]
    df_peak1_DOSY = df_peak1_DOSY / df_peak1_DOSY.max()

    D_popt_DOSY, _ = curve_fit(stejskal_tanner, gradient_length, df_peak1_DOSY, p0=10**-9)
    y_fit_data_points = stejskal_tanner(gradient_length, D_popt_DOSY)

    residuals = df_peak1_DOSY - y_fit_data_points

    ax.plot(gradient_length, residuals, marker='o', linestyle='-', color=color, label=f"{Fitted_Curve[i]}")


ax.set_title(sample_name)
ax.set_xlabel("Gradient Length / s")
ax.set_ylabel("Norm. Integral / a.u.")
ax.legend(loc="best", fontsize="x-large")

# Save the plot using the figure handle
plot_file = f"{save_dir}/{name}_residual_plot.png"
fig_res.savefig(plot_file, dpi=300, bbox_inches='tight')



plt.show()

##############################
##############################
#
#       END LOOPING
#
##############################
##############################





