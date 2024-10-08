#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 11:28:51 2023

@author: lyc
"""

class StackLogger:
    def __init__(self):
        self.stack_log = {}

    def log_stack_before(self, block_id, stack):
        block_id = self._get_unique_block_id_before(block_id)
        stack_copy = stack.copy()  
        self.stack_log[block_id] = {"before": stack_copy, "after": None}

    def log_stack_after(self, stack):
        #block_id = self._get_unique_block_id_after(block_id)
        stack_copy = stack.copy()  
        #if block_id in self.stack_log:
        self.stack_log[list(self.stack_log.keys())[-1]]["after"] = stack_copy
        #else:
            #self.stack_log[block_id] = {"before": [], "after": stack_copy}

    def print_stack_log(self):
        for block_id, stack_data in self.stack_log.items():
            print(f"Block: {block_id}")
            print("Stack before execution:")
            for item in stack_data["before"]:
                print(item)
            print("Stack after execution:")
            for item in stack_data["after"]:
                print(item)
            print("")

    def get_stack_by_block_id(self, block_id):
        if block_id in self.stack_log:
            return self.stack_log[block_id]
        else:
            return None
    
    def _get_unique_block_id_before(self, block_id):
        if block_id not in self.stack_log:
            return block_id

        index = 1
        new_block_id = f"{block_id}.{index}"
        while new_block_id in self.stack_log:
            index += 1
            new_block_id = f"{block_id}.{index}"

        return new_block_id

"""
    def _get_unique_block_id_after(self, block_id):
        if block_id not in self.stack_log:
            return block_id

        index = 1
        new_block_id = f"{block_id}.{index}"
        while new_block_id in self.stack_log:
            index += 1
            new_block_id = f"{block_id}.{index}"

        return new_block_id
"""
class MemoryLogger:
    def __init__(self):
        self.memory_log = {}

    def log_memory_before(self, block_id, memory):
        block_id = self._get_unique_block_id_before(block_id)
        memory_copy = memory.copy()  # 复制内存
        self.memory_log[block_id] = {"before": memory_copy, "after": None}

    def log_memory_after(self, memory):
        #block_id = self._get_unique_block_id_after(block_id)
        memory_copy = memory.copy()  # 复制内存
        #if block_id in self.memory_log:
        self.memory_log[list(self.memory_log.keys())[-1]]["after"] = memory_copy
        #else:
            #self.memory_log[block_id] = {"before": {}, "after": memory_copy}

    def print_memory_log(self):
        for block_id, memory_data in self.memory_log.items():
            print(f"Block: {block_id}")
            print("Memory before execution:")
            for address, value in memory_data["before"].items():
                print(f"{address}: {value}")
            print("Memory after execution:")
            for address, value in memory_data["after"].items():
                print(f"{address}: {value}")
            print("")

    def get_memory_by_block_id(self, block_id):
        if block_id in self.memory_log:
            return self.memory_log[block_id]
        else:
            return None
        
    def _get_unique_block_id_before(self, block_id):
        if block_id not in self.memory_log:
            return block_id

        index = 1
        new_block_id = f"{block_id}.{index}"
        while new_block_id in self.memory_log:
            index += 1
            new_block_id = f"{block_id}.{index}"

        return new_block_id
"""    
    def _get_unique_block_id_after(self, block_id):
        if block_id not in self.memory_log:
            return block_id

        index = 1
        new_block_id = f"{block_id}.{index}"
        while new_block_id in self.memory_log:
            index += 1
            new_block_id = f"{block_id}.{index}"

        return new_block_id
"""
class StorageLogger:
    def __init__(self):
        self.storage_log = {}

    def log_storage_before(self, block_id, storage):
        block_id = self._get_unique_block_id_before(block_id)
        storage_copy = dict(storage)  # Copy the storage
        self.storage_log[block_id] = {"before": storage_copy, "after": None}

    def log_storage_after(self, storage):
        #block_id = self._get_unique_block_id_after(block_id)
        storage_copy = dict(storage)  # Copy the storage
        #if block_id in self.storage_log:
        self.storage_log[list(self.storage_log.keys())[-1]]["after"] = storage_copy
        #else:
            #self.storage_log[block_id] = {"before": {}, "after": storage_copy}

    def print_storage_log(self):
        for block_id, storage_data in self.storage_log.items():
            print(f"Block: {block_id}")
            print("Storage before execution:")
            for slot, value in storage_data["before"].items():
                print(f"{slot}: {value}")
            print("Storage after execution:")
            for slot, value in storage_data["after"].items():
                print(f"{slot}: {value}")
            print("")

    def get_storage_by_block_id(self, block_id):
        if block_id in self.storage_log:
            return self.storage_log[block_id]
        else:
            return None

    def _get_unique_block_id_before(self, block_id):
        if block_id not in self.storage_log:
            return block_id

        index = 1
        new_block_id = f"{block_id}.{index}"
        while new_block_id in self.storage_log:
            index += 1
            new_block_id = f"{block_id}.{index}"

        return new_block_id
"""    
    def _get_unique_block_id_after(self, block_id):
        if block_id not in self.storage_log:
            return block_id

        index = 1
        new_block_id = f"{block_id}.{index}"
        while new_block_id in self.storage_log:
            index += 1
            new_block_id = f"{block_id}.{index}"

        return new_block_id
    """