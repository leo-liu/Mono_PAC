#! /usr/bin/env node
var lzString = require('./lz-string.js');
var fs = require('fs');

if (process.argv.length < 3) {
  console.error('Usage: lz-string <input_file>');
  process.exit(1);
}

console.log('var codeList = \'' + lzString.compressToUTF16(fs.readFileSync(process.argv[2], {
  encoding: 'utf8',
})) + '\';');
