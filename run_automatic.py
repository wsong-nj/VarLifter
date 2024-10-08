#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:49:30 2023

@author: lyc
"""
#This script is responsible for automated batch analysis of contracts
import os
import re
from solcx import compile_files
from solcx import get_installed_solc_versions
from solcx import set_solc_version
import VaTy_Lifter

import multiprocessing


def get_contract_version(contract_file):
    with open(contract_file, 'r') as f:
        content = f.read()
        version_match = re.search(r"pragma solidity (.+?);", content)
        if version_match:
            version = version_match.group(1)
            version = version.strip()
            version = re.sub(r'\s+', '', version)
            version = re.sub(r'\^', '', version)
            version = version.replace('"', '')
            version = version.replace('"', '')
            if version == '0.5.00':
                version = '0.5.0'
            if '>=' in version:
                version = version.lstrip('>= ').strip()
            if '=' in version:
                version = version.lstrip('= ').strip()
            if '<' in version:
                version = version.split('<')[0].strip()
            if '>' in version:
                version = "0.4.25"
            if version == '0.5':            
                version = "0.5.0"

                
            version = version.strip()
            version_parts = re.findall(r'\d+', version)
            
            try:
                version_parts = [int(part) for part in version_parts]
            except Exception:
                return "0.4.17"
            
            target_version = [0, 4, 11]
            
            if version_parts < target_version:
                return "0.4.25"
            else:
                return version
        else:
            return "0.4.25"


def run_analysis():
    VaTy_Lifter.run_analysis()


contract_source_folder = "/home/Lifting Variables & Their Tpyes from Smart Contract Bytecode"
bytecode_lifted_folder = "/home/Lifting Variables & Their Tpyes from Smart Contract Bytecode"


for filename in os.listdir(contract_source_folder):
    if filename.endswith(".sol"):
        source_file_path = os.path.join(contract_source_folder, filename)
        result_file_name = f"{filename.replace('.sol', '')}_lifted.txt"
        destination_file_path = os.path.join(bytecode_lifted_folder, result_file_name)
        
        if result_file_name in os.listdir(bytecode_lifted_folder):
            #print('already have this contract')
            continue
        
        set_solc_version(get_contract_version(source_file_path))

        try:
            compiled_contracts = compile_files([source_file_path])
        except Exception as e:
            print(f"Compilation error：{e}")
            continue

        runtime_bytecode_dict = {}

        for contract_name, contract_data in compiled_contracts.items():
            runtime_bytecode = contract_data['bin-runtime']
            runtime_bytecode_dict[contract_name] = runtime_bytecode
            
        for key, value in runtime_bytecode_dict.items():
            if len(value) == 0 or 'SafeMath' in key:
                
                continue
            
            with open('input_bytecode', 'w') as f:
                f.write(value)

            p = multiprocessing.Process(target=run_analysis)
            p.start()
            p.join(30)
            
            if p.is_alive():
                p.terminate()
                print(f"{key}: out of time")
                continue

            try:
                with open('output_VaTy.txt', 'r') as f2:
                    content = f2.read()
                with open(destination_file_path, 'a') as f1:
                    f1.write(key + ":" + "\n")
                    f1.write(content)
            except Exception as e:
                print(f"Error writing result file：{e}")
                continue

                             
            


                                    

                
                

                




            
            


