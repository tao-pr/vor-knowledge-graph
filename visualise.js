/**
 * Knowledge graph visualiser module
 @author TaoPR (github.com/starcolon)
 */

var args = process.argv.slice(2);
var KB   = require('./jslib/knowledge.js');


// Validate the arguments initially
(function validateArgs(args){
  if (args.length==0){
    console.error('[ERROR] You need to supply OrientDB root database like:');
    console.error('$ node visualise MYPASSWORD');
    process.exit(1);
  }
})(args);



 