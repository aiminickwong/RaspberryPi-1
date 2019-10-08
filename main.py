#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import ctypes 

NUM = 16      
fun = ctypes.CDLL("./libfun.so")
ret = fun.myFunction(NUM)  

print(ret)
