#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 21:52:54 2023

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

class VaTyLifter:
    def __init__(self):        
        self.public_states_VaTy = []
        self.public_functions_VaTy = []
        self.public_functions = []
        #self.public_functions_lift = vaty_analyzer_for_public_function.PublicFunctionAnalyzer(stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime)

    
    def public_states_lift(self):
        public_states = []
        asm_file = 'disassembly_result.txt'
        fun_sig = function_signature_hash_extractor.FunctionSignatureHashExtractor(asm_file)
        signature_list = fun_sig.extract_function_signatures()
        tf_path = path_through_function.PathThroughFunction(asm_file)

        for signature in signature_list:
        
            function_path = tf_path.TFPath(signature)
            analyzer = Analyzer()
            data_lifitime = analyzer.block_analysis(function_path)
            stackvariable_lifetime =  data_lifitime[0]
            calldata_lifetime = data_lifitime[1]
            mvalue_lifetime = data_lifitime[2]
            memory_log = data_lifitime[3]
            svalue_lifetime = data_lifitime[4]

            rule = RulesForPublicStateVars(stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime)
            exception_count = 0


            try:
                _type = rule.rule_for_nested_mapping()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                    #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1  
        
            try:
                _type = rule.rule_for_uint()  
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1

            try:
                _type = rule.rule_for_int()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1
    
            try:
                _type = rule.rule_for_address()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                    #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1  
    
            try:
                _type = rule.rule_for_bool()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                    #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1

            try:
                _type = rule.rule_for_bytesN()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                    #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1

            try:
                _type = rule.rule_for_string() 
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                    #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1

            try:
                _type = rule.rule_for_StaticArray()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1

            try:
                _type = rule.rule_for_DynamicArray()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                    #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1

            try:
                _type = rule.rule_for_mapping()
                pattern = r'//slot'
                match = re.search(pattern, str(_type))
                if match:
                    public_states.append('<%s> %s' % (signature, _type))
                    #print('<%s> %s' % (signature, _type))
                    continue
            except Exception:
                exception_count += 1


    
            try:
                _type = rule.rule_for_struct()
                public_states.append('<%s> %s' % (signature, _type))
            except Exception:
                exception_count += 1  
            
            if exception_count == 11:
                public_states.append('%s needs futher process' % signature)
                #print('%s needs futher process' % signature)
                
        return public_states

    def states_functions_separate(self):
        half_result = self.public_states_lift()
        pattern_states = r'//slot\((0x[0-9A-Fa-f]+)\)'
        pattern_functions = r'\<(0x[0-9A-Fa-f]+)\> None'
        for VaTy in half_result:
            match_states = re.search(pattern_states, VaTy)
            match_functions = re.search(pattern_functions, VaTy)
            
            if match_states:
                self.public_states_VaTy.append(VaTy)
            if match_functions:
                functions = match_functions.group(1)  
                self.public_functions.append(functions)   
                
        order_slot = lambda s: int(re.search(r'//slot\((0x[0-9A-Fa-f]+)\)', s).group(1), 16) 
        self.public_states_VaTy = sorted(self.public_states_VaTy, key=order_slot)
        return(self.public_states_VaTy)


    def public_function_lift(self):

        asm_file = 'disassembly_result.txt'
        #fun_sig = function_signature_hash_extractor.FunctionSignatureHashExtractor(asm_file)
        #signature_list = fun_sig.extract_function_signatures()
        tf_path = path_through_function.PathThroughFunction(asm_file)

        for signature in self.public_functions:
            function_path = tf_path.TFPath(signature)
            analyzer = Analyzer()
            data_lifitime = analyzer.block_analysis(function_path)
            stackvariable_lifetime =  data_lifitime[0]
            calldata_lifetime = data_lifitime[1]
            mvalue_lifetime = data_lifitime[2]
            memory_log = data_lifitime[3]
            svalue_lifetime = data_lifitime[4]
            
            public_functions_lift = vaty_analyzer_for_public_function.PublicFunctionAnalyzer(stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime)
            public_functions_lift.private_states_type_analysis()
            public_functions_lift.stack_value_analysis()
            public_functions_lift.memory_value_analysis()
            public_functions_lift.private_string_constant_analysis()
            public_functions_lift.continuous_slot_analysis()
            
            self.public_functions_VaTy.append('<%s>:%s' % (signature, public_functions_lift.variable_list))   
            
        
        return self.public_functions_VaTy
#The following code is used to execute the tool once and has now been migrated to the run_VarLifter.py module          
"""
    
def run_analysis():
    with open('/home/lyc/Lifting Variables & Their Tpyes from Smart Contract Bytecode/input_bytecode') as f:
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
"""