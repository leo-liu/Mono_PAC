# Mono PAC

A PAC(Proxy auto-config) file generator with fetched China IP range, which helps walk around GFW.

Mono generates a much smaller PAC file than any other project does.

## Installation
<pre>
$ git clone https://github.com/BlackGear/Mono_PAC.git
</pre>

## Uasge
Edit config file in ./src, then:
<pre>
$ python ./src/make.py
</pre>
Both Python 2 and 3 are supported.

## Configuration
- WhiteList / BlackList:

One domains per line, # for comments. Domains will be automatic merged when generating. So you can feel free to add domains to the list.

- ipList:

One record per line with IP/CIDR format. Records will be automatic merged before generating.

- proxyList:

Proxy config infomations in order.
<pre>
PROXY host:port   = use HTTP proxy
SOCKS5 host:port  = use Socks5 proxy
DIRECT            = Do not use proxy
</pre>

Note: Safari do not understand "SOCKS5", use "SOCKS" instead, you can also use a more compatible form like:
<pre>
SOCKS5 xxxx:xxxx
SOCKS xxxx:xxxx
DIRECT
</pre>

Note: The last DIRECT have a potential risk cause the dns pollution will affect the domains in the blackList.

Note: When you use socks proxy, whether dns resolve will through the proxy is determined by the Apps itself. When you use http proxy, the dns resolve will always through the proxy.

## Performance
Performance with Node.js:
<pre>
./performance_test.sh
Testing pac generated by BlackGear/Mono_Pac
avg: 2.268us

Testing pac generated by breakwa11/gfw_whitelist
avg: 4.331us

Testing pac generated by Leask/flora_pac
avg: 145.960us

Testing pac generated by Leask/flora_pac-mod
avg: 4.781us

Testing pac generated by usufu/flora_pac
avg: 2.939us

-rw-r--r--  1 Daniel  staff   45662  2 24 21:53 BlackGear-Mono_Pac.pac
-rw-r--r--  1 Daniel  staff  165129  2 24 21:53 Leask-Flora_Pac-mod.pac
-rw-r--r--  1 Daniel  staff   74738  2 24 21:53 Leask-Flora_Pac.pac
-rw-r--r--  1 Daniel  staff   92854  2 24 21:53 breakwa11-gfw_whitelist.pac
-rw-r--r--  1 Daniel  staff  254539  2 24 21:53 usufu-Flora_Pac.pac
</pre>

Performance with Safari:
<pre>
Testing pac generated by BlackGear/Mono_Pac
Average 192.78ms in 100,000 tests

Testing pac generated by breakwa11/gfw_whitelist
Average 463.54ms in 100,000 tests

Testing pac generated by Leask/flora_pac
Average 4934.83ms in 100,000 tests

Testing pac generated by Leask/flora_pac-mod
Average 400.81ms in 100,000 tests

Testing pac generated by usufu/flora_pac
Average 281.89ms in 100,000 tests
</pre>

Notes:

All Pac files except Leask-Flora_Pac.pac use a full ipList.

Leask-Flora_Pac.pac use a minimal ipList ignored the last two bytes of every ip.

All Pac files except breakwa11-gfw_whitelist.pac use O(1) algorithm to check the domains white or black list.

breakwa11-gfw_whitelist.pac does not check domains white or black list

** Mono generates the smallest PAC but provides the best performance.**

## Trivia

The code in the root field of the PAC file will be run only once.

The code in the FindProxyForURL function's field will be run each time you browser the internet.

Just test this two PAC files:

<pre>
    var unixtime_ms = new Date().getTime();
    while(new Date().getTime() &lt; unixtime_ms + 5000) {}
    function FindProxyForURL(url, host) {
        return "DIRECT;";
    }
</pre>

<pre>
    function FindProxyForURL(url, host) {
        var unixtime_ms = new Date().getTime();
        while(new Date().getTime() &lt; unixtime_ms + 5000) {}
        return "DIRECT;";
    }
</pre>

So put all var xx = yy in the root field will accelerate the PAC file.

PS: if code in the root field of the PAC file will be run many times, we should put the var inside the FindProxyForURL just before it being used.

## LICENSE
The MIT License

Copyright (c) 2015 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
