#Import packages necessary for analysis
import sys
import os
sys.path.append('..')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
from Main.MDA_Huang import Layer3D

#For plotting and interactive features. You may disable/comment out if you just want to run the analysis for a few points in step 1
from Main.Interactive_Functions import fewpoints, plot_interactive_heatmap
from IPython.display import clear_output, display
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual

import io
from xlsxwriter import Workbook
import zipfile

#The following are loaded in fewpoints and plot_interactive_heatmap
#from google.colab import files
#from scipy.interpolate import RegularGridInterpolator
#import plotly.graph_objects as go
#Function for converting everything to a dataset


#Tabela etapa 1
'''
def calcula(e_1, e_2, e_3, h_1, h_2, nu_1, nu_2, nu_3, l_1, l_2, lposx_1, lposy_1, lposx_2, lposy_2, a_1, x_1, x_2, x_3, y_1, z_1, z_2, z_3, xx, depth, h_3, h_4):
    for i in range(10):
        clear_output(wait=True)
        print("All good, move to the next step")

    ## INPUTS, PLEASE USE CONSISTENT UNITS, SAME AS WIINJULEA
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY ################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_1, h_2]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L = [l_1,l_2]                    # Load Magnitudes (lbs). In this case, there are 2 loads, both 9000 lbs
    LPos = [(lposx_1,lposy_1),(lposx_2,lposy_2)]             # Load positions as (x,y) (inch). In this case, there are two loads, one is at 10,0, other is at 20,0
    a = a_1                              # Contact radius (inch)
    x = [x_1,x_2,x_3]                     # x query points for (inch)
    y = [y_1]                            # y query points (inch)
    z =[z_1]                          # z (depth) query points (inch)
    download=False                     # download results as an excel file? [True or False]

    ################DO NOT CHANGE BELOW THIS LINE#############################

    ##### Layered elastic analysis settings. Do not change unless slow or unstable
    ZRO=7*1e-20                 # definition of zero to avoid division by zero
    isBD=np.ones(len(E))        # assumes fully bonded
    it = 1600                   # maximum number of iterations
    tolerance=0.01              # average percent error of query points
    every=10                    # check for convergence every x steps
    #######
    print('Running Elastic Analysis...')
    RSO=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,isBD,tolerance,verbose=True,every=every)
    print('Done')

    ## Save to a pandas dataset to display
    for i in range(10):
        clear_output(wait=True)

    DF=fewpoints(x,y,z,RSO,download) #Save as a dataframe and then display

    buffer = io.BytesIO()
    #DF.to_csv(buffer, index=False)
    # Write the DataFrame to the buffer in Excel format
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        DF.to_excel(writer, sheet_name='Sheet1', index=False)
    buffer.seek(0)

    output = [buffer, "tabela.xlsx"]
    return output
'''

#Graico etapa 4
'''
def calcula(e_1, e_2, e_3, h_1, h_2, nu_1, nu_2, nu_3, l_1, l_2, lposx_1, lposy_1, lposx_2, lposy_2, a_1, x_1, x_2, x_3, y_1, z_1, z_2, z_3, xx, depth, h_3, h_4):
    for i in range(10):
        clear_output(wait=True)
        print("All good, move to the next step")

    ## INPUTS, PLEASE USE CONSISTENT UNITS, SAME AS WIINJULEA
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY ################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_1, h_2]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L = [l_1,l_2]                    # Load Magnitudes (lbs). In this case, there are 2 loads, both 9000 lbs
    LPos = [(lposx_1,lposy_1),(lposx_2,lposy_2)]             # Load positions as (x,y) (inch). In this case, there are two loads, one is at 10,0, other is at 20,0
    a = a_1                              # Contact radius (inch)
    x = np.arange(x_1,x_2,x_3)                     # x query points for (inch)
    y = [y_1]                            # y query points (inch)
    z =np.arange(z_1, z_2, z_3)                          # z (depth) query points (inch)
    download=False                     # download results as an excel file? [True or False]

    ############################ DO NOT CHANGE BELOW THIS LINE#####################
    # Generate new z values just below and above each cumulative sum value
    cumulative_sums = np.cumsum(H)
    z = np.sort(np.concatenate((z, cumulative_sums - 0.01, cumulative_sums + 0.01)))
    ## Layered elastic analysis settings. Do not change unless slow or unstable
    ZRO=7*1e-20
    isBD=np.ones(len(E))
    it = 1600            # number of maximum iterations
    tolerance=0.01       # average percent error of query points
    every=100            # check for convergence every x steps
    print('Running Elastic Analysis...')
    RS=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,isBD,tolerance,verbose=True,every=every)
    print('Done')
    sns.set(rc={'figure.figsize':(20,10)},font_scale=1.15)

    plt.close()
    response='sigma_z' #default response. You can change it here, or below in the response box
    A=np.transpose(RS[response][0,:,:])
    idx=xx
    sns.scatterplot(x=A[:,idx],y=-z,s=70) #plot the idx x element from left
    plt.xlabel('response (response units)')
    plt.ylabel('z')
    plt.title(response+' at x='+str(x[idx]))
    
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    output = [buffer, "Sigma.png"]


    return output
'''

