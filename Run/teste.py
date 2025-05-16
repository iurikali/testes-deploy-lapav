#Import packages necessary for analysis
import sys
import os
sys.path.append('..')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from Main.MDA_Huang import Layer3D

#For plotting and interactive features. You may disable/comment out if you just want to run the analysis for a few points in step 1
from Main.Interactive_Functions import fewpoints, plot_interactive_heatmap
from IPython.display import clear_output, display
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual

#The following are loaded in fewpoints and plot_interactive_heatmap
#from google.colab import files
#from scipy.interpolate import RegularGridInterpolator
#import plotly.graph_objects as go
#Function for converting everything to a dataset

for i in range(10):
    clear_output(wait=True)
    print("All good, move to the next step")

'''
#----------------------------------STEP 1------------------------------------
## INPUTS, PLEASE USE CONSISTENT UNITS, SAME AS WIINJULEA
## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY ################################
E = np.array([500, 50, 10])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
H = [6, 18]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
nu = [0.35, 0.4, 0.45]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
L = [9000,9000]                    # Load Magnitudes (lbs). In this case, there are 2 loads, both 9000 lbs
LPos = [(10,0),(20,0)]             # Load positions as (x,y) (inch). In this case, there are two loads, one is at 10,0, other is at 20,0
a = 4                              # Contact radius (inch)
x = [10,15,20]                     # x query points for (inch)
y = [0]                            # y query points (inch)
z =[5.99]                          # z (depth) query points (inch)
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


#DF = DataFrame
DF=fewpoints(x,y,z,RSO,download) #Save as a dataframe and then display

#---------------------------AQUI--------------------------------------
#Aqui teria que criar um buffer para fazer o download da Planilha
print(DF)

'''

#---------------------------STEP 2-----------------------------------------
## YOU CAN CHANGE THESE PARAMETERS IF NECESSARY################################
E = np.array([500, 50, 10])*1000   # Layer Modulus (psi), [Top Layer, Second to top layer,...,Subgrade]
H = [6, 18]                        # Layer Thicknesses (inch), [Top Layer, Second to top layer,...,nth layer]. Subgrade is not required and assumed semi-infinite
nu = [0.35, 0.4, 0.45]             # Poissons ratio, [Top Layer, Second to top layer,...,Subgrade]
L = [9000,9000]                    # Load Magnitudes (lbs)
LPos = [(10,0),(20,0)]             # Load positions as (x,y) (inch)
a = 4                              # Contact radius (inch)
x = np.arange(0,31,1)              # x query points for (inch). In this example, we are looking from 0 to 31
y = [0]                            # y query points (inch). In this example, not interested in y for now
z = np.arange(0,31,1)              # z (depth) query points (inch). In this example, Interested in depths from 0 to 31
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

'''
#-----------------------------STEP 3---------------------------------------------
# plot_interactive_heatmap('Title for Data', Data, 'Label for Data', x, z, H ,aspect=(15,8))
# for strains use eps_, for stress use sigma_, for displacement use displacement_
# For strain in x use eps_x, for y use eps_y, etc

#If results are nonsensical, please pass interpolate=False

##########First example
aspect=(10,8)
Resp='sigma_z' #Response to evaluate. You can change this response to anything
data = (RS[Resp][0, :, :]) #Do not change
##
#Do not change, other than label and interpolate
plot_interactive_heatmap(title=f'{Resp}',data=data,label='Stress (psi)', x=x, z=z, H=H, aspect=aspect,interpolate=True)

##########Second example
Resp='eps_z' #Response to evaluate. You can change this response to anything
data = (RS[Resp][0, :, :]) #Do not change
##
#Do not change, other than label and interpolate
plot_interactive_heatmap(title=f'{Resp}',data=data,label='Strain', x=x, z=z, H=H, aspect=aspect,interpolate=True)

##########Third example
Resp='eps_y' #Response to evaluate. You can change this response to anything
data = (RS[Resp][0, :, :]) #Do not change
##
#Do not change, other than label and interpolate
#plot_interactive_heatmap(title=f'{Resp}',data=data,label='Strain', x=x, z=z, H=H, aspect=aspect,interpolate=True)
'''
#-------------------------STEP 4---------------------------------
response='sigma_z' #default response. You can change it here, or below in the response box
idx=(np.abs(np.array(x) - LPos[0][0])).argmin() #index under the load by default. You can toggle it with the slider


#### DO NOT CHANGE BELOW THIS LINE#####
#@interact(xx=widgets.IntSlider(min=0, max=len(x)-1, step=1, value=idx), response=response)
def plotx(response=response,xx=0):
  response=response
  A=np.transpose(RS[response][0,:,:])
  idx=xx
  sns.scatterplot(x=A[:,idx],y=-z,s=70) #plot the idx x element from left
  plt.xlabel('response (response units)')
  plt.ylabel('z')
  plt.title(response+' at x='+str(x[idx]))
  plt.show()

plotx(xx= 14)