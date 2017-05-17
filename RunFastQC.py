# -*- coding: utf-8 -*-
"""
Created on Mon May 15 16:10:42 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""

import os
import FileHandler
import subprocess

class RunFastQC:
    """This class is an object that can run codes and generate codes"""
    
    def __init__(self, filehandler):
        """Class builder takes a directory for creating a FileHandler object called input_files"""
        # sets that fh = a given filehandler when creating the RFQ objec
        self.filehandler = filehandler
        
        # Sets working directory
        os.chdir(self.filehandler.dir)
        
        # Sets a validating self.generation
        self.generation = False
        
    def gen_fastqc(self, zip_extract=False):
        # First checks output directory with fh (FileHandler object)
        self.filehandler.check_output_dir()
        # Then creates subdirectories wd/output/fastqc and wd/fastqc_scripts
        fastqc_outdir = self.filehandler.dir + "/output/fastqc/"
        fastqc_scripts_dir = self.filehandler.dir + "/fastqc_scripts/"
        os.makedirs(fastqc_outdir, exist_ok = True)
        os.makedirs(fastqc_scripts_dir, exist_ok = True)
        
        # Checks files in infiles
        self.filehandler.check_files()
        # Returns to working_directory if it was not in
        os.chdir(self.filehandler.dir)
        
        # For every file in self._infiles or in list of file fed when command is run
        for filename in self.filehandler._infiles :
            print("--Generating script file for {} ...".format(filename))
            
            # Creates the string for fastQC
            fa_cmd = "fastqc -o "+ fastqc_outdir + " " + self.filehandler.dir + "/" + filename
            
            # Adds zip_extract if the command was True
            if zip_extract == True:
                fa_cmd += " -extract "
        
            # Creates a file path for fastqc_filename.sh
            script = fastqc_scripts_dir + "fastqc_" + filename + ".sh"
            # Creates and open the fastqc_filename.ext.sh file
            f = open(script, 'w+')
            # Writes generated cmd into the script
            f.write(fa_cmd) 
            # Closes script file
            f.close()
        
            print("Generation done--")
            
        # Turns generation on
        self.generation = True
            
    def run_fastqc(self):
        """Method called when script generation is done"""
        # Checks if generation has been done
        if self.generation == False :
            raise GenerationError
        
        # re sets working directory
        os.chdir(self.filehandler.dir)
        
        # Gathers the fastqc scripts directory path
        fastqc_scripts_dir = self.filehandler.dir + "/fastqc_scripts/"
        
        # Gathers a list of files from the fastqc scripts directory
        scan = os.listdir(fastqc_scripts_dir)
        # for each file in fastqc_scripts_dir, sets the path & runs the script
        for filename in scan:
            path = fastqc_scripts_dir + filename
            subprocess.run(path, shell=True, check=True)
            
            
class GenerationError(Exception):
    """Exception raised when run_fastqc comes before gen_fastqc"""
    def __init__(self):
        """Only stocks the error message"""
        self.message = "in order to run fast_qc first script files must be generated with gen_fastqc"
    def __str__(self):
        """Returns the message"""
        return self.message
            
       
