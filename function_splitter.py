#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 20:55:12 2023

@author: lyc
"""
import io
import sys
import re
from type_analyzer_for_state_variables import RulesForPublicStateVars
import path_through_function
import function_signature_hash_extractor
from variables_read_write_analysis import Analyzer

def check_output(func):
    original_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    func()

    sys.stdout = original_stdout
    output_content = captured_output.getvalue()

    if output_content.strip() == "":
        return False
    else:
        return True

def call_all_rules():
    public_states = []
    asm_file = 'disassembly_result.txt'
    fun_sig = function_signature_hash_extractor.FunctionSignatureHashExtractor(asm_file)
    signature_list = fun_sig.extract_function_signatures()
    tf_path = path_through_function.PathThroughFunction(asm_file)
    """
    indices_to_remove = [5, 11, 13, 18, 24, 25, 26, 28, 30]  
    indices_to_remove.sort(reverse=True)
    for index in indices_to_remove:
        if 0 <= index < len(signature_list):
            del signature_list[index]
    """
    for signature in signature_list:
        
        function_path = tf_path.TFPath(signature)
        #print(function_path)
        analyzer = Analyzer()
        data_lifitime = analyzer.block_analysis(function_path)
        #print(data_lifitime)
        stackvariable_lifetime =  data_lifitime[0]
        calldata_lifetime = data_lifitime[1]
        mvalue_lifetime = data_lifitime[2]
        memory_log = data_lifitime[3]
        svalue_lifetime = data_lifitime[4]
        #print('***********')
        #print(stackvariable_lifetime)
        #break
        rule = RulesForPublicStateVars(stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime)
        exception_count = 0
        
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
            #print(_type)
            pattern = r'//slot'
            match = re.search(pattern, str(_type))
            #print('1')
            if match:
                #print('1')
                public_states.append('<%s> %s' % (signature, _type))
                #print('<%s> %s' % (signature, _type))
                continue
        except Exception:
            #print(f"Exception occurred: {e}")
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
            _type = rule.rule_for_struct()
            public_states.append('<%s> %s' % (signature, _type))
        except Exception:
            exception_count += 1  
        
        if exception_count == 11:
            public_states.append('%s needs futher process' % signature)
            #print('%s needs futher process' % signature)
            
    return public_states
    
    
if __name__ == "__main__":
    result = call_all_rules()
    for item in result:
        print(item)
    
    
    
    
    