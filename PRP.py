# -*- coding: utf-8 -*-
"""
Created on Sat May 20 14:06:50 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""

import Runner as rnr
import FileHandler as fh
import FastQC as fq
import SortMeRNA as smr
import yaml

with open("config.yml", 'r') as confile:
    cfg = yaml.load(confile)
    
"""
for section in cfg: 
    print(section)
    for element in cfg[section]:
        print("  " + element + " > " + str(cfg[section][element]))
"""

# Creates a filehandler from a folder
data = fh.FileHandler(cfg["config"]["reads_dir"], cfg["config"]["work_dir"], clean=cfg["config"]["clean"])

# Checks order :
order = cfg["config"]["test_order"]
# Creates script accordingly
for element in order:
    if element == "fastqc":
        # Creates a fastqc object depending on the config in fastqc
        qc = fq.FastQC(data, cfg["fastqc"]["directory"], zip_extract = cfg["fastqc"]["zipextract"])
        # Runs the generated script
        run = rnr.Runner(data)
    elif element == "sortmerna":
        # Creates a smr object
        rna = smr.SortMeRna(data, cfg["sortmerna"]["database"], number_of_threads=cfg["sortmerna"]["number_of_threads"])
        run = rnr.Runner(data)
    elif element == "trimmer":
        pass
        