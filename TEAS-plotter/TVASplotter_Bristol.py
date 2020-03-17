# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:01:53 2020

@author: ll17354
"""

import pandas as pd, matplotlib.pyplot as plt, os 
import numpy as np

def create_data_frame(data_file_path,
                      data_file_name, 
                      plot_from, 
                      plot_upto,
                      line_rmver):
    """
    creates a dataframe containing the time points vs wavenumbers that need to be plotted 

    Parameters
    ----------
    data_file_path : string that contains the path to the csv file
    data_file_name : string that contains the name of the csv file as X.csv
    plot_from : string of the columns label you would like to plot from e.g. 0.000000
    plot_upto: string of the columns label you would like to plot to e.g. 1.000
    line_remver: an interger which which will emove every nth column

    Notes:
       line_rmver will remove every nth column high values mean less lines to be 
       plotted in your spectra.
       
       pandas will look for the file upwards from teh file space it is currently in.
       make sure to specify exactly upwards OR downwards where your spectral file is
       in relation to TVAS_plotter.py

    Returns
    -------
    df_new a dataframe 
    """
    df = pd.read_csv(os.path.join(data_file_path, data_file_name)) #reads csv file into a dataframe 
    wavenumber_series = df.loc[:,'0.000'] #saves the 1st column which contains wavenumbers 
    df_new = df.loc[:, plot_from:plot_upto] #segments the data function timepoints that you would like to plot
    df_new = df_new.iloc[:, ::line_rmver] #removes extra lines by removing every nth column n
    for column in df_new: #strips any trailing "0" or "." from the column names
        df_new.rename(columns = {column: column.rstrip("0")}, inplace = True) 
    for column in df_new:
        df_new.rename(columns = {column: column.rstrip(".")}, inplace = True)
    df_new.insert(loc=0, column='wavenumber', value=wavenumber_series) #insert the wavenumber column back into dataframe 
    return df_new

def create_TVAS_plot(x_lim_from,
                     x_lim_to,
                     y_lim_from,
                     y_lim_to,
                     df):
    """
    plots a TVAS spectrum

    Parameters
    ----------
    x_lim_from : integer for where to set your x limit from
    x_lim_to : integer for where to set your x limit to
    y_lim_from : integer for where to set your y limit from
    y_lim_to : integer for where to set your y limit to
    df : a data frame to be plotted

    Notes:
        dataframe must be in the format of index's = wavenumbers, columns = time points,
        and elements = signal intensities.

    Returns
    -------
    plotted TVAS figure 
    """
    plt.figure()
    n = len(df.columns)
    colors = plt.cm.viridis(np.linspace(0,1,n)) #choose the colour map needed
    i = 0
    for c in df.columns:
        i += 1
        if c != 'wavenumber': 
            plt.plot(df['wavenumber'], df[c], color=colors[i-1], lw = 3)
    plt.plot(df['wavenumber'], np.zeros(len(df['wavenumber'])), linestyle = ':', color = 'grey')
    plt.legend(df.columns[1:], title = 'Time / ps')
    plt.xlim(x_lim_from, x_lim_to)
    plt.ylim(y_lim_from, y_lim_to)
    plt.ylabel('Absorbance / mOD')
    plt.xlabel('Wavenumber / $\mathregular{cm^{-1}}$')
    plt.show()

data_file_path = r"C:\Users\ll17354\OneDrive - University of Bristol\MyFiles-Migrated\Documents\Scripts\TVAS data plotter"
data_file_name = "D_cych_p360nm_carbonyl_TONYS_TESTTVAS.csv"
plot_from = '0.500' #time point to plot from
plot_upto = '1000.000' #time point to plot to
line_rmver = 6 #how many lines you would like removed
x_lim_from = 1550 
x_lim_to = 1800
y_lim_from = -15
y_lim_to = 5
df = create_data_frame(data_file_path, data_file_name, plot_from, plot_upto, line_rmver)
create_TVAS_plot(x_lim_from, x_lim_to, y_lim_from, y_lim_to, df)



    
    
    