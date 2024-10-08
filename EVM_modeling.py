#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:17:03 2023

@author: lyc
"""
import instruction_handler

class Context(list):
    def __init__(self, max_depth=1024):
        self.max_depth = max_depth
        
    def push(self, value):
        if len(self) < self.max_depth:
            self.append(value)
        else:
            raise Exception("Stack overflow")
    
    def pop(self):
        if len(self) > 0:
            return super().pop()
        else:
            raise Exception("Stack is empty or index is out of range")

class Stack(list):
    def __init__(self, max_depth=1024):
        self.max_depth = max_depth

    def push(self, value):
        if len(self) < self.max_depth:
            self.append(value)
        else:
            raise Exception("Stack overflow")

    def pop(self):
        if len(self) > 0:
            return super().pop()
        else:
            raise Exception("Stack underflow")
    def peek(self, index):
        if len(self) > index:
            return self[-(index+1)]
        else:
            raise Exception("Stack is empty or index is out of range")

    """def peek(self):
        if len(self) > 0:
            return self[-1]
        else:
            raise Exception("Stack is empty")"""
            
            
class Memory(list):
    def read(self, offset, size):
        for item in self:
            if 'offset' in item and 'size' in item:
                return item
        raise Exception('There is no such data in memory')

    def write(self, value):
        self.append(value)

        #self[offset:offset + len(data)] = data

"""class Memory(bytearray):
    def read(self, offset, size):
        return self[offset:offset + size]

    def write(self, offset, data):
        self[offset:offset + len(data)] = data
        
    def to_bytes(self):
        return bytes(self)"""



class Storage(dict):
    def read(self, key):
        if key in self:
            return self[key]
        else:
            raise Exception('Key not found in storage')

    def write(self, key, value):
        self[key] = value




class EVM:
    def __init__(self, max_stack_depth=1024):
        self.stack = Stack(max_depth=max_stack_depth)
        self.context = Context(max_depth=max_stack_depth)
        self.memory = Memory()
        self.storage = Storage()
        
        self.ins_handler= instruction_handler.InstructionHandler()
        
        """
        self.stack_v_event = variables_lifecycle.StackVariableLifecycle()
        self.memory_v_event = variables_lifecycle.MemoryVariableLifecycle()
        self.storage_v_event = variables_lifecycle.StorageVariableLifecycle()
        """

    def execute(self, block, pc, opcode_name, operand=None):
        
        if opcode_name == "STOP":
            pass
            
                
        elif opcode_name == 'ADD':  # 0x01
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s + %s' % (a,b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            
            self.ins_handler.handle_add_instruction(a, b, a_context, b_context, block)
               
                
        elif opcode_name == 'MUL':  # 0x02
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s*%s' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_mul_instruction(a, b, a_context, b_context, block)
                
                
        elif opcode_name == 'SUB':  # 0x03
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s - %s' % (a,b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_sub_instruction(a, b, a_context, b_context, block)
               
                
        elif opcode_name == 'DIV':  # 0x04
            a = self.stack.pop()
            b = self.stack.pop()
            if b == 0:
                self.stack.push(0)
            else:
                self.stack.push('%s/%s' %(a, b))
                
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_div_instruction(a, b, a_context, b_context, block)
               
                
        elif opcode_name == 'SDIV':  # 0x05
            a = self.stack.pop()
            b = self.stack.pop()
            if b == 0:
                self.stack.push(0)
            elif a == -2**255 and b == -1:
                self.stack.push(a)
            else:
                self.stack.push('%s$/%s' %(a, b))
                
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_sdiv_instruction(a, b, a_context, b_context, block)
               
                    
        elif opcode_name == 'MOD':  # 0x06
            a = self.stack.pop()
            b = self.stack.pop()
            if b == 0:
                self.stack.push(0)
            else:
                self.stack.push('%s // %s' %(a, b))
                
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_mod_instruction(a, b, a_context, b_context, block)
                
                
        elif opcode_name == 'SMOD':  # 0x07
            a = self.stack.pop()
            b = self.stack.pop()
            if b == 0:
                self.stack.push(0)
            else:
                self.stack.push('%s $// %s' %(a, b))
                
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_smod_instruction(a, b, a_context, b_context, block)
               
                
        elif opcode_name == 'ADDMOD':  # 0x08
            a = self.stack.pop()
            b = self.stack.pop()
            c = self.stack.pop()
            if c == 0:
                self.stack.push(0)
            else:
                self.stack.push('(%s+%s)//%s' % (a, b, c))
                
            a_context = self.context.pop()
            b_context = self.context.pop()
            c_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_addmod_instruction(a, b, c, a_context, b_context, c_context, block)
                

        elif opcode_name == 'MULMOD':  # 0x09
            a = self.stack.pop()
            b = self.stack.pop()
            c = self.stack.pop()
            if c == 0:
                self.stack.push(0)
            else:
                self.stack.push('(%s*%s)//%s' % (a, b, c))
                
            a_context = self.context.pop()
            b_context = self.context.pop()
            c_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_mulmod_instruction(a, b, c, a_context, b_context, c_context, block)
               
            

        elif opcode_name == 'EXP':  # 0x0a
            base = self.stack.pop()
            exponent = self.stack.pop()
            self.stack.push('%s^%s' % (base, exponent))
            
            base_context = self.context.pop()
            exponent_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            
            self.ins_handler.handle_exp_instruction(base, exponent, base_context, exponent_context, block)
                

        elif opcode_name == 'SIGNEXTEND':  # 0x0b
            bits = self.stack.pop()
            value = self.stack.pop()
            self.stack.push('%s sig %s' % (value, bits))
            
            bits_context = self.context.pop()
            value_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_signextend_instruction(bits, value, bits_context, value_context, block)

               

        elif opcode_name == 'LT':  # 0x10
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s<%s?' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_lt_instruction(a, b, a_context, b_context, block)
               

        elif opcode_name == 'GT':  # 0x11
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s>%s?' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_gt_instruction(a, b, a_context, b_context, block)
               

        elif opcode_name == 'SLT':  # 0x12
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s$<%s?' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_slt_instruction(a, b, a_context, b_context, block)
                

        elif opcode_name == 'SGT':  # 0x13
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s$>%s?' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_sgt_instruction(a, b, a_context, b_context, block)
                

        elif opcode_name == 'EQ':  # 0x14
            a = self.stack.pop()
            b = self.stack.pop()
            #self.stack.push(int(a == b))
            self.stack.push('%s==%s?' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_eq_instruction(a, b, a_context, b_context, block)


        elif opcode_name == 'ISZERO':  # 0x15
            value = self.stack.pop()
            #self.stack.push(int(value == 0))
            self.stack.push('%s==0?' % value)
            
            value_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_iszero_instruction(value, value_context, block)
               

        elif opcode_name == 'AND':  # 0x16
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s & %s' % (a,b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_and_instruction(a, b, a_context, b_context, block)
               

        elif opcode_name == 'OR':  # 0x17
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s | %s' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            
            self.ins_handler.handle_or_instruction(a, b, a_context, b_context, block)
                

        elif opcode_name == 'XOR':  # 0x18
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push('%s X| %s' %(a, b))
            
            a_context = self.context.pop()
            b_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_xor_instruction(a, b, a_context, b_context, block)
               

        elif opcode_name == 'NOT':  # 0x19
            value = self.stack.pop()
            self.stack.push('NOT%s' % value)
            
            value_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_not_instruction(value, value_context, block)
            
                

        elif opcode_name == 'BYTE':  # 0x1a
            index = self.stack.pop()
            value = self.stack.pop()
            if int(index, 16) >= 32:
                self.stack.push(0)
            else:
                #byte = (value >> (8 * (31 - index))) & 0xff
                #self.stack.push(byte)
                self.stack.push('%sBYTE%s' %(value, index))
                
            index_context = self.context.pop()
            value_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_byte_instruction(index, value, index_context, value_context, block)
                
        elif opcode_name == 'SHL':  # 0x1b
            shift = self.stack.pop()
            value = self.stack.pop()
            self.stack.push('(%s)<<(%s)' % (value, shift))
            
            shift_context = self.context.pop()
            value_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_shl_instruction(shift, value, shift_context, value_context, block)
                
        elif opcode_name == 'SHR':  # 0x1c
            shift = self.stack.pop()
            value = self.stack.pop()
            self.stack.push('(%s)>>(%s)' % (value, shift))
            
            shift_context = self.context.pop()
            value_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_shr_instruction(shift, value, shift_context, value_context, block)  
                
                
        elif opcode_name == 'SAR':  # 0x1d
            shift = self.stack.pop()
            value = self.stack.pop()
            self.stack.push('(%s)$>>(%s)' % (value, shift))
            
            shift_context = self.context.pop()
            value_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_sar_instruction(shift, value, shift_context, value_context, block)              
            
            

        elif opcode_name == 'SHA3':  # 0x20
            offset = self.stack.pop()
            size = self.stack.pop()
            #data = self.memory.read(offset, size)
            #hash_bytes = hashlib.sha3_256(data).digest()
            #hash_int = int.from_bytes(hash_bytes, byteorder='big')
            try:               
                self.stack.push('hash of the given data(%s,%s) in memory, offset = %s, size = %s.' % (self.memory[-2], self.memory[-1], offset, size))
            except Exception:
                self.stack.push('hash of the given data in memory, offset = %s, size = %s.' % (offset, size))
                
            
            offset_context = self.context.pop()
            size_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            
            self.ins_handler.handle_sha3_instruction(offset, size, offset_context, size_context, block)
                

        elif opcode_name == 'ADDRESS':  # 0x30
            self.stack.push('address of currently executing account')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
               

        elif opcode_name == 'BALANCE':  # 0x31
            address = self.stack.pop()
            #self.stack.pop()
            #balance = self.env.get_balance(address)
            balance = 'balance of address'
            self.stack.push(balance)
            
            address_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_balance_instruction(address, address_context, block)
                

        elif opcode_name == 'ORIGIN':  # 0x32
            self.stack.push('execution origination address')
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'CALLER':  # 0x33
            self.stack.push('caller address')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
              

        elif opcode_name == 'CALLVALUE':  # 0x34
            self.stack.push('callvalue')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'CALLDATALOAD':  # 0x35
            #offset = self.stack.pop()
                
            offset_in_calldata = self.stack.pop()
            #data = self.data[offset:offset+32]
            #value = int.from_bytes(data, byteorder='big')
            cdvalue = 'CallData(%s)' % offset_in_calldata
            self.stack.push(cdvalue)
            
            offset_in_calldata_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_calldataloadinput_instruction(offset_in_calldata, offset_in_calldata_context, block)
            self.ins_handler.handle_calldataloadoutput_instruction(cdvalue, block)
                
                
                

        elif opcode_name == 'CALLDATASIZE':  # 0x36
               
            self.stack.push('CallDataSize')
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'CALLDATACOPY':  # 0x37
            mem_offset = self.stack.pop()
            cd_offset = self.stack.pop()
            size = self.stack.pop()

            context_1 = self.context.pop()
            context_2 = self.context.pop()
            context_3 = self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")            
            
            calldata_with_offset = 'CallData(moffset=%s,cdoffset=%s,size=%s)' % (mem_offset, cd_offset, size)
            self.memory.write(calldata_with_offset.encode('utf-8'))
            self.ins_handler.handle_calldatacopy_instruction(mem_offset, cd_offset, size, context_1, context_2, context_3, block)
                

        elif opcode_name == 'CODESIZE':  # 0x38
                #size = len(self.code)
            self.stack.push('size of code running in current environment')
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'CODECOPY':  # 0x39
            mem_offset = self.stack.pop()
            code_offset = self.stack.pop()
            size = self.stack.pop()
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")    
                
            code_with_offset = 'RunningCode(moffset=%s,codeoffset=%s,size=%s)' % (mem_offset, code_offset, size)
            self.memory.write(code_with_offset.encode('utf-8'))
            

        elif opcode_name == 'GASPRICE':  # 0x3a

            self.stack.push('price of gas') 
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'EXTCODESIZE':  # 0x3b
                
            address=self.stack.pop()
            #size = len(self.env.get_code(address))
            self.stack.push('Size of %s’s code' % address)
            
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
        

        elif opcode_name == 'EXTCODECOPY':  # 0x3c
            address = self.stack.pop()
            mem_offset = self.stack.pop()
            code_offset = self.stack.pop()
            size = self.stack.pop()
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            
            code_with_offset = 'AccountCode(address=%s,moffset=%s,codeoffset=%s,size=%s)' % (address, mem_offset, code_offset, size)
            self.memory.write(code_with_offset.encode('utf-8'))


        elif opcode_name == 'RETURNDATASIZE':  # 0x3d
            self.stack.push('size of output data from the previous call')
            self.context.push('%s_%s' % (pc, self.stack))  
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")


        elif opcode_name == 'RETURNDATACOPY':  # 0x3e
            memory_offset = self.stack.pop()
            returndata_offset = self.stack.pop()
            size = self.stack.pop()

            self.context.pop()
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.memory.write('output data from the previous call')



        elif opcode_name == 'EXTCODEHASH':  # 0x3f
            address_of_account = self.stack.pop()
            self.stack.push('hash of the chosen accounts code')
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack)) 
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")


        elif opcode_name == 'BLOCKHASH':  # 0x40
                #block_number = self.stack.pop()
                #if self.env.block_number >= block_number > self.env.block_number - 256:
                    #block_hash = self.env.block_hashes[block_number]
                    #self.stack.push(block_hash)
                #else:
                    #self.stack.push(0)
            self.stack.pop()
            self.stack.push('blockhash')
            
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_blockhash_instruction('blockhash', self.context[-1], block)


        elif opcode_name == 'COINBASE':  # 0x41
            self.stack.push('the block’s beneficiary address')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")  
            self.ins_handler.handle_coinbase_instruction('the block’s beneficiary address', self.context[-1], block)
                

        elif opcode_name == 'TIMESTAMP':  # 0x42
            self.stack.push('timestamp')
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency") 
            self.ins_handler.handle_timestamp_instruction('timestamp', self.context[-1], block)


        elif opcode_name == 'NUMBER':  # 0x43
            self.stack.push('block_number')
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency") 
            self.ins_handler.handle_number_instruction('block_number', self.context[-1], block)


        elif opcode_name == 'DIFFICULTY':  # 0x44
            self.stack.push('difficulty')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_difficulty_instruction('difficulty', self.context[-1], block)


        elif opcode_name == 'PREVRANDAO':  # 0x44-1
            self.stack.push('previous block’s RANDAO mix')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_prevrandao_instruction('previous block’s RANDAO mix', self.context[-1], block)
                

        elif opcode_name == 'GASLIMIT':  # 0x45 
            self.stack.push('gas_limit')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_gaslimit_instruction('gas_limit', self.context[-1], block)


        elif opcode_name == 'CHAINID':  # 0x46
            self.stack.push('chain_id')

            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_chainid_instruction('self_balance', self.context[-1], block)
                
        elif opcode_name == 'SELFBALANCE':  # 0x47
            self.stack.push('self_balance')   
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_selfbalance_instruction('self_balance', self.context[-1], block)


        elif opcode_name == 'BASEFEE':  # 0x48
            self.stack.push('base_fee')   
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_basefee_instruction('base_fee', self.context[-1], block)


        elif opcode_name == 'POP':  # 0x50
            self.stack.pop()

            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
        

        elif opcode_name == 'MLOAD':  # 0x51
            offset = self.stack.pop()
            mvalue = 'mvalue(%s)' % offset
            self.stack.push(mvalue)
            
            offset_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))

            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

            self.ins_handler.handle_mload_instruction(mvalue, offset, self.context[-1], offset_context, block)
            
            if mvalue not in self.memory:
                self.memory.write(mvalue)
                    
                
                

        elif opcode_name == 'MSTORE':# 0x52
            offset = self.stack.pop()
            value = self.stack.pop()
            
            offset_context = self.context.pop()
            value_context = self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            value_with_offset = str(value) + '_offset=%s' % offset
            self.memory.write(value_with_offset.encode('utf-8'))
            self.ins_handler.handle_mstore_instruction(value, offset, value_context, offset_context, block)


        elif opcode_name == 'MSTORE8':# 0x53
            offset = self.stack.pop()
            value = self.stack.pop()
            
            offset_context = self.context.pop()
            value_context = self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            value_with_offset = str(value) + '_offset=%s' % offset + '_size=1 byte'
            self.memory.write(value_with_offset.encode('utf-8'))
            self.ins_handler.handle_mstore8_instruction(value, offset, value_context, offset_context, block)
               

        elif opcode_name == 'SLOAD':  # 0x54

            slot = self.stack.pop()
            if slot in self.storage:
                value = self.storage[slot]
                self.stack.push('%s(%s)' % (value, slot))
            if slot not in self.storage:
                self.stack.push('svalue(%s) ' % slot)
                self.storage[slot] = 'svalue'
                #self.storage_v_event.add_activity('svalue_slot=%s ' % slot, block=block)
                #self.storage.write(slot, 'UnkonwnValue')
            slot_context = self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_sload_instruction('svalue(%s) ' % slot, slot_context, block)
            


        elif opcode_name == 'SSTORE':  # 0x55
            slot = self.stack.pop()
            value = self.stack.pop()
            self.storage.write(slot, value)
            #self.pc += 1
            slot_context = self.context.pop()
            value_context = self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_sstore_instruction(slot, value, slot_context, value_context, block)

        elif opcode_name == 'JUMP':  # 0x56
            address = self.stack.pop()
            address_context = self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_jump_instruction(address, address_context)
            
                
        elif opcode_name == 'REQUIRE':
            self.stack.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
        elif opcode_name == 'ASSERT':
            self.stack.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
        elif opcode_name == 'JUMPI':   # 0x57
            address = self.stack.pop()
            condition = self.stack.pop()
            
            address_context = self.context.pop()
            condition_context = self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_jumpi_instruction(address, condition, address_context, condition_context, block)

                
        elif opcode_name == 'PC':  # 0x58
            self.stack.push('pc')
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                #self.pc += 1

        elif opcode_name == 'MSIZE':  # 0x59
            self.stack.push('size of active memory in bytes')
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                #self.pc += 1

        elif opcode_name == 'GAS':  # 0x5a
            self.stack.push('the amount of available gas')
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                #self.pc += 1

        elif opcode_name == 'JUMPDEST':  # 0x5b
            pass
                #self.pc += 1
            
        elif opcode_name == 'PUSH1':  # 0x60
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)

        elif opcode_name == 'PUSH2':  # 0x61
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH3':  # 0x62
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH4':  # 0x63
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH5':  # 0x64
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH6':  # 0x65
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH7':  # 0x66
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH8':  # 0x67
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH9':  # 0x68
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH10':  # 0x69
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH11':  # 0x6a
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH12':  # 0x6b
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH13':  # 0x6c
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH14':  # 0x6d
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
               
        elif opcode_name == 'PUSH15':  # 0x6e
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH16':  # 0x6f
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH17':  # 0x70
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)

        elif opcode_name == 'PUSH18':  # 0x71
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH19':  # 0x72
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH20':  # 0x73
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH21':  # 0x74
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH22':  # 0x75
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH23':  # 0x76
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH24':  # 0x77
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH25':  # 0x78
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH26':  # 0x79
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH27':  # 0x7a
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH28':  # 0x7b
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH29':  # 0x7c
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH30':  # 0x7d
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH31':  # 0x7e
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'PUSH32':  # 0x7f
            self.stack.push(operand)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            self.ins_handler.handle_push_instruction(operand, self.context[-1], block)
            
        elif opcode_name == 'DUP1':  # 0x80
            val = self.stack.peek(0)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)
                #self.pc += 1

        elif opcode_name == 'DUP2':  # 0x81
            val = self.stack.peek(1)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            #if pc == '0x5c':
            #    print(val)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)
                #self.pc += 1

        elif opcode_name == 'DUP3':  # 0x82
            val = self.stack.peek(2)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)          

        elif opcode_name == 'DUP4':  # 0x83
            val = self.stack.peek(3)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)             

        elif opcode_name == 'DUP5':  # 0x84
            val = self.stack.peek(4)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)          

        elif opcode_name == 'DUP6':  # 0x85
            val = self.stack.peek(5)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)               

        elif opcode_name == 'DUP7':  # 0x86
            val = self.stack.peek(6)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)               

        elif opcode_name == 'DUP8':  # 0x87
            val = self.stack.peek(7)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)         

        elif opcode_name == 'DUP9':  # 0x88
            val = self.stack.peek(8)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)        

        elif opcode_name == 'DUP10':  # 0x89
            val = self.stack.peek(9)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)

        elif opcode_name == 'DUP11':  # 0x8a
            val = self.stack.peek(10)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)        

        elif opcode_name == 'DUP12':  # 0x8b
            val = self.stack.peek(11)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)        

        elif opcode_name == 'DUP13':  # 0x8c
            val = self.stack.peek(12)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)

        elif opcode_name == 'DUP14':  # 0x8d
            val = self.stack.peek(13)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)

        elif opcode_name == 'DUP15':  # 0x8e
            val = self.stack.peek(14)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)

        elif opcode_name == 'DUP16':  # 0x8f
            val = self.stack.peek(15)
            self.stack.push(val)
            
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
            self.ins_handler.handle_dup_instruction(val, self.context[-1], block)

        elif opcode_name == 'SWAP1':  # 0x90
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val2)
            
            con1 = self.context.pop()
            con2 = self.context.pop()
            self.context.push(con1)
            self.context.push(con2)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'SWAP2':  # 0x91
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val2)
            self.stack.push(val3)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            self.context.push(con1)
            self.context.push(con2)
            self.context.push(con3)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
               
                          
        elif opcode_name == 'SWAP3':  # 0x92
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val4)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            self.context.push(con1)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con4)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'SWAP4':  # 0x93
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val5)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            self.context.push(con1)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con5)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'SWAP5':  # 0x94
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val6)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            self.context.push(con1)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con6)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'SWAP6':  # 0x95
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val7)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            self.context.push(con1)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con7)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'SWAP7':  # 0x96
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val8)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            self.context.push(con1)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con8)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                                

        elif opcode_name == 'SWAP8':  # 0x97
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val9)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            self.context.push(con1)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con9)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")                


        elif opcode_name == 'SWAP9':  # 0x98
            """val1 = self.stack.pop(8)
            val2 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val2)"""
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val10)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            self.context.push(con1)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con10)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                 

        elif opcode_name == 'SWAP10':  # 0x99
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            val11 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val10)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val11)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            con11 = self.context.pop()
            self.context.push(con1)
            self.context.push(con10)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con11)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                 

        elif opcode_name == 'SWAP11':  # 0x9a
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            val11 = self.stack.pop()
            val12 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val11)
            self.stack.push(val10)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val12)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            con11 = self.context.pop()
            con12 = self.context.pop()
            self.context.push(con1)
            self.context.push(con11)
            self.context.push(con10)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con12)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
                
        elif opcode_name == 'SWAP12':  # 0x9b
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            val11 = self.stack.pop()
            val12 = self.stack.pop()
            val13 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val12)
            self.stack.push(val11)
            self.stack.push(val10)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val13)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            con11 = self.context.pop()
            con12 = self.context.pop()
            con13 = self.context.pop()
            self.context.push(con1)
            self.context.push(con12)
            self.context.push(con11)
            self.context.push(con10)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con13)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                 

        elif opcode_name == 'SWAP13':  # 0x9c
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            val11 = self.stack.pop()
            val12 = self.stack.pop()
            val13 = self.stack.pop()
            val14 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val13)
            self.stack.push(val12)
            self.stack.push(val11)
            self.stack.push(val10)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val14)
                
            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            con11 = self.context.pop()
            con12 = self.context.pop()
            con13 = self.context.pop()
            con14 = self.context.pop()
            self.context.push(con1)
            self.context.push(con13)
            self.context.push(con12)
            self.context.push(con11)
            self.context.push(con10)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con14)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'SWAP14':  # 0x9d
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            val11 = self.stack.pop()
            val12 = self.stack.pop()
            val13 = self.stack.pop()
            val14 = self.stack.pop()
            val15 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val14)
            self.stack.push(val13)
            self.stack.push(val12)
            self.stack.push(val11)
            self.stack.push(val10)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val15)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            con11 = self.context.pop()
            con12 = self.context.pop()
            con13 = self.context.pop()
            con14 = self.context.pop()
            con15 = self.context.pop()
            self.context.push(con1)
            self.context.push(con14)
            self.context.push(con13)
            self.context.push(con12)
            self.context.push(con11)
            self.context.push(con10)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con15)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                  

        elif opcode_name == 'SWAP15':  # 0x9e
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            val11 = self.stack.pop()
            val12 = self.stack.pop()
            val13 = self.stack.pop()
            val14 = self.stack.pop()
            val15 = self.stack.pop()
            val16 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val15)
            self.stack.push(val14)
            self.stack.push(val13)
            self.stack.push(val12)
            self.stack.push(val11)
            self.stack.push(val10)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val16)

            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            con11 = self.context.pop()
            con12 = self.context.pop()
            con13 = self.context.pop()
            con14 = self.context.pop()
            con15 = self.context.pop()
            con16 = self.context.pop()
            self.context.push(con1)
            self.context.push(con15)
            self.context.push(con14)
            self.context.push(con13)
            self.context.push(con12)
            self.context.push(con11)
            self.context.push(con10)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con16)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                 

        elif opcode_name == 'SWAP16':  # 0x9f
            val1 = self.stack.pop()
            val2 = self.stack.pop()
            val3 = self.stack.pop()
            val4 = self.stack.pop()
            val5 = self.stack.pop()
            val6 = self.stack.pop()
            val7 = self.stack.pop()
            val8 = self.stack.pop()
            val9 = self.stack.pop()
            val10 = self.stack.pop()
            val11 = self.stack.pop()
            val12 = self.stack.pop()
            val13 = self.stack.pop()
            val14 = self.stack.pop()
            val15 = self.stack.pop()
            val16 = self.stack.pop()
            val17 = self.stack.pop()
            self.stack.push(val1)
            self.stack.push(val16)
            self.stack.push(val15)
            self.stack.push(val14)
            self.stack.push(val13)
            self.stack.push(val12)
            self.stack.push(val11)
            self.stack.push(val10)
            self.stack.push(val9)
            self.stack.push(val8)
            self.stack.push(val7)
            self.stack.push(val6)
            self.stack.push(val5)
            self.stack.push(val4)
            self.stack.push(val3)
            self.stack.push(val2)
            self.stack.push(val17)
                
            con1 = self.context.pop()
            con2 = self.context.pop()
            con3 = self.context.pop()
            con4 = self.context.pop()
            con5 = self.context.pop()
            con6 = self.context.pop()
            con7 = self.context.pop()
            con8 = self.context.pop()
            con9 = self.context.pop()
            con10 = self.context.pop()
            con11 = self.context.pop()
            con12 = self.context.pop()
            con13 = self.context.pop()
            con14 = self.context.pop()
            con15 = self.context.pop()
            con16 = self.context.pop()
            con17 = self.context.pop()
            self.context.push(con1)
            self.context.push(con16)
            self.context.push(con15)
            self.context.push(con14)
            self.context.push(con13)
            self.context.push(con12)
            self.context.push(con11)
            self.context.push(con10)
            self.context.push(con9)
            self.context.push(con8)
            self.context.push(con7)
            self.context.push(con6)
            self.context.push(con5)
            self.context.push(con4)
            self.context.push(con3)
            self.context.push(con2)
            self.context.push(con17)
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'LOG0':  # 0xa0

            self.stack.pop()
            self.stack.pop()
            
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'LOG1':  # 0xa1

            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'LOG2':  # 0xa2

            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'LOG3':  # 0xa3
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'LOG4':  # 0xa4
 
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'CREATE':  # 0xf0

            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.push('address of a new account with associated code')
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'CALL':    # 0xf1

            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.push('0 if the sub context reverted, 1 otherwise.')
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                

        elif opcode_name == 'CALLCODE':  # 0xf2

            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.push('0 if the sub context reverted, 1 otherwise.')
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == 'RETURN':  # 0xf3
            offset = self.stack.pop()
            size = self.stack.pop()

            self.memory.write('Calling context return data')
            
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
            

        elif opcode_name == 'DELEGATECALL':        # 0xf4
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.pop()
            self.stack.push('0 if the sub context reverted, 1 otherwise.')
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")    



        elif opcode_name == 'CREATE2':  # 0xf5
            value = self.stack.pop()
            offset = self.stack.pop()
            size = self.stack.pop()
            salt = self.stack.pop()
            self.stack.push('address of the deployed contract, 0 if the deployment failed')
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")  

                
                
        elif opcode_name == 'STATICCALL':  # 0xfa
            gas = self.stack.pop()
            address = self.stack.pop()
            argsOffset = self.stack.pop()
            argsSize = self.stack.pop()
            retOffset = self.stack.pop()
            retSize = self.stack.pop()
            self.stack.push('0 if the sub context reverted, 1 otherwise')
            
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.pop()
            self.context.push('%s_%s' % (pc, self.stack))
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")    
                

        elif opcode_name == 'REVERT':  # 0xfd
            offset = self.stack.pop()
            size = self.stack.pop()

            self.memory.write('Calling context return data')
            
            self.context.pop()
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")
                
                    
        elif opcode_name == 'INVALID':  # 0xfe
            #self.stack.push('INVALID')
            pass

        elif opcode_name == 'SELFDESTRUCT':  # 0xff
            self.stack.pop()
            
            self.context.pop()
            if len(self.context) != len(self.stack):
                raise Exception("Dual stack height inconsistency")

        elif opcode_name == '95':  # accident
            pass
 
        elif opcode_name == '94':  # accident
            pass
            
        else:
             print(opcode_name)
             raise Exception("unknown opcode")
                
"""           
        result = {
                'stack': self.stack,
                'memory': self.memory,
                'storage': self.storage}
        return result
        

"""





       

