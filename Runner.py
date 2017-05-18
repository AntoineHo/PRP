# -*- coding: utf-8 -*-
"""
Created on Thu May 18 13:14:53 2017

@author: antoi
"""
import os
import subprocess

class Runner:
    """Class that runs generated scripts"""
    
    def __init__(self, filehandler, fastqc=None):
        """Class constructor"""    
        # Gets the filehandler object from arguments NECESSARY
        self.filehandler = filehandler
        # Gets the fastqc object from args (default = None if fastqc was not done or not necessary)
        self.fqc = fastqc
        
    def run_scripts(self):
        """Method called when scripts must be read after generation is done"""
        
        script_files = []
        
        ## FIRST FASTQC SCRIPTS
        # Checks if generation has been done by the fastqc object (validation step)
        if self.fqc.generation == False :
            raise GenerationError
        else :
            # Re sets working directory
            os.chdir(self.filehandler.dir)
        
            # Gathers the fastqc scripts directory path
            fastqc_scripts_dir = os.path.join(self.filehandler.dir, "fastqc_scripts")
        
            # Gathers a list of files from the fastqc scripts directory
            scan = os.listdir(fastqc_scripts_dir)
            # For each file in fastqc_scripts_dir
            for script in scan:
                # Sets the path
                path = os.path.join(fastqc_scripts_dir, script)
                # Appends the script path to script_files list
                script_files.append(path)
                # Updates info dictionary in the filehandler
                self.filehandler.ran_module("FastQC")
               
        ## OTHER SCRIPTS
        
        ## Runner reads all paths in list script_files every filepath is opened and command is executed
        for filepath in script_files:
            f = open(filepath, 'r')
            command = f.readline()
            subprocess.run(command, shell=True, check=True)
        f.close()
        
class GenerationError(Exception):
    """Exception raised when run_fastqc comes before gen_fastqc"""
    def __init__(self):
        """Only stocks the error message"""
        self.message = "in order to run fast_qc first script files must be generated with gen_fastqc"
    def __str__(self):
        """Returns the message"""
        return self.message