#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:59:01 2023

@author: lyc
"""


class StackVariableLifecycle:
    def __init__(self):
        self.stack_vars = {}   # {value: activities}
        self.variable_bus = []
        self.variable_hotel = []
    
    def add_variable(self, variable, context):
        if variable in self.stack_vars:  # If there are duplicate variables, the old ones will be sent to the bus, and the new ones will always be recorded in the stack
            self.variable_bus.append({variable : self.stack_vars[variable]})
            
        self.stack_vars[context] = [variable]
    
    def delete_variable(self, variable, context):
        if self.stack_vars[context][0] != variable:
            raise Exception("delete failed: variable error")
        del self.stack_vars[context]

    def add_activity(self, variable, context, activity):
        #if isinstance(value, str) and value.startswith("0x") and len(value) > 2 and all(c in "0123456789abcdefABCDEF" for c in value[2:]):
            #if activity == self.stack_vars[value][-1]:
                #return
            #self.stack_vars[value].append(activity)        
            #if value not in stack:
                #self.stack_vars[value].append('DEAD')
        #if self.stack_vars[value][-1] == 'DEAD':
            #raise Exception("add_activity_error: data already dead")

        if activity == self.stack_vars[context][-1]:
            return
        self.stack_vars[context].append(activity)

            
    def get_lifecycle(self):
        for passenger in self.variable_bus:
            if passenger not in self.variable_hotel:
                self.variable_hotel.append(passenger)
        self.stack_vars['hotel'] = self.variable_hotel
        return self.stack_vars


class CallDataLifecycle:
    def __init__(self):
        self.calldata_vars = {}   # {value: activities}
 
    
    def add_variable(self, variable, block):
        self.calldata_vars[variable] = ["born in %s" % block]
    
    def delete_variable(self, variable):
        del self.calldata_vars[variable]

    def add_activity(self, value, activity):

        if activity == self.calldata_vars[value][-1]:
            return
        self.calldata_vars[value].append(activity)

            
    def get_lifecycle(self):

        return self.calldata_vars


class MemoryVariableLifecycle:
    def __init__(self):
        self.memory_vars= {}
        
    def add_variable(self, variable, context):
        self.memory_vars[context] = [variable]

    def add_activity(self, variable, context, activity):
        #if context not in self.memory_vars:
         #   self.memory_vars[context] = [value]
        if activity == self.memory_vars[context][-1]:
            return
        self.memory_vars[context].append(activity)
        

    def get_lifecycle(self):
        return self.memory_vars

class Memorylog:
    def __init__(self):
        self.memorylog = []
        
    def add_read_log(self, offset, block):
        self.memorylog.append('load_%s in %s' % (offset, block))
        
    def add_sha3_log(self, offset, size, block):
        self.memorylog.append('sha3(%s,%s) in %s' % (offset, size, block))
        
    def add_write_log(self, value, offset, block):
        self.memorylog.append('%s_storein_%s in %s' % (value, offset, block))
        
    def add_write8_log(self, value, offset, block):
        self.memorylog.append('%s_store8in_%s in %s' % (value, offset, block))
        
    def get_memorylog(self):
        return self.memorylog
        

    
class StorageVariableLifecycle:
    def __init__(self,):
        self.storage_vars = {}
        
    def add_variable(self, variable, block):
        self.storage_vars[variable] = ["born in %s" % block]

    def add_activity(self, value, activity):
        if activity == self.storage_vars[value][-1]:
            return
        self.storage_vars[value].append(activity)

    def get_lifecycle(self):
        return self.storage_vars
    
