#! /usr/bin/env node
var lzString = require('./lz-string.js');
var fs = require('fs');

if (process.argv.length < 3) {
  console.error('Usage: lz-string <input_file>');
  process.exit(1);
}

r = lzString.compress(fs.readFileSync(process.argv[2], {encoding: 'utf8'}));
s = r.replace('\u2028', '\\u2028');
p = 'var codeList = \'' + s + '\';'

fs.writeFileSync('bbb.js', p, {encoding: 'utf8'});


/*for (var i = r.length - 1; i >= 0; i--) {
    console.log(r[i].charCodeAt(0).toString(16));
}*/
