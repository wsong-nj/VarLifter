#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 17:29:41 2023

@author: lyc
"""

class TypeBase:
 
    def uint_base(self, key):
        key_type_mapping = {
            '0xff': "uint8",
            '0xffff': "uint16",
            '0xffffff': "uint24",
            '0xffffffff': "uint32",
            '0xffffffffff': "uint40",
            '0xffffffffffff': "uint48",
            '0xffffffffffffff': "uint56",
            '0xffffffffffffffff': "uint64",
            '0xffffffffffffffffff': "uint72",
            '0xffffffffffffffffffff': "uint80",
            '0xffffffffffffffffffffff': "uint88",
            '0xffffffffffffffffffffffff': "uint96",
            '0xffffffffffffffffffffffffff': "uint104",
            '0xffffffffffffffffffffffffffff': "uint112",
            '0xffffffffffffffffffffffffffffff': "uint120",
            '0xffffffffffffffffffffffffffffffff': "uint128",
            '0xffffffffffffffffffffffffffffffffff': "uint136",
            '0xffffffffffffffffffffffffffffffffffff': "uint144",
            '0xffffffffffffffffffffffffffffffffffffff': "uint152",
            '0xffffffffffffffffffffffffffffffffffffffff': "address",
            '0xffffffffffffffffffffffffffffffffffffffffff': "uint168",
            '0xffffffffffffffffffffffffffffffffffffffffffff': "uint176",
            '0xffffffffffffffffffffffffffffffffffffffffffffff': "uint184",
            '0xffffffffffffffffffffffffffffffffffffffffffffffff': "uint192",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffff': "uint200",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffff': "uint208",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffff': "uint216",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "uint224",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "uint232",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "uint240",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "uint248",
            '0x8': "uint8",
            '0x10': "uint16",
            '0x18': "uint24",
            '0x20': "uint32",
            '0x28': "uint40",
            '0x30': "uint48",
            '0x38': "uint56",
            '0x40': "uint64",
            '0x48': "uint72",
            '0x50': "uint80",
            '0x58': "uint88",
            '0x60': "uint96",
            '0x68': "uint104",
            '0x70': "uint112",
            '0x78': "uint120",
            '0x80': "uint128",
            '0x88': "uint136",
            '0x90': "uint144",
            '0x98': "uint152",
            '0xa0': "address",
            '0xa8': "uint168",
            '0xb0': "uint176",
            '0xb8': "uint184",
            '0xc0': "uint192",
            '0xc8': "uint200",
            '0xd0': "uint208",
            '0xd8': "uint216",
            '0xe0': "uint224",
            '0xe8': "uint232",
            '0xf0': "uint240",
            '0xf8': "uint248"   
        }
        return  key_type_mapping.get(key, None)

    def int_base(self, key):
        key_type_mapping = {
            '0x0': "int8",
            '0x1': "int16",
            '0x2': "int24",
            '0x3': "int32",
            '0x4': "int40",
            '0x5': "int48",
            '0x6': "int56",
            '0x7': "int64",
            '0x8': "int72",
            '0x9': "int80",
            '0xa': "int88",
            '0xb': "int96",
            '0xc': "int104",
            '0xd': "int112",
            '0xe': "int120",
            '0xf': "int128",
            '0x10': "int136",
            '0x11': "int144",
            '0x12': "int152",
            '0x13': "int160",
            '0x14': "int168",
            '0x15': "int176",
            '0x16': "int184",
            '0x17': "int192",
            '0x18': "int200",
            '0x19': "int208",
            '0x1a': "int216",
            '0x1b': "int224",
            '0x1c': "int232",
            '0x1d': "int240",
            '0x1e': "int248"
         }
        return  key_type_mapping.get(key, None)

    def bool_base(self, key):
        key_type_mapping = {
            'double iszero': "bool"
         }
        return  key_type_mapping.get(key, None) 

    def bytesN_base(self, key):
        key_type_mapping = {
            '0xf8': "bytes1",
            '0xf0': "bytes2",    #240/8=30
            '0xe8': "bytes3",  
            '0xe0': "bytes4", 
            '0xd8': "bytes5", 
            '0xd0': "bytes6", 
            '0xc8': "bytes7",
            '0xc0': "bytes8",
            '0xb8': "bytes9",
            '0xb0': "bytes10",
            '0xa8': "bytes11",
            '0xa0': "bytes12",         
            '0x98': "bytes13",          
            '0x90': "bytes14",          
            '0x88': "bytes15",          
            '0x80': "bytes16",          
            '0x78': "bytes17",            
            '0x70': "bytes18",            
            '0x68': "bytes19",            
            '0x60': "bytes20",
            '0x58': "bytes21",
            '0x50': "bytes22",
            '0x48': "bytes23",
            '0x40': "bytes24",
            '0x38': "bytes25",
            '0x30': "bytes26",
            '0x28': "bytes27",
            '0x20': "bytes28",
            '0x18': "bytes29",
            '0x10': "bytes30",
            '0x8': "bytes31",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "bytes1",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "bytes2",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "bytes3",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffff': "bytes4",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffffff': "bytes5",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffffff': "bytes6",
            '0xffffffffffffffffffffffffffffffffffffffffffffffffff': "bytes7",
            '0xffffffffffffffffffffffffffffffffffffffffffffffff': "bytes8",
            '0xffffffffffffffffffffffffffffffffffffffffffffff': "bytes9",
            '0xffffffffffffffffffffffffffffffffffffffffffff': "bytes10",
            '0xffffffffffffffffffffffffffffffffffffffffff': "bytes11",
            '0xffffffffffffffffffffffffffffffffffffffff': "bytes12",
            '0xffffffffffffffffffffffffffffffffffffff': "bytes13", 
            '0xffffffffffffffffffffffffffffffffffff': "bytes14",
            '0xffffffffffffffffffffffffffffffffff': "bytes15",
            '0xffffffffffffffffffffffffffffffff': "bytes16",
            '0xffffffffffffffffffffffffffffff': "bytes17",            
            '0xffffffffffffffffffffffffffff': "bytes18",            
            '0xffffffffffffffffffffffffff': "bytes19",            
            '0xffffffffffffffffffffffff': "bytes20",            
            '0xffffffffffffffffffffff': "bytes21",             
            '0xffffffffffffffffffff': "bytes22",
            '0xffffffffffffffffff': "bytes23",              
            '0xffffffffffffffff': "bytes24",             
            '0xffffffffffffff': "bytes25",
            '0xffffffffffff': "bytes26",            
            '0xffffffffff': "bytes27",            
            '0xffffffff': "bytes28",            
            '0xffffff': "bytes29", 
            '0xffff': "bytes30", 
            '0xff': "bytes31"
         }
        return  key_type_mapping.get(key, None)   
    
    def address_base(self, key):
        key_type_mapping = {
            '0xa0': "address"
         }
        return  key_type_mapping.get(key, None)                  