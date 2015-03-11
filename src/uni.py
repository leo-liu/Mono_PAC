#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import sys

class RouteChain(object):
    def __init__(self):
        self.rule = []
        self.list = []
        self.insert('0.0.0.0/8')
        self.insert('10.0.0.0/8')
        self.insert('127.0.0.0/8')
        self.insert('169.254.0.0/16')
        self.insert('172.16.0.0/12')
        self.insert('192.0.0.0/24')
        self.insert('192.0.2.0/24')
        self.insert('192.88.99.0/24')
        self.insert('192.168.0.0/16')
        self.insert('198.18.0.0/15')
        self.insert('198.51.100.0/24')
        self.insert('203.0.113.0/24')
        self.insert('224.0.0.0/4')
        self.insert('240.0.0.0/4')

    def insert(self, ipnet):
        addr, mask = ipnet.split('/')
        bits = addr.split('.')
        addr = 0
        for byte in bits:
            addr = (addr << 8) + int(byte)
        mask = 1 << 32 - int(mask)
        self.rule.append((addr, mask))

    def reduce(self):
        self.rule.sort(key=lambda x: x[0])
        head = 0
        rule = []
        for (addr, mask) in self.rule:
            flag = addr + mask
            if head > flag:
                continue
            if head > addr:
                addr, _ = rule.pop()
                mask = flag - addr
            head = flag
            rule.append((addr, mask))
        for (addr, mask) in rule:
            while mask > 0:
                head = 1 << mask.bit_length() - 1
                if addr + head >> 24 != addr >> 24:
                    head = (((addr >> 24) + 1) << 24) - addr
                self.list.append((addr, head))
                mask = mask - head
                addr = addr + head

def load_config(data):
    lines = []
    for line in data.splitlines():
        line = line.split('#')[0].strip()
        if line:
            lines.append(line)
    return lines

def load_range(data):
    lines = load_config(data)
    route = RouteChain()
    for line in lines:
        route.insert(line)
    route.reduce()

    codelist = []
    masklist = []

    for (addr, mask) in route.list:
        atom = addr >> 24
        codelist.append(unichr(addr >> 8 & 0x00FFFF))
        masklist.append(addr >> 8 & 0x00FFFF)

    codelist.append(unichr(0x2028))
    codelist.append(unichr(0x2029))
    codelist.append(unichr(0x00A))
    codelist.append(unichr(0x00D))

    masklist.append(0x2028)
    masklist.append(0x2029)
    masklist.append(0x00A)
    masklist.append(0x00D)

    codelist = json.dumps(codelist, separators=(',', ':'), ensure_ascii=False).replace(u'\u2028', '\u2028').replace(u'\u2029', '\u2029')
    masklist = json.dumps(masklist, separators=(',', ':'))

    return codelist, masklist

def main():
    payload = open('ipList').read()
    codelist, masklist = load_range(payload)
    with open('1.js', 'w') as output:
        output.write(('a=' + codelist + '\n').encode('utf-8'))
        output.write(('b=' + masklist + '\n').encode('utf-8'))

if __name__ == '__main__':
    main()
