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

    // Read all nodes in
    var nodes = KB.nodes();
    console.log('All nodes retrieved...')

    // Fulfill the values and go on
    return Promise.resolve(nodes)
  })
  .then((nodes) => {

    // TAODEBUG:
    console.log(JSON.stringify(nodes[0]).cyan);

    // Take up to 20 outbound edges from a node
    // console.log('Enumurating edges...');
    // var getUpto20E = KB.getOutE(20);
    // var edges      = nodes.map(getUpto20E);
    var edges = [];

    var graph = { vertices: nodes, edges: edges };
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

 