#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:53:17 2023

@author: lyc
"""

import re

class FunctionSignatureHashExtractor:
    def __init__(self, asm_file):
        self.asm_file = asm_file
    def extract_function_signatures(self):
        function_signatures = []
        with open(self.asm_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            current_block = None
            for line in lines:
                if line.startswith("block"):
                    # Extract the lines starting with block, such as "block-0", "block_1", and so on
                    current_block = line.strip()
                else:
                    # Extract function signature hash value
                    if ("PUSH4" or "PUSH3") in line and "DUP1" in lines[lines.index(line) - 1] and \
                       "EQ" in lines[lines.index(line) + 1] and \
                       "PUSH" in lines[lines.index(line) + 2] and \
                       "JUMPI" in lines[lines.index(line) + 3]:
                        # Using regular expressions to match operands after "PUSH4"
                        match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", line)
                        if match:
                            function_signature = match.group(1)
                            #function_signature = match.group(2)
                            #function_signatures.append((current_block, function_signature))
                            function_signatures.append(str(function_signature))
                    if "DUP2" in line and ("PUSH4" or "PUSH3") in lines[lines.index(line) - 1] and \
                       "EQ" in lines[lines.index(line) + 1] and \
                       "PUSH" in lines[lines.index(line) + 2] and \
                       "JUMPI" in lines[lines.index(line) + 3]:
                        match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", line)
                        if match:
                            function_signature = match.group(1)
                            #function_signature = match.group(2)
                            function_signatures.append(str(function_signature))
                    if ("PUSH4" in line or "PUSH3" in line)  and "DUP1" in lines[lines.index(line) - 1] and \
                       "EQ" in lines[lines.index(line) + 1] and \
                       "REQUIRE" in lines[lines.index(line) + 2] and \
                       "PUSH" in lines[lines.index(line) + 3] and \
                       "JUMP" in lines[lines.index(line) + 4]: 
                        match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", line)
                        if match:
                            function_signature = match.group(1)
                            #function_signature = match.group(2)
                            function_signatures.append(str(function_signature))                
                    if "DUP2" in line and ("PUSH4" or "PUSH3") in lines[lines.index(line) - 1] and \
                       "EQ" in lines[lines.index(line) + 1] and \
                       "REQUIRE" in lines[lines.index(line) + 2] and \
                       "PUSH" in lines[lines.index(line) + 3] and \
                       "JUMP" in lines[lines.index(line) + 4]:
                        match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", line)
                        if match:
                            function_signature = match.group(1) 
                            #function_signature = match.group(2)
                            function_signatures.append(str(function_signature))    
                    if "0xffffffff" in line and "AND" in lines[lines.index(line) + 1] and \
                       "DUP1" in lines[lines.index(line) +2] and \
                       ("PUSH4" or "PUSH3") in lines[lines.index(line) +3] and \
                       "EQ" in lines[lines.index(line) +4] :
                        match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", lines[lines.index(line) +3])
                        if match:
                            function_signature = match.group(1) 
                            #function_signature = match.group(2)
                            function_signatures.append(str(function_signature)) 
                    if "DUP2" in line and ("PUSH4" or "PUSH3") in lines[lines.index(line) - 1] and \
                       "EQ" in lines[lines.index(line) + 1] and \
                       "REQUIRE" in lines[lines.index(line) + 2] and \
                       "PUSH" in lines[lines.index(line) + 3] and \
                       "JUMP" in lines[lines.index(line) + 4]:
                        match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", lines[lines.index(line) - 1])
                        if match:
                            function_signature = match.group(1) 
                            #function_signature = match.group(2)
                            function_signatures.append(str(function_signature))   
                    if 'PUSH4' in line and 'DUP2' in lines[lines.index(line) + 1] and \
                       'EQ' in lines[lines.index(line) + 2] and \
                       'PUSH' in lines[lines.index(line) + 3] and \
                       'JUMPI' in lines[lines.index(line) + 4]:
                        match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", line)
                        if match:
                            function_signature = match.group(1) 
                            function_signatures.append(str(function_signature))     
                    

                    index = lines.index(line)
                    if index + 1 < len(lines) and index + 2 < len(lines) and index + 3 < len(lines) and index + 4 < len(lines):
                        if ('PUSH3' in line or 'PUSH4' in line) and 'DUP2' in lines[index + 1] and \
                            'EQ' in lines[index + 2] and \
                            'PUSH' in lines[index + 3] and \
                            'JUMPI' in lines[index + 4]:
                            match = re.search(r"PUSH[3|4]\s+(0x[0-9A-Fa-f]+)", line)
                            if match:
                                function_signature = match.group(1) 
                                function_signatures.append(str(function_signature))
                            
                            
                            
        unique_function_signatures = list(dict.fromkeys(function_signatures))
        return unique_function_signatures


if __name__ == '__main__':
    
    asm_file = 'disassembly_result.txt'
    fshe = FunctionSignatureHashExtractor(asm_file)
    signatures_hash = fshe.extract_function_signatures()
    print(signatures_hash)
    print(len(signatures_hash))