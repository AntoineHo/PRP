# -*- coding: utf-8 -*-
"""
Created on Sun May 14 22:27:34 2017

@author: AntoineHo

PyRPi : Python RNAseq Pipeline
"""

import os

class FileHandler:
    """Will create a working directory in the path/to/dir in argument"""
    _infiles = []
    
    def __init__(self, dir):
        """This is the class constructor of FileHandler objects"""
        
        # Creates an info dictionary
        self.info = {}
        # Sets self.dir
        self.dir = dir
        # Sets self.uid unique to every add file (if file got deleted then added back ID will change)
        self.uid = 0
                
        # Checks if current working directory is called /working_directory
        os.chdir(self.dir)
        split = os.getcwd().split('\\')
        cwd = split[-1]
        # If current wd is not working_directory : change self.dir
        if cwd != "working_directory" :
            # If it is not working_directory sets the dir path to dir/working_directory
            self.dir = os.path.join(dir, "working_directory")
            
            os.walk(self.dir, topdown = True)
            # Creates working_directory
            os.makedirs(self.dir, exist_ok = True)
            # Changes working directory to self.dir
            os.chdir(self.dir)
            # Checks if the directory was created and raises an error if not
            if os.path.isdir(self.dir) == False :
                raise NotADirectoryError("The directory was not created.")
            
            # Gets list of files in the directory, if there are already files raises a WorkingDirectory error
            scan = os.listdir(self.dir)
            if len(scan) > 0 :
                # Checks if elements are dirs or file
                for element in scan :
                    path = os.path.join(str(dir), element)
                    # If it is a file : raise WorkingDirectoryError
                    if os.path.isfile(path) :
                        raise WorkingDirectoryError
        
        # Gathers files in dir
        scan = os.listdir(dir)
        # Checks if there are files in dir
        if len(scan) > 0 :
            # Checks last char of dir
            if dir[-1] == "\\" or dir[-1] == "/" :
                # loops through scan
                for file_name in scan:
                    # defines a path for each file in scan
                    path = os.path.join(str(dir), file_name)
                    # Checks if the path is a file
                    if os.path.isfile(path) :                    
                        # Adds file (checks & everything to _infiles)
                        self.__add__(path)
            else:
                # loops through scan
                for file_name in scan:
                    # Defines a path for each file in scan
                    path = os.path.join(str(dir), file_name)
                    # Checks if the path is a file
                    if os.path.isfile(path) :                    
                        # Adds file (checks & everything to _infiles)
                        self.__add__(path)
            
        self.check_files()            
        ###print(self._infiles)
        ###self.get_info()
        
    def __add__(self, file_list):
        """Method called when doing our object + a path list [file_1, file_2, ...] or + a single file path"""
        # Creates a list for potential errors (elements that are not file paths)
        excluded = []
        
        # Checks if the argument file_list is a single string then if it is a path
        if type(file_list) == str:
            # Checks if the string corresponds to a path
            if not os.path.isfile(file_list) :
                raise SyntaxError("The arg file_path is not a file or is not found in the directory")
                
            # Gets file_name from file_list (from the path)
            file_name = os.path.basename(file_list)
            
            # Appends the filename to the _infile list if it is not already in
            if file_name not in self._infiles:
                # Adds file to _infiles list
                self._infiles.append(file_name)
                # Fills info dictionary with the file path (here name file_list)
                self.fill_info(file_name)
                
        # Checks if the argument file_list is a list of paths
        elif type(file_list) == list:
            # Removes duplicates
            file_set = set(file_list)
            # Checks if each element of file_set is a path
            for file_path in file_set:
                if not os.path.isfile(file_path) :
                    # Fills a list with elements that are not files
                    excluded.append(file_path)
                    continue
                
                # Gets filename from file_path
                file_name = os.path.basename(file_path)
                
                # If element is a file and not already in _infiles, it appends the infiles list
                if file_name not in self._infiles:
                    # Adds filename to _infiles list
                    self._infiles.append(file_name)
                    # Fills info dictionary with new file path
                    self.fill_info(file_name)
        
        # If the argument file_list is not a list nor a string : raise AttributeError 
        else :
            raise AttributeError("the argument is not a string nor a list of string")
        
        # Prints every element as they were excluded
        for element in excluded :
            try:
                split = element.split('/')
                ext = split[len(split)-1]
            except: ext = 'invalid_filename'
            print("###Error : {} is not a file name or does not exist.".format(ext))
        
    
    def __sub__(self, file_list):
        """Method called when doing FileHandler - file_name or [file_names list]"""
        # Checks if file list is just a single string (in this case a file name)
        if type(file_list) == str:
            # Gets the file path
            file_path = os.path.realpath(file_list)
            # Checks if the file path exists
            if not os.path.isfile(file_path) : 
                raise SyntaxError("The argument is not a file or is not found in the directory")
            # Checks if the file_name is in _infiles of the FileHandler
            elif file_list in self._infiles:
                # Removes the filename from _infiles & from info dictionary
                self._infiles.remove(file_list)
                del self.info[file_list]
            # If the file is not in the _infiles list raise an index error
            else: 
                raise IndexError('filename not in file list')
        # If the argument is a list of filenames
        elif type(file_list) == list:
            for file_name in file_list:
                # Gets the file path
                file_path = os.path.realpath(file_name)
                # Checks if the file exists raise an error if not
                if not os.path.isfile(file_path) : 
                    raise SyntaxError("The element is not a file or is not found in the directory")
                # Removes the filename from infiles and from the info dictionary
                elif file_name in self._infiles:
                    self._infiles.remove(file_name)
                    del self.info[file_name]
        # If the argument file_list is not a list nor a string : raise AttributeError 
        else :
            raise AttributeError("the argument is not a string nor a list of string")
            
        print("File(s) successfully removed\n")
        
    def __repr__(self):
        """Method called when our object needs to be represented"""
        string = ""
        for file in self._infiles:
            string += str(file) + "\n"
        
        return string[:-1]
        
    def __str__(self):
        """Method called when the object is printed"""
        return repr(self)
    
    def check_files(self):
        """Method used to check if files in _infiles are usable"""
        print("--Checking files...")
        
        # List of all accepted extensions, need to remove .pdf
        extension_list = [".fastq",".fq",".gz",".fa",".fasta",".fas",".sam",".bam",".faa",".frn",".fna",".ffn",".cram",".pdf"]
        for file in self._infiles:
            # Split the extension from the path and normalise it to lowercase.
            ext = os.path.splitext(file)[-1].lower()
            # Checks if the extension is valid (is in extension list)
            if ext not in extension_list:
                # When an extension is not in list : prints a warning
                print("##Warning : unknown file extension : {}".format(file))
                # The file could be valid but with unknown extension so ASKs for removal
                ans = input("Do you want to remove this file from the list y/n?")
                # if ans is y or Y then the file is removed from _infiles
                if ans == "y" or ans == "Y":
                    # Removes file from _infiles list
                    self._infiles.remove(file)
                    # Removes file info from info dictionary
                    del self.info[file]
        
        # Prints files in self._infiles
        to_print = "-Files in _infiles- \n"
        for file in self._infiles:
            to_print += str(file) + "\n"
        print(to_print[:-1])
        print("Checking files done-- \n")
        
    def check_output_dir(self):
        """Method called to check if output directory exists, if it is writeable and create it if it does not exist"""
        
        print("--Checking output directory...")
        # Changes current working directory to working_directory
        os.chdir(self.dir)
        
        # Gets current working directory
        cwd = os.getcwd()
        ###print("Current working directory : {} \n".format(cwd))
        
        # Lists directories & files in working_directory
        listdir = os.listdir(cwd)
        # Creates a path for output_dir
        output_dir = self.dir + "/output/"
        # If output directory not in working_directory : create one
        if "output" not in listdir:
            os.makedirs(output_dir, exist_ok = True)
            print("Output directory created")
        
        # Checks if directory is writeable : tries to write a file & remove it, raise an exception if not possible
        file_test = output_dir + "write_test.txt"
        try : 
            f = open(file_test, 'w+')
            f.close()
            os.remove(file_test)
        except : 
            raise PermissionError('the directory is not writeable')
        
        print("Checking output directory done-- \n")
    
    def get_info(self, file=None):
        """Method called to print the info dictionary or a key in info dictionary"""
        print('--File infos...\n')
        if file == None:
            for key in self.info:
                #gets only the file name
                split = key.split("/")
                file_name = split[-1]
                print("{} : \n- ID = {} \n- location = {} \n- Tests = {}\n".format(file_name, self.info[key][0], self.info[key][1], self.info[key][2]))
        else :
            #gets only the file name
            split = file.split("/")
            file_name = split[-1]
            print("{} : \n- ID = {} \n- location = {} \n- Tests = {}\n".format(file_name, self.info[file][0], self.info[file][1], self.info[file][2]))
        
        print("File infos--\n")
    
    def fill_info(self, file_name):
        """Function used to fill infos into info dict when a new file is added"""
        # Fills dictionary with ID (int = hash(self.info)), path, [ran_tests]
        self.info[file_name] = [self.uid,os.path.join(str(self.dir), file_name),[None]]
        self.uid += 1
        
    def info_update(self, file, new_path):
        """Function called when a file is moved to another directory : updates location"""
        # Checks if new_path corresponds to the file
        path = os.path.join(new_path, file)
        if os.path.isfile(path) :
            self.info[file][1] = new_path
        # if true location is not new location : raise attribute error
        else :
            raise AttributeError('location argument is not true location of the file')
    
    def ran_module(self, test):
        """This class updates the object info dictionary when a test is run
        It however requires to be called by another object using a FileHandler"""
        
        for filename in self._infiles:
            # Checks if another test has already been done
            if self.info[filename][2] == None:
                # If it is the first test, change None to a list [test]
                self.info[filename][2] = [test]
            else :
                # If it is not the first test, appends the list [test1, test2, ...] with test
                self.info[filename][2].append(test)


class WorkingDirectoryError(Exception):
    """Exception raised when run_fastqc comes before gen_fastqc"""
    def __init__(self):
        """Only stocks the error message"""
        self.message = "there are already files in working directory, avoid by changing dir argument x = FileHandler('dir')"
    def __str__(self):
        """Returns the message"""
        return self.message

