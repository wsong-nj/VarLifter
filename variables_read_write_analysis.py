#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:35:49 2023

@author: lyc
"""
import EVM_modeling
import path_through_function
import function_signature_hash_extractor
import execution_state_tracker


class Analyzer:
    def __init__(self):
        self.evm = EVM_modeling.EVM()
        
        self.variables_lifecycle = self.evm.ins_handler

        
        self.stack_logger = execution_state_tracker.StackLogger()
        self.memory_logger = execution_state_tracker.MemoryLogger()
        self.storage_logger = execution_state_tracker.StorageLogger()


    def block_analysis(self, path):
        asm_file = 'disassembly_result.txt'
        tf_path = path_through_function.PathThroughFunction(asm_file)

        #path = tf_path.TFPath(fun_sig.extract_function_signatures()[0])
        #print(path)

        for block in path:
            code = tf_path.blocks[block]

            self.stack_logger.log_stack_before(block, self.evm.stack)
            self.memory_logger.log_memory_before(block, self.evm.memory)
            self.storage_logger.log_storage_before(block, self.evm.storage)
            
            if (code[-1][1] == 'JUMP' and 
                code[-2][1] == 'AND' and 
                'PUSH' in code[-3][1] and 
                'PUSH' in code[-4][1] and 
                '0xff' in code[-4][2]):
                del code[-4]
                del code[-2]

            for codeline in code: #The code here is a nested list, and the internal list is for each instruction line
    
                if len(codeline) > 2:
                    self.evm.execute(block, codeline[0], codeline[1], codeline[2])
                    
                else:
                    self.evm.execute(block, codeline[0], codeline[1])
                    
            self.stack_logger.log_stack_after(self.evm.stack)
            self.memory_logger.log_memory_after(self.evm.memory)
            self.storage_logger.log_storage_after(self.evm.storage)
        stack_vars_lifetime_pure = list(self.variables_lifecycle.stack_vars_lifetime_recorder.get_lifecycle().values())
        calldata_lifetime_pure = list(self.variables_lifecycle.calldata_vars_lifetime_recorder.get_lifecycle().values())
        mvalue_lifetime_pure = list(self.variables_lifecycle.memory_vars_lifetime_recorder.get_lifecycle().values())
        svalue_lifetime_pure = list(self.variables_lifecycle.storage_vars_lifetime_recorder.get_lifecycle().values())
        
        #unique_stack_vars_lifetime_set = set(map(tuple, stack_vars_lifetime_pure))
        #unique_calldata_lifetime_set = set(map(tuple, calldata_lifetime_pure))
        #unique_mvalue_lifetime_set = set(map(tuple, mvalue_lifetime_pure))
        #unique_svalue_lifetime_set = set(map(tuple, svalue_lifetime_pure))
        
        #unique_stack_vars_lifetime_list = list(map(list, unique_stack_vars_lifetime_set))
        #unique_calldata_lifetime_list = list(map(list, unique_calldata_lifetime_set))
        #unique_mvalue_lifetime_list = list(map(list, unique_mvalue_lifetime_set))
        #unique_svalue_lifetime_list = list(map(list, unique_svalue_lifetime_set))
        #unique_svalue_lifetime_list = []


        #for sublist in svalue_lifetime_pure:
        #    if sublist not in unique_svalue_lifetime_list:
        #        unique_svalue_lifetime_list.append(sublist)
        
        result = (stack_vars_lifetime_pure,
                  calldata_lifetime_pure,
                  mvalue_lifetime_pure,
                  self.variables_lifecycle.memory_log.get_memorylog(),
                  svalue_lifetime_pure)
        return result


        #result = (self.variables_lifecycle.stack_vars_lifetime_recorder.get_lifecycle(),
        #          self.variables_lifecycle.calldata_vars_lifetime_recorder.get_lifecycle(),
        #          self.variables_lifecycle.memory_vars_lifetime_recorder.get_lifecycle(),
        #          self.variables_lifecycle.memory_log.get_memorylog(),
        #          self.variables_lifecycle.storage_vars_lifetime_recorder.get_lifecycle())




if __name__ == '__main__':
    #evm = EVM_modeling.EVM()
    asm_file = 'disassembly_result.txt'
    fun_sig = function_signature_hash_extractor.FunctionSignatureHashExtractor(asm_file)
    tf_path = path_through_function.PathThroughFunction(asm_file)
    path = tf_path.TFPath(fun_sig.extract_function_signatures()[0])
    print(fun_sig.extract_function_signatures()[0])
    a = Analyzer()
    result = a.block_analysis(path)
    print(result)
    #print(a.stack_logger.get_stack_by_block_id('block_750'))




    





