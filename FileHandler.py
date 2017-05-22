# -*- coding: utf-8 -*-
"""
Created on Fri May 19 20:09:39 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""
import os
import shutil

class FileHandler:
    """Object that captures files and locations, store them and prepare for tests"""
    
    def __init__(self, dir, prp_dir, clean=False):
        """Class constructor, sets the variables for the filehandler"""
        
        # First Check if arguments are valid
        if not os.path.isdir(dir) :
            raise NotADirectoryError("the inserted argument is not a directory")
        # Second Check if the arguments is a prp_directory
        if os.path.basename(dir) == "prp_directory" :
            raise WorkingDirectoryError("invalid argument directory : this is a PRP directory")
        
        # dir is the directory set when creating the filehandler, ideally all working files should be there
        self.dir = dir
        # prp_dir is the path to the scripts and output directory, it is used by the other classes in the PRP
        self.prpdir = os.path.join(prp_dir, "prp_directory")
        # infiles is a list of filenames handled by the object
        self.infiles = []
        # uid is a unique ID given to a file upon addition
        self.uid = 0
        # info is a dictionary which keys are filenames and values are lists [uid,path,[tests done]]
        self.info = {}
        
        # Third Check if clean = True : it will remove tree of any directory in prp_directory
        # Best way to avoid further errors when a test must be rerun, but DELETES PREVIOUS OUTPUTS
        if clean :
            self.clean()
        
        # Creates the directory
        os.makedirs(self.prpdir, exist_ok = True) # exist_ok=True will avoid an error if the directory already exists
        # Checks if the directory was created and raises an error if it is not
        if not os.path.isdir(self.prpdir) :
            raise NotADirectoryError("the directory was not created")
        # Checks if the directory already contains output directories and/or files in them
        if not self.check_prp_directory():
            raise WorkingDirectoryError("the prp_directory already contains files or /output or /scripts directories with dirs / files in it")
        
        # Scans for files in the designated directory
        scan = os.scandir(self.dir)
        for element in scan:
            # Sets a path for the element
            el_path = os.path.join(self.dir, element)
            # Checks if the path is a file
            if os.path.isfile(el_path):
                # Checks the file : if the function returns True appends it to the infiles and info dictionary
                if self.check_file(el_path):
                    self.__add__(el_path)
                    
        # Creates path for two directories
        output = os.path.join(self.prpdir, "output")
        scripts = os.path.join(self.prpdir, "scripts")
        
        # Creates the directories and check if they are writeable
        os.makedirs(output, exist_ok = True)
        os.makedirs(scripts, exist_ok = True)
        
        # Checks if output is writeable : tries to write a file & remove it, raise an exception if not possible
        self.check_writeable(output)
        self.check_writeable(scripts)
        
    
    def __add__(self, filepath):
        """This method adds a valid file to the infiles list"""
        # Gets infos on the file to fill info dictionary and appends infiles
        filename = os.path.basename(filepath)
        self.infiles.append(filename)
        # Adds infos to self.info dictionary [0] = filepath ; [1] = uid and [2] = [ran tests]
        self.info[filename] = [filepath, self.uid, [None]]
        # Increment the uid
        self.uid += 1
        
    def __sub__(self, filename):
        """This method is used when we want to remove one particular file from infiles and info"""
        # Remove filename from self.infiles
        self.infiles.remove(filename)
        # Delete the key in self.info dict
        del self.info[filename]
        # Prints feedback
        print("File {}, successfully removed".format(filename))
        
    def get_info(self, file=None):
        """Method called to print the info dictionary or a key in info dictionary"""
        
        # If no file is in the argument then prints the whole dict
        if file == None:
            # for each filename (keys) of the self.info dict
            for filename in self.info:
                print("{} : \n- location = {} \n- ID = {} \n- Tests = {}\n".format(filename, self.info[filename][0], self.info[filename][1], self.info[filename][2]))
        else :
            # Gets info for only file
            print("{} : \n- location = {} \n- ID = {} \n- Tests = {}\n".format(file, self.info[file][0], self.info[file][1], self.info[file][2]))        
    
    def __repr__(self):
        """Method called when our object needs to be represented"""
        string = ""
        for file in self._infiles:
            string += str(file) + "\n"
        
        return string[:-1]
        
    def __str__(self):
        """Method called when the object is printed"""
        return repr(self)
        
    def check_file(self, filepath):
        """This method checks if a file is valid and usable by the PRP"""
        # The extension list is used to avoid appending a non valid file
        extension_list = [".fastq",".fq",".gz",".fa",".fasta",".fas",".sam",".bam",".faa",".frn",".fna",".ffn",".cram"]
        # Gets the extension of the filepath
        ext = os.path.splitext(filepath)[-1].lower()
        # Checks if the extension is exotic
        if ext not in extension_list :
            # Returns False the file won't be added
            return False
        else :
            return True
    
    def check_prp_directory(self):
        """This method checks if a prp_directory contains already dirs or files
        it will return False (then raise an error in __init__ of the filehandler)
        if any test_output dir is already in /prp_directory
        if any test_scripts dir is already in /prp_directory
        if files are found in any prp subdirectory (output & scripts)
        IT DOES NOT CHECK FILES INSIDE TEST DIRS !"""
        # Gets list of files in the directory, if there are already files raises a WorkingDirectory error
        scan = os.listdir(self.prpdir)
        
        # Checks if there are files in prp_directory
        for element in scan:
            # Sets the path to the element
            el_path = os.path.join(self.prpdir, element)
            # Checks if the element is a file
            if os.path.isfile(el_path):
                return False
        
        # Checks if there is an output directory in scan
        if "output" in scan:
            # If there is an output directory checks the path
            out_path = os.path.join(self.prpdir, "output")
            # Scan the path of the output dir
            scan_output = os.listdir(out_path)
            # for all elements in scan checks if there are output directories
            outdir = ["fastqc_out","rna_out","other_out"]
            for element in scan_output:
                # If there are output dirs returns False
                if element in outdir:
                    return False
                # If there are files in output dir returns False (one should not find files in there anyway)
                elif os.path.isfile(os.path.join(out_path, element)):
                    return False
                
        # Checks if there is an output directory in scan
        if "scripts" in scan:
            # If there is an output directory checks the path
            script_path = os.path.join(self.prpdir, "scripts")
            # Scan the path of the scripts directory
            scan_scripts = os.listdir(script_path)
            # for all elements in scan checks if there are output directories
            scriptsdir = ["fastqc_scripts","rna_scripts","other_scripts"]
            for element in scan_scripts:
                # If there already are scripts dirs returns False
                if element in scriptsdir:
                    return False
                # If there are files in scripts dir returns False (one should not find files in there anyway)
                elif os.path.isfile(os.path.join(script_path, element)):
                    return False
        # If there are no files in prp_dir, if there are no output files or script files then good to go
        return True
    
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
        
    def clean(self):
        # Checks if there is something to clean
        if not os.path.isdir(self.prpdir):
            print("there is nothing to clean")
            return True
        # Gets a list of directory in prp_directory
        scandir = os.listdir(self.prpdir)
        for element in scandir:
            # Sets the path for every element in scandir
            path = os.path.join(self.prpdir, element)
            # Removes directory tree (files included)
            shutil.rmtree(path)
            
    def ran_module(self, test):
        """This class updates the object info dictionary when a test is run
        It however requires to be called by another object using a FileHandler"""
        
        for filename in self.infiles:
            # Checks if another test has already been done
            if self.info[filename][2] == None:
                # If it is the first test, change None to a list [test]
                self.info[filename][2] = [test]
            else :
                # If it is not the first test, appends the list [test1, test2, ...] with test
                self.info[filename][2].append(test)
                
class WorkingDirectoryError(Exception):
    """Exception raised when prp_directory is used as an argument directory"""
    def __init__(self, error_message):
        """Only stocks the error message"""
        self.message = error_message
    def __str__(self):
        """Returns the message"""
        return self.message
    
#test = FileHandler("C:\\Users\\antoi\\Dropbox\\Umea 2017\\Applied Functionnal Genomics\\Assignment\\V2\\testdir", "C:\\Users\\antoi\\Dropbox\\Umea 2017\\Applied Functionnal Genomics\\Assignment\\V2\\testdir", clean=False)