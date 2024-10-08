#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 22:01:15 2023

@author: lyc
"""

class Stack(list):
    def __init__(self, max_depth=1024):
        self.max_depth = max_depth

    def push(self, value):
        if len(self) < self.max_depth:
            self.append(value)
        else:
            print(self)
            raise Exception("Stack overflow")

    def pop(self):
        if len(self) > 0:
            return super().pop()
        else:
            print(self)
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
        self.memory = Memory()
        self.storage = Storage()

    def execute(self, opcode_name, operand=None):
            if opcode_name == "STOP":
                pass
            
                
            elif opcode_name == 'ADD':  # 0x01
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s + %s' % (a,b))
               
                
            elif opcode_name == 'MUL':  # 0x02
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s*%s' %(a, b))
                
                
            elif opcode_name == 'SUB':  # 0x03
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s - %s' % (a,b))
               
                
            elif opcode_name == 'DIV':  # 0x04
                a = self.stack.pop()
                b = self.stack.pop()
                if b == 0:
                    self.stack.push(0)
                else:
                    self.stack.push('%s/%s' %(a, b))
               
                
            elif opcode_name == 'SDIV':  # 0x05
                a = self.stack.pop()
                b = self.stack.pop()
                if b == 0:
                    self.stack.push(0)
                elif a == -2**255 and b == -1:
                    self.stack.push(a)
                else:
                    self.stack.push('%s$/%s' %(a, b))
               
                    
            elif opcode_name == 'MOD':  # 0x06
                a = self.stack.pop()
                b = self.stack.pop()
                if b == 0:
                    self.stack.push(0)
                else:
                    self.stack.push('%s // %s' %(a, b))
                
                
            elif opcode_name == 'SMOD':  # 0x07
                a = self.stack.pop()
                b = self.stack.pop()
                if b == 0:
                    self.stack.push(0)
                else:
                    self.stack.push('%s $// %s' %(a, b))
               
                
            elif opcode_name == 'ADDMOD':  # 0x08
                a = self.stack.pop()
                b = self.stack.pop()
                c = self.stack.pop()
                if c == 0:
                    self.stack.push(0)
                else:
                    self.stack.push('(%s+%s)//%s' % (a, b, c))
                

            elif opcode_name == 'MULMOD':  # 0x09
                a = self.stack.pop()
                b = self.stack.pop()
                c = self.stack.pop()
                if c == 0:
                    self.stack.push(0)
                else:
                    self.stack.push('(%s*%s)//%s' % (a, b, c))
               
            

            elif opcode_name == 'EXP':  # 0x0a
                base = self.stack.pop()
                exponent = self.stack.pop()
                self.stack.push('%s^%s' %(base, exponent))
                

            elif opcode_name == 'SIGNEXTEND':  # 0x0b
                bits = self.stack.pop()
                value = self.stack.pop()
                self.stack.push('%s sig %s' % (value, bits))
                """if bits >= 256:
                    self.stack.push(value)
                else:
                    sign_bit = 1 << (bits - 1)
                    mask = sign_bit - 1
                    sign = (value & sign_bit) != 0
                if sign:
                    self.stack.push(value | (~mask))
                else:
                    self.stack.push(value & mask)"""
               

            elif opcode_name == 'LT':  # 0x10
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s<%s?' %(a, b))
               

            elif opcode_name == 'GT':  # 0x11
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s>%s?' %(a, b))
               

            elif opcode_name == 'SLT':  # 0x12
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s$<%s?' %(a, b))    #fu hao xiao yu
                

            elif opcode_name == 'SGT':  # 0x13
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s$>%s?' %(a, b))
                

            elif opcode_name == 'EQ':  # 0x14
                a = self.stack.pop()
                b = self.stack.pop()
                #self.stack.push(int(a == b))
                self.stack.push('%s==%s?' %(a, b))
               

            elif opcode_name == 'ISZERO':  # 0x15
                value = self.stack.pop()
                #self.stack.push(int(value == 0))
                self.stack.push('%s==0?' % value)
               

            elif opcode_name == 'AND':  # 0x16
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s & %s' % (a,b))
               

            elif opcode_name == 'OR':  # 0x17
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s | %s' %(a, b))
                

            elif opcode_name == 'XOR':  # 0x18
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push('%s X| %s' %(a, b))
               

            elif opcode_name == 'NOT':  # 0x19
                value = self.stack.pop()
                self.stack.push('NOT%s' % value)
                

            elif opcode_name == 'BYTE':  # 0x1a
                index = self.stack.pop()
                value = self.stack.pop()
                #print(index)
                if int(index, 16) >= 32:
                    self.stack.push(0)
                else:
                    #byte = (value >> (8 * (31 - index))) & 0xff
                    #self.stack.push(byte)
                    self.stack.push('%sBYTE%s' %(value, index))
                #self.pc += 1
                
            elif opcode_name == 'SHL':   #0x1b
                shift = self.stack.pop()
                value = self.stack.pop()
                self.stack.push('(%s)<<(%s)' % (value, shift))
                
            elif opcode_name == 'SHR':   #0x1c
                shift = self.stack.pop()
                value = self.stack.pop()
                self.stack.push('(%s)>>(%s)' % (value, shift))
                
            elif opcode_name == 'SAR':   #0x1d
                shift = self.stack.pop()
                value = self.stack.pop()
                self.stack.push('(%s)$>>(%s)' % (value, shift))

            elif opcode_name == 'SHA3':  # 0x20
                offset = self.stack.pop()
                size = self.stack.pop()
                #data = self.memory.read(offset, size)
                #hash_bytes = hashlib.sha3_256(data).digest()
                #hash_int = int.from_bytes(hash_bytes, byteorder='big')
                self.stack.push('hash of the given data in memory, offset = %s, size = %s.' % (offset, size))
                

            elif opcode_name == 'ADDRESS':  # 0x30
                self.stack.push('address of currently executing account')
               

            elif opcode_name == 'BALANCE':  # 0x31
                #address = self.stack.pop()
                self.stack.pop()
                #balance = self.env.get_balance(address)
                balance = 'balance of address'
                self.stack.push(balance)
                

            elif opcode_name == 'ORIGIN':  # 0x32
                self.stack.push('execution origination address')
                

            elif opcode_name == 'CALLER':  # 0x33
                self.stack.push('caller address')
              

            elif opcode_name == 'CALLVALUE':  # 0x34
                self.stack.push('callvalue')
                

            elif opcode_name == 'CALLDATALOAD':  # 0x35
                #offset = self.stack.pop()
                offset_in_calldata = self.stack.pop()
                #data = self.data[offset:offset+32]
                #value = int.from_bytes(data, byteorder='big')
                self.stack.push('CallData-cdoffset_is_%s.' % offset_in_calldata)
                

            elif opcode_name == 'CALLDATASIZE':  # 0x36
               #size = len(self.data)
                self.stack.push('CallDataSize')
                

            elif opcode_name == 'CALLDATACOPY':  # 0x37
                mem_offset = self.stack.pop()
                cd_offset = self.stack.pop()
                size = self.stack.pop()
                calldata_with_offset = 'CallData-offset_is_%s_cdoffset_is_%s_size_is_%s' % (mem_offset,cd_offset,size)
                self.memory.write(calldata_with_offset.encode('utf-8'))
                

            elif opcode_name == 'CODESIZE':  # 0x38
                #size = len(self.code)
                self.stack.push('size of code running in current environment')
                

            elif opcode_name == 'CODECOPY':  # 0x39
                mem_offset = self.stack.pop()
                code_offset = self.stack.pop()
                size = self.stack.pop()
                code_with_offset = 'RunningCode-offset=%s_codeoffset=%s_size=%s' % (mem_offset,code_offset,size)
                self.memory.write(code_with_offset.encode('utf-8'))

            elif opcode_name == 'GASPRICE':  # 0x3a
                #self.stack.push(self.gas_price)
                self.stack.push('price of gas') 
                

            elif opcode_name == 'EXTCODESIZE':  # 0x3b
                #address = self.stack.pop()
                address=self.stack.pop()
                #size = len(self.env.get_code(address))
                self.stack.push('Size of %s’s code' % address)
        

            elif opcode_name == 'EXTCODECOPY':  # 0x3c
                address = self.stack.pop()
                mem_offset = self.stack.pop()
                code_offset = self.stack.pop()
                size = self.stack.pop()
                code_with_offset = 'AccountCode-address=%s_offset=%s_codeoffset=%s_size=%s' % (address,mem_offset,code_offset,size)
                self.memory.write(code_with_offset.encode('utf-8'))


            elif opcode_name == 'RETURNDATASIZE':  # 0x3d
                self.stack.push('size of output data from the previous call')


            elif opcode_name == 'RETURNDATACOPY':  # 0x3e
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()


            elif opcode_name == 'EXTCODEHASH':  # 0x3f
                self.stack.pop()
                self.stack.push('hash of the chosen accounts code')


            elif opcode_name == 'BLOCKHASH':  # 0x40
                #block_number = self.stack.pop()
                #if self.env.block_number >= block_number > self.env.block_number - 256:
                    #block_hash = self.env.block_hashes[block_number]
                    #self.stack.push(block_hash)
                #else:
                    #self.stack.push(0)
                self.stack.pop()
                self.stack.push('blockhash')

            elif opcode_name == 'COINBASE':  # 0x41
                self.stack.push('the block’s beneficiary address')
                

            elif opcode_name == 'TIMESTAMP':  # 0x42
                self.stack.push('timestamp')
                

            elif opcode_name == 'NUMBER':  # 0x43
                self.stack.push('block_number')
                

            elif opcode_name == 'DIFFICULTY':  # 0x44
                self.stack.push('difficulty')
                

            elif opcode_name == 'GASLIMIT':  # 0x45
                self.stack.push('gas_limit')
                
                
            elif opcode_name == 'CHAINID':  # 0x46
                self.stack.push('chain_id')
                
                
            elif opcode_name == 'SELFBALANCE':  # 0x47
                self.stack.push('self_balance')    


            elif opcode_name == 'BASEFEE':  # 0x48
                self.stack.push('chain_id')


            elif opcode_name == 'POP':  # 0x50
                self.stack.pop()
               

            elif opcode_name == 'MLOAD':  # 0x51
                offset = self.stack.pop()
                #value = self.memory.read(offset, 32)
                mvalue = 'mvalue_offset=%s' % offset
                self.stack.push(mvalue)
                if mvalue not in self.memory:
                    self.memory.write(mvalue)
                
                

            elif opcode_name == 'MSTORE':# 0x52

            
                offset = self.stack.pop()
                value = self.stack.pop()
                value_with_offset = str(value) + '_offset=%s' % offset
                self.memory.write(value_with_offset.encode('utf-8'))


            elif opcode_name == 'MSTORE8':# 0x53
                offset = self.stack.pop()
                value = self.stack.pop()
                value_with_offset = str(value) + '_offset=%s' % offset + '_size=1 byte'
                self.memory.write(value_with_offset.encode('utf-8'))
                """mem_index = self.stack.pop()
                value = self.stack.pop() & 0xff
                self.memory.write(mem_index, value.to_bytes(1, byteorder='big'))
                #self.pc += 1"""

            elif opcode_name == 'SLOAD':  # 0x54
                slot = self.stack.pop()
                #slot = int(slot)
                if slot in self.storage:
                    value = self.storage[slot]
                    self.stack.push('%s_slot=%s ' % (value, slot))
                if slot not in self.storage:
                    self.stack.push('svalue_slot=%s ' % slot)
                    self.storage[slot] = 'svalue'
                #self.storage.write(slot, 'UnkonwnValue')
                #self.pc += 1

            elif opcode_name == 'SSTORE':  # 0x55
                slot = self.stack.pop()
                value = self.stack.pop()
                self.storage.write(slot, value)
                #self.pc += 1

            elif opcode_name == 'JUMP':  # 0x56
                #dest = self.stack.pop()
                #if dest in self.valid_jump_destinations:
                    #self.pc = dest - 1
                #else:
                    #self.invalid_jump()
                #self.pc += 1
                self.stack.pop()
                
            elif opcode_name == 'REQUIRE':
                self.stack.pop()
                
            elif opcode_name == 'ASSERT':
                self.stack.pop()
                
                
            elif opcode_name == 'JUMPI':  # 0x57
                """dest = self.stack.pop()
                flag = self.stack.pop()
                if dest in self.valid_jump_destinations:
                        if flag:
                            self.pc = dest - 1
                        else:
                            self.invalid_jump()
                self.pc += 1"""
                self.stack.pop()
                self.stack.pop()

            elif opcode_name == 'PC':  # 0x58
                self.stack.push('pc')
                #self.pc += 1

            elif opcode_name == 'MSIZE':  # 0x59
                self.stack.push('size of active memory in bytes')
                #self.pc += 1

            elif opcode_name == 'GAS':  # 0x5a
                self.stack.push('the amount of available gas')
                #self.pc += 1

            elif opcode_name == 'JUMPDEST':  # 0x5b
                pass
                #self.pc += 1
            
            elif opcode_name == 'PUSH1':  # 0x60
                """data = self.code[self.pc + 1:self.pc + 2]
                value = int.from_bytes(data, 'big')
                self.stack.push(value)
                self.pc += 1"""
                self.stack.push(operand)

            elif opcode_name == 'PUSH2':  # 0x61
                self.stack.push(operand)

            elif opcode_name == 'PUSH3':  # 0x62
                self.stack.push(operand)

            elif opcode_name == 'PUSH4':  # 0x63
                self.stack.push(operand)

            elif opcode_name == 'PUSH5':  # 0x64
                self.stack.push(operand)

            elif opcode_name == 'PUSH6':  # 0x65
                self.stack.push(operand)

            elif opcode_name == 'PUSH7':  # 0x66
                self.stack.push(operand)

            elif opcode_name == 'PUSH8':  # 0x67
                self.stack.push(operand)

            elif opcode_name == 'PUSH9':  # 0x68
                self.stack.push(operand)

            elif opcode_name == 'PUSH10':  # 0x69
                self.stack.push(operand)

            elif opcode_name == 'PUSH11':  # 0x6a
                self.stack.push(operand)

            elif opcode_name == 'PUSH12':  # 0x6b
                self.stack.push(operand)

            elif opcode_name == 'PUSH13':  # 0x6c
                self.stack.push(operand)

            elif opcode_name == 'PUSH14':  # 0x6d
                self.stack.push(operand)
               
            elif opcode_name == 'PUSH15':  # 0x6e
                self.stack.push(operand)

            elif opcode_name == 'PUSH16':  # 0x6f
                self.stack.push(operand)

            elif opcode_name == 'PUSH17':  # 0x70
                self.stack.push(operand)
    

            elif opcode_name == 'PUSH18':  # 0x71
                self.stack.push(operand)

            elif opcode_name == 'PUSH19':  # 0x72
                self.stack.push(operand)

            elif opcode_name == 'PUSH20':  # 0x73
                self.stack.push(operand)

            elif opcode_name == 'PUSH21':  # 0x74
                self.stack.push(operand)

            elif opcode_name == 'PUSH22':  # 0x75
                self.stack.push(operand)

            elif opcode_name == 'PUSH23':  # 0x76
                self.stack.push(operand)

            elif opcode_name == 'PUSH24':  # 0x77
                self.stack.push(operand)

            elif opcode_name == 'PUSH25':  # 0x78
                self.stack.push(operand)

            elif opcode_name == 'PUSH26':  # 0x79
                self.stack.push(operand)

            elif opcode_name == 'PUSH27':  # 0x7a
                self.stack.push(operand)

            elif opcode_name == 'PUSH28':  # 0x7b
                self.stack.push(operand)

            elif opcode_name == 'PUSH29':  # 0x7c
                self.stack.push(operand)

            elif opcode_name == 'PUSH30':  # 0x7d
                self.stack.push(operand)

            elif opcode_name == 'PUSH31':  # 0x7e
                self.stack.push(operand)

            elif opcode_name == 'PUSH32':  # 0x7f
                self.stack.push(operand)
    
            elif opcode_name == 'DUP1':  # 0x80
                val = self.stack.peek(0)
                self.stack.push(val)
                #self.pc += 1

            elif opcode_name == 'DUP2':  # 0x81
                val = self.stack.peek(1)
                self.stack.push(val)
                #self.pc += 1

            elif opcode_name == 'DUP3':  # 0x82
                val = self.stack.peek(2)
                self.stack.push(val)
                

            elif opcode_name == 'DUP4':  # 0x83
                val = self.stack.peek(3)
                self.stack.push(val)
                

            elif opcode_name == 'DUP5':  # 0x84
                val = self.stack.peek(4)
                self.stack.push(val)
                

            elif opcode_name == 'DUP6':  # 0x85
                val = self.stack.peek(5)
                self.stack.push(val)
                

            elif opcode_name == 'DUP7':  # 0x86
                val = self.stack.peek(6)
                self.stack.push(val)
                

            elif opcode_name == 'DUP8':  # 0x87
                val = self.stack.peek(7)
                self.stack.push(val)
                

            elif opcode_name == 'DUP9':  # 0x88
                val = self.stack.peek(8)
                self.stack.push(val)
                

            elif opcode_name == 'DUP10':  # 0x89
                val = self.stack.peek(9)
                self.stack.push(val)
                

            elif opcode_name == 'DUP11':  # 0x8a
                val = self.stack.peek(10)
                self.stack.push(val)
                

            elif opcode_name == 'DUP12':  # 0x8b
                val = self.stack.peek(11)
                self.stack.push(val)
                

            elif opcode_name == 'DUP13':  # 0x8c
                val = self.stack.peek(12)
                self.stack.push(val)
                

            elif opcode_name == 'DUP14':  # 0x8d
                val = self.stack.peek(13)
                self.stack.push(val)
                

            elif opcode_name == 'DUP15':  # 0x8e
                val = self.stack.peek(14)
                self.stack.push(val)
                

            elif opcode_name == 'DUP16':  # 0x8f
                val = self.stack.peek(15)
                self.stack.push(val)
                

            elif opcode_name == 'SWAP1':  # 0x90
                val1 = self.stack.pop()
                val2 = self.stack.pop()
                self.stack.push(val1)
                self.stack.push(val2)
                

            elif opcode_name == 'SWAP2':  # 0x91
                val1 = self.stack.pop()
                val2 = self.stack.pop()
                val3 = self.stack.pop()
                self.stack.push(val1)
                self.stack.push(val2)
                self.stack.push(val3)
                
                          
            elif opcode_name == 'SWAP3':  # 0x92
                val1 = self.stack.pop()
                val2 = self.stack.pop()
                val3 = self.stack.pop()
                val4 = self.stack.pop()
                self.stack.push(val1)
                self.stack.push(val3)
                self.stack.push(val2)
                self.stack.push(val4)
                

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
                

            elif opcode_name == 'LOG0':  # 0xa0
                """address = self.stack.pop()
                data = self.stack.pop()
                topics = []
                self.logs.append((address, topics, data.to_bytes(32, 'big')))
                self.pc += 2"""
                self.stack.pop()
                self.stack.pop()

            elif opcode_name == 'LOG1':  # 0xa1
                """address = self.stack.pop()
                data = self.stack.pop()
                topic1 = self.stack.pop()
                topics = [topic1]
                self.logs.append((address, topics, data.to_bytes(32, 'big')))
                self.pc += 2"""
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()

            elif opcode_name == 'LOG2':  # 0xa2
                """address = self.stack.pop()
                data = self.stack.pop()
                topic1 = self.stack.pop()
                topic2 = self.stack.pop()
                topics = [topic1, topic2]
                self.logs.append((address, topics, data.to_bytes(32, 'big')))
                self.pc += 2"""
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()

            elif opcode_name == 'LOG3':  # 0xa3
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()

            elif opcode_name == 'LOG4':  # 0xa4
                """address = self.stack.pop()
                data = self.stack.pop()
                topic1 = self.stack.pop()
                topic2 = self.stack.pop()
                topic3 = self.stack.pop()
                topic4 = self.stack.pop()
                topics = [topic1, topic2, topic3, topic4]
                self.logs.append((address, topics, data.to_bytes(32, 'big')))
                self.pc += 2"""
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()

            elif opcode_name == 'CREATE':  # 0xf0
                """value = self.stack.pop()
                in_offset = self.stack.pop()
                in_size = self.stack.pop()
                if not self.state.can_transfer_value(self.msg.sender, value):
                    self.stack.push(0)
                else:
                    endowment = self.state.db.get_balance(self.address)
                    if value > endowment:
                        self.stack.push(0)
                    else:
                        contract_code = self.memory.read(in_offset, in_size)
                        success, address = self.state.create_contract(self.msg.sender, value, contract_code)
                        if success:
                            self.stack.push(address)
                        else:
                            self.stack.push(0)
                self.pc += 1"""
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.push('address of a new account with associated code')

            elif opcode_name == 'CALL':    # 0xf1
                """CALL_NEW_ACCOUNT_COST = 2000
                CALL_COST = 700
            
                gas = self.stack.pop()
                to = self.stack.pop()
                value = self.stack.pop()
                in_offset = self.stack.pop()
                in_size = self.stack.pop()
                out_offset = self.stack.pop()
                out_size = self.stack.pop()
                gas -= CALL_NEW_ACCOUNT_COST if self.state.get_nonce(to) == 0 else CALL_COST
                if not self.state.can_transfer_value(self.msg.sender, value):
                    success = False
                    output = b''
                else:
                    contract_code = self.state.db.get_code(to)
                    if len(contract_code) == 0:
                        success = False
                        output = b''
                    else:
                        self.memory.extend(out_offset, out_size)
                        if in_size > 0:
                            self.memory.copy(in_offset, 0, in_size)
                        output, gas_left, success = self.state.send(to, value, gas, self.memory, in_offset, in_size)
                        self.gas -= gas - gas_left
                        if not success:
                            self.memory.resize(out_offset, 0)
                        else:
                            self.memory.resize(out_offset, len(output))
                            self.memory.copy(0, out_offset, len(output))
                if success:
                    self.stack.push(1)
                else:
                    self.stack.push(0)
                self.gas -= gas
                self.pc += 1"""
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.push('0 if the sub context reverted, 1 otherwise.')
                

            elif opcode_name == 'CALLCODE':  # 0xf2
                """gas = self.stack.pop()
                to = self.stack.peek(1)
                value = self.stack.pop()
                in_offset = self.stack.pop()
                in_size = self.stack.pop()
                out_offset = self.stack.pop()
                out_size = self.stack.pop()
                gas -= CALL_NEW_ACCOUNT_COST if self.state.get_nonce(to) == 0 else CALL_COST
                if not self.state.can_transfer_value(self.msg.sender, value):
                    success = False
                    output = b''
                else:
                    code = self.state.get_code(to)
                    self.memory.extend(out_offset, out_size)
                    if in_size > 0:
                        self.memory.copy(in_offset, 0, in_size)
                    output, gas_left, success = self.state.send(self.msg.contract_address, value, gas, self.memory, in_offset, in_size, code)
                    self.gas -= gas - gas_left
                    if not success:
                        self.memory.resize(out_offset, 0)
                    else:
                        self.memory.resize(out_offset, len(output))
                        self.memory.copy(0, out_offset, len(output))
                if success:
                    self.stack.push(1)
                else:
                    self.stack.push(0)
                self.gas -= gas
                self.pc += 1"""
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.push('0 if the sub context reverted, 1 otherwise.')

            elif opcode_name == 'RETURN':  # 0xf3
                offset = self.stack.pop()
                size = self.stack.pop()
                #self.memory.copy(offset, 0, size)
                #self.return_data = self.memory.get_contents()[:size]
                #self.pc += 1
                #return
                self.memory.write('Calling context return data')

            elif opcode_name == 'DELEGATECALL':        # 0xf4
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.push('0 if the sub context reverted, 1 otherwise.')
                """gas = self.stack.pop()
                to = self.stack.peek(1)
                in_offset = self.stack.pop()
                in_size = self.stack.pop()
                out_offset = self.stack.pop()
                out_size = self.stack.pop()
                code = self.state.get_code(to)
                if not self.state.can_transfer_value(self.msg.sender, 0):
                    success = False
                    output = b''
                else:
                    self.memory.extend(out_offset, out_size)
                    if in_size > 0:
                        self.memory.copy(in_offset, 0, in_size)
                    success, output, gas_left = self.state.execute(to=to, sender=self.msg.sender, gas=gas, value=0, data=bytes(self.memory[:in_size]), code=code)
                    if success:
                        self.memory.copy(0, out_offset, len(output))
                        self.memory.write32(out_size - 32, len(output))
                        self.stack.push(len(output))
                    self.gas -= gas - gas_left
                self.stack.push(success)
                self.pc += 1
            elif opcode_name == 'CREATE2':  # 0xf5
                CREATE2 = 0xf5

                endowment = self.stack.pop()
                in_offset = self.stack.pop()
                in_size = self.stack.pop()
                salt = self.stack.pop()
                new_address = utils.mk_contract_address(self.msg.sender, salt, initcode=bytes(self.memory[:in_size]))
                contract_exists = self.state.account_exists(new_address)
                if contract_exists:
                    self.stack.push(new_address)
                    self.stack.push(1)
                    self.pc += 1
                elif not self.state.can_transfer_value(self.msg.sender, endowment):
                    self.stack.push(0)
                    self.pc += 1
                else:
                    gas = self.gas - CREATE_GAS
                    if self.state.get_nonce(self.msg.sender) == 0:
                        gas -= CREATE_NEW_ACCOUNT_COST
                    if self.state.get_balance(self.msg.sender) < endowment:
                        gas -= CREATE_BALANCE_COST
                    success, gas_left, contract = self.state.create(
                        endowment=endowment,
                        sender=self.msg.sender,
                        salt=salt,
                        code=bytes(self.memory[:in_size]),
                        gas=gas,
                    )
                    if success:
                        self.stack.push(new_address)
                        self.stack.push(1)
                        self.logs.append(LogEntry(self.tx_origin, CREATE2, self.gas_price, self.gas_price * in_size + CREATE_GAS - gas_left, self.pc, contract, [new_address]))
                    else:
                        self.stack.push(0)
                    self.gas = gas_left
                    self.pc += 1"""
                    
                    
                    
            elif opcode_name == 'CREATE2':  # 0xf5
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.push('address of the deployed contract, 0 if the deployment failed')
            

          
            elif opcode_name == 'STATICCALL':  # 0xfa
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.push('0 if the sub context reverted, 1 otherwise')
              
                    
                    
            elif opcode_name == 'REVERT':  # 0xfd
                self.stack.push('REVERT')                   
                    
            elif opcode_name == 'INVALID':  # 0xfe
                self.stack.push('INVALID')
                #success = False
                #output = b''
                #self.stack.clear()
                #self.memory.clear()
                #self.storage.clear()

            elif opcode_name == 'SELFDESTRUCT':  # 0xff
                """recipient = self.stack.pop()
                self.state.set_balance(recipient, self.state.get_balance(recipient) + self.state.get_balance(self.msg.to))
                self.state.set_nonce(self.msg.to, self.state.get_nonce(self.msg.to) + 1)
                self.state.db.delete_account(self.msg.to)
                self.pc += 1
                success = False
                output = b"""
                self.stack.pop()

            elif opcode_name == '95':  # accident
                pass
            
            elif opcode_name == '94':  # accident
                pass
                
            else:
                print(opcode_name)
                raise Exception("unknown opcode")
                
                
            result = {
                'stack': self.stack,
                'memory': self.memory,
                'storage': self.storage
            }
            return result
        







       

