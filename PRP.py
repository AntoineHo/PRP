# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:56:34 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""
import FastQC as fq
import FileHandler as fh
import Runner as rnr

data = fh.FileHandler('/studenthome/user9/testdata')

qc = fq.FastQC(data)

Run = rnr.Runner(data, qc)

Run.run_scripts()
