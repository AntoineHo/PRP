# -*- coding: utf-8 -*-
"""
Created on Sat May 20 14:06:34 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""
import os
import subprocess

class Runner:
    """Class that runs generated scripts"""
    
    def __init__(self, filehandler):
        """Class constructor"""    
        
        self.filehandler = filehandler
        # Sets a list of scripts to run from the filehandler object
        to_run = []
        
        
        # Sets the path for the scripts directory
        scripts_dir = os.path.join(self.filehandler.prpdir, "scripts")
        
        # Gathers all the files in scripts_dir
        for root, directories, filenames in os.walk(scripts_dir):
            for filename in filenames:
                filepath = os.path.join(root,filename)
                # Appends the filepaths to the to_run list
                to_run.append(filepath)
        
        # loops through the script list:
        for filepath in to_run:
            f = open(filepath, 'r')
            command = f.readline()
            print("Run > {}".format(command))
            subprocess.run(command, shell=True, check=True)
            f.close()
        