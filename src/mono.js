/*
 * Copyright (C) 2015 BlackGear
 * https://github.com/BlackGear/Mono_PAC
 */
var tunnel = __proxyList__;
var direct = "DIRECT;";
var whiteList = __whiteList__;
var blackList = __blackList__;
var codeList = __codeList__;
var maskList = __maskList__;

function FindProxyForURL(url, host) {
    if (isPlainHostName(host)) {
        return direct;
    }

    var suffix = host;
    var pos = 0;

    do {
        if (blackList.hasOwnProperty(suffix)) {
            return tunnel;
        }
        if (whiteList.hasOwnProperty(suffix)) {
            return direct;
        }
        pos = host.indexOf(".", pos) + 1;
        suffix = host.substring(pos);
    } while (pos > 0);

    var IP = dnsResolve(host);

    if (!IP) {
        return tunnel;
    }

    var atom = IP.split(".");
    var code = ((atom[1] & 0xff) << 8) | ((atom[2] & 0xff));
    var hash = atom[0];

    var codeHash = codeList[hash];
    var maskHash = maskList[hash];

    if (codeHash === 0) {
        return tunnel;
    }

    var min = 0;
    var max = codeHash.length;

    while (min + 1 < max) {
        var mid = (min + max) >> 1;
        if (codeHash[mid].charCodeAt(0) > code) {
            max = mid;
        } else {
            min = mid;
        }
    }

    if (maskHash[min] === 0) {
        return direct;
    } else {
        mask = parseInt(maskHash[min], 16);
    }

    if (code - codeHash[min].charCodeAt(0) >> mask === 0) {
        return direct;
    }

    return tunnel;
}
