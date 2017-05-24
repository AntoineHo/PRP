# -*- coding: utf-8 -*-
"""
Created on Sat May 20 14:06:34 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""

import subprocess

class Runner:
    """Class that runs generated scripts"""
    
    def __init__(self, filehandler):
        """Class constructor"""    
        
        self.filehandler = filehandler
        
        # Sets a list of scripts to run from the filehandler object
        for filename in  self.filehandler.infiles:            
            to_run = []
            # Gets all path to scripts to run in the script dict & appends to_run list
            for script_path in self.filehandler.script_dict[filename]:
                if script_path != None:
                    to_run.append(script_path)
            # loops through the script list, opens, reads and close scripts
            for filepath in to_run:
                f = open(filepath, 'r')
                nline = self.file_len(filepath)
                i = 0
                while i < nline:
                    command = f.readline()
                    print("Run > {}".format(command))
                    subprocess.run(command, shell=True, check=True)
                    i+=1
                f.close()
            # Erase the scripts to run in the script_dict filename key
            self.filehandler.script_dict[filename] = []
        
    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
            return i + 1