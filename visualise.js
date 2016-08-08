/**
 * Knowledge graph visualiser module
 @author TaoPR (github.com/starcolon)
 */

var args   = process.argv.slice(2);
var colors = require('colors');
var KB     = require('./jslib/knowledge.js');


// Validate the arguments initially
(function validateArgs(args){
  if (args.length==0){
    console.error('[ERROR] You need to supply OrientDB root database like:'.red);
    console.error('$ node visualise MYPASSWORD'.red);
    process.exit(1);
  }
})(args);

// Initialise a connection
const db = 'vor';
const usrname = 'root';
var password = args[0];
KB.connect(db,usrname,password)
  .catch((e) => {
    console.error('[ERROR] connection to OrientDB failed.'.red);
    console.error(e);
    process.exit(1);
  }) 
  .then((g) => {
    console.log('[Connected] to OrientDB knowledge graph.'.green);

    // TAOTODO: Implement the visualiser
    KB.topics();
  })



 