# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:59:46 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""
import os

class Trimmer:
    
    def __init__(self, filehandler, quality):
        """Method that will generate script for Trimming adapters"""
        
        self.filehandler = filehandler
        
        # Checks whether sortmerna was done before
        self.check_sortmerna()
        
        # Sets a path for sortmerna subdirectory in prp_directory/output/ and sortmerna_scripts in prp_directory/scripts/
        self.trim_outdir = os.path.join(self.filehandler.prpdir, "output", "trim_out")
        self.trim_scripts_dir = os.path.join(self.filehandler.prpdir, "scripts", "trim_scripts")
        # Creates the directories
        os.makedirs(self.trim_outdir, exist_ok=True)
        os.makedirs(self.trim_scripts_dir, exist_ok=True)
        # Checks if the directories are writeable
        self.check_writeable(self.trim_outdir)
        self.check_writeable(self.trim_scripts_dir)
        
        # Finds paired_end reads!
        pairlist = self.find_paired(self.filehandler)
        
        if pairlist == None:
            raise PermissionError("the code cannot handle single end reads or pairs are not found")
        # if paired reads are found : generate a script for each pair
        else :
            # Generates scripts
            for pair in pairlist :
                print("--Generating script file for the pair {} ...".format(pair))
                # Sets the path for each read
                read1 = self.filehandler.info[pair[0]][0]
                read2 = self.filehandler.info[pair[1]][0]
                path = os.path.dirname(read1)
                # Sets the script string
                trim_cmd = ""
            
        
        for filename in self.filehandler.infiles:
            # Adds Trimmer in the ran_test section of the filehandler info dictionary
            self.filehandler.ran_module(filename, "Trimmer", None)
            
            
    def create_script_file(self, filename, script_string):
        # Creates a file path for fastqc_filename.sh
        scriptfile = "trim_" + filename.split(".")[0] + ".sh"
        script = os.path.join(self.smr_scripts_dir, scriptfile)
        # Adds the filepath to the script dict in the FileHandler
        self.filehandler.script_dict[filename].append(script)
        # Creates and open the trim_filename.ext.sh file
        f = open(script, 'w+')
        # Writes generated cmd into the script
        f.write(script_string) 
        # Closes script file
        f.close()
    
    def find_paired(self, filehandler):
        """ Method called when we need to find paired end reads in the file_handler"""
        # Sets a list of pair_list
        filepairs = []
        
        # Checks what reads are paired
        filelist = set(self.filehandler.infiles)
        filelist_to_empty = set(self.filehandler.infiles)
        
        for file in filelist:
            filename = re.split(".fq", file)[0]
            for pair in filelist_to_empty:
                pairname = re.split(".fq", pair)[0]
                if pairname[:-2] == filename[:-2] and pairname != filename :
                    print(file,pair)
                    filepairs.append([file, pair])
                    filelist_to_empty.remove(pair)
                    filelist_to_empty.remove(file)
                    break
        
        if len(filepairs) == 0 :
            return None
        else :
            return filepairs
    
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
            
    def check_sortmerna(self):
        """Method called to check wether sormerna was run before"""
        # Sets the path for output of SortMeRna
        smr_outdir = os.path.join(self.filehandler.prpdir, "output", "sortmerna_out")
        # Checks if the output directory for sortmerna exists
        if os.path.isdir(smr_outdir):
            file_list = os.listdir(smr_outdir)
            for element in file_list:
                # Sets the path for the element in sortmerna_out
                path = os.path.join(self.filehandler.smr_outdir, element)
                if os.path.isfile(path):
                    return True
            raise PermissionError("sortmerna_out exists but no file was found in the directory")
        # If the directory does not exist : raise an error
        else:
            raise PermissionError("SortMeRna should be done before trimming")
        
        