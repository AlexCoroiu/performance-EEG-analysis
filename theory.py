# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from math import sqrt

#----INDIVIDUAL ALPHA CORRECTION----

#no correction
def basic(a_target,m):
    return 1 - ((1 - a_target)**m)

#bonferroni
def bonferroni(a_target,m):
    a_corrected = a_target/m
    return 1 - ((1 - a_corrected)**m)
    
#bonferroni extension v.d. Lubbe
def bonferroni_ext(a,m):
    return sqrt(a/m)


#----PLOTTING----

#calculating alphas
def fwer_alpha(a_target,tests_ns,func):
    fwers = []
    for n in tests_ns:
        fwers.append(func(a_target,n))
    return fwers

#plotting function
def plot(target_a, tests_ns, func, name):
    fwers = fwer_alpha(target_a,tests_ns,func)   
    plt.plot(tests_ns,fwers)
    plt.xlabel('nr. individual tests')
    plt.ylabel('FW alpha') 
    plt.title(name)
    plt.show()     
    
#values
tests_n_max = 10000
tests_ns = range(1,tests_n_max)
a_target = 0.05

plot(a_target, tests_ns, basic, 'No Correction FW alpha')
plot(a_target, tests_ns, bonferroni, 'Bonferroni FW alpha')
plot(a_target, tests_ns, bonferroni_ext, 'Bonferroni extension FW alpha')

#----SIMPLE EXAMPLE----

#example 
time_windows = 80
electrodes = 60

no_corr = basic(a_target, time_windows*electrodes)
bon = bonferroni(a_target, time_windows*electrodes)
bon_ext = bonferroni_ext(a_target, (time_windows-1)*electrodes)

print(no_corr, bon, bon_ext)

