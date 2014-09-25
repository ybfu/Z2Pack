#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@ethz.ch>
# Date:    13.08.2014 12:02:54 CEST
# File:    abinit_run.py

import abinit.read_mmn as mmn
import abinit.abinit_input_io as io
import abinit.wannier90_input as wannier90_input

import os
import sys
import subprocess

#-----------------------------------------------------------------------#
#                                                                       #
#                                                                       #
#-----------------------------------------------------------------------#
class AbinitRun:
    """
    AbinitRun Class
    ~~~~~~~~~~~~~~~
    Creates input files and makes calls to ABINIT
    
    methods: scf, nscf
    """
    def __init__(   self, 
                    name,
                    common_vars, 
                    psps_files, 
                    working_folder, 
                    num_occupied,
                    abinit_command = "abinit"
                ):
        """
        args:
        ~~~~
        name:               name of the system
        common_vars:        variables to be applied for scf and nscf
        psps_files:         path to pseudopotential file or list of
                            paths to psp files
        working_folder:     path to 'build' folder
        num_occupied:       number of occupied bands
        abinit_command:     command to execute ABINIT
        """
        self._name = name
        self._calling_path = os.getcwd()
        self._common_vars = common_vars
        if(working_folder[0] == "/" or working_folder[0] == "~"): # absolute
            self._working_folder = working_folder
        else: #relative
            self._working_folder = self._calling_path + '/' + working_folder
        if(isinstance(psps_files, str)):
            if(psps_files[0] == "/" or psps_files[0] == "~"): # absolute
                self.psps_files = psps_files
            else: # relative
                self.psps_files = self._calling_path + '/' + psps_files
        else:
            self.psps_files = []
            for psps_file in psps_files:
                if(psps_file[0] == "/" or psps_file[0] == "~"): # absolute
                    self.psps_files.append(psps_file)
                else: # relative
                    self.psps_files.append(self._calling_path + '/' + psps_file)
                    
        # create working folder if it doesn't exist
        if not(os.path.isdir(self._working_folder)):
            subprocess.call("mkdir " + self._working_folder, shell = True)
        
        self.abinit_command = abinit_command
        self.num_occupied = num_occupied
        
    def _abinit_run  (   self, 
                            subfolder,
                            tag = "", 
                            input_wfct_path = None,
                            additional_args = {},
                            create_wannier90_input = False,
                            clean_subfolder = True,
                            setup_only = False
                        ):
        data = {}
        data.update(self._common_vars)
        data.update(additional_args)
        subfolder = self._working_folder + '/' + subfolder
        run_name = self._name + tag
        
        # print input file(s) to working_folder
        if(clean_subfolder):
            try:
                subprocess.call("rm -rf " + subfolder +  "/*", shell = True) 
            except:
                pass
        
        if not(os.path.isdir(subfolder)):
            subprocess.call("mkdir " + subfolder, shell = True)
        io.produce_input(data, subfolder + "/" + run_name + ".in")
        
        if(create_wannier90_input):
            if(self.num_occupied is None):
                raise ValueError('number of occupied bands not set')
            wannier90_input.write_input(self.num_occupied, data['nband'], subfolder + '/wannier90.win')
            
        # get correct runtime input
        abinit_runtime_input = run_name + ".in\n" + run_name + ".out\n"
        
        if(input_wfct_path is None):
            abinit_runtime_input += run_name + "_i\n"
        else:
            abinit_runtime_input += self._working_folder + "/" + input_wfct_path + "\n"
            
        abinit_runtime_input += run_name + "_o\n" + run_name + "_\n"
        
        if(isinstance(self.psps_files, str)):
            abinit_runtime_input += self.psps_files+ "\n"
        else:
            for psps_file in self.psps_files:
                abinit_runtime_input +=  psps_file + "\n"
        
        f = open(subfolder + "/" + run_name + ".files", "w")
        f.write(abinit_runtime_input)
        f.close()

        # ABINIT run
        if not(setup_only):
            subprocess.call(self.abinit_command + " < " + run_name + ".files" + " >& log", cwd = subfolder, shell = True)
        

    def scf(self, scf_args = {}, setup_only = False, abinit_args = {}, **kwargs):
        """
        creates input for SCF run and executes it
        
        args:
        ~~~~
        scf_args:           input for SCF only (not in common variables)
        
        kwargs:
        ~~~~~~
        setup_only:         only create input files, without execution
        abinit_args:        additional arguments for ABINIT
                            takes precedence over arguments from the 
                            input file (prtden: 1 is enforced)
        """
        scf_args.update(abinit_args)
        scf_args.update({'prtden': 1})
        self._abinit_run("work_scf_" + self._name, tag = "_scf", additional_args = scf_args, setup_only = setup_only, **kwargs)
        
    def nscf(   self,
                string_dir, 
                string_pos, 
                string_N, 
                **kwargs 
                ):
        """
        creates input for NSCF run and executes it
        
        args:
        ~~~~
        string_dir:         axis along which string lies
        string_pos:         [a, b] -> shiftk [0, a, b] if string_dir = 0, 
                            [a, 0, b] if string_dir = 1, 
                            [a, b, 0] if string_dir = 2
        
        kwargs:             additional variables passed to ABINIT
        ~~~~~~
        """
                    
        # prepare additional_args
        string_begin = list(string_pos) # avoid immutables
        string_end = list(string_pos)
        string_begin.insert(string_dir, 0)
        string_end.insert(string_dir, 1)
        ngkpt = [1, 1, 1]
        ngkpt[string_dir] = string_N
        string_pos.insert(string_dir,0.0)
        string_args = {'kptopt': 3}
        string_args.update({"ngkpt": ngkpt})
        string_args.update({"nshiftk": 1})
        string_args.update({"shiftk": string_pos})
        
        # global nscf variables
        nscf_args = {}
        nscf_args.update({"iscf": -2})
        nscf_args.update({"tolwfr": 1e-21})
        nscf_args.update({"irdwfk": 1})
        nscf_args.update({"irdden": 1})
        nscf_args.update({"prtwant": 2})
        nscf_args.update({"nstep": 100})
        
        nscf_args.update(string_args)
        nscf_args.update(kwargs)
        

        # clean out working directory
        subfolder = "work_nscf_" + self._name
        
        # call to abinit_run
        self._abinit_run( 
                    subfolder,
                    tag = "_nscf",
                    input_wfct_path = "work_scf_" + self._name + "/" + self._name + "_scf_o", 
                    additional_args = nscf_args, 
                    create_wannier90_input = True,
                    clean_subfolder = True
                    )
        # read in mmn
        M = mmn.getM(self._working_folder + '/' + subfolder + "/wannier90.mmn")
        return M

    