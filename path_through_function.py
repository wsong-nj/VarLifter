#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 14:52:59 2023

@author: lyc
"""


import EVM_for_path_exploration
from function_signature_hash_extractor import FunctionSignatureHashExtractor

class PathThroughFunction(object):
    def __init__(self, asm_file):
        self.asm_file = asm_file
        self.blocks = self.read_file(asm_file)
        #self.signatures = self.extract_function_signatures(asm_file)
        #self.signature_hash = signature_hash
        #self.entrance = self.find_start_block(signature_hash, asm_file)
        
        
    def read_file(self, asm_file):
        with open(asm_file, 'r') as f:
            content = f.read()

        paragraphs = content.split('\n\n')
        result = {}

        for p in paragraphs:
            lines = p.split('\n')
            index = None
            elements = []
            found_first_line = False

            for line in lines:
                if line.strip() != "":
                    if not found_first_line:
                        index = line.strip()
                        found_first_line = True
                    else:
                        elements.append(line.split())

            if found_first_line:
                result[index] = elements

        return result        
        
    

    def find_start_block(self, signature_hash, asm_file):
        with open(asm_file, 'r') as f:
            lines = f.readlines()
            start_index = -1
            #for hash_value in hash_values:
            for i in range(len(lines)): 
                if str(signature_hash) in lines[i] and ('EQ' in lines[i+1] or 'EQ' in lines[i+2]):
                    start_index = i
                    break
                if start_index != -1:
                    break
            if start_index == -1:
                print("Start block not found in the ASM file.")
                return None

            for j in range(start_index, len(lines)):
                line = lines[j].split()
                if len(line) == 3:
                    index = line[-1]
                    for k in range(j + 1, len(lines)):
                        if lines[k].startswith(index):
                            return lines[k-1].split()[0]

            print("Start block not found in the ASM file.")
            return None


    def TFPath(self, signature_hash):
        function_path = []
        function_path.append(self.find_start_block(signature_hash, self.asm_file))
        evm = EVM_for_path_exploration.EVM()
        execute_block_number = self.find_start_block(signature_hash, self.asm_file)
        #print(self.find_start_block(signature_hash, self.asm_file))
        sign = ''
        stack = []
        while sign not in ('RETURN', 'STOP', 'SELFDESTRUCT'):
        #while sign < 2:
            #JUMP block
            if ((self.blocks[execute_block_number][-1][1] == 'JUMP') and 
                ('AND' not in self.blocks[execute_block_number][-2][1])):        #normal jump
                #print(execute_block_number)
                for codeline in self.blocks[execute_block_number][:-1]:
                    #print(codeline)-['0x30', 'JUMPDEST']
                    #print(len(codeline))
                    if len(codeline) > 2:
                        #print(codeline[1], codeline[2])
                        stack = evm.execute(codeline[1], codeline[2])['stack']
                        #print(stack)
                    else:
                        #print(codeline[1])
                        stack = evm.execute(codeline[1])['stack']
                
                        
                try:
                    next_block_index = stack[-1]
                except IndexError:
                    print("Error: The stack is empty.") 
                #print(stack)
                stack = evm.execute('JUMP')['stack']
                #print(stack)
                for key, value in self.blocks.items():
                    first_item_for_sure = 0
                    for sub_value in value[0]:
                        first_item_for_sure += 1
                        if next_block_index == sub_value and first_item_for_sure == 1 :
                            execute_block_number = key
                            #print(execute_block_number)
                            if execute_block_number != 'block_0':
                                function_path.append(execute_block_number)
                            #print(execute_block_number)
                        
            elif (self.blocks[execute_block_number][-1][1] == 'JUMP' and     # wash jump
                self.blocks[execute_block_number][-2][1] == 'AND' and
                'PUSH' in self.blocks[execute_block_number][-3][1] and
                'PUSH' in self.blocks[execute_block_number][-4][1] and
                '0xff' in self.blocks[execute_block_number][-4][2]):
                #print(execute_block_number)
                #print(self.blocks[execute_block_number][-2][1])
                del self.blocks[execute_block_number][-4]
                del self.blocks[execute_block_number][-2]
                for codeline in self.blocks[execute_block_number][:-1]:
                    if len(codeline) > 2:
                        stack = evm.execute(codeline[1], codeline[2])['stack']
                    else:
                        stack = evm.execute(codeline[1])['stack']
                                        
                try:
                    next_block_index = stack[-1]
                except IndexError:
                    print("Error: The stack is empty.") 
                #print(stack)
                stack = evm.execute('JUMP')['stack']
                #print(stack)
                for key, value in self.blocks.items():
                    first_item_for_sure = 0
                    for sub_value in value[0]:
                        first_item_for_sure += 1
                        if next_block_index == sub_value and first_item_for_sure == 1 :
                            execute_block_number = key
                            if execute_block_number != 'block_0':
                                function_path.append(execute_block_number)
                                                            

                            
            # JUMPI block
            elif self.blocks[execute_block_number][-1][1] == 'JUMPI':
                #print(self.blocks[execute_block_number][-1][1])
                #print(execute_block_number)
                #if execute_block_number == 'block_394':
                #    print(stack)
                for codeline in self.blocks[execute_block_number][:-1]:
                    if len(codeline) > 2:
                        #print(codeline[1], codeline[2])
                        stack = evm.execute(codeline[1], codeline[2])['stack']
                        #print(stack)
                    else:
                        #print(codeline[1])
                        stack = evm.execute(codeline[1])['stack']
                        #print(stack)
                try:
                    next_block_index = stack[-1]
                except IndexError:
                    print("Error: The stack is empty.")

                stack = evm.execute('JUMPI')['stack']  
                #print(stack) 
                for key, value in self.blocks.items():
                    first_item_for_sure = 0
                    for sub_value in value[0]:
                        first_item_for_sure += 1
                        if first_item_for_sure == 1 and next_block_index == sub_value and 'REVERT' not in self.blocks[key][-1][1]:
                            execute_block_number = key
                            function_path.append(execute_block_number)
                        elif first_item_for_sure == 1 and next_block_index == sub_value and 'REVERT' in self.blocks[key][-1][1]:
                            block_list = list(self.blocks.keys())
                            execute_block_index = block_list.index(execute_block_number)
                            execute_block_number = block_list[execute_block_index+1]
                            function_path.append(execute_block_number)
                        """
                        else:
                            block_list = list(self.blocks.keys())
                            execute_block_index = block_list.index(execute_block_number)
                            next_block_number = block_list[execute_block_index+1]
                            function_cfg.append(next_block_number) 

                            for values in self.blocks[execute_block_number]:
                                if 'REVERT' not in values:
                                    function_cfg.append(execute_block_number)
                                else:
                                    block_list = list(self.blocks.keys())
                                    execute_block_number = block_list.index('execute_block_number')+1
                                    function_cfg.append(execute_block_number)
                        """
                            
            # order block
            elif self.blocks[execute_block_number][-1][1] not in ['REVERT', 'INVALID', 'JUMP', 'JUMPI']:
                #print(self.blocks[execute_block_number][-1][1])
                #print(execute_block_number)
                #print(blocks[execute_block_number][-1][1])
                for codeline in self.blocks[execute_block_number]:
                    if len(codeline) > 2:
                        #print(codeline[1], codeline[2])
                        evm.execute(codeline[1], codeline[2])['stack']
                    else:
                        #print(codeline[1])
                        evm.execute(codeline[1])['stack']
                block_list = list(self.blocks.keys())
                execute_block_index = block_list.index(execute_block_number)
                execute_block_number = block_list[execute_block_index+1]
                function_path.append(execute_block_number)
                #execute_block_number = block_list.index('execute_block_number')+1
                #function_cfg.append(execute_block_number)
                
            
                                            
            sign = self.blocks[execute_block_number][-1][1]
            
            #if sign == 1:
               #print(execute_block_number)
            #sign = sign + 1
        return function_path


if __name__ == '__main__':
    
    asm_file = 'disassembly_result.txt'
    fshe = FunctionSignatureHashExtractor(asm_file)
    signatures_hash = fshe.extract_function_signatures()
    #print(signatures_hash[30])
    
    cfg = PathThroughFunction(asm_file)
    #print(cfg.find_start_block(signatures_hash[30], asm_file))
     
    
    
    function_path = cfg.TFPath(signatures_hash[4])
    #first_block = cfg.find_start_block(signatures_hash[5], asm_file)
    print(function_path)
    print(len(function_path))
    print(signatures_hash[4])
