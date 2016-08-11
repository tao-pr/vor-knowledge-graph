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

    // Reduce the form of nodes so they become renderable.
    nodes = nodes.map((n) => {
      return {
        id:    n['@rid'],
        type:  n['@class'],
        label: n['@class']=='TOPIC' ? n.title : n.w,
        x:     Math.random()*3,
        y:     Math.random(),
        size:  n['@class']=='TOPIC' ? 10 : 1,
        color: n['@class']=='TOPIC' ? '#F00000' : '#FFAAAA'
      }
    })

    // Take outbound edges of those underlying nodes
    console.log('Enumurating edges...');
    var edges = [];
    var collectEdges = (es) => es.then((e) => {
      edges.push(e);
    });
    var topic = (n) => n.type=='TOPIC';

    // Prepare edge enumuration jobs
    var jobs = nodes
      .filter(topic)
      .map(KB.getOutE(20))
      .map((n) => {
        return collectEdges(n);
      });

    // Make sure edges of all underlying nodes are processed.
    return Promise.all(jobs).then(() => [nodes,edges])
  })
  .then((p) => {

    var nodes = p[0];
    var edges = p[1];

    // Flatten edges
    edges = edges.reduce((a,b) => a.concat(b), []);

    // Make all edges renderable
    edges = edges.map((e) => {
      return {
        id:     Math.random()*10000,
        source: e.out,
        target: e.in
      }
    })

    var graph = { nodes: nodes, edges: edges }; 
    var sgraph = JSON.stringify(graph);

    var content = `function getGraph(){ return ${sgraph} }`;
    return new Promise((done,reject) => {
      fs.writeFile('./HTML/graph-data.js',content,(err) => {
        console.log('Serialising graph to JS ...'.green);
        console.log(`   ${graph.nodes.length} nodes`);
        console.log(`   ${graph.edges.length} links`);
        if (err){
          console.error('Serialisation failed...'.red);
          console.error(err);
          return reject();
        }
        else{
          console.log('Graph HTML is ready in ./HTML/'.green);
          return done();
        }
      })
    })
  })
  .then((_) => process.exit())

 