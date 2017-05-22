# -*- coding: utf-8 -*-
"""
Created on Sat May 20 13:46:33 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""

import FileHandler
import os

class FastQC:
    """Class that generate fastqc scripts"""
    
    def __init__(self, filehandler, dirname, zip_extract=False):
        """Class builder takes a filehandler object to get files and generate scripts"""
        
        self.filehandler = filehandler
        # Name that will be used to create a directory for scripts & output
        self.dirname = dirname
        
        # Sets a path for fastqc subdirectory in prp_directory/output/ and fastqc_scripts in prp_directory/scripts/
        fastqc_outdir = os.path.join(self.filehandler.prpdir, "output", "fastqc_out", self.dirname)
        fastqc_scripts_dir = os.path.join(self.filehandler.prpdir, "scripts", "fastqc_scripts", self.dirname + "_scripts")
        # Creates the directories
        os.makedirs(fastqc_outdir, exist_ok=True)
        os.makedirs(fastqc_scripts_dir, exist_ok=True)
        # Checks if the directories are writeable
        self.check_writeable(fastqc_outdir)
        self.check_writeable(fastqc_scripts_dir)
        
        for filename in self.filehandler.infiles :
            print("--Generating script file for {} ...".format(filename))
            
            # Creates the string for fastQC filepath is taken from the info dictionary of the filehandler
            fa_cmd = "fastqc -o "+ fastqc_outdir + " " + self.filehandler.info[filename][0]
             
            # Adds zip_extract if the command was True
            if zip_extract == True:
                fa_cmd += " -extract"
        
            # Creates a file path for fastqc_filename.sh
            scriptfile = "fastqc_" + filename + ".sh"
            script = os.path.join(fastqc_scripts_dir, scriptfile)
            # Creates and open the fastqc_filename.ext.sh file
            f = open(script, 'w+')
            # Writes generated cmd into the script
            f.write(fa_cmd) 
            # Closes script file
            f.close()
        
            print("Generation done--")  
            
    def check_writeable(self, dirpath):
        """This method raise an error if the directory is not writeable"""
        # Sets a path for file_test
        file_test = os.path.join(dirpath, "test.txt")
        try :
            # Tries to create the file with a path in the tested directory
            f = open(file_test, 'w+')
            f.close()
            os.remove(file_test)
        except : 
            # Raise an error if the file could not be written or removed
            raise PermissionError('the directory {} is not writeable'.format(dirpath))