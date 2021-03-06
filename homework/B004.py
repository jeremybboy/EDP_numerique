#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Homework B004
Numerical methods for non-stationary Partial Differential Equations (PDEs):
Finite Differences and Finite Volumes

Mathematics and Modeling
Master of Mathematics and Applications

@author: Andre ALMEIDA ROCHA (3701739)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import random

def main():    
    points = [10, 20, 40, 80, 160, 320]
    
    errors = []
    
    for NX in points:
        norme = difference_finites(NX+1)
        errors.append(norme)

    print(errors)

    lix = [1/x for x in points]
    
    plt.figure(0)
    plt.plot(points, lix)
    plt.plot(points, errors, "r")
    
    
    plt.figure(1)
    plt.loglog(points, lix)
    plt.loglog(points, errors, "r")
    
    plt.show()
        
    
def difference_finites(NX):    
    """
    Finite differences method
    NX = 101  #nombre de points de grille
    """    
    # PARAMETRES PHYSIQUES    
    Lx = 1.0  #taille du domaine    
    T = 0.4 #temps d'integration
    
    print("T final=",T)    
    
    # PARAMETRES NUMERIQUES
    #NX = 11  #nombre de points de grille
    dx = Lx/(NX-1) #pas de grille (espace)
    CFL = 0.375    
    dt = CFL * dx    #pas de grille (temps)    
    NT = int(T/dt)  #nombre de pas de temps
    
    print("Nombre pas de espace= ",NX)
    print("Nombre pas de temps= ",NT)
    print("dt= ",dt)
    
    # PARAMETRES FONCTION INITIAL
    alpha = 1
    beta = 1
    
    
    # Pour la figure
    xx = np.zeros(NX)
    for i in np.arange(0,NX):
          xx[i] = i*dx
    
    #Initialisation
    ddU   = np.zeros(NX)
    U_old =  np.zeros(NX)    
    U_new =  np.zeros(NX)
    
    # Solution exacte
    U_sol =  np.zeros(NX)
    
    # Condition initial    
    U_data = np.zeros(NX)
    U_data = alpha * np.sin(2*np.pi*xx) + beta * np.cos(2*np.pi*xx)
    
    for i in np.arange(0, NX):
        U_old[i] = U_data[i]
   
    U_new = np.zeros(NX)
     
    plt.figure(-1)
    plt.plot(xx,U_old)
    plt.legend(("t=0."), 'best')
    plt.xlabel('x')
    plt.ylabel('u')
     
    # Boucle en temps  
    random.seed()
    
    
    time=0.
    for n in np.arange(0, NT):
        
        time=time+dt    
        if (n%100 == 0):
            print ("t=",time)            

        for j in np.arange(0, NX):            
            U_sol[j] = np.exp(-time) * (alpha * np.sin(2*np.pi*xx[j]) + beta * np.cos(2*np.pi*xx[j]))            
            
        
               
        # schemas explicites 
        for j in np.arange(2, NX-2):
            ddU[j] = -4/3*(U_old[j+1] - 2*U_old[j] + U_old[j-1]) + 1/12*(U_old[j+2] - 2*U_old[j] + U_old[j-2]) - 0.5*CFL*(U_old[j+2] - 4*U_old[j+1] + 6*U_old[j] - 4*U_old[j-1] + U_old[j-2])
            
        ddU[1] = -4/3 * (U_old[2] - 2 * U_old[1] + U_old[0]) + 1/12 * (U_old[3] - 2 * U_old[1] + U_old[NX-1]) - 0.5*CFL*(U_old[3] - 4*U_old[2] + 6*U_old[1] - 4*U_old[0] + U_old[NX-1])
        ddU[0] = -4/3 * (U_old[1] - 2 * U_old[0] + U_old[NX-1]) + 1/12 * (U_old[2] - 2 * U_old[0] + U_old[NX-2]) - 0.5*CFL*(U_old[2] - 4 * U_old[1] + 6 * U_old[0] - 4 * U_old[NX-1] + U_old[NX-2])
        

        # Actualisation schemas explicites
        for j in np.arange(0, NX-2):
            U_new[j] = U_old[j] - CFL * ddU[j]

        # Actualisation pour la 1-periodicite
        U_new[NX-1] = U_new[0]
        U_new[NX-2] = U_new[1]

        # Actualisation en temps
        for j in np.arange(0, NX-1):
            U_old[j] = U_new[j]
    
    print ("tFinal=", time)
    
    # caclul erreur numerique
    norme = 0.
    for j in np.arange(0, NX-1):
        norme = norme + dx*np.fabs(U_new[j] - U_data[j])**2
        
    norme = np.sqrt(norme)
            
    print ("Erreur/norme L2",norme) 
    plt.figure(0)
    
    plt.plot(xx,U_new,"r",marker='x')
    plt.plot(xx,U_sol,"b",marker='o')
    plt.legend(("t=T"), 'best')
    plt.xlabel('x')
    plt.ylabel('u')
    
    plt.show()

    return norme    
    
if __name__ == '__main__':
    main()