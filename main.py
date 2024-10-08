#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 21:43:06 2024

@author: lyc
"""



import argparse
import subprocess
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Bytecode Analyzer Tool")
    parser.add_argument("input_bytecode", type=str, help="Input bytecode string")
    args = parser.parse_args()

    input_bytecode = args.input_bytecode

    # Get the absolute path to the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Write runtime-bytecode into file input_bytecode 
    with open(os.path.join(script_dir, 'input_bytecode'), 'w') as f:
        f.write(input_bytecode)
    
    # Call run_VarLifter using absolute path
    run_VarLifter_path = os.path.join(script_dir, 'run_VarLifter.py')
    subprocess.run(['python3', run_VarLifter_path])

    # Print output
    output_file = os.path.join(script_dir, 'output_VaTy.txt')
    with open(output_file, 'r') as f:
        output = f.read()
        print(output)

if __name__ == "__main__":
    main()


"""
import argparse
import subprocess
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Bytecode Analyzer Tool")
    parser.add_argument("input_bytecode", type=str, help="Input bytecode string")
    args = parser.parse_args()

    input_bytecode = args.input_bytecode

    # Get the absolute path to the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the directory containing main.py to the Python path
    sys.path.append(script_dir)

    # Write runtime-bytecode into file input_bytecode 
    with open(os.path.join(script_dir, 'input_bytecode'), 'w') as f:
        f.write(input_bytecode)
    
    # Call main function from main.py using absolute import
    from main import main as run_main
    run_main()

    # Print output
    output_file = os.path.join(script_dir, 'output_VaTy.txt')
    with open(output_file, 'r') as f:
        output = f.read()
        print(output)

if __name__ == "__main__":
    main()

"""