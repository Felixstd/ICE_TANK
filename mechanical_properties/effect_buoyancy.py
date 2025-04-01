import numpy as np
import IceMechProperties as me
import matplotlib.pyplot as plt
import scienceplots 

plt.style.use('science')


h_beams = np.linspace(0.01,0.5, 5)
h_beams = np.array([0.01, 0.1, 0.2, 0.5])
# print(h_beams)
L_beams = 5*h_beams
b_beams = h_beams*3
rhow = 998
g = 9.80

Force = 50

x_lengths = np.array([np.linspace(0, l, 100) for l in L_beams])


Elastic_modulus = np.linspace(1, 10, 1000)*1e9

ratios_E = []
lambda_E = []


for i, l in enumerate(L_beams):
    
    b = b_beams[i]
    h = h_beams[i]
    
    ratios_sigma = np.zeros_like(Elastic_modulus)
    lamdas       = np.zeros_like(Elastic_modulus)
    
    for j, E in enumerate(Elastic_modulus):
    
    
        I_moment = (b*h**3)/12

        lamdas[j] = (E*I_moment/(rhow*g*b))**(1/4)  
        
        
        sigmaf_buoyancy = me.sigmaf_buoyancyCanti(Force, \
                    l, b, h, E)
        sigmaf_classic = me.cantilever(Force, \
                    l, b, h, 0, 0, False)
        
        
        ratios_sigma[j] = (sigmaf_buoyancy-sigmaf_classic)/sigmaf_classic
        
    lambda_E.append(lamdas)
    ratios_E.append(ratios_sigma)
    
xkcd_pastel_colors = [
"xkcd:light blue",
"xkcd:teal",
"xkcd:orange",
# "xkcd:pastel yellow",
"xkcd:pastel pink",
"xkcd:pastel purple",
"xkcd:pastel orange",
"xkcd:pastel cyan"
]
    
plt.figure()
ax = plt.axes()

for i in range(len(lambda_E)):# label = 'E = {} GPa'.format(Elastic_modulus[i]/1e9))
    if h_beams[i]*L_beams[i]*b_beams[i] < 0.01:
        plt.plot(Elastic_modulus/1e9, ratios_E[i], label = '$V = {}$ (m$^3$)'.format(h_beams[i]*L_beams[i]*b_beams[i]))
    else:
        plt.plot(Elastic_modulus/1e9, ratios_E[i],label = '$V = {0:.2f}$ (m$^3$)'.format(h_beams[i]*L_beams[i]*b_beams[i]))
plt.grid()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.ylabel(r'$\frac{\sigma^C - \sigma^B}{\sigma^{\text{C}}}$')
plt.xlabel(r'$E$ (GPa)')
plt.savefig('sigmaf.png')

plt.figure()
