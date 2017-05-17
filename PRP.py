# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:56:34 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""
import RunFastQC as rfq
import FileHandler as fh

data = fh.FileHandler('C:/Users/antoi/Dropbox/Umea 2017/Applied Functionnal Genomics/Assignment/Test_fastqc')

#%%
fastqc = rfq.RunFastQC(data)

fastqc.gen_fastqc()

#%%
fastqc.run_fastqc()