#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 14:59:46 2023

@author: lyc
"""
import path_through_function
import function_signature_hash_extractor
import variables_read_write_analysis
from function_splitter import call_all_rules
import time
from type_base import TypeBase
import re
start_time = time.time()
class PublicFunctionAnalyzer:
    def __init__(self, stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime):
        self.stackvariable_lifetime = stackvariable_lifetime
        self.calldata_lifetime = calldata_lifetime
        self.mvalue_lifetime = mvalue_lifetime
        self.memory_log = memory_log
        self.svalue_lifetime = svalue_lifetime
        self.type = TypeBase()
        self.public_states = call_all_rules()
        self.solved_slot_type_dict = {}
        
        self.private_value_type_slot = []
        self.private_staticarray_slot = []
        self.private_nestedstaticarray_slot = []
        self.private_dynamicarray_slot =[]
        self.private_mapping_slot = []
        self.private_nested_mapping_slot = []
        
        self.variable_list = []
    
    def slot_analysis(self):
        public_slot = []
        
        for item in self.public_states:
            pattern = r'slot\((0x[0-9A-Fa-f]+)\)'
            match = re.search(pattern, item)
            if match:
                public_slot.append(match.group(1))
        #Different variables have different ways of presenting slots
        #uint, int, bool, address, bytesN, string: svalue (slot)
        pattern_value_type_slot = r'svalue\((0x[0-9A-Fa-f]+)\)'
        #_[-]: svalue(CallData(-) + slot)
        pattern_staticarray_slot = r'svalue\(CallData\(.*?\).*?\+(0x[0-9A-Fa-f]+)\)'
        #_[-][-]: svalue(CallData(0x4 + 0x20)/0x10 + CallData(0x4) + slot)
        pattern_nestedstaticarray_slot = r'svalue\(CallData\(.*?\).*?\+CallData\(.*?\).*?\+(0x[0-9A-Fa-f]+)\)'
        #_[]:(CallData(0x4))<(svalue(slot) )?
        #_[-][]: (CallData(0x4))<(svalue(slot) )?
        pattern_dynamicarray_slot_1 = r'\(CallData\(0x4\)\)?<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?'
        #(CallData(0x24))<(svalue(0x6) )?
        pattern_dynamicarray_slot_2 = r'\(CallData\(0x24\)\)?<\(svalue\((0x[0-9A-Fa-f]+)\)\)\?'
        #mapping: 'caller address & (0x1)<<(0xa0) - 0x1_storein_0x0 in block_284', '0x7_storein_0x20 in block_284', 'sha3(0x0,0x40) in block_284',
        pattern_mapping_key = r'_storein_0x0 in block'
        pattern_mapping_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20'
        pattern_mapping_hash = r'sha3\(0x0,(?:0x20\s*\+\s*){2}0x0|0x40\) in block'
        
        #nested mapping #CallData(0x4)_storein_0x0
        pattern_nested_mapping_foreign_key = r'(CallData.*?)?_storein_0x0'
        #0x4_storein_0x20
        pattern_nested_mapping_slot = r'(0x[0-9A-Fa-f]+)_storein_0x20'
        #sha3(0x0,0x40)
        pattern_nested_mapping_internal_slot_computing = r'sha3\(0x0,(?:0x20\s*\+\s*){2}0x0|0x40\)'
        #(0x1)<<(0xa0) - 0x1 & CallData(0x4 + 0x20)_storein_0x0
        pattern_nested_mapping_internal_key = r'_storein_0x0'
        #hash of the given data(b'(0x1)<<(0xa0) - 0x1 & CallData(0x4)_offset=0x0',b'0x4_offset=0x20') in memory, offset = 0x0, size = 0x40._storein_0x20
        pattern_nested_mapping_internal_slot_store = r'hash of the given data\(b.*?_storein_0x20'
        #sha3(0x0,0x40)
        pattern_nested_mapping_value_slot_computing = r'sha3\(0x0,(?:0x20\s*\+\s*){2}0x0|0x40\)'
        
        
        for variable_lifetime in self.svalue_lifetime:
            for lifetime in variable_lifetime:
                lifetime_without_space = lifetime.replace(" ", "")
                
                match_dynamicarray_slot_1 = re.search(pattern_dynamicarray_slot_1, lifetime_without_space)
                if match_dynamicarray_slot_1:
                    slot = match_dynamicarray_slot_1.group(1)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_value_type_slot:
                        self.private_dynamicarray_slot.append(slot)
                        break
                match_dynamicarray_slot_2 = re.search(pattern_dynamicarray_slot_2, lifetime_without_space)
                if match_dynamicarray_slot_2:
                    slot = match_dynamicarray_slot_2.group(1)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_value_type_slot:
                        self.private_dynamicarray_slot.append(slot)
                        break
                
                match_value_type_slot = re.search(pattern_value_type_slot, lifetime_without_space)
                if match_value_type_slot:
                    slot = match_value_type_slot.group(1)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list) and ('<(svalue(%s)' % slot not in lifetime_without_space):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_value_type_slot and '<(svalue(%s)' % slot not in lifetime_without_space:
                        self.private_value_type_slot.append(slot)
                        break
                        
                match_staticarray_slot = re.search(pattern_staticarray_slot, lifetime_without_space)
                if match_staticarray_slot:
                    slot = match_staticarray_slot.group(1)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_staticarray_slot:
                        self.private_staticarray_slot.append(slot)
                        break
                
                match_nestedstaticarray_slot = re.search(pattern_nestedstaticarray_slot, lifetime_without_space)
                if match_nestedstaticarray_slot:
                    slot = match_nestedstaticarray_slot.group(1)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_nestedstaticarray_slot:
                        self.private_nestedstaticarray_slot.append(slot)
                        break
                        

                        

        for index, log in enumerate(self.memory_log):                            #mapping slot
            #print(index)
            if index < len(self.memory_log) - 2:
                match_mapping_key = re.search(pattern_mapping_key, log)
                match_mapping_slot = re.search(pattern_mapping_slot, self.memory_log[index + 1])
                match_mapping_hash = re.search(pattern_mapping_hash, self.memory_log[index + 2])
                
                if (len(self.memory_log) < 4 and
                    match_mapping_key and 
                    match_mapping_slot and 
                    match_mapping_hash):
                    slot = match_mapping_slot.group(1)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_mapping_slot:
                        self.private_mapping_slot.append(slot)
                
                if (len(self.memory_log) > 3 and 
                    index < len(self.memory_log) - 4 and
                    match_mapping_key and 
                    match_mapping_slot and 
                    match_mapping_hash and 
                    'storein_0x20' not in self.memory_log[index + 4]):
                    slot = match_mapping_slot.group(1)
                    #print(slot)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_mapping_slot:
                        self.private_mapping_slot.append(slot)

                        
        for index, log in enumerate(self.memory_log):                            #nested mapping slot
            if index < len(self.memory_log) - 5:
                #print('1')
                match_nested_mapping_foreign_key = re.search(pattern_nested_mapping_foreign_key, log)
                match_nested_mapping_slot = re.search(pattern_nested_mapping_slot, self.memory_log[index + 1])
                match_nested_mapping_internal_slot_computing = re.search(pattern_nested_mapping_internal_slot_computing, self.memory_log[index + 2])
                match_nested_mapping_internal_key = re.search(pattern_nested_mapping_internal_key, self.memory_log[index + 3])
                match_nested_mapping_internal_slot_store = re.search(pattern_nested_mapping_internal_slot_store, self.memory_log[index + 4])
                match_nested_mapping_value_slot_computing = re.search(pattern_nested_mapping_value_slot_computing, self.memory_log[index + 5])
                
                if (match_nested_mapping_foreign_key and
                    match_nested_mapping_slot and
                    match_nested_mapping_internal_slot_computing and
                    match_nested_mapping_internal_key and
                    match_nested_mapping_internal_slot_store and
                    match_nested_mapping_value_slot_computing):
                    #print('1')
                    slot = match_nested_mapping_slot.group(1)
                    if (slot in public_slot) and ('Using State(%s)' % slot not in self.variable_list):
                        self.variable_list.append('Using State(%s)' % slot)
                    if slot not in public_slot and slot not in self.private_nested_mapping_slot:
                        self.private_nested_mapping_slot.append(slot)
                        #print(self.private_nested_mapping_slot)

                
                
    def get_public_slot_type(self, slot):        
        pattern_slot = r'<0x[0-9A-Fa-f]+> (.*?) //slot\((0x[0-9A-Fa-f]+)\)'
        for state in self.public_states:
            #<0xf8b45b05> uint256 //slot(0xf)
            match = re.search(pattern_slot, state)
            if match:
                _type = match.group(1)
                _slot = match.group(2)
                self.solved_slot_type_dict[_slot] = _type
        return self.solved_slot_type_dict.get(slot, None)
         
        
    def private_states_type_analysis(self):
        self.slot_analysis()
        if len(self.private_value_type_slot) != 0:  
            #print(self.private_value_type_slot)
            for slot in self.private_value_type_slot:          #value type including uint,int,bool,addrss,bytesN,string,bytes  
                for svalue in self.svalue_lifetime:
                    #(svalue(0x0) )SSTORE IN(hash of the given data(b'0x1 + svalue(0x7)  - 0x1_offset=0x0',b'0x4_offset=0x20') in memory, offset = 0x0, size = 0x40.) in block_260
                    pattern_uint = r'svalue\({}\).*?\)SSTORE IN'.format(re.escape(slot))
                    if len(svalue) > 1:
                        match_uint = re.search(pattern_uint, svalue[1])
                        if match_uint and '0x2^0xa0 - 0x1 & svalue(%s)' % slot not in svalue[1]:
                            self.variable_list.append('uint private //slot(%s)' % slot)
                            break
                    if len(svalue) > 1 and '0x2^0xa0 - 0x1 & svalue(%s)' % slot in svalue[1]:
                        self.variable_list.append('address private //slot(%s)' % slot)
                        break

                for stackvariable_lifetime in self.stackvariable_lifetime:                    
                    if len(stackvariable_lifetime) > 1 and '0x1f' in stackvariable_lifetime[0] and 'mvalue(mvalue(0x40))' in stackvariable_lifetime[1]:                        
                        count = 0
                        for log in self.memory_log:                            
                            count += 1
                            if 'mstore8' in log:                                
                                self.variable_list.append('bytes private //slot(%s)' % slot)
                                break
                            if count == len(self.memory_log):
                                flag = True
                                for item in self.variable_list:
                                    if '//slot(%s)' % slot in item:
                                        flag = False
                                        break
                                if flag:

                                    self.variable_list.append('string private //slot(%s)' % slot)
                                        
                                
                                
                    else:     
                        continue
                    break
                
        if len(self.private_mapping_slot) != 0:
            #print(self.private_mapping_slot)
            for slot in self.private_mapping_slot:                           # mapping
                for index, log in enumerate(self.memory_log):
                    #0x7_storein_0x20
                    if '%s_storein_0x20' % slot in log:                       #First determine the mapping to ensure accuracy
                        if (('address' in self.memory_log[index - 1] or
                             '<<(0xa0)' in self.memory_log[index - 1] or
                             '0xffffffffffffffffffffffffffffffffffffffff &' in self.memory_log[index - 1] or
                             '& 0xffffffffffffffffffffffffffffffffffffffff' in self.memory_log[index - 1] or
                             '^0xa0' in self.memory_log[index - 1]) and
                            'storein_0x0' in self.memory_log[index - 1]):           #key
                            key_type = 'address'
                            #print(key_type)
                            break
                        if 'CallData(0x4)_storein_0x0' in self.memory_log[index - 1]:
                            key_type = '(u)int/bytes32'
                            break 
                        else:
                            key_type = 'uint256'


                if len(self.svalue_lifetime) ==0:                                 #value
                    mapping_value_lifetime = self.memory_log[-2]                     
                if len(self.svalue_lifetime) ==1:
                    mapping_value_lifetime = self.svalue_lifetime[0] 
                                       
                for lifetime in self.svalue_lifetime:  #There will be multiple svalues, the relevant one needs to be determined first                               
                    if len(self.svalue_lifetime) > 1 and len(lifetime) > 1 and '%s_offset=0x20' % slot in lifetime[1]:
                        mapping_value_lifetime = lifetime
                        break
                        
                mapping_value_lifetime_list = []  # get longest one in case it is struct
                for lifetime in self.svalue_lifetime:
                    if len(self.svalue_lifetime) > 2 and len(lifetime) > 1 and '%s_offset=0x20' % slot in lifetime[1]:
                        mapping_value_lifetime_list.append(lifetime)
                if mapping_value_lifetime_list:
                    mapping_value_lifetime = max(mapping_value_lifetime_list, key=len)
                #print(mapping_value_lifetime)
                
                    
           
                string_sign = True
                for lifetime in mapping_value_lifetime:
                    if '0x1f' in lifetime:
                        string_sign = False
                        break
                #print(mapping_value_lifetime)
                for lifetime in mapping_value_lifetime:                     #value
                
                    #(svalue(hash of the given data(b'address of currently executing account_offset=0x0',b'0x3_offset=0x20') in memory, offset = 0x0, size = 0x40.) )<(svalue(0xd) )? 
                    pattern_compare_with_svalue = r'svalue\(hashofthegiven.*?\)[<>]\(svalue\((0x[0-9A-Fa-f]+)\)'
                    lifetime_without_space = lifetime.replace(" ", "")
                    match_compare_with_svalue = re.search(pattern_compare_with_svalue, lifetime_without_space)
                    if match_compare_with_svalue:
                        value_type = self.get_public_slot_type(match_compare_with_svalue.group(1))
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' % (key_type, value_type, slot))
                        break
                    
                    if ((len(mapping_value_lifetime) < 6) and 
                        (string_sign) and 
                        ('svalue(hash' in lifetime) and
                        ('+' in lifetime or '-' in lifetime or '*' in lifetime or '/' in lifetime) and
                        '==0?' not in lifetime and
                        '0xff' not in lifetime):
                        #print('here')
                        value_type = 'uint'
                        #print(len(mapping_value_lifetime) < 6)
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' %(key_type, value_type, slot))
                        break
                    elif '==0?' in lifetime and '0xff ' in lifetime and '&' in lifetime:
                        value_type = 'bool'
                        #print(lifetime)
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' %(key_type, value_type, slot))
                        break
                    elif lifetime.startswith('__mstore') and len(mapping_value_lifetime) < 6:
                        value_type = 'uint'
                        #print(len(mapping_value_lifetime) < 6)
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' %(key_type, value_type, slot))
                        break
                        
                    elif 'none' == mapping_value_lifetime:
                        value_type = 'none'
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' %(key_type, value_type, slot))
                        break
                    elif'0x1f' in lifetime and '0x100*0x1' in lifetime and '&' in lifetime and 'svalue(hash' in lifetime and '%s_offset' % slot in lifetime:
                        value_type = 'string'
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' %(key_type, value_type, slot))
                        break               

                    else:
                        value_type = 'uint'
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' %(key_type, value_type, slot))
                        break
                        

                if len(mapping_value_lifetime) >= 6 and string_sign:  #struct
                    #print(mapping_value_lifetime)
                    value_type_list = []
                    for lifetime in mapping_value_lifetime[:-1]:
                        if '0xff ' in lifetime and '&' in lifetime and '==0?' not in lifetime and '%s_offset' % slot in lifetime:
                            value_type_list.append('uint8')
                        if lifetime.startswith('__mstore'):
                            value_type_list.append('(u)int256/bytes32')
                        if '÷' in lifetime:
                            value_type_list.append('(u)int256/bytes32')
                        if '0xff &' in lifetime and '==0?)==0?' in lifetime:
                            value_type_list.append('bool')
                    value_type = 'struct%s' % value_type_list
                    if len(value_type_list) > 1:
                        self.variable_list.append('mapping(%s => %s) private //slot(%s)' %(key_type, value_type, slot))
                    
                    
        if len(self.private_nested_mapping_slot) != 0:           #nested mapping
            #print(self.private_nested_mapping_slot)
            for slot in self.private_nested_mapping_slot:
                for index, log in enumerate(self.memory_log):    #Extract corresponding calldata
                    #print('1')
                    if (index < len(self.memory_log) - 4 and
                        'storein_0x0' in log and 
                        'storein_0x20' in self.memory_log[index + 1] and
                        ('sha3(0x0,0x40)' in self.memory_log[index + 2] or 'sha3(0x0,0x20 + 0x20 + 0x0)' in self.memory_log[index + 2]) and
                        'storein_0x0' in self.memory_log[index + 3] and
                        'storein_0x20' in self.memory_log[index + 4] and
                        'hash of the given data(b' in self.memory_log[index + 4] and
                        ('sha3(0x0,0x40)' in self.memory_log[index + 5] or 'sha3(0x0,0x20 + 0x20 + 0x0)' in self.memory_log[index + 2])):
                        #print('1')
                        
                        if ('<<(0xa0)' in log and '&' in log) or ('address' in log):    #foreign_key
                            foreign_key = 'address'
                            #print('1')
                        elif '0xffffffffffffffffffffffffffffffffffffffff &' in log:
                            foreign_key = 'address'
                        elif '& 0xffffffffffffffffffffffffffffffffffffffff' in log:
                            foreign_key = 'address'
                        elif '^0xa0' in log and '&' in log:
                            foreign_key = 'address'
                        else:
                            foreign_key = 'uint256'
                                                                                        #internal_key
                        if '^0xa0' in self.memory_log[index + 3] and '&' in self.memory_log[index + 3]:
                            internal_key = 'address'                            
                        elif ('<<(0xa0)' in self.memory_log[index + 3] and '&' in self.memory_log[index + 3]) or ('address' in self.memory_log[index + 3]):
                            internal_key = 'address'
                            #print('1')
                        elif '0xffffffffffffffffffffffffffffffffffffffff &' in self.memory_log[index + 3]:
                            internal_key = 'address'
                        elif '& 0xffffffffffffffffffffffffffffffffffffffff' in self.memory_log[index + 3]:
                            internal_key = 'address'                            
                        else:
                            #print(self.memory_log[index + 3])
                            internal_key = 'uint256'
                        if len(self.svalue_lifetime) == 1:                               #value
                            #print('3')
                            for svalue_lifetime in self.svalue_lifetime:
                                if 1 < len(svalue_lifetime)<3 and '__mstore(mvalue(0x40))' in svalue_lifetime[1]:
                                    #print('li')
                                    value_type = 'uint256'
                                    self.variable_list.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot))
                                    break
                                #print(len(svalue_lifetime))
                                if len(svalue_lifetime)>=3:
                                    for lifetime in svalue_lifetime:
                                        if (('+' in lifetime or
                                            '-' in lifetime or
                                            '*' in lifetime or
                                            '/' in lifetime or
                                            '÷' in lifetime or
                                            '>' in lifetime or
                                            '<' in lifetime)):
                                            #'$' not in lifetime and
                                            #'==?)==?' not in lifetime and
                                            #'0xa0' not in lifetime):
                                            value_type = 'uint256'
                                            if 'mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot) not in self.variable_list:
                                                self.variable_list.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot))
                                                break
                                        if '$' in lifetime:
                                            value_type = 'int256'
                                            if 'mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot) not in self.variable_list:
                                                self.variable_list.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot))
                                                break                                            
                                        if '==?)==?' in lifetime:
                                            value_type = 'bool'
                                            if 'mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot) not in self.variable_list:
                                                self.variable_list.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot))
                                                break                                                           
                       
                        if len(self.svalue_lifetime) > 1:
                            #print('4')
                            for svalue_lifetime in self.svalue_lifetime:
                                for lifetime in svalue_lifetime:
                                    #(svalue(hash of the given data(b\'caller address_offset=0x0\',b"hash of the given data(b\'CallData(0x4) & (0x1)<<(0xa0) - 0x1_offset=0x0\',b\'0x4_offset=0x20\'
                                    pattern_value_located = r'svalue\(hash of the.*?{}_offset=0x20'
                                    match_value_located = re.search(pattern_value_located.format(slot), lifetime)
                                    if match_value_located:
                                        if (('+' in lifetime or
                                             '-' in lifetime or
                                             '*' in lifetime or
                                             '/' in lifetime or
                                             '÷' in lifetime or
                                             '>' in lifetime or
                                             '<' in lifetime )):
                                            #'$' not in lifetime and
                                            #'==?)==?' not in lifetime and
                                            #'0xa0' not in lifetime):
                                            value_type = 'uint256'
                                            if 'mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot) not in self.variable_list:
                                                self.variable_list.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot))
                                                break
                                        if '$' in lifetime:
                                            value_type = 'int256'
                                            if 'mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot) not in self.variable_list:
                                                self.variable_list.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot))
                                                break                     
                                        if '==?)==?' in lifetime:
                                            value_type = 'bool'
                                            if 'mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot) not in self.variable_list:
                                                self.variable_list.append('mapping(%s => mapping(%s => %s)) //slot(%s)' % (foreign_key, internal_key, value_type, slot))
                                                break                 

                                
        if len(self.private_dynamicarray_slot) != 0:    # dynamicarray
            for slot in self.private_dynamicarray_slot:
                for svalue in self.svalue_lifetime:
                    for lifetime in svalue:
                        if '(CallData(0x24))<(svalue(%s) )?' % slot in lifetime:
                            if '(u)int256/bytes32[] //slot(%s)' % slot not in self.variable_list:
                                self.variable_list.append('(u)int256/bytes32[] //slot(%s)' % slot)
                                break


        #return(self.variable_list)                                       

    def has_uppercase(self, input_string):       #Filter: Local variables must not have uppercase letters
        return not any(char.isupper() for char in input_string)

    def stack_value_analysis(self):
        mask_list = [0x0, 0x1, 0x4, 0x20, 0x40, 0x60, 0xa0, 0x1f, 0xff, 0x100]
        for stackvalue_lifetime in self.stackvariable_lifetime:
            #print(self.has_uppercase(stackvalue_lifetime[0]))
            if len(stackvalue_lifetime) > 1 and stackvalue_lifetime[0].startswith('0x') and self.has_uppercase(stackvalue_lifetime[0]):

                if (('>' in stackvalue_lifetime[1] or
                    '<' in stackvalue_lifetime[1] or
                    '+' in stackvalue_lifetime[1] or
                    '-' in stackvalue_lifetime[1] or
                    '*' in stackvalue_lifetime[1] or
                    '/' in stackvalue_lifetime[1] or
                    '÷' in stackvalue_lifetime[1] or
                    '==' in stackvalue_lifetime[1]) and
                    ('__' in stackvalue_lifetime[1]) and
                    ('<<__' not in stackvalue_lifetime[1]) and
                    ('CallData(0x4)' in stackvalue_lifetime[1] or
                    'CallData(0x4 + 0x20)' in stackvalue_lifetime[1]) and
                    int(stackvalue_lifetime[0], 16) not in mask_list):
                    if 'local uint256 value=%s' % stackvalue_lifetime[0] not in self.variable_list and len(stackvalue_lifetime[0])<10:
                        self.variable_list.append('local uint256 value=%s' % stackvalue_lifetime[0])
                    
        for stackvalue_lifetime in self.stackvariable_lifetime:
            if len(stackvalue_lifetime) > 1 and stackvalue_lifetime[0].startswith('0x') and self.has_uppercase(stackvalue_lifetime[0]):
                if (('>' in stackvalue_lifetime[1] or
                    '<' in stackvalue_lifetime[1] or
                    '+' in stackvalue_lifetime[1] or
                    '-' in stackvalue_lifetime[1] or
                    '*' in stackvalue_lifetime[1] or
                    '/' in stackvalue_lifetime[1] or
                    '÷' in stackvalue_lifetime[1] or
                    '==' in stackvalue_lifetime[1] or
                    '&0xff' in stackvalue_lifetime[1]) and
                    ('__' in stackvalue_lifetime[1]) and
                    ('<<__' not in stackvalue_lifetime[1]) and
                    int(stackvalue_lifetime[0], 16) not in mask_list):
                    if 'local uint256 value=%s' % stackvalue_lifetime[0] not in self.variable_list and len(stackvalue_lifetime[0])<10:
                        self.variable_list.append('local uint256 value=%s' % stackvalue_lifetime[0])
                        
        for stackvalue_lifetime in self.stackvariable_lifetime:   # storage write confirm
            for lifetime in stackvalue_lifetime:
                #SSTORE IN(0xf)
                pattern_storage_write = r'SSTORE IN\((0x[0-9A-Fa-f]+)\)'
                match_storage_write = re.search(pattern_storage_write, lifetime)
                if match_storage_write:
                    slot_to_write = match_storage_write.group(1)
                    if 'storage(%s)-write' % slot_to_write not in self.variable_list:
                        self.variable_list.append('storage(%s)-write' % slot_to_write)
                    if 'NOT0xff & svalue(%s)' % slot_to_write in lifetime:
                        self.variable_list.append('bool internal //slot(%s)' % slot_to_write)
                        


        for stackvalue_lifetime in self.stackvariable_lifetime:   # system variable
            for lifetime in stackvalue_lifetime:
                if 'timestamp' in lifetime:
                    if 'timestamp' not in self.variable_list:
                        self.variable_list.append('global variable: timestamp')
                    
          
        for stackvalue_lifetime in self.stackvariable_lifetime:
            for lifetime in stackvalue_lifetime:
                if ('CallData(0x4)' in lifetime and
                    'CallData(0x4 + 0x20)' in lifetime):    
                 #CallData(0x4 + 0x20) + 0xff & CallData(0x4)
                    pattern_arguments_computing = r'CallData\(.*?\+?.*?\).*?([+\-*/]).*?CallData\(.*?\+?.*?\)'
                    match_arguments_computing = re.search(pattern_arguments_computing, stackvalue_lifetime[1])
                    if match_arguments_computing:
                        computing = match_arguments_computing.group(1)
                        if 'local uint256 value=arguments%s' % computing not in self.variable_list:
                            self.variable_list.append('local uint256 value=arguments%s' % computing)      
        #return(self.variable_list)
                            
    def memory_value_analysis(self):
        pattern_loading_free = r'load_0x40'
        #0x9_storein_mvalue(0x40) in block_92
        pattern_store_value = r'(0x[0-9A-Fa-f]+)_storein_mvalue\(0x40\)'
        pattern_read_value = r'load_0x40'
        for index, log in enumerate(self.memory_log):
            if index < len(self.memory_log) - 2:               
                match_loading_free = re.search(pattern_loading_free, log)
                match_store_value = re.search(pattern_store_value, self.memory_log[index + 1])
                match_read_value = re.search(pattern_read_value, self.memory_log[index + 2])
                if match_loading_free and match_read_value and match_store_value:                    
                    self.variable_list.append('constant variable (u)int/bytes32 %s(m)' % match_store_value.group(1))
        #return(self.variable_list)
        #0x60 + mvalue(0x40)_storein_0x40
        pattern_space = r'(0x[0-9A-Fa-f]+) \+ mvalue\(0x40\)_storein_0x40'
        flag = False
        for log in self.memory_log:
            match_space = re.search(pattern_space, log)
            if match_space:
                type_list = []
                space_length = match_space.group(1)
                elements_count = int(space_length, 16)//0x20
                flag = True
                break
                #print(elements_count)

        if flag:
            
            for log in self.memory_log:
                pattern_uint = r'0x[0-9A-Fa-f]+_storein_(0x0 + )?mvalue\(0x40\)'
                if re.search(pattern_uint, log):
                    #print(123)
                   type_list.append('uint')
                   if len(type_list) == elements_count:
                        break
                if '==0?==0?' in log and ('storein_mvalue(0x40)' in log or 'storein_0x0 + mvalue(0x40)' in log):
                    type_list.append('bool')
                    if len(type_list) == elements_count:
                        break
                if '0xffffffffffffffffffffffffffffffffffffffff' in log and ('storein_mvalue(0x40)' in log or 'storein_0x0 + mvalue(0x40)' in log):
                    type_list.append('address')
                    if len(type_list) == elements_count:
                       break
                pattern_uint = r'0x[0-9A-Fa-f]+_storein_0x20 + mvalue\(0x40\)'
                if re.search(pattern_uint, log):
                    type_list.append('uint')
                    if len(type_list) == elements_count:
                        break
                if '==0?==0?' in log and ('storein_0x20 + mvalue(0x40)' in log or 'storein_mvalue(0x40) + 0x20' in log):
                    type_list.append('bool')
                    if len(type_list) == elements_count:
                        break
                if '0xffffffffffffffffffffffffffffffffffffffff' in log and ('storein_mvalue(0x40) + 0x20' in log or 'storein_0x20 + mvalue(0x40)' in log):
                    type_list.append('address')  
                    if len(type_list) == elements_count:
                        break
                pattern_uint = r'0x[0-9A-Fa-f]+_storein_0x20 + 0x20 + mvalue\(0x40\)'
                if re.search(pattern_uint, log):
                    type_list.append('uint')
                    if len(type_list) == elements_count:
                        break
                if '==0?==0?' in log and ('storein_0x20 + 0x20 + mvalue(0x40)' in log or 'storein_mvalue(0x40) + 0x20 + 0x20' in log):
                    type_list.append('bool')
                    if len(type_list) == elements_count:
                        break
                if '0xffffffffffffffffffffffffffffffffffffffff' in log and ('storein_mvalue(0x40) + 0x20 + 0x20' in log or 'storein_0x20 + 0x20 + mvalue(0x40)' in log):
                    type_list.append('address')
                    if len(type_list) == elements_count:
                        break
               
        try:
            self.variable_list.append(f"local struct{elements_count}[{', '.join(type_list)}]")
        except:
            pass
        

            

    def private_string_constant_analysis(self):
        string_sign = False
        for stackvalue_lifetime in self.stackvariable_lifetime:
            for lifetime in stackvalue_lifetime:
                if '0x1f' in lifetime:
                    string_sign = True
                    
        mvalue_rule = False
        for mvalue_lifetime in self.mvalue_lifetime:
            for lifetime in mvalue_lifetime:
                if '0x1f' in lifetime:
                    mvalue_rule = True
                
        if len(self.calldata_lifetime) == 0 and len(self.svalue_lifetime) ==0:
            for stackvalue_lifetime in self.stackvariable_lifetime:
                if stackvalue_lifetime and stackvalue_lifetime[0].startswith('0x') and len(stackvalue_lifetime) > 1:
                    pattern_string_unicode = r'(0x[0-9A-Fa-f]{6,})'
                    match_string_uincode = re.search(pattern_string_unicode, stackvalue_lifetime[0])
                    if match_string_uincode:
                        #print(match_string_uincode.group(1))                        
                        if '__<<0x' in stackvalue_lifetime[1]:
                            unicode = stackvalue_lifetime[0]                            
                            for log in self.memory_log:
                                if mvalue_rule and '<<(0x' in log and string_sign and unicode in log:
                                    self.variable_list.append('private string constant Uincode=%s' % unicode)
                        if '__mstore' in stackvalue_lifetime[1]:
                            unicode = stackvalue_lifetime[0]
                            for log in self.memory_log:
                                if mvalue_rule and string_sign and unicode in log:
                                    self.variable_list.append('private string constant Uincode=%s' % unicode)

        #return(self.variable_list)
                
            
    def continuous_slot_analysis(self):
        if len(self.svalue_lifetime) >3:
            pattern_slot = r'svalue\((0x[0-9A-Fa-f]+)\)'
            #svalue(0x3 + 0xc)
            pattern_slot_add = r'svalue\((0x[0-9A-Fa-f]+) \+ (0x[0-9A-Fa-f]+)\)'
            for index, svalue in enumerate(self.svalue_lifetime):
                for lifetime in svalue:
                    match_slot = re.search(pattern_slot, lifetime)
                    if match_slot:
                        slot = int(match_slot.group(1), 16)
                        next_slot_10 = slot + 1 
                        next_slot = hex(next_slot_10)
                        next_next_slot_10 = slot + 2
                        next_next_slot = hex(next_next_slot_10)
                        if (index + 2 < len(self.svalue_lifetime)) and any('svalue(%s)' % next_slot in lifetime for lifetime in self.svalue_lifetime[index+1]):
                            if any('svalue(%s)' % next_next_slot in lifetime for lifetime in self.svalue_lifetime[index+2]):
                                if '(u)int256/bytes32[%s] //slot(%s)' % (3, hex(slot)) not in self.variable_list:
                                    self.variable_list.append('(u)int256/bytes32[%s] //slot(%s)' % (3, hex(slot)))
                                
                    match_slot_add = re.search(pattern_slot_add, lifetime)
                    if match_slot_add:
                        slot = match_slot_add.group(2)
                        length = hex(int(match_slot_add.group(1), 16) + 1)
                        if '(u)int256/bytes32[%s] //slot(%s)' % (length, slot) not in self.variable_list:
                            self.variable_list.append('(u)int256/bytes32[%s] //slot(%s)' % (length, slot))
                        
                                
                            
                    
        
            
            
            
            
end_time = time.time()                                         
run_time = end_time - start_time                   
if __name__ == '__main__':
    asm_file = 'disassembly_result.txt'
    fun_sig = function_signature_hash_extractor.FunctionSignatureHashExtractor(asm_file)
    tf_path = path_through_function.PathThroughFunction(asm_file)
    path = tf_path.TFPath(fun_sig.extract_function_signatures()[0])
    print(fun_sig.extract_function_signatures()[0])
    r_w_analysis = variables_read_write_analysis.Analyzer()
    result = r_w_analysis.block_analysis(path)
    stackvariable_lifetime =  result[0]
    calldata_lifetime = result[1]
    mvalue_lifetime = result[2]
    memory_log = result[3]
    svalue_lifetime = result[4]
    rule = PublicFunctionAnalyzer(stackvariable_lifetime, calldata_lifetime, mvalue_lifetime, memory_log, svalue_lifetime)
    rule.private_states_type_analysis()
    rule.stack_value_analysis()
    rule.memory_value_analysis()
    rule.private_string_constant_analysis()
    rule.continuous_slot_analysis()
    print(rule.variable_list)
    #print(rule.public_states)
    #print(rule.private_mapping_slot)
    #print(rule.private_nested_mapping_slot)
    print(f"Time Consumption：{run_time:.6f} S")