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

# Creates a filehandler from a folder
data = fh.FileHandler("/studenthome/user9/testdata", "/studenthome/user9/testdata", clean = True)
#data = fh.FileHandler("C:\\Users\\antoi\\Dropbox\\Umea 2017\\Applied Functionnal Genomics\\Assignment\\V2\\testdir", "C:\\Users\\antoi\\Dropbox\\Umea 2017\\Applied Functionnal Genomics\\Assignment\\V2\\testdir", clean=True)

rna = smr.SortMeRna(data)
#%%
# Creates a FastQC object from the filehandler, directory name is "raw"
#qc = fq.FastQC(data, "raw")
# Runs the generated scripts
#Run = rnr.Runner(data)