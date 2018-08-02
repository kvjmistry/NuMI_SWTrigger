"""
Function that plots the NuMI SWTrigger Data

"""


import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['axes.linewidth'] = 1.5 # Sets the boarder width 
plt.rcParams.update({'errorbar.capsize': 1})

xlen = 12

# load NuMI data from csv file
NuMI_Data = np.loadtxt(open("NuMI.csv", "r"), delimiter=",")

NuMI_Tresh = NuMI_Data[:,0]; 
NuMI_Eff = NuMI_Data[:,1] # colon = "all of"
NuMI_Eff_Upper= NuMI_Data[:,2]
NuMI_Eff_Lower= NuMI_Data[:,3]

NuMI_Err = [NuMI_Eff - NuMI_Eff_Lower , NuMI_Eff_Upper - NuMI_Eff]


# load EXT data from csv file
EXT_Data = np.loadtxt(open("EXT.csv", "r"), delimiter=",")

EXT_Tresh = EXT_Data[:,0]
EXT_Eff = EXT_Data[:,1] # colon = "all of"
EXT_Eff_Upper= EXT_Data[:,2]
EXT_Eff_Lower= EXT_Data[:,3]

EXT_Err = [EXT_Eff - EXT_Eff_Lower , EXT_Eff_Upper - EXT_Eff]



fig = plt.figure()
frame1=fig.add_axes((.1,.3,.8,.6))
plt.errorbar(NuMI_Tresh/20, NuMI_Eff, yerr=NuMI_Err, fmt='ro-',  markersize=2, label = "NuMI", lw = 0.3)
plt.xlabel('Threshold', fontweight = "bold")
plt.ylabel('PMT Trigger Firing Fraction ', fontweight = "bold")
plt.axhline(y=0.14, color='k', linestyle='--', label = "Original Firing Fraction")
plt.errorbar(EXT_Tresh/20, EXT_Eff, yerr=EXT_Err, fmt='bo-',  markersize=2, label = "EXT",lw=0.3)
plt.yticks(fontweight = "bold")

#plt.xlim(0,xlen);

plt.legend()
plt.grid()


#Residual plot
#Propagate the errors for ratio plot
sigma_Ratio_lower = np.sqrt( (NuMI_Err[0]/EXT_Eff)**2 +  ( (NuMI_Eff * EXT_Err[0])/(EXT_Eff**2) )**2  )
sigma_Ratio_upper = np.sqrt( (NuMI_Err[1]/EXT_Eff)**2 +  ( (NuMI_Eff * EXT_Err[1])/(EXT_Eff**2) )**2  )
Ratio_Err = [sigma_Ratio_lower, sigma_Ratio_upper  ]


sigma_Diff_lower = np.sqrt( (NuMI_Err[0])**2 +  ( EXT_Err[0] )**2  )
sigma_Diff_upper = np.sqrt( NuMI_Err[1]**2 +   EXT_Err[1]**2  )
Diff_Err = [sigma_Diff_lower, sigma_Diff_upper  ]


Ratio = NuMI_Eff / EXT_Eff
Difference = NuMI_Eff - EXT_Eff

frame2=fig.add_axes((.1,.1,.8,.2)) #(moves left,)       

# Choose whether to plot the difference or the ratio
#plt.plot(NuMI_Tresh/20, Ratio ,'og',  markersize=2)
#plt.ylabel('Ratio', fontweight = "bold") 

plt.plot(NuMI_Tresh/20, Difference ,'og',  markersize=2)
#plt.errorbar(NuMI_Tresh/20, Difference ,yerr = Diff_Err,fmt='og',  markersize=2)
plt.ylabel('Diff', fontweight = "bold") 
plt.ylim(-0.01,0.03);

plt.xlabel('Effective PE Threshold [ADC/20]', fontweight = "bold")
plt.xticks(fontweight = "bold")
plt.yticks(fontweight = "bold")

plt.axhline(y=1, color='m', linestyle='--')
plt.grid()





fig.savefig("SWTrigger.png", dpi=500)