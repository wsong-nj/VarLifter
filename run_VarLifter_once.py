#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 21:38:18 2024

@author: lyc
"""


import io
import sys
import time
import re
from type_analyzer_for_state_variables import RulesForPublicStateVars
import path_through_function
import function_signature_hash_extractor
from variables_read_write_analysis import Analyzer
import vaty_analyzer_for_public_function
from disassembler import Disassembler
from missing_slot_analysis import MissingSlot
from VaTy_Lifter import VaTyLifter

def run_analysis():
    with open('input_bytecode') as f:
        line = f.readline().strip()
    dis = Disassembler(line)
    with open('disassembly_result.txt', 'w') as f:
        pass
    dis.debug_bytecodes()

    start_time = time.time()
    VaTy_lift = VaTyLifter()
    public_states_VaTy = VaTy_lift.states_functions_separate()
    public_functions_VaTy = VaTy_lift.public_function_lift()

    slot_list = []
    for item in public_states_VaTy:
        pattern_1 = r'slot\((0x[0-9A-Fa-f]+)\)'
        match_1 = re.findall(pattern_1, item)
        if match_1:
            for match in match_1:
                slot_list.append(match)
            
    for item in public_functions_VaTy:
        pattern_2 = r'slot\((0x[0-9A-Fa-f]+)\)'
        match_2 = re.findall(pattern_2, item)
        if match_2:
            for match in match_2:
                slot_list.append(match)
            
    sorted_slot_list = sorted(slot_list, key=lambda x: int(x, 16))
    missing_slots = []
    if len(sorted_slot_list) > 0 and sorted_slot_list[0] == '0x2':
        missing_slots.append('0x1')
        missing_slots.append('0x0')
    if len(sorted_slot_list) > 0 and sorted_slot_list[0] == '0x1':
        missing_slots.append('0x0')    
    for i in range(len(sorted_slot_list) - 1):
        current_slot = int(sorted_slot_list[i], 16)
        next_slot = int(sorted_slot_list[i + 1], 16)
        if next_slot - current_slot > 1:
            missing_slots.extend([hex(slot) for slot in range(current_slot + 1, next_slot)])
    for slot in missing_slots:
        #print(slot)
        public_states_VaTy.append(MissingSlot(slot).slot_search())

    with open("output_VaTy.txt", "w") as f:
        for item in public_states_VaTy:
            f.write(item + "\n")
        for item in public_functions_VaTy:
            f.write(item + "\n")
        end_time = time.time()
        run_time = end_time - start_time
        f.write(f"Time Consumption: {run_time:.6f} S" + "\n")

if __name__ == '__main__':
    run_analysis()