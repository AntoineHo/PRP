# -*- coding: utf-8 -*-
"""
Created on Mon May 22 20:43:30 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""

import FileHandler
import os

class SortMeRna:
    """Class object that will create a script for each file in the FileHandler"""
    
    def __init__(self, filehandler, ends="SE", ):
        
        self.filehandler = filehandler
        
        # Sets a path for sortmerna subdirectory in prp_directory/output/ and sortmerna_scripts in prp_directory/scripts/
        smr_outdir = os.path.join(self.filehandler.prpdir, "output", "sortmerna_out")
        smr_scripts_dir = os.path.join(self.filehandler.prpdir, "scripts", "sortmerna_scripts")
        # Creates the directories
        os.makedirs(smr_outdir, exist_ok=True)
        os.makedirs(smr_scripts_dir, exist_ok=True)
        # Checks if the directories are writeable
        self.check_writeable(smr_outdir)
        self.check_writeable(smr_scripts_dir)
        
        
        
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