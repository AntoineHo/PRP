# -*- coding: utf-8 -*-
"""
Created on Sun May 14 22:27:34 2017

@author: AntoineHo

PyRPi : Python RNAseq Pipeline
"""

import os
import shutil

class FileHandler:
    """Will create a working directory in the path/to/dir in argument"""
    _infiles = []
    
    def __init__(self, dir):
        """This is the class constructor of FileHandler objects"""
        
        # Creates an info dictionary
        self.info = {}
        # Sets self.dir
        self.dir = dir
        
        # Checks if current working directory is called /working_directory
        os.chdir(self.dir)
        split = os.getcwd().split('\\')
        cwd = split[len(split)-1]
        if cwd != "working_directory" :
            # If it is not working_directory sets the dir path to dir/working_directory
            self.dir = dir + "/working_directory"
            
            os.walk(self.dir, topdown = True)
            # Creates working_directory
            os.makedirs(self.dir, exist_ok = True)
            # Changes working directory to self.dir
            os.chdir(self.dir)
            # Checks if the directory was created and raises an error if not
            if os.path.isdir(self.dir) == False :
                raise NotADirectoryError("The directory was not created.")
            
            # scan is a list of files in the directory, if there are files it ask to remove them
            scan = os.listdir(self.dir)
            if len(scan) > 0 :
                ask = input("There are files in the working directory. Do you want to delete them? (y/n) :")
                if ask == "y" or ask == "Y" :
                    # Checks for every element in listdir if it is a file or a directory and deletes it
                    for element in scan:
                        path = self.dir + "/" + str(element)
                        if os.path.isfile(path) == True:
                            os.remove(path)
                        elif os.path.isdir(path) == True:
                            shutil.rmtree(path, ignore_errors=False)
                        else :
                            raise TypeError('The element is not a directory or a file')
        
        # Gathers files in dir
        scan = os.listdir(dir)
        # Checks if there are files in dir
        if len(scan) > 0 :
            # loops through scan
            for file_name in scan:
                path = str(dir)+'/'+file_name
                #Checks if the path is a file
                if os.path.isfile(path) == True :                    
                    # Adds file (checks & everything to _infiles)
                    self.__add__(path)
        
        print(self._infiles)
        """
        self.get_info()
        """
        
    def __add__(self, file_list):
        """Method called when doing our object + a path list [file_1, file_2, ...] or + a single file path"""
        # Creates a list for potential errors (elements that are not file paths)
        excluded = []
        
        # Checks if the argument file_list is a single string then if it is a path
        if type(file_list) == str:
            # Checks if the string corresponds to a path
            if os.path.isfile(file_list) == False :
                raise SyntaxError("The arg file_path is not a file or is not found in the directory")
                
            # Gets file_name from file_list (from the path)
            split = file_list.split('/')
            file_name = split[len(split)-1]
            
            # Moves file to working_directory
            os.replace(file_list,self.dir+'/'+file_name)
                
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
                if os.path.isfile(file_path) == False :
                    # Fills a list with elements that are not files
                    excluded.append(file_path)
                    continue
                
                
                # Gets filename from file_path
                split = file_path.split('/')
                file_name = split[len(split)-1]
                # Moves file to working_directory
                os.replace(file_path,self.dir+'/'+file_name)
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
            if os.path.isfile(file_path) == False : 
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
                if os.path.isfile(file_path) == False : 
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
        
        return string[0:len(string)-1]
        
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
        print(to_print[:len(to_print)-1])
        print("Checking files done-- \n")
            
    def check_input_dir(self):
        """Method called when we want to check if input directory exists and is writeable.
        Creates input directory if it does not exist"""
        
        print("--Checking input directory...")
        # Changes current working directory to working_directory
        os.chdir(self.dir)
        # Gets current working directory
        cwd = os.getcwd()
        ###print("Current working directory : {} \n".format(cwd))
        # Lists directories & files in working_directory
        listdir = os.listdir(cwd)
        # Creates the path for an input directory
        input_dir = self.dir + "/input/"
        # Checks whether input_dir already exists
        if "input" not in listdir:
            # Creates the input directory
            os.makedirs(input_dir, exist_ok = True)
            print("Input directory created")
            
        # Checks if directory is writeable : tries to write a file & remove it, raise an exception if not possible
        file_test = input_dir + "write_test.txt"
        try : 
            f = open(file_test, 'w+')
            f.close()
            os.remove(file_test)
        except : 
            raise PermissionError('the directory is not writeable')
            
        print("Checking input directory done-- \n")
            
    def move_to_input(self):
        """Method called when we want to move all files to an input directory"""
        
        print("--Moving files to input directory...")
        # Checks input directory
        self.check_input_dir()
        # Checks if all the files are valid
        self.check_files()
        
        # Creates the path for an input directory
        input_dir = self.dir + "/input/"
        # Move all the input files to the input folder
        for file_name in self._infiles:
            # Gets current file path & realpath of input_dir
            src = os.path.realpath(file_name)
            dst = os.path.realpath(input_dir)
            # Moves files from working directory to input
            os.replace(src,dst+'\\'+file_name)
            # Update location of file in self.info dictionary
            new_location = dst
            self.info_update(file_name, new_location)
        
        # Change working directory to /input
        os.chdir(input_dir)
        # Gets current working directory
        cwd = os.getcwd()
        # Gets files in cwd (could have been in input_dir)
        listdir = os.listdir(cwd)
        
        # prints files in cwd
        to_print = "-Files in input directory- \n"
        for element in listdir : 
            to_print += str(element) + "\n"
        print(to_print[:len(to_print)-1])
        
        print("Moving files to input done-- \n")
        
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
                file_name = split[len(split)-1]
                print("{} : \n- ID = {} \n- location = {} \n- Tests = {}\n".format(file_name, self.info[key][0], self.info[key][1], self.info[key][2]))
        else :
            #gets only the file name
            split = file.split("/")
            file_name = split[len(split)-1]
            print("{} : \n- ID = {} \n- location = {} \n- Tests = {}\n".format(file_name, self.info[file][0], self.info[file][1], self.info[file][2]))
        
        print("File infos--\n")
    
    def fill_info(self, file_name):
        """Function used to fill infos into info dict when a new file is added"""
        # Fills dictionary with ID (int = len(self.info)), location, [ran_tests]
        self.info[file_name] = [len(self.info),str(os.path.realpath(file_name)),[None]]
        
    def info_update(self, file, new_path):
        """Function called when a file is moved to another directory : updates location"""
        # Checks if new_path corresponds to the file
        if os.path.isfile(new_path+"\\"+file) == True:
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



#%%
"""
test = FileHandler("Path/To/dir")

#%% Adding files to test
test + ["Path/To/file/test_1.pdf","Path/To/file/test_2.pdf","Path/To/file/test_2.pdf"]
test + "Path/To/file/test_3.pdf"
#%% Checking files in _infiles
test.check_files()
#%% Checks input directory
test.check_input_dir()

#%% Checks output directory
test.check_output_dir()

#%% Move files to input directory
test.move_to_input()

#%% Try the get_info
print("\n====Try for get_info====")
test.get_info()
print("\n====Try for get_info('test_1.pdf')====")
test.get_info("test_1.pdf")

#%%
print("\n====Try for test - 'test_1.pdf'====")

test - "test_1.pdf"
print("\n====Try get_info() after removal of a file (test_1.pdf)====")
test.get_info()
"""
