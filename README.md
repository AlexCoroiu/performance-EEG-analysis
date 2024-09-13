# Evaluating EEG Analysis Methods on Simulated Data

This project is used to test the performance of parametric and non-parametric FWER correction methods with a Monte Carlo simulation. The simulation covers a wide range of parameters that define EEG data properties like the signal-to-noise ratio, dimensionality, or dependencies. Synthetic EEG data is simulated from scratch and processed using the MNE Python library. The parametric Bonferroni and Succesive Time Window approach are comapred agaisnt a non-parametric Cluster permutation method. All these methods aim to solve the multiple testing problem that arises in explorative ERP studies. Their performance is measured in terms of type I and type II error rates, and false discovery rate (FDR). 

## INSTALLATION

First, make sure to install all the required libraries (see Requirements.txt). Then clone this repository. 

## RUNNING THE PROJECT

The main file that can be used to run the project is run.py. Here you can choose to simulate, process and analyse data. You can edit the functions in this file to select which steps to do, and which methods to analyse the data with. 

The results of the analysis can be summarised using summary_statistics.py. This file also includes an explorative analysis for the effect of parameters used to generate the data.

Additionally, the file lateralization.py, does the same as run.py, but for testing the methods for ERP lateralization. This file includes summary statistics as well. 

The files exploration.py and vizualization.py can be used to generate plots for intermediary steps of the project. 

## CHANGING PARAMETERS

The file constants.py contains the main parameters used to generate, process and analyse data. They can be changed here prior to running the project. 

