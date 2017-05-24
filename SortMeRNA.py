# -*- coding: utf-8 -*-
"""
Created on Mon May 22 20:43:30 2017

@author: antoi

PyRPi : Python RNAseq Pipeline
"""

import os
import re

class SortMeRna:
    """Class object that will create a script for each file in the FileHandler"""
    
    def __init__(self, filehandler):
        
        self.filehandler = filehandler
        
        # Sets a path for sortmerna subdirectory in prp_directory/output/ and sortmerna_scripts in prp_directory/scripts/
        self.smr_outdir = os.path.join(self.filehandler.prpdir, "output", "sortmerna_out")
        self.smr_scripts_dir = os.path.join(self.filehandler.prpdir, "scripts", "sortmerna_scripts")
        # Creates the directories
        os.makedirs(self.smr_outdir, exist_ok=True)
        os.makedirs(self.smr_scripts_dir, exist_ok=True)
        # Checks if the directories are writeable
        self.check_writeable(self.smr_outdir)
        self.check_writeable(self.smr_scripts_dir)
        
        # Finds paired_end reads!
        pairlist = self.find_paired(self.filehandler)
        
        if pairlist == None:
            # Generates a script for each read
            for filename in self.filehandler.infiles :
                print("--Generating script file for {} ...".format(filename))
                # Sets the filepath
                filepath = self.filehandler.info[filename][0]
                
                # Sets the script string
                smr_cmd = ""
                # Uncompress the read
                smr_cmd += "gunzip " + filepath + "\n"
                # Sets the SortMeRna script
                smr_cmd += "sortmerna"
                smr_cmd += " --reads " + filename.split(".")[0] + ".fq "
                smr_cmd += " --ref $SORTMERNADIR/rRNA_databases/rfam-5s-database-id98.fasta $SORTMERNADIR/rRNA_databases/rfam-5.8s-database-id98.fasta $SORTMERNADIR/rRNA_databases/silva-bac-16s-database-id85.fasta $SORTMERNADIR/rRNA_databases/silva-euk-18s-database-id95.fasta $SORTMERNADIR/rRNA_databases/silva-bac-23s-database-id98.fasta $SORTMERNADIR/rRNA_databases/silva-euk-28s-database-id98.fasta $SORTMERNADIR/rRNA_databases/phix.fasta"
                
                # Sets output for rRNA :
                rrna_path = os.path.join(self.smr_outdir, filename.split(".")[0] + "_rrna_out.fq")
                smr_cmd += " --aligned " + rrna_path
                # Sets output for clean :
                clean_path = os.path.join(self.smr_outdir, filename.split(".")[0] + "_clean_out.fq")
                smr_cmd += " --other " + clean_path
                
                # Sets nber of threads
                number_of_threads = 1
                smr_cmd += " --fastx --log -v -a " + str(number_of_threads) + "\n"
                
                # Compress the read back
                smr_cmd += "gzip " + filepath[:-3] + "\n"
                # Compress the output from the SortMeRna
                smr_cmd += "gzip " + rrna_path + "\n"
                smr_cmd += "gzip " + clean_path
                # Creates the script file
                self.create_script_file(filename, smr_cmd)
                
                print("Generation done--") 
                
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
                smr_cmd = ""
                # Uncompress the reads
                smr_cmd += "gunzip " + read1 + "\n"
                smr_cmd += "gunzip " + read2 + "\n"
                # Sets merged reads path
                merged_path = os.path.join(path,"read-interleaved.fq")
                # Merges the pair
                smr_cmd += "merge-paired-reads.sh " + read1[:-3] + " " + read2[:-3] + " " + merged_path + "\n"
                # Sets the sortmerna script
                smr_cmd += "sortmerna --reads " + merged_path
                smr_cmd += " --ref $SORTMERNADB"
                #smr_cmd += " --ref $SORTMERNADIR/rRNA_databases/rfam-5s-database-id98.fasta $SORTMERNADIR/rRNA_databases/rfam-5.8s-database-id98.fasta $SORTMERNADIR/rRNA_databases/silva-bac-16s-database-id85.fasta $SORTMERNADIR/rRNA_databases/silva-euk-18s-database-id95.fasta $SORTMERNADIR/rRNA_databases/silva-bac-23s-database-id98.fasta $SORTMERNADIR/rRNA_databases/silva-euk-28s-database-id98.fasta $SORTMERNADIR/rRNA_databases/phix.fasta"
                # Sets output for rRNA :
                rrna_path = os.path.join(self.smr_outdir, pair[0].split(".")[0][:-2] + "_rrna_out.fq")
                smr_cmd += " --aligned " + rrna_path
                # Sets output for clean :
                clean_path = os.path.join(self.smr_outdir, pair[0].split(".")[0][:-2] + "_clean_out.fq")
                smr_cmd += " --other " + clean_path
                # Sets nber of threads
                number_of_threads = 1
                smr_cmd += " --fastx --paired_in --log -v -a " + str(number_of_threads) + "\n"
                
                # Compress the reads from the pair
                smr_cmd += "gzip " + read1[:-3] + "\n"
                smr_cmd += "gzip " + read2[:-3] + "\n"
                # Compress the output from the SortMeRna
                smr_cmd += "gzip " + rrna_path + "\n"
                smr_cmd += "gzip " + clean_path
                
                   
                # Creates a file.sh for the runner
                self.create_script_file(pair[0], smr_cmd)
                
                print("Generation done--") 
        
        for filename in self.filehandler.infiles:
            # Adds SortMeRna in the ran_test section of the filehandler info dictionary
            self.filehandler.ran_module(filename, "SortMeRna", None)
                
            
    def create_script_file(self, filename, script_string):
        # Creates a file path for fastqc_filename.sh
        scriptfile = "sortmerna_" + filename.split(".")[0] + ".sh"
        script = os.path.join(self.smr_scripts_dir, scriptfile)
        # Adds the filepath to the script dict in the FileHandler
        self.filehandler.script_dict[filename].append(script)
        # Creates and open the fastqc_filename.ext.sh file
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