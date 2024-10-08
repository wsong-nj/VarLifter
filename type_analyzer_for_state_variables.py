#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:23:51 2023

@author: lyc
"""


import path_through_function
import function_signature_hash_extractor
import variables_read_write_analysis
from type_base import TypeBase
import re
class RulesForPublicStateVars:
    def __init__(self, stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime):
        self.stackvariable_lifetime = stackvariable_lifetime
        self.calldata_lifetime = calldata_lifetime
        self.mvalue_lifetime = mvalue_lifetime
        self.memory_log = memory_log
        self.svalue_lifetime = svalue_lifetime
        self.type = TypeBase()
        
    def rule_for_uint(self):
        result = []
        stack_rule_list = ['0x1<<', 'as slot index', '+(mvalue(0x40))', 'ff & svalue(0x0)']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        if (len(set(mvalue)) == 1 and 'mvalue(0x40)' in set(mvalue)):
           #any('0x20 + mvalue(0x40)' in life for life in mvalue_life)):
               mvalue_lifetime_rule = True
               
        sign_differ_bool = 0
        for lifetime in self.svalue_lifetime[0]:
            if '==0?' not in lifetime:
                sign_differ_bool += 1
               
        memory_log_rule = False                                       #mlog rules
        if ('load_0x40' in self.memory_log[0] and 
            'storein_mvalue(0x40)' in self.memory_log[1] and
            'load_0x40' in self.memory_log[2]):
            memory_log_rule = True
        #print(mvalue_lifetime_rule)
        if(stack_rule_compliance_level >= 1 and
           len(self.calldata_lifetime) == 0 and
           mvalue_lifetime_rule and 
           memory_log_rule and
           sign_differ_bool == len(self.svalue_lifetime[0])):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_modern = r'\(?\(0x1\)<<\((0x[0-9A-Fa-f]+)\)-0x1\)?&\(?svalue\((0x[0-9A-Fa-f]+)\)\)?'
                pattern_classic = r'(0x[fF]+)\)?&\(?svalue\((0x[0-9A-Fa-f]+)\)'
                matches = re.findall(pattern_modern + "|" + pattern_classic, svalue_lifetime_without_spaces)
                if matches:
                    for match in matches:
                        if match[0]:
                            mask = match[0]
                            slot = match[1]
                            type_looking = self.type.uint_base(mask)
                        elif match[2]:
                            mask = match[2]
                            slot = match[3]
                            type_looking = self.type.uint_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))
                    if len(set(result)) == 1 and len(result) >= 2:
                        return(next(iter(set(result))))
                        
            for log in self.memory_log:
                pattern_slot = r'svalue\((0x[0-9A-Fa-f]+)\)'
                match_slot = re.search(pattern_slot, log)
                if match_slot:
                    slot = match_slot.group(1)
                    break
            uint_count = 0
            for lifetime in self.svalue_lifetime[0]:
                if('<<' not in lifetime and
                   '&' not in lifetime):
                    uint_count += 1
                if uint_count == len(self.svalue_lifetime[0]):
                    result.append('uint256 //slot(%s)' % slot)
                    return(next(iter(set(result))))
                    
        #else:
        #    print('oops')
                
    def rule_for_int(self):
        result = []
        stack_rule_list = [ 'as slot index', 'as size for svalue(', '_sigextend', '+(mvalue(0x40))']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        if (len(set(mvalue)) == 1 and 'mvalue(0x40)' in set(mvalue) and
           any('0x20 + mvalue(0x40)' in life for life in mvalue_life)):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        if ('load_0x40' in self.memory_log[0] and 
            'storein_mvalue(0x40)' in self.memory_log[1] and
            'load_0x40' in self.memory_log[2]):
            memory_log_rule = True

        if(stack_rule_compliance_level >= 4 and
           len(self.calldata_lifetime) == 0 and
           mvalue_lifetime_rule and memory_log_rule):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern = r'\((0x[0-9A-Fa-f]+)\)?sig_ext\(?svalue\((0x[0-9A-Fa-f]+)\)'
                match = re.search(pattern, svalue_lifetime_without_spaces)
                if match:
                    mask = match.group(1)
                    slot = match.group(2)
                    type_looking = self.type.int_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))
            if len(set(result)) == 1 and len(result) >= 1:
                return(next(iter(set(result))))
        #else:
        #    print('oops')

    def rule_for_address(self):
        result = []
        stack_rule_list = [ 'as slot index', '^--']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        if (len(set(mvalue)) >= 1 and 'mvalue(0x40)' in set(mvalue)):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        if ('load_0x40' in self.memory_log[0] and
            '& svalue(0x' in self.memory_log[1] and
            'storein_mvalue(0x40)' in self.memory_log[1] and
            'load_0x40' in self.memory_log[2]):
            memory_log_rule = True
        #print(mvalue_lifetime_rule)   
        if(stack_rule_compliance_level >= 2 and
           len(self.calldata_lifetime) == 0 and
           mvalue_lifetime_rule and memory_log_rule):
            #print('1')
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_address = r'0x.*?\^0xa0.*?&svalue\((0x[0-9A-Fa-f]+)\)'
                #0x2^0xa0 - 0x1 & svalue(0x2)
                match = re.search(pattern_address, svalue_lifetime_without_spaces)
                if match:
                    
                    slot = match.group(1)
                    mask = '0xa0'
                    type_looking = self.type.address_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))
            if len(set(result)) == 1 and len(result) >= 1:
                return(next(iter(set(result))))
            
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_address_modern = r'0xffffffffffffffffffffffffffffffffffffffff&svalue\((0x[0-9A-Fa-f]+)\).*?0x100\^0x'
                #0xffffffffffffffffffffffffffffffffffffffff & svalue(0x0) /0x100^0x0
                match = re.search(pattern_address_modern, svalue_lifetime_without_spaces)
                if match:                   
                    slot = match.group(1)
                    mask = '0xa0'
                    type_looking = self.type.address_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))
            if len(set(result)) == 1 and len(result) >= 1:
                return(next(iter(set(result))))            
            
                
    def rule_for_bool(self):
        result = []
        stack_rule_list = [ 'as slot index', '0xff', '__&svalue(0x', '+(mvalue(0x40))']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        if (len(set(mvalue)) == 1 and 'mvalue(0x40)' in set(mvalue)):
           #any('0x20 + mvalue(0x40)' in life for life in mvalue_life)):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        if ('load_0x40' in self.memory_log[0] and
            '0xff & svalue(0x' in self.memory_log[1] and
            '==0?==0?' in self.memory_log[1] and
            'storein_mvalue(0x40)' in self.memory_log[1] and
            'load_0x40' in self.memory_log[2]):
            memory_log_rule = True
        #print(mvalue_lifetime_rule)   
        if(stack_rule_compliance_level >= 3 and
           len(self.calldata_lifetime) == 0 and
           mvalue_lifetime_rule and memory_log_rule):
            #print('diu')
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                #0xff & svalue(0x0) /0x10000000000000000000000000000000000000000==0?)==0?
                pattern_0 = r'0xff&svalue\((0x[0-9A-fa-f]+)\).*?==0\?\)==0\?'
                match_0 = re.search(pattern_0, svalue_lifetime_without_spaces)
                if match_0:
                    slot = match_0.group(1)
                    mask = 'double iszero'
                    type_looking = self.type.bool_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))                
                pattern = r'\(0xff&svalue\((0x[0-9A-Fa-f]+)\)(/0x100\^0x0)?==0\?\)==0\?'
                match = re.search(pattern, svalue_lifetime_without_spaces)
                if match:
                    slot = match.group(1)
                    mask = 'double iszero'
                    type_looking = self.type.bool_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))
            if len(set(result)) == 1 and len(result) >= 1:
                return(next(iter(set(result))))
        #else:
        #    print('oops')
                            
    def rule_for_bytesN(self):
        result = []
        stack_rule_list = [ '(0x100)^--', 'as slot index', '__^(0x0)', '(mvalue(0x40))', '<<__', '__<<', '~__']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        if (len(set(mvalue)) <= 2 and
            'mvalue(0x40)' in set(mvalue) and
            ('mvalue(0x40) + 0x0' in set(mvalue) or 'mvalue(0x40) + 0x0' not in set(mvalue)) and
            any('0x20 + mvalue(0x40)' in life for life in mvalue_life or '(mvalue(0x40) + 0x20)' in life for life in mvalue_life)):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        pattern = r"0x[f]+[0]+"
        match = re.search(pattern, self.memory_log[1])
        if ('load_0x40' in self.memory_log[0] and
            (match or 'NOT' in self.memory_log[1]) and                 #watch the using of 'match'
            'storein_mvalue(0x40)' in self.memory_log[1] and
            'load_0x40' in self.memory_log[2]):
            memory_log_rule = True
            
        if(stack_rule_compliance_level >= 5 and
           len(self.calldata_lifetime) == 0 and
           mvalue_lifetime_rule and memory_log_rule):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_modern = r'\(svalue\((0x[0-9A-Fa-f]+)\)(\/0x100\^0x0)?\)<<\((0x[0-9A-Fa-f]+)\)'
                match = re.search(pattern_modern, svalue_lifetime_without_spaces)
                if match:
                    slot = match.group(1)
                    mask = match.group(3)
                    type_looking = self.type.bytesN_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))
                pattern_classic = r'NOT(0x[f]+)&.+svalue\((0x[0-9A-Fa-f]+)\)'
                match = re.search(pattern_classic, svalue_lifetime_without_spaces)
                if match:
                    mask = match.group(1)
                    slot = match.group(2)
                    type_looking = self.type.bytesN_base(mask)
                    result.append('%s //slot(%s)' % (type_looking, slot))
            if len(set(result)) == 1 and len(result) >= 1:
                return(next(iter(set(result))))
        #else:
        #    print('oops')

    def rule_for_StaticArray(self):
        result = []
        stack_rule_list = [ 'as CDL_offset', '(CallDataSize - 0x4)$<', 'CallData(0x', '<__?', '0xf1', 'svalue(CallData(', '<<', 'sigextend']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        calldata_rule_compliance_level = 0        #calldata rules                
        if len(self.calldata_lifetime) == 1:                       
            pattern_1 = r'\(CallData\((0x[0-9A-Fa-f]+)\)\)<\((0x[0-9A-Fa-f]+)\)\?'  
            #(CallData(0x4))<(0x3)?
            pattern_2 = r'\(CallData\(0x4\)\)\+\((0x[0-9A-Fa-f]+)\)'    
            #(CallData(0x4))+(0x0)
            #(CallData(0x4))+(0x0)
            for lifetime in self.calldata_lifetime[0]:
                lifetime_without_spaces = lifetime.replace(" ", "")
                match_1 = re.search(pattern_1, lifetime_without_spaces)
                if match_1:
                    #print('4')
                    length = match_1.group(2)
                    #print(length)
                    calldata_rule_compliance_level += 1
                    break
            for lifetime in self.calldata_lifetime[0]:
                lifetime_without_spaces = lifetime.replace(" ", "")
                match_2 = re.search(pattern_2, lifetime_without_spaces)
                if match_2:
                    #print('3')
                    slot = match_2.group(1)
                    calldata_rule_compliance_level += 1
                    break

        if len(self.calldata_lifetime) == 2:                      #nest array calldata rules
            nestarray_calldata_rule_compliance_level = 0
            pattern_1 = r'\(CallData\(0x4\)\)<\((0x[0-9A-Fa-f]+)\)\?'  
            #(CallData(0x4))<(0x6)?
            pattern_2 = r'\(CallData\((0x4\+0x20|0x24)\)\)<\((0x[0-9A-Fa-f]+)\)\?'    
            #(CallData(0x4 + 0x20))<(0x7)?
            #(CallData(0x24))<(0x7)?
            for lifetime in self.calldata_lifetime[0]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_1 = re.search(pattern_1, calldata_lifetime_without_spaces)
                if match_1:
                    outside_length = match_1.group(1)
                    nestarray_calldata_rule_compliance_level += 1
                    break
            for lifetime in self.calldata_lifetime[1]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_2 = re.search(pattern_2, calldata_lifetime_without_spaces)
                if match_2:
                    inside_length = match_2.group(2)
                    nestarray_calldata_rule_compliance_level += 1
                    break
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        if (len(set(mvalue)) <= 2 and
            'mvalue(0x40)' in set(mvalue)):
            #any('0x20 + mvalue(0x40)' in life for life in mvalue_life or '(mvalue(0x40) + 0x20)' in life for life in mvalue_life)):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        if ('load_0x40' in self.memory_log[0] and
            'svalue(CallData(' in self.memory_log[1] and
            '_storein_mvalue(0x40)' in self.memory_log[1] and 
            'load_0x40' in self.memory_log[2]):
            memory_log_rule = True
            
        #print(memory_log_rule)
        if(stack_rule_compliance_level >= 3 and            #svalue rule   for uint
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           all('NOT' not in log for log in self.memory_log) and
           '==0?==0?' not in self.memory_log[1] and
           memory_log_rule):
            #print('in')
            staticarray_count = 0
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_uint_1 = r"(0x[f]+)\)?&\(?svalue\(CallData"
                match = re.search(pattern_uint_1, svalue_lifetime_without_spaces)
                if match:
                    item_mask = match.group(1)
                    item_type_for_uint = self.type.uint_base(item_mask)
                    result.append('%s[%s] //slot(%s)' % (item_type_for_uint, length, slot))
                    return(next(iter(set(result))))
                    break
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_uint_2 = r"<<\((0x[0-9A-Fa-f]+)\)"   #<<(0xa0)
                match = re.search(pattern_uint_2, svalue_lifetime_without_spaces)
                if match:
                    item_mask = match.group(1)
                    item_type_for_uint = self.type.uint_base(item_mask)
                    result.append('%s[%s] //slot(%s)' % (item_type_for_uint, length, slot))
                    return(next(iter(set(result))))
                    break
            for lifetime in self.svalue_lifetime[0]:
                if ('<<' not in lifetime and
                    '&' not in lifetime):
                    staticarray_count += 1
                if staticarray_count == len(self.svalue_lifetime[0]):
                    result.append('uint256[%s] //slot(%s)' % (length, slot))
                    return(next(iter(set(result))))


        if(stack_rule_compliance_level >= 3 and            #svalue rule   for address
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           all('NOT' not in log for log in self.memory_log) and
           '==0?==0?' not in self.memory_log[1] and
           memory_log_rule):
            #print('in')
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_address = r"\(0x.*?\^0xa0.*?\)&\(svalue\(CallData\("
                #(0x2^0xa0 - 0x1)&(svalue(CallData(0x4) + 0x5)
                match = re.search(pattern_address, svalue_lifetime_without_spaces)
                if match:
                    item_mask = '0xa0'
                    item_type_for_address = self.type.address_base(item_mask)
                    result.append('%s[%s] //slot(%s)' % (item_type_for_address, length, slot))
                    return(next(iter(set(result))))                    
                    
                    

        elif(stack_rule_compliance_level >= 10 and            #rule for string/bytes
           calldata_rule_compliance_level == 2 and
           any('NOT0x1f' in life for life in mvalue_life) and
           any('0xf1' in log for log in self.memory_log)):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_string = r'svalue\(CallData\((0x[0-9A-Fa-f]+)\)\+(0x[0-9A-Fa-f]+)\)' #svalue(CallData(0x4) + 0x0)
                match = re.search(pattern_string, svalue_lifetime_without_spaces)
                if match:
                    slot = match.group(2)
                    result.append('string/bytes[%s] //slot(%s)' % (length, slot))
                    return(next(iter(set(result))))
                    break   


        elif(stack_rule_compliance_level >=8 and            #rule for bytesN
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and
           any('NOT' in log for log in self.memory_log) and
           memory_log_rule):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_morden = r'NOT\(0x[0-9A-Fa-f]+\)<<\((0x[0-9A-Fa-f]+)\)' #NOT(0x1)<<(0xd0)
                match = re.search(pattern_morden, svalue_lifetime_without_spaces)
                if match:
                    item_mask = match.group(1)
                    item_type = self.type.bytesN_base(item_mask)
                    result.append('%s[%s] //slot(%s)' % (item_type, length, slot))
                    return(next(iter(set(result))))
                    break
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_classic = r'NOT(0x[f]+)'                                 #NOT0xfffffffff
                match = re.search(pattern_classic, svalue_lifetime_without_spaces)
                if match:
                    item_mask = match.group(1)
                    item_type = self.type.bytesN_base(item_mask)
                    result.append('%s[%s] //slot(%s)' % (item_type, length, slot)) 
                    return(next(iter(set(result))))
                    break


        elif(stack_rule_compliance_level >= 5 and            #svalue rule   for int
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           'sig' in self.memory_log[1] and
           memory_log_rule):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_int = r"\((0x[0-9A-Fa-f]+)\)sig_ext\(svalue\(CallData\(" 
                #(0x1)sig_ext(svalue(CallData(
                match = re.search(pattern_int, svalue_lifetime_without_spaces)
                if match:                   
                    item_mask = match.group(1)               
                    item_type_for_int = self.type.int_base(item_mask)
                    result.append('%s[%s] //slot(%s)' % (item_type_for_int, length, slot))
                    return(next(iter(set(result))))   
                    break

        elif(stack_rule_compliance_level >= 4 and            #svalue rule   for bool
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           '==0?==0?' in self.memory_log[1] and
           memory_log_rule):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_bool = r"0xff&svalue\(CallData\(0x4\).*\+0x.*==0\?\)==0\?" 
                #0xff & svalue(CallData(0x4)/0x20 + 0x0) /0x100^CallData(0x4) // 0x20==0?)==0?
                match = re.search(pattern_bool, svalue_lifetime_without_spaces)
                if match:                   
                    item_mask = 'double iszero'              
                    item_type = self.type.bool_base(item_mask)
                    result.append('%s[%s] //slot(%s)' % (item_type, length, slot))
                    return(next(iter(set(result))))   
                    break


        #print(stack_rule_compliance_level)        
        elif(stack_rule_compliance_level >= 9 and            #svalue rule   for uint[6][7]
           nestarray_calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           len(self.svalue_lifetime) == 1 and
           memory_log_rule):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                #pattern_uint = r"\((0x[1-9A-Fa-f]+)\)&\(svalue\(CallData\0x4\+0x20\)/0x10\+CallData\(0x4\)\+(0x[1-9A-Fa-f]+)\)" 
                #pattern_uint = r"\((0x[0-9A-Fa-f]+)\)&\(svalue\(CallData\(0x[0-9A-Fa-f]+\+0x[0-9A-Fa-f]+\)/0x[0-9A-Fa-f]+\+CallData\(0x[0-9A-Fa-f]+\)\+(0x[0-9A-Fa-f]+)\)/"
                #pattern_uint = r"\((0x[0-9A-Fa-f]+)\)&\(svalue\(CallData\((.*?)\+(0x[0-9A-Fa-f]+)\)/0x100"
                pattern_uint = r"\((0x[f]+)\)&\(svalue\(CallData\(.*?\).*?\+.*?CallData\(.*?\)\+(0x[0-9A-Fa-f]+)\)"
                #(0xffff)&(svalue(CallData(0x4 + 0x20)/0x10 + CallData(0x4) + 0x0)/0x100
                match = re.search(pattern_uint, svalue_lifetime_without_spaces)
                if match:
                    item_mask = match.group(1)   
                    slot = match.group(2)
                    item_type = self.type.uint_base(item_mask)
                    result.append('%s[%s][%s] //slot(%s)' % (item_type, inside_length, outside_length, slot))
                    return(next(iter(set(result))))   
                    break
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_uint_modern = r"<<\((0x[0-9A-Fa-f]+)\).*?\)&\(svalue\(CallData\(.*?\).*?\+.*?CallData\(.*?\)\+(0x[0-9A-Fa-f]+)\)"
                #((0x1)<<(0xa0) - 0x1)&(svalue(CallData(0x4 + 0x20) + 0x7*CallData(0x4) + 0x0)
                match = re.search(pattern_uint_modern, svalue_lifetime_without_spaces)
                if match:
                    item_mask = match.group(1)   
                    slot = match.group(2)
                    item_type = self.type.uint_base(item_mask)
                    result.append('%s[%s][%s] //slot(%s)' % (item_type, inside_length, outside_length, slot))
                    return(next(iter(set(result))))   
                    break
            for log in self.memory_log:
                log_without_spaces = log.replace(" ", "")
                pattern_slot = r'svalue\(CallData\(.*?\)\+.*?CallData\(.*?\)\+(0x[0-9A-Fa-f]+)\)'
                match_slot = re.search(pattern_slot, log_without_spaces)
                if match_slot:
                    slot = match_slot.group(1)
                    break
            nest_static_array_count = 0
            for lifetime in self.svalue_lifetime[0]:
                if ('<<' not in lifetime and
                    '&' not in lifetime):
                    nest_static_array_count += 1
                if nest_static_array_count == len(self.svalue_lifetime[0]):
                    result.append('uint256[%s][%s] //slot(%s)' % (inside_length, outside_length, slot))
                    return(next(iter(set(result))))   
                  

        #print(stack_rule_compliance_level)        
        elif(stack_rule_compliance_level >= 15 and            #svalue rule   for int[6][7]
           nestarray_calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           len(self.svalue_lifetime) == 1 and
           memory_log_rule):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_int = r'\((0x[0-9A-Fa-f]+)\)sig_ext\(svalue\(CallData\(.*?\).*?\+.*?CallData\(.*?\)\+(0x[0-9A-Fa-f]+)\)'
                #(0x1)sig_ext(svalue(CallData(0x4 + 0x20)/0x10 + CallData(0x4) + 0x0)
                match = re.search(pattern_int, svalue_lifetime_without_spaces)
                if match:
                    item_mask = match.group(1)
                    slot = match.group(2)
                    item_type = self.type.int_base(item_mask)
                    result.append('%s[%s][%s] //slot(%s)' % (item_type, inside_length, outside_length, slot))
                    return(next(iter(set(result))))   
                    break
        #else:
        #    print('oops')                  



    def rule_for_string(self):
        result = []
        stack_rule_list = [ 'as slot index', '0x1f', '\'0x20\', \'__+(mvalue(0x40))']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        #print(any('__+(0x20' in life for life in mvalue_life))
        if (len(set(mvalue)) >= 2 and
            'mvalue(0x40)' in set(mvalue) and
            'mvalue(mvalue(0x40))' in set(mvalue) and
            any('0x1f' in life for life in mvalue_life) and
            any('__+(0x20' in life for life in mvalue_life)):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        if ('load_0x40' in self.memory_log[0] and
            '0x1f' in self.memory_log[1] and
            'mvalue(0x40) + 0x20' in self.memory_log[1] and
            '0x20_storein_0x40' in self.memory_log[1] and
            'storein_mvalue(0x40)' in self.memory_log[2] and
            'load_0x40' in self.memory_log[3] and
            'storein_mvalue(0x40)' in self.memory_log[4] and
            'load_mvalue(0x40)' in self.memory_log[5] and
            ('mvalue(mvalue(0x40))_storein_mvalue(0x40) + 0x20' in self.memory_log[6] or
             'mvalue(mvalue(0x40))_storein_0x20 + mvalue(0x40)' in self.memory_log[6]) and
            'load_0x40' in self.memory_log[8]):
            memory_log_rule = True
        #print(stack_rule_compliance_level)
        if(stack_rule_compliance_level >= 7 and
           len(self.calldata_lifetime) == 0 and
           mvalue_lifetime_rule and memory_log_rule):
            #print(1)
            if len(self.svalue_lifetime) == 2 and len(self.svalue_lifetime[0]) ==1:
                #print(1)
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    pattern = r'svalue\((0x[0-9A-Fa-f]+)\)'
                    match = re.search(pattern, svalue_lifetime_without_spaces)
                    if match:
                        slot = match.group(1)
                        if 'string //slot(%s)' % slot not in result:
                            result.append('string //slot(%s)' % slot)
                        
            if len(self.svalue_lifetime) == 1:
                #print(1)
                for lifetime in self.svalue_lifetime[0]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    pattern = r'svalue\((0x[0-9A-Fa-f]+)\)'
                    match = re.search(pattern, svalue_lifetime_without_spaces)
                    if match:
                        slot = match.group(1)
                        if 'string //slot(%s)' % slot not in result:
                            result.append('string //slot(%s)' % slot)
                            
            if len(self.svalue_lifetime) == 2 and len(self.svalue_lifetime[0]) > 2:
                for lifetime in self.svalue_lifetime[0]:
                    if 'NOT0x0' in lifetime and '0x1f' in lifetime:
                        pattern_slot = r'svalue\((0x[0-9A-Fa-f]+)\)'
                        match_slot = re.search(pattern_slot, lifetime)
                        if match_slot:
                            slot = match_slot.group(1)
                        if 'string //slot(%s)' % slot not in result:
                            result.append('string //slot(%s)' % slot)
                
                        
        return(result)



    def rule_for_DynamicArray(self):
        result = []
        stack_rule_list = [ 'as CDL_offset', '__mstore(0x0)', 'as slot index', 'mstore in', 'as size of SHA3', 'as offset of SHA3', 'as size for svalue(hash', 'sigextend', '~', '0x1f', '0xff', '<__?']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        calldata_rule_compliance_level = 0               
        if len(self.calldata_lifetime) == 1:                      #calldata rules
            pattern_bounds_checking = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?'   
            #(CallData(0x4))<(svalue(0x0))?
            pattern_join_slot_1 = r'\(CallData\(0x4\)/?(0x[0-9A-Fa-f]+)?\)\+\(hashofthegivendata'
            #(CallData(0x4)/0xa)+(hash of the given data in memory
            pattern_join_slot_2 = r"\(hashofthegivendatainmemory,offset=0x0,size=0x20\.\)\+\(CallData\(0x4\)\)"
            #(hash of the given data in memory, offset = 0x0, size = 0x20.)+(CallData(0x4))
            pattern_int_specific_1 = r'\(0x[0-9A-Fa-f]+\)sig_ext\(svalue\(hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\+CallData\(0x4\)\)'
            #(0x1d)sig_ext(svalue(hash of the given data in memory, offset = 0x0, size = 0x20. + CallData(0x4)) )
            pattern_int_specific_2 = r'\(0x[0-9A-Fa-f]+\)sig_ext\(svalue\(CallData\(0x4\).*\+hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\)'
            #(0x2)sig_ext(svalue(CallData(0x4)/0xa + hash of the given data in memory, offset = 0x0, size = 0x20.)
            for lifetime in self.calldata_lifetime[0]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_bounds_checking = re.search(pattern_bounds_checking, calldata_lifetime_without_spaces)
                if match_bounds_checking:
                    #slot = match_bounds_checking.group(1)
                    calldata_rule_compliance_level += 1
                    #print(123)
                    break
            for lifetime in self.calldata_lifetime[0]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_join_slot_1 = re.search(pattern_join_slot_1, calldata_lifetime_without_spaces)
                if match_join_slot_1:
                    calldata_rule_compliance_level += 1
                    break
            for lifetime in self.calldata_lifetime[0]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_join_slot_2 = re.search(pattern_join_slot_2, calldata_lifetime_without_spaces)
                if match_join_slot_2:
                    calldata_rule_compliance_level += 1
                    break
            for lifetime in self.calldata_lifetime[0]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_int_specific_1 = re.search(pattern_int_specific_1, calldata_lifetime_without_spaces)
                if match_int_specific_1:
                    calldata_rule_compliance_level += 1
                    break
            for lifetime in self.calldata_lifetime[0]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_int_specific_2 = re.search(pattern_int_specific_2, calldata_lifetime_without_spaces)
                if match_int_specific_2:
                    calldata_rule_compliance_level += 1
                    break  

        NestStaticArray_calldata_rule_compliance_level = 0       #nest array calldata rules
        if len(self.calldata_lifetime) == 2:                      
            
            pattern_dynamic_bounds_checking = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?'   
            #(CallData(0x4))<(svalue(0x0) )?
            pattern_static_bounds_checking = r'\(CallData\((0x4\+0x20|0x24)\)\)<\((0x[0-9A-Fa-f]+)\)\?'
            #(CallData(0x4 + 0x20))<(0x7)? 
            for lifetime in self.calldata_lifetime[0]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_dynamic_bounds_checking = re.search(pattern_dynamic_bounds_checking, calldata_lifetime_without_spaces)
                if match_dynamic_bounds_checking:
                    #slot = match_dynamic_bounds_checking.group(1)
                    NestStaticArray_calldata_rule_compliance_level += 1
                    break
            for lifetime in self.calldata_lifetime[1]:
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                match_static_bounds_checking = re.search(pattern_static_bounds_checking, calldata_lifetime_without_spaces)
                if match_static_bounds_checking:
                    staticarray_length = match_static_bounds_checking.group(2)
                    NestStaticArray_calldata_rule_compliance_level += 1
                    break
                      
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False
        if (len(set(mvalue)) == 1 and
            'mvalue(0x40)' in set(mvalue) and
            (any('0x20 + mvalue(0x40)' in life for life in mvalue_life) or
             any('(mvalue(0x40))-__' in life for life in mvalue_life))):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        if ('_storein_0x0' in self.memory_log[0] and
            'sha3(0x0,0x20)' in self.memory_log[1] and
            'load_0x40' in self.memory_log[2] and 
            ('svalue(CallData(0x' in self.memory_log[3] or 'svalue(hash of the given data' in self.memory_log[3]) and
            ('+ hash of the given data' in self.memory_log[3] or '+ CallData(0x4)' in self.memory_log[3]) and
            'storein_mvalue(0x40)' in self.memory_log[3] and
            'load_0x40' in self.memory_log[4]):
            memory_log_rule = True
            
        #print(len(self.svalue_lifetime) == 2)   
        if(stack_rule_compliance_level >= 6 and            #svalue rule for uint
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           memory_log_rule and
           '==0?==0?' not in self.memory_log[3] and
           len(self.svalue_lifetime) == 2):
            #print(12)
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_bound_check = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?' #(CallData(0x4))<(svalue(0x0) )?
                match_bound_check = re.search(pattern_bound_check, svalue_lifetime_without_spaces)
                if match_bound_check:
                    slot = match_bound_check.group(1)
                    #print(slot)
                    break
            if '__mstore(mvalue(0x40))' in self.svalue_lifetime[1][-1]:   
                pattern_for_morden_uint_1 = r'\(\(0x1\)<<\((0x[0-9A-Fa-f]+)\)\-0x1\)&\(svalue\(hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\+CallData\(0x4\)\)\)'
                pattern_for_morden_uint_2 = r'\((0x[f]+)\)&\(svalue\(CallData\(0x4\).*\+hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\)'
                #((0x1)<<(0xf0) - 0x1)&(svalue(hash of the given data in memory, offset = 0x0, size = 0x20. + CallData(0x4)) )
                #(0xffffff)&(svalue(CallData(0x4)/0xa + hash of the given data in memory, offset = 0x0, size = 0x20.)
                pattern_for_classic_uint_1 = r'\((0x[f]+)\)&\(svalue\(hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\+CallData\(0x4\)\)\)'
                pattern_for_classic_uint_2 = r'\((0x[f]+)\)&\(svalue\(CallData\(0x4\).*\+hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\+CallData\(0x4\)\)\)'
                #(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)&(svalue(hash of the given data in memory, offset = 0x0, size = 0x20. + CallData(0x4)) )
                #(0xffffff)&(svalue(CallData(0x4)/0xa + hash of the given data in memory, offset = 0x0, size = 0x20.)
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_modern_uint_1 = re.search(pattern_for_morden_uint_1, svalue_lifetime_without_spaces)
                    if match_modern_uint_1:
                        item_mask = match_modern_uint_1.group(1)
                        item_type = self.type.uint_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_modern_uint_2 = re.search(pattern_for_morden_uint_2, svalue_lifetime_without_spaces)
                    if match_modern_uint_2:
                        item_mask = match_modern_uint_2.group(1)
                        item_type = self.type.uint_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_classic_uint_1 = re.search(pattern_for_classic_uint_1, svalue_lifetime_without_spaces)
                    if match_classic_uint_1:
                        item_mask = match_classic_uint_1.group(1)
                        item_type = self.type.uint_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_classic_uint_2 = re.search(pattern_for_classic_uint_2, svalue_lifetime_without_spaces)
                    if match_classic_uint_2:
                        item_mask = match_classic_uint_2.group(1)
                        item_type = self.type.uint_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break
                for lifetime in self.svalue_lifetime[1]:
                    if '0xa0' in lifetime and '&' in lifetime:
                        item_type = 'address'
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break
                    
                dynamic_array_count = 0
                for lifetime in self.svalue_lifetime[1]:
                    if ('<<' not in lifetime and
                        '&' not in lifetime):
                        dynamic_array_count += 1
                    if dynamic_array_count == len(self.svalue_lifetime[1]):
                        result.append('uint256[] //slot(%s)' % slot)
                        return(next(iter(set(result))))
                        
                        
        #print(stack_rule_compliance_level)           
        elif(stack_rule_compliance_level >= 8 and            #svalue rule for int
           calldata_rule_compliance_level == 3 and
           mvalue_lifetime_rule and 
           memory_log_rule and
           'sig' in self.memory_log[3] and
           len(self.svalue_lifetime) == 2):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_bound_check = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?' 
                #(CallData(0x4))<(svalue(0x0) )?
                match_bound_check = re.search(pattern_bound_check, svalue_lifetime_without_spaces)
                if match_bound_check:
                    slot = match_bound_check.group(1)
                    break
            if '__mstore(mvalue(0x40))' in self.svalue_lifetime[1][-1]:
                pattern_svalue_mask_1 = r'\((0x[0-9A-Fa-f]+)\)sig_ext\(svalue\(CallData\(0x4\).*\+hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\)'
                #(0x2)sig_ext(svalue(CallData(0x4)/0xa + hash of the given data in memory, offset = 0x0, size = 0x20.)
                pattern_svalue_mask_2 = r'\((0x[0-9A-Fa-f]+)\)sig_ext\(svalue\(hashofthegivendata\(.*?\)inmemory,offset=0x0,size=0x20\.\+CallData\(0x4\)\)\)'
                #(0x1d)sig_ext(svalue(hash of the given data in memory, offset = 0x0, size = 0x20. + CallData(0x4)))
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_int_1 = re.search(pattern_svalue_mask_1, svalue_lifetime_without_spaces)
                    if match_int_1:
                        item_mask = match_int_1.group(1)
                        item_type = self.type.int_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_int_2 = re.search(pattern_svalue_mask_2, svalue_lifetime_without_spaces)
                    if match_int_2:
                        item_mask = match_int_2.group(1)
                        item_type = self.type.int_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break
        #print(stack_rule_compliance_level)
        elif(stack_rule_compliance_level >= 7 and            #svalue rule for bytesN
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           memory_log_rule and
           'NOT' in self.memory_log[3] and
           len(self.svalue_lifetime) == 2):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_bound_check = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?' 
                #(CallData(0x4))<(svalue(0x0) )?
                match_bound_check = re.search(pattern_bound_check, svalue_lifetime_without_spaces)
                if match_bound_check:
                    slot = match_bound_check.group(1)
                    break
            if '__mstore(mvalue(0x40))' in self.svalue_lifetime[1][-1]:
                pattern_bytesN_classic_mask = r'&\(NOT(0x[1-9A-Fa-f]+)\)'
                #&(NOT0xffffffffffffffff)
                pattern_bytesN_modern_mask = r'svalue.*hash.*<<\((0x[0-9A-Fa-f]+)\)'
                #svalue(hash of the given data in memory, offset = 0x0, size = 0x20. + CallData(0x4)) )<<(0x40)
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_bytesN_classic = re.search(pattern_bytesN_classic_mask, svalue_lifetime_without_spaces)
                    if match_bytesN_classic:
                        item_mask = match_bytesN_classic.group(1)
                        item_type = self.type.bytesN_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result)))) 
                        break
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_bytesN_modern = re.search(pattern_bytesN_modern_mask, svalue_lifetime_without_spaces)
                    if match_bytesN_modern:
                        item_mask = match_bytesN_modern.group(1)
                        #print(item_mask)
                        item_type = self.type.bytesN_base(item_mask)
                        if not result:
                            result.append('%s[] //slot(%s)' % (item_type, slot))
                            return(next(iter(set(result)))) 
                        break         


        #print(len(set(mvalue)))
        elif(stack_rule_compliance_level >= 12 and            #svalue rule for string\bytes
           calldata_rule_compliance_level == 2 and
           len(set(mvalue)) >= 2 and
           'mvalue(0x40)' in set(mvalue) and
           'mvalue(mvalue(0x40))' in set(mvalue) and
           any('(0x0)<__?' in life for life in mvalue_life) and
           any('0x1f' in life for life in mvalue_life) and
           '_storein_0x0' in self.memory_log[0] and
           'sha3(0x0,0x20)' in self.memory_log[1] and
           'load_0x40' in self.memory_log[2] and
           ('svalue(CallData(0x4)' in self.memory_log[3] or 'svalue(hash of the given data' in self.memory_log[3]) and
           ('+ hash of the given data' in self.memory_log[3] or '+ CallData(0x4)' in self.memory_log[3]) and
           'storein_0x40' in self.memory_log[3] and
           'hash of the given data' in self.memory_log[4] and
           'storein_mvalue(0x40)' in self.memory_log[4] and
           'load_0x40' in self.memory_log[5] and
           '0x20_storein_mvalue(0x40)' in self.memory_log[6] and
           'load_mvalue(0x40)' in self.memory_log[7] and
           'mvalue(mvalue(0x40))_storein_mvalue(0x40) + 0x20' in self.memory_log[8] and
           'load_0x40' in self.memory_log[-1]):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_bound_check = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?' 
                #(CallData(0x4))<(svalue(0x0) )?
                match_bound_check = re.search(pattern_bound_check, svalue_lifetime_without_spaces)
                if match_bound_check:
                    slot = match_bound_check.group(1)
                    result.append('string[] //slot(%s)' % slot)
                    return(next(iter(set(result)))) 
                    break
        #print(stack_rule_compliance_level)
        elif(stack_rule_compliance_level >= 7 and            #svalue rule for bool
           calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           memory_log_rule and
           '==0?==0?' in self.memory_log[3] and
           len(self.svalue_lifetime) == 2):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_bound_check = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?' 
                #(CallData(0x4))<(svalue(0x0) )?
                match_bound_check = re.search(pattern_bound_check, svalue_lifetime_without_spaces)
                if match_bound_check:
                    slot = match_bound_check.group(1)
                    break
            if '__mstore(mvalue(0x40))' in self.svalue_lifetime[1][-1]:
                pattern_bool = r'0xff&svalue\(CallData\(0x4\).*\+hash.*==0\?\)==0\?'
                #0xff & svalue(CallData(0x4)/0x20 + hash of the given data in memory, offset = 0x0, size = 0x20.) /0x100^CallData(0x4) // 0x20==0?)==0?
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_bool = re.search(pattern_bool, svalue_lifetime_without_spaces)
                    if match_bool:
                        item_mask = 'double iszero'
                        item_type = self.type.bool_base(item_mask)
                        result.append('%s[] //slot(%s)' % (item_type, slot))
                        return(next(iter(set(result))))   
                        break   
                    

        #print(stack_rule_compliance_level)
        elif(stack_rule_compliance_level >= 8 and            #svalue rule for uint[-][]
           len(self.calldata_lifetime) == 2 and
           NestStaticArray_calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           memory_log_rule and
           len(self.svalue_lifetime) == 2):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_dynamic_bound_check = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?' 
                #(CallData(0x4))<(svalue(0x0) )?
                match_dynamic_bound_check = re.search(pattern_dynamic_bound_check, svalue_lifetime_without_spaces)
                if match_dynamic_bound_check:
                    slot = match_dynamic_bound_check.group(1)
                    break
            if '__mstore(mvalue(0x40))' in self.svalue_lifetime[1][-1]:
                nest_dynamic_array_count = 0
                pattern_uint = r'\((0x[f]+)\)&\(svalue'
                #0xff & svalue(CallData
                pattern_uint_modern = r'<<\((0x[0-9A-Fa-f]+)\).*?\)&\(svalue\(CallData'
                #<<(0xa0) - 0x1)&(svalue(CallData
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match = re.search(pattern_uint, svalue_lifetime_without_spaces)
                    if match:
                        item_mask = match.group(1)
                        item_type = self.type.uint_base(item_mask)
                        result.append('%s[%s][] //slot(%s)' % (item_type, staticarray_length, slot))
                        return(next(iter(set(result))))   
                        break
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match = re.search(pattern_uint_modern, svalue_lifetime_without_spaces)
                    if match:
                        item_mask = match.group(1)
                        item_type = self.type.uint_base(item_mask)
                        result.append('%s[%s][] //slot(%s)' % (item_type, staticarray_length, slot))
                        return(next(iter(set(result))))   
                        break
                for lifetime in self.svalue_lifetime[1]:
                    if ('<<' not in lifetime and
                        '&' not in lifetime):
                        nest_dynamic_array_count += 1
                    if nest_dynamic_array_count == len(self.svalue_lifetime[1]):
                        result.append('uint256[%s][] //slot(%s)' % (staticarray_length, slot))
                        return(next(iter(set(result))))
                        

        #print(stack_rule_compliance_level)
        elif(stack_rule_compliance_level >= 7 and            #svalue rule for int[-][]
           NestStaticArray_calldata_rule_compliance_level == 2 and
           mvalue_lifetime_rule and 
           'sig' in self.memory_log[3] and
           memory_log_rule and
           len(self.svalue_lifetime) == 2):
            for lifetime in self.svalue_lifetime[0]:
                svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_dynamic_bound_check = r'\(CallData\(0x4\)\)<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?' 
                #(CallData(0x4))<(svalue(0x0) )?
                match_dynamic_bound_check = re.search(pattern_dynamic_bound_check, svalue_lifetime_without_spaces)
                if match_dynamic_bound_check:
                    slot = match_dynamic_bound_check.group(1)
                    break
            if '__mstore(mvalue(0x40))' in self.svalue_lifetime[1][-1]:
                pattern_int = r'\((0x[0-9A-Fa-f]+)\)sig_ext\(svalue\(CallData\('
                #(0x13)sig_ext(svalue(CallData(
                for lifetime in self.svalue_lifetime[1]:
                    svalue_lifetime_without_spaces = lifetime.replace(" ", "")
                    match_int = re.search(pattern_int, svalue_lifetime_without_spaces)
                    if match_int:
                        item_mask = match_int.group(1)
                        item_type = self.type.int_base(item_mask)
                        result.append('%s[%s][] //slot(%s)' % (item_type, staticarray_length, slot))
                        return(next(iter(set(result))))   
                        break         

        #else:
        #    print('oops')

    def rule_for_mapping(self):
        result = []
        stack_rule_list = [ 'as CDL_offset', 'as offset of SHA3', 'as offset of CallData', 'as offset of 0xff', 'as size of SHA3', 'mstore(0x20)']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False

        if (len(set(mvalue)) == 1 and
            'mvalue(0x40)' in set(mvalue)):
               mvalue_lifetime_rule = True
               
               
        differ_from_nested_mapping = True
        if len(self.memory_log) > 5 and 'sha3' in self.memory_log[5]:
            differ_from_nested_mapping = False
               
        memory_log_rule = False                                       #mlog rules
        if ('storein_0x20' in self.memory_log[0] and
            'CallData(' in self.memory_log[1] and
            'storein_0x0' in self.memory_log[1] and
            'sha3(0x0,0x40)' in self.memory_log[2] and
            'load_0x40' in self.memory_log[3] and
            'svalue(hash of the given data' in self.memory_log[4] and
            'storein_mvalue(0x40)' in self.memory_log[4] and
            'load_0x40' in self.memory_log[5]):
            memory_log_rule = True
        memory_log_rule_1 = False
        if ('storein_0x0' in self.memory_log[0] and
            'CallData(' in self.memory_log[0] and
            'storein_0x20' in self.memory_log[1] and
            'sha3(0x0,0x40)' in self.memory_log[2] and
            'load_0x40' in self.memory_log[3] and
            'svalue(hash of the given data' in self.memory_log[4] and
            'storein_mvalue(0x40)' in self.memory_log[4] and
            'load_0x40' in self.memory_log[5]):
            memory_log_rule_1 = True

            
        pattern_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20'
        #0x0_storein_0x20
        match_slot = re.search(pattern_slot, self.memory_log[0])
        if match_slot:
            slot = match_slot.group(1)
        #else:
            #print('mapping slot match failed')
        #print((memory_log_rule or memory_log_rule_1))
        if(stack_rule_compliance_level >= 4 and
           len(self.calldata_lifetime) == 1 and
           len(self.svalue_lifetime) == 1 and
           mvalue_lifetime_rule and (memory_log_rule or memory_log_rule_1)):
            #print('here comes')
            if memory_log_rule_1:
                pattern_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20'
                match_slot = re.search(pattern_slot, self.memory_log[1])
                if match_slot:
                    slot = match_slot.group(1)
                if ('address' in self.memory_log[0] or 
                   ('0xffffffffffffffffffffffffffffffffffffffff' in self.memory_log[0] and '&' in self.memory_log[0])):
                    key_type = 'address'
                if '0xff &' in self.memory_log[4]:                    
                    value_type = 'bool'
                    if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:          
                        result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))
            if memory_log_rule:
                pattern_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20'
                match_slot = re.search(pattern_slot, self.memory_log[0])
                if match_slot:
                    slot = match_slot.group(1)
                     
            
            key_count = 0
            for lifetime in self.calldata_lifetime[0]:                               #for key
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_uint_classic_1 = r'\(CallData\(0x4\)\)&\((0x[f]+)\)'
                #(CallData(0x4))&(0xffffffffffffffffffffffffffffffffffffffff)
                match_uint_classic_1 = re.search(pattern_uint_classic_1, calldata_lifetime_without_spaces)
                if match_uint_classic_1:
                    key_mask = match_uint_classic_1.group(1)
                    key_type = self.type.uint_base(key_mask)
                    break
                pattern_uint_classic_2 = r'\((0x[f]+)\)&\(CallData\(0x4\)\)'
                #(0xffffffffffffffffffffffffffffffffffffffff)&(CallData(0x4))
                match_uint_classic_2 = re.search(pattern_uint_classic_2, calldata_lifetime_without_spaces)
                if match_uint_classic_2:
                    key_mask = match_uint_classic_2.group(1)
                    key_type = self.type.uint_base(key_mask)
                    break
                pattern_uint_modern = r'\(CallData\(0x4\)\)&\(\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(0x4))&((0x1)<<(0xa0)
                match_uint_modern = re.search(pattern_uint_modern, calldata_lifetime_without_spaces)
                if match_uint_modern:
                    key_mask = match_uint_modern.group(1)
                    key_type = self.type.uint_base(key_mask)
                    break
                pattern_int = r'\((0x[0-9A-Fa-f]+)\)sig_ext\(CallData\(0x4\)\)'
                #(0x13)sig_ext(CallData(0x4))
                match_int = re.search(pattern_int, calldata_lifetime_without_spaces)
                if match_int:
                    key_mask = match_int.group(1)
                    key_type = self.type.int_base(key_mask)
                    break
                pattern_bool = r'\(CallData\(0x4\)==0\?\)==0\?'
                #(CallData(0x4)==0?)==0?
                match_bool = re.search(pattern_bool, calldata_lifetime_without_spaces)
                if match_bool:
                    key_mask = 'double iszero'
                    key_type = self.type.bool_base(key_mask)
                    break
                pattern_bytesN_classic = r'\(CallData\(0x4\)\)&\(NOT(0x[f]+)\)'
                #(CallData(0x4))&(NOT0xffffffffffffffffffffffffffffffffffffffffffffffffff)
                match_bytesN_classic = re.search(pattern_bytesN_classic, calldata_lifetime_without_spaces)
                if match_bytesN_classic:
                    key_mask = match_bytesN_classic.group(1)
                    key_type = self.type.bytesN_base(key_mask)
                    break                
                pattern_bytesN_modern = r'\(CallData\(0x4\)\)&\(NOT\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(0x4))&(NOT(0x1)<<(0xd8)  
                match_bytesN_modern = re.search(pattern_bytesN_modern, calldata_lifetime_without_spaces)
                if match_bytesN_modern:
                    key_mask = match_bytesN_modern.group(1)
                    key_type = self.type.bytesN_base(key_mask)
                    break                    
                pattern_bytesN_modern = r'\(CallData\(0x4\)\)&\(NOT\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(0x4))&(NOT(0x1)<<(0xd8)  
                match_bytesN_modern = re.search(pattern_bytesN_modern, calldata_lifetime_without_spaces)
                if match_bytesN_modern:
                    key_mask = match_bytesN_modern.group(1)
                    key_type = self.type.bytesN_base(key_mask)
                    break
                if '0xa0' in lifetime and '&' in lifetime:
                    key_type = 'address'
                    #print(key_type)
                    break
                if lifetime.startswith('__mstore(0x0)'):
                    #print(1)
                    key_type = '(u)int256/bytes32'
                    break
                key_count += 1
                if key_count == len(self.calldata_lifetime[0]):
                    #print(1)
                    key_type = '(u)int256/bytes32'
                    
            #print(key_type)    
            pattern_bool_svalue = r'==0\?==0\?'                                                #for value
            #0xff & svalue(hash of the given data in memory, offset = 0x0, size = 0x40.) ==0?==0?_storein_mvalue(0x40)
            memory_log_without_spaces = self.memory_log[4].replace(" ", "")
            match_bool_svalue = re.search(pattern_bool_svalue, memory_log_without_spaces)
            if match_bool_svalue:
                #print(1122)
                value_mask = 'double iszero'
                value_type = self.type.bool_base(value_mask)
                #print(key_type,value_type)
                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))

                
            pattern_uint_svalue = r'(0x[f]+)&svalue\(hash'                                         #for value
            #0xffffffffffffffffffffffffffffffffffffffff & svalue(hash
            memory_log_without_spaces = self.memory_log[4].replace(" ", "")
            match_uint_svalue = re.search(pattern_uint_svalue, memory_log_without_spaces)
            if match_uint_svalue and '==0?' not in memory_log_without_spaces:
                value_mask = match_uint_svalue.group(1)
                value_type = self.type.uint_base(value_mask)
                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))
            pattern_int_svalue = r'sig(0x[0-9A-Fa-f]+)'                                            #for value
            #sig 0x13
            memory_log_without_spaces = self.memory_log[4].replace(" ", "")
            match_int_svalue = re.search(pattern_int_svalue, memory_log_without_spaces)
            if match_int_svalue:
                value_mask = match_int_svalue.group(1)
                value_type = self.type.int_base(value_mask)
                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))          
            pattern_bytesN_svalue = r'NOT(0x[f]+)'                                                 #for value
            #NOT0xffffffffffff 
            memory_log_without_spaces = self.memory_log[4].replace(" ", "")
            match_bytesN_svalue = re.search(pattern_bytesN_svalue, memory_log_without_spaces)
            if match_bytesN_svalue:
                value_mask = match_bytesN_svalue.group(1)
                value_type = self.type.bytesN_base(value_mask)
                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))                   
            pattern_bytesN_unop_svalue = r'<<\((0x[0-9A-Fa-f]+)\)&0x[f]+[0]+'                                            #for value
            #<<(0x30) & 0xffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000  
            memory_log_without_spaces = self.memory_log[4].replace(" ", "")
            match_bytesN_unop_svalue = re.search(pattern_bytesN_unop_svalue, memory_log_without_spaces)
            if match_bytesN_unop_svalue:
                value_mask = match_bytesN_unop_svalue.group(1)
                value_type = self.type.bytesN_base(value_mask)
                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))
            if len(self.svalue_lifetime) == 1 and len(self.svalue_lifetime[0]) == 2:
                if '__mstore(mvalue(0x40)) in block' in self.svalue_lifetime[0][1]:
                    #print(2)
                    value_type = '(u)int256/bytes32'
                    if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                        result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))                        
            if ('sig' not in self.memory_log[4] and
                '<<' not in self.memory_log[4] and
                '&' not in self.memory_log[4] and
                '==0?' not in self.memory_log[4] and
                'NOT' not in self.memory_log[4]):
                
                value_type = '(u)int256/bytes32'
                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))
            
            #svalue(hash of the given data(b'0x2^0xa0 - 0x1 & 0x2^0xa0 - 0x1 & CallData(0x4)_offset=0x0',b'0x0_offset=0x20') in memory, offset = 0x0, size = 0x40.) _storein_mvalue(0x40) in block_19
            pattern_corner_case_0 = r'svalue\(hash of the given data\(.*?0x2\^0xa0.*?&.*?\) _storein_mvalue'
            match_corner_case_0 = re.search(pattern_corner_case_0, self.memory_log[4]) 
            #svalue(hash of the given data(b'0x0_offset=0x20',b'CallData(0x4) & 0x2^0xa0 - 0x1_offset=0x0') in memory, offset = 0x0, size = 0x40.) _storein_mvalue(0x40)
            pattern_corner_case_1 = r'svalue\(hash of the given data\(.*?&.*?0x2\^0xa0.*?\) _storein_mvalue'
            match_corner_case_1 = re.search(pattern_corner_case_1, self.memory_log[4]) 
            if (not match_corner_case_0 and
                not match_corner_case_1 and
                '0xa0' in self.memory_log[4] and 
                '&' in self.memory_log[4] and 
                'svalue(hash' in self.memory_log[4] and 
                '%s_offset' % slot in self.memory_log[4] and
                '0xff &' not in self.memory_log[4] and
                '<<(0xa0)' not in self.memory_log[4]):
                #print(6)
                value_type = 'address'
                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))


        
        pattern_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20'   #for dynamic value mapping .case1
        match_slot = re.search(pattern_slot, self.memory_log[0])
        pattern_key = r'CallData\(0x4\).*?_storein_0x0'
        match_key = re.search(pattern_key, self.memory_log[1])
        pattern_hash = r'sha3\(0x0,0x40\)'
        match_hash = re.search(pattern_hash, self.memory_log[2])
        if match_slot and match_key and match_hash:
            slot = match_slot.group(1)
        if '0xa0' in self.memory_log[1] and '&' in self.memory_log[1]:
            key_type = 'address'
        if 'CallData(0x4)_storein_0x0 in block' in self.memory_log[1]:
            key_type = '(u)int256/bytes32'
        if(stack_rule_compliance_level >= 4 and     # mapping value if dynamic
           len(self.calldata_lifetime) == 2 and
           len(self.svalue_lifetime) == 2 and
           mvalue_lifetime_rule):
         
            if 'sha3' in self.memory_log[4]: #The memory location is not the value, go storage and analysis
                for item in self.svalue_lifetime:
                    if 'svalue(hash' in item[1] and '%s_offset=0x20' % slot in item[1]:
                        if ('CallData(0x24))<(svalue(hash of the' in item[1] or
                            '>CallData(0x24)' in item[1]):
                                value_type = 'uint256[]'
                                if 'mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot) not in result:
                                    result.append('mapping(%s => %s) //slot(%s)' % (key_type, value_type, slot))
                                    break

        pattern_slot_struct = r'(0x[0-9A-Fa-f]+)_storein_0x20'   #for struct value mapping 
        match_slot_struct = re.search(pattern_slot_struct, self.memory_log[0])
        pattern_key_struct = r'CallData\(0x4\).*?_storein_0x0'
        match_key_struct = re.search(pattern_key_struct, self.memory_log[1])
        pattern_hash_struct = r'sha3\(0x0,0x40\)'
        match_hash_struct = re.search(pattern_hash_struct, self.memory_log[2])
        if match_slot_struct and match_key_struct and match_hash_struct:
            slot = match_slot_struct.group(1)
            #print(slot)
        if '0xa0' in self.memory_log[1]:                #key
            key_type = 'address'
        if self.memory_log[1].startswith('CallData(0x4)_storein_0x0'):
            key_type = '(u)int256/bytes32'
            #print(key_type)
        value_list = []
        if len(self.memory_log) > 6 and len(self.svalue_lifetime) ==2 and differ_from_nested_mapping:   # for value struct case1
            #svalue(hash of the given data(b'0x6_offset=0x20',b'CallData(0x4)_offset=0x0') in memory, offset = 0x0, size = 0x40. + 0x1)  & 0xffffffffff & 0xffffffffff_storein_mvalue(0x40) + 0x20 in block_91
            #print(1234)
            pattern_uint = r'svalue\(hash of the given data\(.*?{}_offset=0x20.*?& (0x[f]+).*?storein'.format(re.escape(slot))
            for log in self.memory_log[4:]:
                if log.startswith('svalue(hash') and '&' not in log:
                    value_list.append('(u)int/bytes32')
                if re.search(pattern_uint, log) and '==0?' not in log:
                    value_mask = re.search(pattern_uint, log).group(1)
                    value_list.append(self.type.uint_base(value_mask))
                if '0xff & svalue' in log and '==0?' in log:
                    value_list.append('bool')
                if '0xa0' in log and '& svalue' in log:
                    value_list.append('address')
            if 'mapping(%s => struct%s) //slot(%s)' % (key_type, value_list, slot) not in result and len(value_list) > 0:
                result.append('mapping(%s => struct%s) //slot(%s)' % (key_type, value_list, slot))
                        
                    
                    
        if len(self.memory_log) > 6 and len(self.svalue_lifetime) > 3:   # for value struct case2
            #svalue(hash of the given data(b'0x2_offset=0x20',b'CallData(0x4)_offset=0x0')
            #print(1235)
            pattern_struct = r'svalue\(hash of the given data\(b.*?{}_offset=0x20.*?CallData\(0x4\)'.format(re.escape(slot))
            count = 0
            #print(slot)
            for index, item in enumerate(self.memory_log[4:]):  #Continuous values are judged as structural entities
                if index < 3:
                    match = re.search(pattern_struct, item)
                    if match:
                        count = count + 1

            #svalue(0x0 + hash of the given data(b'0x5_offset=0x20',b'CallData(0x4)_offset=0x0') in memory, offset = 0x0, size = 0x40.) _storein_mvalue(0x40) in block_69
            pattern_struct_1 = r'svalue\(0x[0-9A-Fa-f]+ \+ hash of the given data\(b.*?{}_offset=0x20.*?CallData\(0x4\)'.format(re.escape(slot))
            for index, item in enumerate(self.memory_log[4:]):  #Continuous values are judged as structural entities
                if index < 3:
                    match = re.search(pattern_struct_1, item)
                    if match:
                        count = count + 1
            #print(count)            
            if count == 3:
                value_list = []
                for item in self.memory_log[4:]:
                    if item.startswith('svalue(') and '0x1 & 0x2^0xa0' not in item:
                        value_list.append('(u)int256/bytes32')
                    if '0x1 & 0x2^0xa0' in item:
                        value_list.append('address')
                    if '0x2^0xa0 - 0x1 & svalue' in item:
                        value_list.append('address')
                    if '0xff' in item and '==0?' not in item:
                        value_list.append('uint8')
                    if '0xff' in item and '==0?' in item:
                        value_list.append('bool')
            if 'mapping(%s => struct%s) //slot(%s)' % (key_type, value_list, slot) not in result and len(value_list) > 0:
                result.append('mapping(%s => struct%s) //slot(%s)' % (key_type, value_list, slot))
      
     
        return(result) 
        #else:
        #    print('oops')
            
    def rule_for_nested_mapping(self):
        result = []
        stack_rule_list = [ 'as CDL_offset', 'as offset of SHA3', 'as offset of CallData', 'as offset of 0xff', 'as size of SHA3']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1
                        
        mvalue = [lifetime[0] for lifetime in self.mvalue_lifetime]  #mvalue rules
        mvalue_life = [item for lifetime in self.mvalue_lifetime for item in lifetime]
        mvalue_lifetime_rule = False

        if (len(set(mvalue)) == 1 and
            'mvalue(0x40)' in set(mvalue)):
               mvalue_lifetime_rule = True
               
        memory_log_rule = False                                       #mlog rules
        if ('storein_0x20' in self.memory_log[0] and
            'CallData(' in self.memory_log[1] and
            'storein_0x0' in self.memory_log[1] and
            'sha3(0x0,0x40)' in self.memory_log[2] and
            'hash of the given data' in self.memory_log[3] and
            'storein_0x20' in self.memory_log[3] and
            'CallData(' in self.memory_log[4] and
            'storein_0x0' in self.memory_log[4] and         
            'sha3(0x0,0x40)' in self.memory_log[5] and
            'load_0x40' in self.memory_log[6] and
            'svalue(hash' in self.memory_log[7] and
            'load_0x40' in self.memory_log[8]):
            memory_log_rule = True
            
        pattern_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20'             #slot
        #0x0_storein_0x20
        match_slot = re.search(pattern_slot, self.memory_log[0])
        if match_slot:
            slot = match_slot.group(1)

        #print(memory_log_rule)
        if(stack_rule_compliance_level >= 7 and
           len(self.calldata_lifetime) == 2 and
           len(self.svalue_lifetime) == 1 and
           mvalue_lifetime_rule and memory_log_rule):
            #print(slot)
            foreign_key_count = 0
            for lifetime in self.calldata_lifetime[0]:                               #for foreign key
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_uint_modern = r'\(CallData\(0x4\)\)&\(\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(0x4))&((0x1)<<(0xa0)
                match_uint_modern = re.search(pattern_uint_modern, calldata_lifetime_without_spaces)
                if match_uint_modern:
                    foreign_key_mask = match_uint_modern.group(1)
                    foreign_key_type = self.type.uint_base(foreign_key_mask)
                    break
                pattern_uint_classic_1 = r'\(CallData\(0x4\)\)&\((0x[f]+)\)'
                #(CallData(0x4))&(0xffffffffffffffffffffffffffffffffffffffff)
                match_uint_classic_1 = re.search(pattern_uint_classic_1, calldata_lifetime_without_spaces)
                if match_uint_classic_1:
                    foreign_key_mask = match_uint_classic_1.group(1)
                    foreign_key_type = self.type.uint_base(foreign_key_mask)
                    break
                pattern_uint_classic_2 = r'\((0x[f]+)\)&\(CallData\(0x4\)\)'
                #(0xffffffffffffffffffffffffffffffffffffffff)&(CallData(0x4))
                match_uint_classic_2 = re.search(pattern_uint_classic_2, calldata_lifetime_without_spaces)
                if match_uint_classic_2 and '==0?' not in calldata_lifetime_without_spaces:
                    foreign_key_mask = match_uint_classic_2.group(1)
                    foreign_key_type = self.type.uint_base(foreign_key_mask)
                    break  
                pattern_bool = r'\(CallData\(0x4\)==0\?\)==0\?'
                #(CallData(0x4)==0?)==0?
                match_bool = re.search(pattern_bool, calldata_lifetime_without_spaces)
                if match_bool:
                    foreign_key_mask = 'double iszero'
                    foreign_key_type = self.type.bool_base(foreign_key_mask)
                    break 
                pattern_int = r'\((0x[0-9A-Fa-f]+)\)sig_ext\(CallData\('
                #(0x13)sig_ext(CallData(
                match_int = re.search(pattern_int, calldata_lifetime_without_spaces)
                if match_int:
                    foreign_key_mask = match_int.group(1)
                    foreign_key_type = self.type.int_base(foreign_key_mask)
                    break  
                pattern_bytesN_classic = r'\(CallData\(0x4\)\)&\(NOT(0x[f]+)\)'
                #(CallData(0x4))&(NOT0xffffffffffffffffffffffffffffffffffffffffffffffffff)
                match_bytesN_classic  = re.search(pattern_bytesN_classic , calldata_lifetime_without_spaces)
                if match_bytesN_classic :
                    foreign_key_mask = match_bytesN_classic.group(1)
                    foreign_key_type = self.type.bytesN_base(foreign_key_mask)
                    break 
                pattern_bytesN_modern = r'\(CallData\(0x4\)\)&\(NOT\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(0x4))&(NOT(0x1)<<(0xc8)
                match_bytesN_modern  = re.search(pattern_bytesN_modern , calldata_lifetime_without_spaces)
                if match_bytesN_modern :
                    foreign_key_mask = match_bytesN_modern.group(1)
                    foreign_key_type = self.type.bytesN_base(foreign_key_mask)
                    break
                if '0xa0' in lifetime and '&' in lifetime:
                    foreign_key_type = 'address'
                    break
                foreign_key_count += 1
                if foreign_key_count == len(self.calldata_lifetime[0]):
                    foreign_key_type = 'uint256'
                 
            #print(foreign_key_type)    
            internal_key_count = 0 
            for lifetime in self.calldata_lifetime[1]:                               #for internal key
                calldata_lifetime_without_spaces = lifetime.replace(" ", "")
                pattern_uint_modern = r'\(CallData\(0x4\+0x20\)\)&\(\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(0x4 + 0x20))&((0x1)<<(0xf0)
                match_uint_modern = re.search(pattern_uint_modern, calldata_lifetime_without_spaces)
                if match_uint_modern:
                    internal_key_mask = match_uint_modern.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break
                pattern_uint_modern_1 = r'\(CallData\(0x20\+0x4\)\)&\(\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(0x4 + 0x20))&((0x1)<<(0xf0)
                match_uint_modern_1 = re.search(pattern_uint_modern_1, calldata_lifetime_without_spaces)
                if match_uint_modern_1:
                    internal_key_mask = match_uint_modern_1.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break
                pattern_uint_classic_1 = r'\(CallData\(0x24\)\)&\((0x[f]+)\)'
                #(CallData(0x24))&(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
                match_uint_classic_1 = re.search(pattern_uint_classic_1, calldata_lifetime_without_spaces)
                if match_uint_classic_1:
                    internal_key_mask = match_uint_classic_1.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break
                pattern_uint_classic_1_1 = r'\(CallData\(0x20\+0x4\)\)&\((0x[f]+)\)'
                #(CallData(0x20+0x4))&(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
                match_uint_classic_1_1 = re.search(pattern_uint_classic_1_1, calldata_lifetime_without_spaces)
                if match_uint_classic_1_1:
                    internal_key_mask = match_uint_classic_1_1.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break
                pattern_uint_classic_1_2 = r'\(CallData\(0x4\+0x20\)\)&\((0x[f]+)\)'
                #(CallData(0x4+0x20))&(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
                match_uint_classic_1_2 = re.search(pattern_uint_classic_1_2, calldata_lifetime_without_spaces)
                if match_uint_classic_1_2:
                    internal_key_mask = match_uint_classic_1_2.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break
                pattern_uint_classic_2 = r'\((0x[f]+)\)&\(CallData\(0x24\)\)'
                #(0xffffffffffffffffffffffffffffffffffffffff)&(CallData(0x24))
                match_uint_classic_2 = re.search(pattern_uint_classic_2, calldata_lifetime_without_spaces)
                if match_uint_classic_2 and '==0?' not in calldata_lifetime_without_spaces:
                    internal_key_mask = match_uint_classic_2.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break  
                pattern_uint_classic_2_1 = r'\((0x[f]+)\)&\(CallData\(0x20\+0x4\)\)'
                #(0xffffffffffffffffffffffffffffffffffffffff)&(CallData(0x20+0x4))
                match_uint_classic_2_1 = re.search(pattern_uint_classic_2_1, calldata_lifetime_without_spaces)
                if match_uint_classic_2_1 and '==0?' not in calldata_lifetime_without_spaces:
                    internal_key_mask = match_uint_classic_2_1.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break  
                pattern_uint_classic_2_2 = r'\((0x[f]+)\)&\(CallData\(0x4\+0x20\)\)'
                #(0xffffffffffffffffffffffffffffffffffffffff)&(CallData(0x4+0x20))
                match_uint_classic_2_2 = re.search(pattern_uint_classic_2_2, calldata_lifetime_without_spaces)
                if match_uint_classic_2_2 and '==0?' not in calldata_lifetime_without_spaces:
                    internal_key_mask = match_uint_classic_2_2.group(1)
                    internal_key_type = self.type.uint_base(internal_key_mask)
                    break  
                pattern_int = r'\((0x[0-9A-Fa-f]+)\)sig_ext\(CallData\('
                #(0x13)sig_ext(CallData(
                match_int = re.search(pattern_int, calldata_lifetime_without_spaces)
                if match_int:
                    internal_key_mask = match_int.group(1)
                    internal_key_type = self.type.int_base(internal_key_mask)
                    break  
                pattern_bool = r'\(CallData\(.*?\)==0\?\)==0\?'
                #(CallData(...)==0?)==0?
                match_bool = re.search(pattern_bool, calldata_lifetime_without_spaces)
                if match_bool:
                    internal_key_mask = 'double iszero'
                    internal_key_type = self.type.bool_base(internal_key_mask)
                    break                 
                pattern_bytesN_classic = r'\(CallData\(.*?\)\)&\(NOT(0x[f]+)\)'
                #(CallData(...))&(NOT0xffffffffffffffffffffffffffffffffffffffffffffffffff)
                match_bytesN_classic  = re.search(pattern_bytesN_classic , calldata_lifetime_without_spaces)
                if match_bytesN_classic :
                    internal_key_mask = match_bytesN_classic.group(1)
                    internal_key_type = self.type.bytesN_base(internal_key_mask)
                    break 
                pattern_bytesN_modern = r'\(CallData\(.*?\)\)&\(NOT\(0x1\)<<\((0x[0-9A-Fa-f]+)\)'
                #(CallData(...))&(NOT(0x1)<<(0xc8)
                match_bytesN_modern  = re.search(pattern_bytesN_modern , calldata_lifetime_without_spaces)
                if match_bytesN_modern :
                    internal_key_mask = match_bytesN_modern.group(1)
                    internal_key_type = self.type.bytesN_base(internal_key_mask)
                    break
                if '0xa0' in lifetime and '&' in lifetime:
                    internal_key_type = 'address'
                    break
                internal_key_count += 1
                if internal_key_count == len(self.calldata_lifetime[1]):
                    internal_key_type = 'uint256'
                
            #print(internal_key_type)    
            pattern_bytesN_svalue = r'<<\((0x[0-9A-Fa-f]+)\)&NOT0x[f]+'                        #for value
            #<<(0x30) & NOT0xffffffffffff 
            memory_log_without_spaces = self.memory_log[7].replace(" ", "")
            match_bytesN_svalue = re.search(pattern_bytesN_svalue, memory_log_without_spaces)
            if match_bytesN_svalue:
                value_mask = match_bytesN_svalue.group(1)
                value_type = self.type.bytesN_base(value_mask)
                result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot))   
            pattern_bytesN_classic_svalue = r'&NOT(0x[f]+)'                        
            #& NOT0xffffffffffff 
            memory_log_without_spaces = self.memory_log[7].replace(" ", "")
            match_bytesN_classic_svalue = re.search(pattern_bytesN_classic_svalue, memory_log_without_spaces)
            if match_bytesN_classic_svalue:
                value_mask = match_bytesN_classic_svalue.group(1)
                value_type = self.type.bytesN_base(value_mask)
                result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot))      
            pattern_bool_svalue = r'==0\?==0\?'                        
            #==0?==0?
            memory_log_without_spaces = self.memory_log[7].replace(" ", "")
            match_bool_svalue = re.search(pattern_bool_svalue, memory_log_without_spaces)
            if match_bool_svalue:
                value_mask = 'double iszero'
                value_type = self.type.bool_base(value_mask)
                result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot))     
            pattern_uint_svalue = r'(0x[f]+)&svalue\(hash'                        
            # 0xffffffffff & svalue(ha
            memory_log_without_spaces = self.memory_log[7].replace(" ", "")
            match_uint_svalue = re.search(pattern_uint_svalue, memory_log_without_spaces)
            if match_uint_svalue and '==0?' not in memory_log_without_spaces:
                value_mask = match_uint_svalue.group(1)
                value_type = self.type.uint_base(value_mask)
                result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot))                    
            pattern_uint_modern_svalue = r'\(0x1\)<<\((0x[0-9A-Fa-f]+)\)\-0x1&svalue\(hash'                        
            #(0x1)<<(0xf0) - 0x1 & svalue(hash 
            memory_log_without_spaces = self.memory_log[7].replace(" ", "")
            match_uint_modern_svalue = re.search(pattern_uint_modern_svalue, memory_log_without_spaces)
            if match_uint_modern_svalue and '==0?' not in memory_log_without_spaces:
                value_mask = match_uint_modern_svalue.group(1)
                value_type = self.type.uint_base(value_mask)
                result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot))        
            pattern_int_svalue = r'sig(0x[0-9A-Fa-f]+)'                        
            #sig 0x1d 
            memory_log_without_spaces = self.memory_log[7].replace(" ", "")
            match_int_svalue = re.search(pattern_int_svalue, memory_log_without_spaces)
            if match_int_svalue:
                value_mask = match_int_svalue.group(1)
                value_type = self.type.int_base(value_mask)
                result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot)) 
            #uint256
            if len(self.svalue_lifetime) == 1 and len(self.svalue_lifetime[0]) == 2:
                if '__mstore(mvalue(0x40)) in block' in self.svalue_lifetime[0][1]:
                    value_type = '(u)int256/bytes32'
                    result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot)) 

            if ('sig' not in self.memory_log[7] and
                '<<' not in self.memory_log[7] and
                '&' not in self.memory_log[7] and
                '==0?' not in self.memory_log[7] and
                'NOT' not in self.memory_log[7]):
                value_type = '(u)int256/bytes32'
                result.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_type, slot)) 
               
            


        memory_log_rule_for_struct_nestedmapping = False                     #for nestedmapping value is struct
        if ('storein_0x20' in self.memory_log[0] and
            'CallData(' in self.memory_log[1] and
            'storein_0x0' in self.memory_log[1] and
            'sha3(0x0,0x40)' in self.memory_log[2] and
            'hash of the given data' in self.memory_log[3] and
            'storein_0x20' in self.memory_log[3] and
            'CallData(' in self.memory_log[4] and
            'storein_0x0' in self.memory_log[4] and         
            'sha3(0x0,0x40)' in self.memory_log[5] and
            'load_0x40' in self.memory_log[6] and
            'svalue(hash' in self.memory_log[7] and
            'svalue(hash' in self.memory_log[8] and
            'svalue(hash' in self.memory_log[9]):
            memory_log_rule_for_struct_nestedmapping = True
            
        value_list = []                
        if(stack_rule_compliance_level >= 7 and
           len(self.calldata_lifetime) == 2 and
           len(self.svalue_lifetime) == 2 and
           mvalue_lifetime_rule and memory_log_rule_for_struct_nestedmapping):
            
            pattern_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20 in'
            if re.search(pattern_slot, self.memory_log[0]):
                slot = re.search(pattern_slot, self.memory_log[0]).group(1)
            
            if ('CallData(0x4)' in self.calldata_lifetime[0][1] and
                '&' in self.calldata_lifetime[0][1] and
                '^0xa0' in self.calldata_lifetime[0][1]):
                foreign_key_type = 'address'
            if self.calldata_lifetime[1][1].startswith('__mstore(0x0)'):
                internal_key_type = '(u)int/bytes32'
                
            for item in self.memory_log[7:]:
                if item.startswith('svalue') and re.search(r'svalue\(.*?\) _storein', item):
                    value_list.append('(u)int/bytes32')
                if re.search(r'(0x[f]+) & svalue\(hash', item):
                    mask = re.search(r'(0x[f]+) & svalue\(hash', item).group(1)
                    value_list.append(self.type.uint_base(mask))
            result.append('mapping(%s => mapping(%s => struct%s)) //slot(%s)' % (foreign_key_type, internal_key_type, value_list, slot)) 

        return(result) 
   
        
   
    def rule_for_struct(self):
        value_list = []
        stack_rule_list = ['as slot index']  #stack rules
        stack_rule_compliance_level = 0
        for rule_item in stack_rule_list:
            for lifetime in self.stackvariable_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        stack_rule_compliance_level += 1    
                        
        calldata_rule = False
        if len(self.calldata_lifetime) == 0:
            calldata_rule = True
            
        svalue_lifetime_rule = False
        svalue_rule_list_1 = [ 'mstore']
        svalue_rule_compliance_level_1 = 0
        for rule_item in svalue_rule_list_1:
            for lifetime in self.svalue_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        svalue_rule_compliance_level_1 += 1
        svalue_rule_list_2 = [ '/', '÷']                
        svalue_rule_compliance_level_2 = 0
        for rule_item in svalue_rule_list_2:
            for lifetime in self.svalue_lifetime:
                for life in lifetime:
                    if rule_item in life:
                        svalue_rule_compliance_level_2 += 1
                        
        if (len(self.svalue_lifetime) >= 2 and
            svalue_rule_compliance_level_1 >= 2):
            svalue_lifetime_rule = True

        if (len(self.svalue_lifetime) < 2 and
            svalue_rule_compliance_level_2 > 1):
            svalue_lifetime_rule = True
            
            
            
            
        #print('storein_mvalue(' in self.memory_log[1])    
        if (stack_rule_compliance_level >= 1 and
            calldata_rule and
            svalue_lifetime_rule and
            'svalue(' in self.memory_log[1] and
            'storein_' in self.memory_log[1] and
            'load_0x40' in self.memory_log[0] and
            'load_0x40' in self.memory_log[-1] and
            len(self.memory_log) > 3):
            for log in self.memory_log:
                #print('1')
                log_without_spaces = log.replace(" ", "")
                #svalue(0x5)  & 0xffffffffffffffffffffffffffffffffffffffff
                pattern_address_classic = r'svalue\((0x[0-9A-Fa-f]+)\).*?&0xffffffffffffffffffffffffffffffffffffffff'
                match_address_classic = re.search(pattern_address_classic, log_without_spaces)
                if match_address_classic and '0xfffffffffffffffffffffffffffffffffffffffff' not in log_without_spaces:
                    slot = match_address_classic.group(1)
                    value_list.append('address //slot(%s)' % slot)
                    continue
                #svalue(0x5)  & (0x1)<<(0xa0) - 0x1 
                pattern_address_modern = r'svalue\((0x[0-9A-Fa-f]+)\).*?&\(0x1\)<<\(0xa0\)'
                match_address_modern = re.search(pattern_address_modern, log_without_spaces)
                if match_address_modern:
                    slot = match_address_modern.group(1)
                    value_list.append('address //slot(%s)' % slot)
                    continue
                #svalue(0x4) _storein_0x40 + mvalue(0x40)
                pattern_uint256_0 = r'svalue\((0x[0-9A-Fa-f]+)\)_storein_0x40\+mvalue\(0x40\)'
                match_uint256_0 = re.search(pattern_uint256_0, log_without_spaces)
                if match_uint256_0:
                    slot = match_uint256_0.group(1)
                    value_list.append('(u)int256/bytes32 //slot(%s)' % slot)
                    continue
                #svalue(0x1) _storein_mvalue(0x40)
                pattern_uint256 =  r'svalue\((0x[0-9A-Fa-f]+)\)_storein_mvalue\(0x40\)'
                match_uint256 = re.search(pattern_uint256, log_without_spaces)
                if match_uint256:
                    slot = match_uint256.group(1)
                    value_list.append('(u)int256/bytes32 //slot(%s)' % slot)
                    continue
                #svalue(0x2) /0x100 & 0xff
                pattern_uint_low_packing = r'svalue\((0x[0-9A-Fa-f]+)\)/0x[0-9A-Fa-f]+&(0x[f]+)'
                match_uint_low_packing = re.search(pattern_uint_low_packing, log_without_spaces)
                if match_uint_low_packing and '==0?' not in log_without_spaces and '00000' not in log_without_spaces:
                    slot = match_uint_low_packing.group(1)
                    mask = match_uint_low_packing.group(2)
                    _type = self.type.uint_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #0xff & svalue(0x2)
                pattern_uint_low = r'(0x[f]+)&svalue\((0x[0-9A-Fa-f]+)\)'
                match_uint_low = re.search(pattern_uint_low, log_without_spaces)
                if match_uint_low and '==0?==0?' not in log_without_spaces:
                    #print('diu')
                    mask = match_uint_low.group(1)
                    slot = match_uint_low.group(2)
                    _type = self.type.uint_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #svalue(0x3)  & (0x1)<<(0xf0) - 0x1
                pattern_uint_high_1 = r'svalue\((0x[0-9A-Fa-f]+)\).*?&\(0x1\)<<\((0x[0-9A-Fa-f]+)\)\-0x1'
                match_uint_high_1 = re.search(pattern_uint_high_1, log_without_spaces)
                if match_uint_high_1:
                    mask = match_uint_high_1.group(2)
                    slot = match_uint_high_1.group(1)
                    _type = self.type.uint_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #svalue(0x3)  & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
                pattern_uint_high_2 = r'svalue\((0x[0-9A-Fa-f]+)\)&(0x[f]+)'
                match_uint_high_2 = re.search(pattern_uint_high_2, log_without_spaces)
                if match_uint_high_2 and '==0?' not in log_without_spaces and '00000' not in log_without_spaces:
                    slot = match_uint_high_2.group(1)
                    mask  = match_uint_high_2.group(2)
                    _type = self.type.uint_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #svalue(0x0) /0x10000 sig 0x1
                pattern_int_low_packing = r'svalue\((0x[0-9A-Fa-f]+)\)/0x[0-9A-Fa-f]+sig(0x[0-9A-Fa-f]+)'
                match_int_low_packing = re.search(pattern_int_low_packing, log_without_spaces)
                if match_int_low_packing:
                    slot = match_int_low_packing.group(1)
                    mask = match_int_low_packing.group(2)
                    _type = self.type.int_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #svalue(0x4)  sig 0x1d
                pattern_int_unpacking = r'svalue\((0x[0-9A-Fa-f]+)\)sig(0x[0-9A-Fa-f]+)'
                match_int_unpacking = re.search(pattern_int_unpacking, log_without_spaces)
                if match_int_unpacking:
                    slot = match_int_unpacking.group(1)
                    mask = match_int_unpacking.group(2)
                    _type = self.type.int_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #0xff & svalue(0x0 + 0xc) ==0?==0?
                pattern_bool_1 = r'0xff&svalue\(0x0\+(0x[0-9A-Fa-f]+)\).*?==0\?==0\?'
                match_bool_1 = re.search(pattern_bool_1, log_without_spaces)
                if match_bool_1:
                    slot = match_bool_1.group(1)
                    mask = 'double iszero'
                    _type = self.type.bool_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #0xff & svalue(0xc + 0x0) ==0?==0?
                pattern_bool_2 = r'0xff&svalue\((0x[0-9A-Fa-f]+)\+0x0\).*?==0\?==0\?'
                match_bool_2 = re.search(pattern_bool_2, log_without_spaces)
                if match_bool_2:
                    slot = match_bool_2.group(1)
                    mask = 'double iszero'
                    _type = self.type.bool_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #0xff & svalue(0xc) ==0?==0?
                pattern_bool_3 = r'0xff&svalue\((0x[0-9A-Fa-f]+)\).*?==0\?==0\?'
                match_bool_3 = re.search(pattern_bool_3, log_without_spaces)
                if match_bool_3:
                    slot = match_bool_3.group(1)
                    mask = 'double iszero'
                    _type = self.type.bool_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #svalue(0x0) /0x10000000000000000000000000000000000000000 & 0xff==0?==0?_storein
                pattern_bool_4 = r'svalue\((0x[0-9A-Fa-f]+)\).*?&0xff==0\?==0\?_storein'
                match_bool_4 = re.search(pattern_bool_4, log_without_spaces)
                if match_bool_4:
                    slot = match_bool_4.group(1)
                    mask = 'double iszero'
                    _type = self.type.bool_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue            
                #NOT(0x1)<<(0xe8) - 0x1 & (svalue(0x0 + 0x7) )<<(0xe8)_storein_mvalue(0x40) + 0x100
                pattern_bytesN_1 = r'NOT\(0x1\)<<\((0x[0-9A-Fa-f]+)\)\-0x1&\(svalue\(0x0\+(0x[0-9A-Fa-f]+)\)\)'
                match_bytesN_1 = re.search(pattern_bytesN_1, log_without_spaces)
                if match_bytesN_1:
                    mask = match_bytesN_1.group(1)
                    slot = match_bytesN_1.group(2)
                    _type = self.type.bytesN_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #NOT(0x1)<<(0xe8) - 0x1 & (svalue(0x7 + 0x0) )<<(0xe8)_storein_mvalue(0x40) + 0x100
                pattern_bytesN_2 = r'NOT\(0x1\)<<\((0x[0-9A-Fa-f]+)\)\-0x1&\(svalue\((0x[0-9A-Fa-f]+)\+0x0\)\)'
                match_bytesN_2 = re.search(pattern_bytesN_2, log_without_spaces)
                if match_bytesN_2:
                    mask = match_bytesN_2.group(1)
                    slot = match_bytesN_2.group(2)
                    _type = self.type.bytesN_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #NOT(0x1)<<(0xe8) - 0x1 & (svalue(0x7) )<<(0xe8)_storein_mvalue(0x40) + 0x100
                pattern_bytesN_3 = r'NOT\(0x1\)<<\((0x[0-9A-Fa-f]+)\)\-0x1&\(svalue\((0x[0-9A-Fa-f]+)\)\)'
                match_bytesN_3 = re.search(pattern_bytesN_3, log_without_spaces)
                if match_bytesN_3:
                    mask = match_bytesN_3.group(1)
                    slot = match_bytesN_3.group(2)
                    _type = self.type.bytesN_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #svalue(0x7)  & 0xffffffff0000000000000000000000000000000000000000000000000000000000_storein_mvalue(0x40)
                pattern_bytesN_low_1 = r'svalue\((0x[0-9A-Fa-f]+)\).*?0xffffffff[0]+'
                match_bytesN_low_1 = re.search(pattern_bytesN_low_1, log_without_spaces)
                if match_bytesN_low_1:
                    slot = match_bytesN_low_1.group(1)
                    value_list.append('bytes4 //slot(%s)' % slot)
                    continue
                #svalue(0x7)  & 0xffffff00000000000000000000000
                pattern_bytesN_low_2 = r'svalue\((0x[0-9A-Fa-f]+)\).*?0xffffff[0]+'
                match_bytesN_low_2 = re.search(pattern_bytesN_low_2, log_without_spaces)
                if match_bytesN_low_2:
                    slot = match_bytesN_low_2.group(1)
                    value_list.append('bytes3 //slot(%s)' % slot)
                    continue
                #svalue(0x7)  & 0xffff00000000000000000000000
                pattern_bytesN_low_3 = r'svalue\((0x[0-9A-Fa-f]+)\).*?0xffff[0]+'
                match_bytesN_low_3 = re.search(pattern_bytesN_low_3, log_without_spaces)
                if match_bytesN_low_3:
                    slot = match_bytesN_low_3.group(1)
                    value_list.append('bytes2 //slot(%s)' % slot)
                    continue
                #svalue(0x7)  & 0xff00000000000000000000000
                pattern_bytesN_low_4 = r'svalue\((0x[0-9A-Fa-f]+)\).*?0xff[0]+'
                match_bytesN_low_4 = re.search(pattern_bytesN_low_4, log_without_spaces)
                if match_bytesN_low_4:
                    slot = match_bytesN_low_4.group(1)
                    value_list.append('bytes1 //slot(%s)' % slot)
                    continue
                #svalue(0x4) *0x1000000000000000000000000000000000000000000000000 & NOT0xffffffffffffffffffffffffffffffffffffffffffffffff
                pattern_bytesN_5 = r'svalue\((0x[0-9A-Fa-f]+)\).*?&NOT(0x[f]+)'
                match_bytesN_5 = re.search(pattern_bytesN_5, log_without_spaces)
                if match_bytesN_5:
                    slot = match_bytesN_5.group(1)
                    mask = match_bytesN_5.group(2)
                    _type = self.type.int_base(mask)
                    value_list.append('%s //slot(%s)' % (_type, slot))
                    continue
                #svalue(0x6)  & NOT0x0 + 0x100*svalue(0x6)  & 0x1==0?/0x2_storein_mvalue(0x40) + 0x140
                pattern_string_1 = r'svalue\((0x[0-9A-Fa-f]+)\)&NOT0x0\+0x100'
                match_string_1 = re.search(pattern_string_1, log_without_spaces)
                if match_string_1 and '0x140' in log_without_spaces:
                    slot = match_string_1.group(1)
                    value_list.append('string //slot(%s)' % slot)
                    continue
                #mvalue(0x40) + 0x20 + 0x1f + (svalue(0x6) )>>(0x1)/0x20*0x20_storein
                pattern_string_2 = r'svalue\((0x[0-9A-Fa-f]+)\)\)?>>\(0x1\)'
                match_string_2 = re.search(pattern_string_2, log_without_spaces)
                if match_string_2 and '0x1f' in log_without_spaces:
                    slot = match_string_2.group(1)
                    value_list.append('string //slot(%s)' % slot)
                    continue
                #'0x20 + mvalue(0x40) + 0x20*svalue(0x18)  & NOT0x0 + 0x100*svalue(0x18)  & 0x1==0?/0x2 + 0x1f/0x20_storein_0x40 in block_955'
                pattern_string_3 = r'&NOT0x0\+0x100\*svalue\((0x[0-9A-Fa-f]+)\).*?0x1f'
                match_string_3 = re.search(pattern_string_3, log_without_spaces)
                if match_string_3:
                    slot = match_string_3.group(1)
                    value_list.append('string //slot(%s)' % slot)
                    continue
                #'0x2^0xa0 - 0x1 & 0x2^0xa0 - 0x1 & svalue(0x17 + 0x3)  & 0x2^0xa0 - 0x1_storein_0x20 + 0x20 + mvalue(0x40) in block_405'
                pattern_add_slot = r'svalue\((0x[0-9A-Fa-f]+)\+(0x[0-9A-Fa-f]+)\)'
                match_add_slot = re.search(pattern_add_slot, log_without_spaces)
                if match_add_slot:
                    slot = hex(int(match_add_slot.group(1), 16) + int(match_add_slot.group(2), 16))
                    if '0xa0' in log_without_spaces:
                        value_list.append('address //slot(%s)' % slot)
                        continue
                    if log_without_spaces.startswith('svalue(%s+%s)_storein' % (match_add_slot.group(1) , match_add_slot.group(2))):
                        #print(123)
                        value_list.append('(u)int256/bytes32 //slot(%s)' % slot)
                        continue
                
            struct_slot_list = []   
            for item in value_list:
                pattern_slot = r'//slot\((0x[0-9A-Fa-f]+)\)'
                match_slot = re.search(pattern_slot, item)
                if match_slot:
                    struct_slot_list.append(match_slot.group(1))
            decimal_list = [int(hex_val, 16) for hex_val in struct_slot_list]
            min_slot = min(decimal_list)
            max_slot = max(decimal_list)
            complete_struct_slot_list = [i for i in range(min_slot, max_slot + 1)]
            missing_slots = [val for val in complete_struct_slot_list if val not in decimal_list]
            missing_hex_slots = [hex(val) for val in missing_slots]
            for slot in missing_hex_slots:
                value_list.append('_[-],_[ ],mapping //slot(%s)' % slot)  #If the slot is found to be discontinuous, it will be automatically completed because these types are invisible
            
            if len(value_list) == 0:
                raise ValueError("not struct but in")
                
            return ('struct{%s}' % value_list)
                    
  
            
if __name__ == '__main__':
    asm_file = 'disassembly_result.txt'
    fun_sig = function_signature_hash_extractor.FunctionSignatureHashExtractor(asm_file)
    tf_path = path_through_function.PathThroughFunction(asm_file)
    path = tf_path.TFPath(fun_sig.extract_function_signatures()[0])
    #print(fun_sig.extract_function_signatures()[1])
    r_w_analysis = variables_read_write_analysis.Analyzer()
    result = r_w_analysis.block_analysis(path)
    #print(result)
    stackvariable_lifetime =  result[0]
    calldata_lifetime = result[1]
    mvalue_lifetime = result[2]
    memory_log = result[3]
    svalue_lifetime = result[4]
    rule = RulesForPublicStateVars(stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime)
    result = rule.rule_for_mapping()
    print(result)
  