#STEP 5
'''
def calcula(e_1, e_2, e_3, h_1, h_2, nu_1, nu_2, nu_3, l_1, l_2, lposx_1, lposy_1, lposx_2, lposy_2, a_1, x_1, x_2, x_3, y_1, z_1, z_2, z_3, xx, depth, h_3, h_4):
    for i in range(10):
        clear_output(wait=True)
        print("All good, move to the next step")

    ## INPUTS, PLEASE USE CONSISTENT UNITS, SAME AS WIINJULEA
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY ################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_1, h_2]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L = [l_1,l_2]                    # Load Magnitudes (lbs). In this case, there are 2 loads, both 9000 lbs
    LPos = [(lposx_1,lposy_1),(lposx_2,lposy_2)]             # Load positions as (x,y) (inch). In this case, there are two loads, one is at 10,0, other is at 20,0
    a = a_1                              # Contact radius (inch)
    x = np.arange(x_1,x_2,x_3)                     # x query points for (inch)
    y = [y_1]                            # y query points (inch)
    z =np.arange(z_1, z_2, z_3)                          # z (depth) query points (inch)
    download=False                     # download results as an excel file? [True or False]

    ############################ DO NOT CHANGE BELOW THIS LINE#####################
    # Generate new z values just below and above each cumulative sum value
    cumulative_sums = np.cumsum(H)
    z = np.sort(np.concatenate((z, cumulative_sums - 0.01, cumulative_sums + 0.01)))
    ## Layered elastic analysis settings. Do not change unless slow or unstable
    ZRO=7*1e-20
    isBD=np.ones(len(E))
    it = 1600            # number of maximum iterations
    tolerance=0.01       # average percent error of query points
    every=100            # check for convergence every x steps
    print('Running Elastic Analysis...')
    RS=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,isBD,tolerance,verbose=True,every=every)
    print('Done')
    sns.set(rc={'figure.figsize':(20,10)},font_scale=1.15)


    plt.close()
    response='sigma_z' #default response. You can change it here, or below in the response box

    depthindex = depth
    #depthindex=6 #how deep do we want to go?
    A=np.transpose(RS[response][0,:,:])

    sns.scatterplot(y=A[depthindex,:],x=x,s=70) #plot the idx x element from left
    plt.xlabel('x')
    plt.ylabel('response (response units)')
    plt.title(response+' at z ='+str(z[depth]))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    output = [buffer, "Sigma_z.png"]

    return output
'''

