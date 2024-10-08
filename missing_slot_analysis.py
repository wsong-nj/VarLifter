#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:49:30 2023

@author: lyc
"""

import re

class MissingSlot:
    def __init__(self, missing_slot):
        self.missing_slot = missing_slot

    def read_file_as_list(self, file_path):
        result = []  

        with open(file_path, 'r') as f:
            for line in f:
                result.append(line.strip())

        return result



    def slot_search(self):
        asm_file = 'disassembly_result.txt'
        asm_list = self.read_file_as_list(asm_file)
        #print(asm_list)
        for index, codeline in enumerate(asm_list[:-1]):
            
            codeline_1 = codeline.replace(" ", "")
            codeline_2 = asm_list[index + 1].replace(" ", "")
            pattern_slot_number = r'PUSH1.*?{}'.format(re.escape(self.missing_slot))
            pattern_slot_load = r'0x[0-9A-Fa-f]+.*?SLOAD'
            match_slot_number = re.search(pattern_slot_number, codeline_1)
            match_slot_load = re.search(pattern_slot_load, codeline_2)
            if self.missing_slot in codeline and match_slot_number and match_slot_load and '0xff' not in asm_list[index+2]:
                return 'uint256 slot(%s)' % self.missing_slot

                    
            if self.missing_slot in codeline and match_slot_number and match_slot_load and '0xff' in asm_list[index+2]:
                if 'AND' in asm_list[index+3] and 'ISZERO' in asm_list[index+4]:
                    return 'bool slot(%s)' % self.missing_slot
            if self.missing_slot in codeline and match_slot_number and match_slot_load:                                
                for item in [asm_list[index+1], asm_list[index+2], asm_list[index+3], asm_list[index+4], asm_list[index+5], asm_list[index+6], asm_list[index+7], asm_list[index+8], asm_list[index+9], asm_list[index+10]]:
                    if item.endswith('0xa0'):
                        #print(item)
                        return 'address slot(%s)' % self.missing_slot
            if self.missing_slot in codeline and match_slot_number and match_slot_load:
                if asm_list[index + 2].endswith('0xffffffffffffffffffffffffffffffffffffffff'):
                    return 'address slot(%s)' % self.missing_slot   
                                
                

        return 'missing slot(%s)' % self.missing_slot

            





    





