/**
 * Knowledge graph visualiser module
 * @author TaoPR (github.com/starcolon)
 */

var args   = process.argv.slice(2);
var colors = require('colors');
var fs     = require('fs');
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

    var nodes = KB.nodes();
    var edges = KB.edges();

    // Generate [graph-data.js] file
    // for front-end graph rendering
    var graph = {
      vertices: nodes,
      edges:    edges
    }
    var sgraph = JSON.stringify(graph);

    var content = `function getGraph(){ return ${sgraph} }`;
    return new Promise((done,reject) => {
      fs.writeFile('./HTML/graph-data.js',content,(err) => {
        console.log('Serialising graph to JS ...'.green);
        console.log(`   ${graph.vertices.length} nodes`);
        console.log(`   ${graph.edges.length} links`);
        if (err){
          console.error('Serialisation failed...'.red);
          console.error(err);
          reject();
        }
        else{
          console.log('Graph HTML is ready in ./HTML/'.green);
          done();
        }
      })
    })
  })
  .then((_) => process.exit())

 