#STEP 6 e 7
'''
def calcula(e_1, e_2, e_3, h_1, h_2, nu_1, nu_2, nu_3, l_1, l_2, lposx_1, lposy_1, lposx_2, lposy_2, a_1, x_1, x_2, x_3, y_1, z_1, z_2, z_3, xx, depth, h_3, h_4):
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_1, h_2]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L = [l_1,l_2]                    # Load Magnitudes (lbs)
    LPos = [(lposx_1,lposy_1),(lposx_2,lposy_2)]             # Load positions as (x,y) (inch)
    a = a_1                              # Contact radius (inch)
    x = np.arange(x_1,x_2,x_3)              # x query points for (inch). In this example, we are looking from 0 to 31
    y = [y_1]                            # y query points (inch). In this example, not interested in y for now
    z = np.arange(z_1,z_2,z_3)              # z (depth) query points (inch). In this example, Interested in depths from 0 to 31
    ###############################################################################

    ############################ DO NOT CHANGE BELOW THIS LINE#####################
    # Generate new z values just below and above each cumulative sum value
    cumulative_sums = np.cumsum(H)
    z = np.sort(np.concatenate((z, cumulative_sums - 0.01, cumulative_sums + 0.01)))
    ## Layered elastic analysis settings. Do not change unless slow or unstable
    ZRO=7*1e-20
    isBD=np.ones(len(E))
    it = 1600            # number of maximum iterations
    tolerance=0.01       # average percent error of query points
    every=100            # check for convergence every x steps
    print('Running Elastic Analysis...')
    RS=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,isBD,tolerance,verbose=True,every=every)
    print('Done')
    sns.set(rc={'figure.figsize':(20,10)},font_scale=1.15)

    idx=(np.abs(np.array(x) - LPos[0][0])).argmin() #index under the load by default. You can toggle it with the slider

    
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_3, h_4]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L=[l_1,l_2]                      # Load Magnitudes (lbs)
    LPos=[(lposx_1,lposy_1),(lposx_2,lposy_2)]               # Load positions as (x,y) (inch)
    a = a_1                              # Contact radius (inch)
    x = x                              # keep the same with the previous structrue! x query points for (inch)
    y = y                              # keep the same with the previous structrue! y query points (inch)
    z = z                              # keep the same with the previous structrue! z (depth) query points (inch)
    ###############################################################################
    
    print('Running Elastic Analysis...')
    RS2=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,np.ones(len(E)),tolerance,verbose=True) #This is the second structure to compare
    print('Done')

    response='sigma_z' #default response. You can change it here.


    ### By default, this plots response with respect to depth. You can modify it to do anything else##
    A=np.transpose(RS[response][0,:,:]) #Get the response from first structure
    B=np.transpose(RS2[response][0,:,:]) #Get the response from second structure

    idxA = (np.abs(np.array(x) - LPos[0][0])).argmin() #index under the load for first structrue
    idxB = (np.abs(np.array(x) - LPos[0][0])).argmin() #index under the load for second structrue
    sns.scatterplot(x=A[:,idxA],y=-z,s=70,label='Baseline') #plot the first structure
    sns.scatterplot(x=B[:,idxB],y=-z,s=70,label='New') #plot the second structure
    plt.xlabel('response (response units)')
    plt.ylabel('z')
    plt.title(response+' at x='+str(x[idx]))
    plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    output = [buffer, "Sigma_z.png"]
    return output
'''

'''
def calcula(e_1, e_2, e_3, h_1, h_2, nu_1, nu_2, nu_3, l_1, l_2, lposx_1, lposy_1, lposx_2, lposy_2, a_1, x_1, x_2, x_3, y_1, z_1, z_2, z_3, xx, depth, h_3, h_4):
    for i in range(10):
        clear_output(wait=True)
        print("All good, move to the next step")

    ## INPUTS, PLEASE USE CONSISTENT UNITS, SAME AS WIINJULEA
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY ################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_1, h_2]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L = [l_1,l_2]                    # Load Magnitudes (lbs). In this case, there are 2 loads, both 9000 lbs
    LPos = [(lposx_1,lposy_1),(lposx_2,lposy_2)]             # Load positions as (x,y) (inch). In this case, there are two loads, one is at 10,0, other is at 20,0
    a = a_1                              # Contact radius (inch)
    x = np.arange(x_1,x_2,x_3)                     # x query points for (inch)
    y = [y_1]                            # y query points (inch)
    z =np.arange(z_1, z_2, z_3)                          # z (depth) query points (inch)
    download=False                     # download results as an excel file? [True or False]

    ############################ DO NOT CHANGE BELOW THIS LINE#####################
    # Generate new z values just below and above each cumulative sum value
    cumulative_sums = np.cumsum(H)
    z = np.sort(np.concatenate((z, cumulative_sums - 0.01, cumulative_sums + 0.01)))
    ## Layered elastic analysis settings. Do not change unless slow or unstable
    ZRO=7*1e-20
    isBD=np.ones(len(E))
    it = 1600            # number of maximum iterations
    tolerance=0.01       # average percent error of query points
    every=100            # check for convergence every x steps
    print('Running Elastic Analysis...')
    RS=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,isBD,tolerance,verbose=True,every=every)
    print('Done')
    sns.set(rc={'figure.figsize':(20,10)},font_scale=1.15)

    ##########First example
    aspect=(10,8)
    Resp='sigma_z' #Response to evaluate. You can change this response to anything
    data = (RS[Resp][0, :, :]) #Do not change
    ##
    #Do not change, other than label and interpolate
    html1 = plot_interactive_heatmap(title=f'{Resp}',data=data,label='Stress (psi)', x=x, z=z, H=H, aspect=aspect,interpolate=True)


    ##########Second example
    Resp='eps_z' #Response to evaluate. You can change this response to anything
    data = (RS[Resp][0, :, :]) #Do not change
    ##
    #Do not change, other than label and interpolate
    html2 = plot_interactive_heatmap(title=f'{Resp}',data=data,label='Strain', x=x, z=z, H=H, aspect=aspect,interpolate=True)

    ##########Third example
    Resp='eps_y' #Response to evaluate. You can change this response to anything
    data = (RS[Resp][0, :, :]) #Do not change
    ##
    #Do not change, other than label and interpolate
    html3 = plot_interactive_heatmap(title=f'{Resp}',data=data,label='Strain', x=x, z=z, H=H, aspect=aspect,interpolate=True)

    # Criar o buffer ZIP em memória
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Adiciona os arquivos HTML ao ZIP (precisa converter para bytes)
        zip_file.writestr("heat1.html", html1.getvalue())
        zip_file.writestr("heat2.html", html2.getvalue())
        zip_file.writestr("heat3.html", html3.getvalue())
    zip_buffer.seek(0)

    return [zip_buffer, "heats.zip"]

'''


