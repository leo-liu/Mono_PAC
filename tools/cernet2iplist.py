#!/usr/bin/env python3

import urllib.request
import html.parser
import re

class CernetIPListParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self._dolist = False
    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self._dolist = True
    def handle_endtag(self, tag):
        if tag == 'pre':
            self._dolist = False
    def handle_data(self, data):
        if self._dolist:
            pattern = re.compile(r'^((?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+((?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+((?:[0-9]{1,3}\.){3}[0-9]{1,3})')
            for line in data.splitlines():
                match = pattern.match(line)
                if match:
                    ip, _, mask = match.groups()
                    print('{}/{}'.format(ip, mask))


iplist_url = 'http://www.nic.edu.cn/RS/ipstat/internalip/real.html'
with urllib.request.urlopen(iplist_url) as f:
    parser = CernetIPListParser()
    parser.feed(f.read().decode('gb2312'))
