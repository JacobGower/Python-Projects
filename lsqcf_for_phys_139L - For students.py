# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 09:44:53 2021

@author: Erick Membreno

Hi everyone,

For those who have no experience with programming and plotting your data in 
python, I wrote this script for you. Use this example to put in your values
and your own fit function. This example's fit function will be that of Lab 3's
Shockley Equation.



"""

#-----------------------Preamble (Don't change this)----------------------------------------------

import os
import numpy as np
from decimal import Decimal
import sympy as sym

from scipy import linalg as la
from scipy import optimize
import math as m


import matplotlib as mpl

import matplotlib.ticker as mtick
import matplotlib.pyplot as plt;
from matplotlib.path import Path
from matplotlib.patches import Circle, PathPatch, Ellipse
import matplotlib.patches as patches
plt.style.use('seaborn-white')


from tkinter import filedialog
from tkinter import *
import tkinter as tk

import csv

from skimage import data,filters
import matplotlib.image as img 
from PIL import Image



#-----------------------------------------------------------------------------

"""
This is where you put YOUR values
"""
R = 1e3; #Resistor is 1 kOhm



V_in = np.array([0.569,0.822,1.056,1.682,2.58,3.47,4.32,5.03,6.67,7.37,8.04,8.6]); # units in volts




V_diode = np.array([0.456,0.462,0.473,0.492,0.510,0.523,0.534,0.541,0.554,0.559,0.563,0.566]) # units in volts



I_diode = (V_in-V_diode)/R;

#------------------Finding the lsqcurvefit-----------------------------------

k = 8.617e-5; # Boltzmann constant with units eV/K
T = 300;      # Room temperature in kelvin
e = 1.6e-19;  # electron chargein coulomb

xdata = np.linspace(-1,2,100) #range of values for x-axis for fit equation
A = np.array([1e-8, .4]) #Guess parameters

"""
This is where you express your fitting function. Here we will use Schockley 
Equation
"""
def fun1(x, A1, A2):
    return (A1*(m.exp((A2*x)/(k*T))-1)) 



yf = np.array([])
yd = np.vectorize(fun1, excluded=['A1', 'A2'])
y3 = yd(xdata, *A)


def g(A):
    n=24
    return I_diode[0:n] - yd(V_diode[0:n], *A)

FitParams, b2 = optimize.leastsq(g, A[:])



#------------------Plotting your data----------------------------------------
fig = plt.figure(figsize =(5,5))
ax0 = fig.add_axes([0,0,1,.5], ylim=(-0.002, 0.01), xlim =(-1,3) )
plt.rc('text',usetex=True)
plt.rc('font', family='serif')
gs = mpl.gridspec.GridSpec(4,4)


ax0.plot(V_diode, I_diode, marker = 'o', color ='black',
         linestyle = 'none', label=r'\textbf{$I(V) exp$}')
ax0.plot(xdata, yd(xdata, *FitParams), color='red', 
         label = r'\textbf{$I(V) =A(1) \bigg[e^{A(2)\frac{V_{diode}}{V_{T}} } -1 \bigg] $}' )
ax0.set_ylabel(r'\textbf{I (A)}', fontsize = 12)
ax0.set_xlabel(r'\textbf{V$_{diode} $(volts)}', fontsize = 12)
ax0.xaxis.set_major_locator(mpl.ticker.MaxNLocator(8))
ax0.yaxis.set_major_locator(mpl.ticker.MaxNLocator(8))
ax0.tick_params(which='minor', length=4, color='k')
ax0.legend()
plt.grid(True, which = 'both')


#-----------------------------------------------------------------------------
n = 1/FitParams[1];
n_format = "{:.2f}".format(n)
print('The ideality factor is equal to the second fitted parameter divided by the charge of an electron. '
      '\n n = ' +  str(n) )