#TUDO JUNTO E MISTURADO
def calcula(e_1, e_2, e_3, h_1, h_2, nu_1, nu_2, nu_3, l_1, l_2, lposx_1, lposy_1, lposx_2, lposy_2, a_1, x_1_1, x_2_1, x_3_1, y_1, z_1_1, x_1, x_2, x_3, z_1, z_2, z_3, xx, depth, h_3, h_4):
    for i in range(10):
        clear_output(wait=True)
        print("All good, move to the next step")

    ## INPUTS, PLEASE USE CONSISTENT UNITS, SAME AS WIINJULEA
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY ################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_1, h_2]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L = [l_1,l_2]                    # Load Magnitudes (lbs). In this case, there are 2 loads, both 9000 lbs
    LPos = [(lposx_1,lposy_1),(lposx_2,lposy_2)]             # Load positions as (x,y) (inch). In this case, there are two loads, one is at 10,0, other is at 20,0
    a = a_1                              # Contact radius (inch)
    x = [x_1_1,x_2_1,x_3_1]                     # x query points for (inch)
    y = [y_1]                            # y query points (inch)
    z =[z_1_1]                          # z (depth) query points (inch)
    download=False                     # download results as an excel file? [True or False]

    ################DO NOT CHANGE BELOW THIS LINE#############################

    ##### Layered elastic analysis settings. Do not change unless slow or unstable
    ZRO=7*1e-20                 # definition of zero to avoid division by zero
    isBD=np.ones(len(E))        # assumes fully bonded
    it = 1600                   # maximum number of iterations
    tolerance=0.01              # average percent error of query points
    every=10                    # check for convergence every x steps
    #######
    print('Running Elastic Analysis...')
    RSO=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,isBD,tolerance,verbose=True,every=every)
    print('Done')

    ## Save to a pandas dataset to display
    for i in range(10):
        clear_output(wait=True)

    DF=fewpoints(x,y,z,RSO,download) #Save as a dataframe and then display

    buffer_ex = io.BytesIO()
    # Write the DataFrame to the buffer in Excel format
    with pd.ExcelWriter(buffer_ex, engine='xlsxwriter') as writer:
        DF.to_excel(writer, sheet_name='Sheet1', index=False)


    ## INPUTS, PLEASE USE CONSISTENT UNITS, SAME AS WIINJULEA
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY ################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_1, h_2]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L = [l_1,l_2]                    # Load Magnitudes (lbs). In this case, there are 2 loads, both 9000 lbs
    LPos = [(lposx_1,lposy_1),(lposx_2,lposy_2)]             # Load positions as (x,y) (inch). In this case, there are two loads, one is at 10,0, other is at 20,0
    a = a_1                              # Contact radius (inch)
    x = np.arange(x_1,x_2,x_3)                     # x query points for (inch)
    y = [y_1]                            # y query points (inch)
    z =np.arange(z_1, z_2, z_3)                          # z (depth) query points (inch)

    ############################ DO NOT CHANGE BELOW THIS LINE#####################
    # Generate new z values just below and above each cumulative sum value
    cumulative_sums = np.cumsum(H)
    z = np.sort(np.concatenate((z, cumulative_sums - 0.01, cumulative_sums + 0.01)))
    ## Layered elastic analysis settings. Do not change unless slow or unstable
    ZRO=7*1e-20
    isBD=np.ones(len(E))
    it = 1600            # number of maximum iterations
    tolerance=0.01       # average percent error of query points
    every=100            # check for convergence every x steps
    print('Running Elastic Analysis...')
    RS=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,isBD,tolerance,verbose=True,every=every)
    print('Done')
    sns.set(rc={'figure.figsize':(20,10)},font_scale=1.15)

    ##########First example
    aspect=(10,8)
    Resp='sigma_z' #Response to evaluate. You can change this response to anything
    data = (RS[Resp][0, :, :]) #Do not change
    ##
    #Do not change, other than label and interpolate
    html1 = plot_interactive_heatmap(title=f'{Resp}',data=data,label='Stress (psi)', x=x, z=z, H=H, aspect=aspect,interpolate=True)


    ##########Second example
    Resp='eps_z' #Response to evaluate. You can change this response to anything
    data = (RS[Resp][0, :, :]) #Do not change
    ##
    #Do not change, other than label and interpolate
    html2 = plot_interactive_heatmap(title=f'{Resp}',data=data,label='Strain', x=x, z=z, H=H, aspect=aspect,interpolate=True)

    ##########Third example
    Resp='eps_y' #Response to evaluate. You can change this response to anything
    data = (RS[Resp][0, :, :]) #Do not change
    ##
    #Do not change, other than label and interpolate
    html3 = plot_interactive_heatmap(title=f'{Resp}',data=data,label='Strain', x=x, z=z, H=H, aspect=aspect,interpolate=True)

    plt.close()
    response='sigma_z' #default response. You can change it here, or below in the response box
    A=np.transpose(RS[response][0,:,:])
    idx=xx
    sns.scatterplot(x=A[:,idx],y=-z,s=70) #plot the idx x element from left
    plt.xlabel('response (response units)')
    plt.ylabel('z')
    plt.title(response+' at x='+str(x[idx]))
    
    
    buffer_4 = io.BytesIO()
    plt.savefig(buffer_4, format='png')

    plt.close()
    response='sigma_z' #default response. You can change it here, or below in the response box

    depthindex = depth
    #depthindex=6 #how deep do we want to go?
    A=np.transpose(RS[response][0,:,:])

    sns.scatterplot(y=A[depthindex,:],x=x,s=70) #plot the idx x element from left
    plt.xlabel('x')
    plt.ylabel('response (response units)')
    plt.title(response+' at z ='+str(z[depth]))

    buffer_5 = io.BytesIO()
    plt.savefig(buffer_5, format='png')

    plt.close()
    idx=(np.abs(np.array(x) - LPos[0][0])).argmin() #index under the load by default. You can toggle it with the slider

    
    ## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY################################
    E = np.array([e_1, e_2, e_3])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
    H = [h_3, h_4]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
    nu = [nu_1, nu_2, nu_3]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
    L=[l_1,l_2]                      # Load Magnitudes (lbs)
    LPos=[(lposx_1,lposy_1),(lposx_2,lposy_2)]               # Load positions as (x,y) (inch)
    a = a_1                              # Contact radius (inch)
    x = x                              # keep the same with the previous structrue! x query points for (inch)
    y = y                              # keep the same with the previous structrue! y query points (inch)
    z = z                              # keep the same with the previous structrue! z (depth) query points (inch)
    ###############################################################################
    
    print('Running Elastic Analysis...')
    RS2=Layer3D(L,LPos,a,x,y,z,H,E,nu,it,ZRO,np.ones(len(E)),tolerance,verbose=True) #This is the second structure to compare
    print('Done')

    response='sigma_z' #default response. You can change it here.


    ### By default, this plots response with respect to depth. You can modify it to do anything else##
    A=np.transpose(RS[response][0,:,:]) #Get the response from first structure
    B=np.transpose(RS2[response][0,:,:]) #Get the response from second structure

    idxA = (np.abs(np.array(x) - LPos[0][0])).argmin() #index under the load for first structrue
    idxB = (np.abs(np.array(x) - LPos[0][0])).argmin() #index under the load for second structrue
    sns.scatterplot(x=A[:,idxA],y=-z,s=70,label='Baseline') #plot the first structure
    sns.scatterplot(x=B[:,idxB],y=-z,s=70,label='New') #plot the second structure
    plt.xlabel('response (response units)')
    plt.ylabel('z')
    plt.title(response+' at x='+str(x[idx]))
    plt.legend()

    buffer_7 = io.BytesIO()
    plt.savefig(buffer_7, format='png')

    # Criar o buffer ZIP em memória
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Adiciona os arquivos HTML ao ZIP (precisa converter para bytes)
        zip_file.writestr("tabela.xlsx", buffer_ex.getvalue())

        zip_file.writestr("heat_1.html", html1.getvalue())
        zip_file.writestr("heat_2.html", html2.getvalue())
        zip_file.writestr("heat_3.html", html3.getvalue())

        zip_file.writestr("step_4.png", buffer_4.getvalue())

        zip_file.writestr("step_5.png", buffer_5.getvalue())

        zip_file.writestr("step_7.png", buffer_7.getvalue())
    zip_buffer.seek(0)

    return [zip_buffer, "output.zip"]