#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 21:26:21 2023

@author: lyc
"""
import variables_lifecycle

class InstructionHandler:
    def __init__(self):
        self.stack_vars_lifetime_recorder = variables_lifecycle.StackVariableLifecycle()
        self.calldata_vars_lifetime_recorder = variables_lifecycle.CallDataLifecycle()
        self.memory_vars_lifetime_recorder = variables_lifecycle.MemoryVariableLifecycle()
        self.storage_vars_lifetime_recorder = variables_lifecycle.StorageVariableLifecycle()
        self.memory_log = variables_lifecycle.Memorylog()
        
    def handle_add_instruction(self, operand_1, operand_2, context_1, context_2, block):

        # check if this operand is ever recorded
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__+(%s) in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)+__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)+(%s) in %s' % (operand_1, operand_2, block))
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)+(%s) in %s' % (operand_1, operand_2, block))
        
        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__+(%s) in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)+__ in %s' % (operand_1, block))
       
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__+(%s) in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)+__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)+(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)+(%s) in %s' % (operand_1, operand_2, block))            

    def handle_mul_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__*(%s) in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)*__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)*(%s) in %s' % (operand_1, operand_2, block))
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)*(%s) in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__*(%s) in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)*__ in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__*(%s) in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)*__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)*(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)*(%s) in %s' % (operand_1, operand_2, block))
                         
        
    def handle_sub_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__-(%s) in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)-__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)-(%s) in %s' % (operand_1, operand_2, block))
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)-(%s) in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__-(%s) in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)-__ in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__-(%s) in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)-__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)-(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)-(%s) in %s' % (operand_1, operand_2, block))         
  
    def handle_div_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__÷(%s) in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)÷__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)÷(%s) in %s' % (operand_1, operand_2, block))
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)÷(%s) in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__÷(%s) in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)÷__ in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__÷(%s) in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)÷__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)÷(%s) in %s' % (operand_1, operand_2, block))
                
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)÷(%s) in %s' % (operand_1, operand_2, block))
                      
              
    def handle_sdiv_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$÷(%s) in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$÷__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)$÷(%s) in %s' % (operand_1, operand_2, block))
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)$÷(%s) in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$÷(%s) in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$÷__ in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$÷(%s) in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$÷__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)$÷(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)$÷(%s) in %s' % (operand_1, operand_2, block))       
        
    def handle_mod_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__%({}) in {}'.format(operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({})%__ in {}'.format(operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})%({}) in {}'.format(operand_1, operand_2, block))
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})%({}) in {}'.format(operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__%({}) in {}'.format(operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({})%__ in {}'.format(operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__%({}) in {}'.format(operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({})%__ in {}'.format(operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})%({}) in {}'.format(operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})%({}) in {}'.format(operand_1, operand_2, block)) 
        
    def handle_smod_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$%({}) in {}'.format(operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({})$%__ in {}'.format(operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})$%({}) in {}'.format(operand_1, operand_2, block))
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})$%({}) in {}'.format(operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$%({}) in {}'.format(operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({})$%__ in {}'.format(operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$%({}) in {}'.format(operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({})$%__ in {}'.format(operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})$%({}) in {}'.format(operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})$%({}) in {}'.format(operand_1, operand_2, block)) 

    def handle_addmod_instruction(self, operand_1, operand_2, operand_3, context_1, context_2, context_3, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(__+{})%{} in {}'.format(operand_2, operand_3, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({}+__)%{} in {}'.format(operand_1, operand_3, block))
        if context_3 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_3, context_3, activity = '({}+{})%__ in {}'.format(operand_1, operand_2, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})+({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})+({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))
            if key in operand_3:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})+({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(__+{})%{} in {}'.format(operand_2, operand_3, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({}+__)%{} in {}'.format(operand_1, operand_3, block))
        if context_3 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_3, context_3, activity = '({}+{})%__ in {}'.format(operand_1, operand_2, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(__+{})%{} in {}'.format(operand_2, operand_3, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({}+__)%{} in {}'.format(operand_1, operand_3, block))
        #if context_3 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_3, context_3, activity = '({}+{})%__ in {}'.format(operand_1, operand_2, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})+({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})+({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))
            if key in operand_3:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})+({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))
                

    def handle_mulmod_instruction(self, operand_1, operand_2, operand_3, context_1, context_2, context_3, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(__*{})%{} in {}'.format(operand_2, operand_3, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({}*__)%{} in {}'.format(operand_1, operand_3, block))
        if context_3 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_3, context_3, activity = '({}*{})%__ in {}'.format(operand_1, operand_2, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})*({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})*({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))
            if key in operand_3:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '({})*({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(__*{})%{} in {}'.format(operand_2, operand_3, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({}*__)%{} in {}'.format(operand_1, operand_3, block))
        if context_3 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_3, context_3, activity = '({}*{})%__ in {}'.format(operand_1, operand_2, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(__*{})%{} in {}'.format(operand_2, operand_3, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '({}*__)%{} in {}'.format(operand_1, operand_3, block))
        #if context_3 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_3, context_3, activity = '({}*{})%__ in {}'.format(operand_1, operand_2, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})*({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})*({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))
            if key in operand_3:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '({})*({})%({}) in {}'.format(operand_1, operand_2, operand_3, block))


    def handle_exp_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__^(%s) in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)^-- in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)^(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)^(%s) in %s' % (operand_1, operand_2, block)) 

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__^(%s) in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)^-- in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__^(%s) in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)^-- in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)^(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)^(%s) in %s' % (operand_1, operand_2, block)) 


    def handle_signextend_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as size for %s_sigextend in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = 'as value to sigextend %s in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)sig_ext(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)sig_ext(%s) in %s' % (operand_1, operand_2, block)) 

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as size for %s_sigextend in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = 'as value to sigextend %s in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as size for %s_sigextend in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = 'as value to sigextend %s in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)sig_ext(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)sig_ext(%s) in %s' % (operand_1, operand_2, block)) 

    def handle_lt_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__<(%s)? in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)<__? in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)<(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)<(%s)? in %s' % (operand_1, operand_2, block)) 

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__<(%s)? in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)<__? in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__<(%s)? in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)<__? in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)<(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)<(%s)? in %s' % (operand_1, operand_2, block)) 

    def handle_gt_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__>(%s)? in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)>__? in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)>(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)>(%s)? in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__>(%s)? in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)>__? in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__>(%s)? in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)>__? in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)>(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)>(%s)? in %s' % (operand_1, operand_2, block)) 

    def handle_slt_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$<(%s)? in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$<__? in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)$<(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)$<(%s)? in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$<(%s)? in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$<__? in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$<(%s)? in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$<__? in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)$<(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)$<(%s)? in %s' % (operand_1, operand_2, block))

    def handle_sgt_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$>(%s)? in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$>__? in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)$>(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)$>(%s)? in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$>(%s)? in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$>__? in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__$>(%s)? in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)$>__? in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)$>(%s)? in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)$>(%s)? in %s' % (operand_1, operand_2, block))

    def handle_eq_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__==%s? in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s==__? in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)==(%s)? in %s' % (operand_1, operand_2, block))
                #self.storage_vars_lifetime_recorder.add_activity(key, activity = 'DEAD in %s' % block)
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)==(%s)? in %s' % (operand_1, operand_2, block))
                #self.storage_vars_lifetime_recorder.add_activity(key, activity = 'DEAD in %s' % block)

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__==%s? in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s==__? in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__==%s? in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s==__? in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)==(%s)? in %s' % (operand_1, operand_2, block))
                #self.storage_vars_lifetime_recorder.add_activity(key, activity = 'DEAD in %s' % block)
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)==(%s)? in %s' % (operand_1, operand_2, block))
                #self.storage_vars_lifetime_recorder.add_activity(key, activity = 'DEAD in %s' % block)
                
    def handle_iszero_instruction(self, operand_1, context_1, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__==0? in %s' % block)
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)==0? in %s' % (operand_1, block))    

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__==0? in %s' % block)
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__==0? in %s' % block)
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)==0? in %s' % (operand_1, block))    
            
        
    def handle_and_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__&%s in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s&__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)&(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)&(%s) in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__&%s in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s&__ in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__&%s in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s&__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)&(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)&(%s) in %s' % (operand_1, operand_2, block))
            
    def handle_or_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__|%s in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s|__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)|(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)|(%s) in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__|%s in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s|__ in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__|%s in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%s|__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)|(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)|(%s) in %s' % (operand_1, operand_2, block))
            
    def handle_xor_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__XOR%s in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%sXOR__ in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)XOR(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)XOR(%s) in %s' % (operand_1, operand_2, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__XOR%s in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%sXOR__ in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '__XOR%s in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '%sXOR__ in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)XOR(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)XOR(%s) in %s' % (operand_1, operand_2, block))
            
    def handle_not_instruction(self, operand_1, context_1, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '~__ in %s' % block)
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '~(%s) in %s' % (operand_1, block)) 

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '~__ in %s' % block)
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '~__ in %s' % block)
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '~(%s) in %s' % (operand_1, block))    

            
    def handle_byte_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as offset to byte %s in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = 'as value to byte %s in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = 'as offset to byte %s in %s' % (operand_2, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = 'as value to byte %s in %s' % (operand_1, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as offset to byte %s in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = 'as value to byte %s in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as offset to byte %s in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = 'as value to byte %s in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)BYTE(%s) in %s' % (operand_1, operand_2, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)BYTE(%s) in %s' % (operand_1, operand_2, block))
            
    def handle_shl_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%s<<__ in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__<<%s in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)<<(%s) in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)<<(%s) in %s' % (operand_2, operand_1, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%s<<__ in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__<<%s in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%s<<__ in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__<<%s in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)<<(%s) in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)<<(%s) in %s' % (operand_2, operand_1, block))
            
    def handle_shr_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%s>>__ in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__>>%s in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)>>(%s)? in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)>>(%s)? in %s' % (operand_2, operand_1, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%s>>__ in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__>>%s in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%s>>__ in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__>>%s in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)>>(%s)? in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)>>(%s)? in %s' % (operand_2, operand_1, block))
            
    def handle_sar_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%sS>>__ in %s' % (operand_2, block))
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__S>>%s in %s' % (operand_1, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)S>>(%s)? in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)S>>(%s)? in %s' % (operand_2, operand_1, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%sS>>__ in %s' % (operand_2, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__S>>%s in %s' % (operand_1, block))
        #if context_1 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '%sS>>__ in %s' % (operand_2, block))
        #if context_2 in self.storage_vars_lifetime_recorder.storage_vars:
        #    self.storage_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '__S>>%s in %s' % (operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)S>>(%s)? in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)S>>(%s)? in %s' % (operand_2, operand_1, block))

    def handle_sha3_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as offset of SHA3 in %s' % block )
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = 'as size of SHA3 in %s' % block )
        self.memory_log.add_sha3_log(operand_1, operand_2, block)


    def handle_balance_instruction(self, operand_1, context_1, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as address to get balance in %s' % block )
            

    def handle_calldataloadinput_instruction(self, operand_1, context_1, block):        
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = 'as CDL_offset in %s' % block)
            
    def handle_calldataloadoutput_instruction(self, operand_1, block):
        self.calldata_vars_lifetime_recorder.add_variable(operand_1, block)
        
    def handle_calldatacopy_instruction(self, memory_offset, cdoffset, size, context_1, context_2, context_3, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(memory_offset, context_1, activity = 'as moffset of calldatacopy in %s' % block)
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(cdoffset, context_2, activity = 'as cdffset of calldatacopy in %s' % block)        
        if context_3 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(size, context_3, activity = 'as size of calldatacopy in %s' % block)
        self.memory_log.add_write_log('calldatacopy(offset=%s,size=%s)' % (cdoffset, size), memory_offset, block)
            
            
            
    def handle_mload_instruction(self, value, offset, value_context, offset_context, block):
        self.memory_vars_lifetime_recorder.add_variable(value, value_context)
        self.memory_log.add_read_log(offset, block)
        
    def handle_mstore_instruction(self, value, offset, value_context, offset_context, block):
        if value_context in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(value, value_context, activity = '__mstore(%s) in %s' % (offset, block))
        if offset_context in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(offset, offset_context, activity = 'as offset of %s_mstore in %s' % (value, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in value:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '__mstore(%s) in %s' % (offset, block)) 
            if key in offset:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = 'as offset of %s_mstore in %s' % (value, block))
        
        self.memory_log.add_write_log(value, offset, block)

        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in value:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '__mstore(%s) in %s' % (offset, block))    
            if key in offset:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = 'as offset of %s_mstore in %s' % (value, block))

    def handle_mstore8_instruction(self, value, offset, value_context, offset_context, block):
        if value_context in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(value, value_context, activity = '__mstore8(%s) in %s' % (offset, block))
        if offset_context in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(offset, offset_context, activity = 'as offset of %s_mstore8 in %s' % (value, block))
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in value:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '__mstore8(%s) in %s' % (offset, block)) 
            if key in offset:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = 'as offset of %s_mstore8 in %s' % (value, block))
        
        self.memory_log.add_write8_log(value, offset, block)

        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in value:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '__mstore8(%s) in %s' % (offset, block))    
            if key in offset:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = 'as offset of %s_mstore8 in %s' % (value, block))
        
        
    def handle_sload_instruction(self, operand_1, slot_context, block):
        self.storage_vars_lifetime_recorder.add_variable(operand_1, block)
        if slot_context in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, slot_context, activity = 'as slot index in %s' % block)
    
    def handle_push_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1)
    
    def handle_dup_instruction(self, operand_1, context_1, block):
        if isinstance(operand_1, str) and operand_1.startswith("0x") and len(operand_1) > 2 and all(c in "0123456789abcdefABCDEF" for c in operand_1[2:]):
            self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1)
        if 'CallDataSize' in operand_1:
            self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1)
        if operand_1.startswith('mvalue('):
            self.memory_vars_lifetime_recorder.add_variable(operand_1, context_1)
        if operand_1.startswith('svalue('):
            self.storage_vars_lifetime_recorder.add_variable(operand_1, block)
            
    
    def handle_jump_instruction(self, value, context):
        #for key in list(self.stack_vars_lifetime_recorder.stack_vars.keys()):
            #if key.startswith(operand_1):
                #self.stack_vars_lifetime_recorder.delete_variable(key)
        self.stack_vars_lifetime_recorder.delete_variable(value, context)
    
    def handle_jumpi_instruction(self, address, condition, address_context, condition_context, block):
        #for key in list(self.stack_vars_lifetime_recorder.stack_vars.keys()):
            #if key.startswith(operand_1):
                #self.stack_vars_lifetime_recorder.delete_variable(key)
        self.stack_vars_lifetime_recorder.delete_variable(address, address_context)
        if condition_context in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(condition, condition_context, activity = 'as condition of jumpi in %s' % block)
        
    def handle_sstore_instruction(self, operand_1, operand_2, context_1, context_2, block):
        if context_1 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block)) 
        if context_2 in self.stack_vars_lifetime_recorder.stack_vars:
            self.stack_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block)) 
        for key in list(self.calldata_vars_lifetime_recorder.calldata_vars.keys()):
            if key in operand_1:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.calldata_vars_lifetime_recorder.add_activity(key, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block))

        if context_1 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_1, context_1, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block))
        if context_2 in self.memory_vars_lifetime_recorder.memory_vars:
            self.memory_vars_lifetime_recorder.add_activity(operand_2, context_2, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block))
        for key in list(self.storage_vars_lifetime_recorder.storage_vars.keys()):
            if key in operand_1:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block))    
            if key in operand_2:
                self.storage_vars_lifetime_recorder.add_activity(key, activity = '(%s)SSTORE IN(%s) in %s' % (operand_2, operand_1, block))


    def handle_basefee_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1)    
        
    def handle_selfbalance_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1) 

    def handle_chainid_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1) 

    def handle_gaslimit_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1) 

    def handle_prevrandao_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1) 

    def handle_number_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1) 
        
    def handle_timestamp_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1)         
        
    def handle_coinbase_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1)

    def handle_blockhash_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1) 

    def handle_difficulty_instruction(self, operand_1, context_1, block):
        self.stack_vars_lifetime_recorder.add_variable(operand_1, context_1) 



            