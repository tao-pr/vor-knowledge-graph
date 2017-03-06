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

const usrname = 'root';
var password = args[0];

var indexGraphMapper = function(nodes){
  // TAOTODO:
}

var circularGraphMapper = function(nodes){
  return new Promise((done,reject) => {
    // Reduce the form of nodes so they become renderable.
    var L = nodes.filter((n) => n['@class']=='TOPIC').length;
    var degreeStep = 2*Math.PI/L;
    var i = -1;

    nodes = nodes.map((n) => {
      i++;
      var randomDegree = Math.random()*2*Math.PI;
      var randomR = Math.random()*0.8;
      var x = randomR * Math.cos(randomDegree);
      var y = randomR * Math.sin(randomDegree);

      return {
        id:    n['@rid'],
        type:  n['@class'],
        label: n['@class']=='TOPIC' ? n.title : n.w,
        x:     n['@class']=='TOPIC' ? Math.cos(degreeStep*i) : x,
        y:     n['@class']=='TOPIC' ? Math.sin(degreeStep*i) : y, 
        size:  n['@class']=='TOPIC' ? 10 : 1,
        color: n['@class']=='TOPIC' ? '#F00000' : '#FFAAAA'
      }
    })

    // Take outbound edges of those underlying nodes
    console.log('Enumerating edges...');
    var edges = [];
    var collectEdges = (es) => es.then((e) => {
      edges.push(e);
    });
    var topic = (n) => n.type=='TOPIC';

    // Prepare edge enumuration jobs
    var jobs = nodes
      .filter(topic)
      .map(KB.getOutE(100))
      .map((n) => {
        return collectEdges(n);
      });

    // Make sure edges of all underlying nodes are processed.
    return Promise.all(jobs).then(() => [nodes,edges])
  })
  .then((p) => {

    console.log('Transforming nodes & edges ...')
    var nodes = p[0];
    var edges = p[1];

    // Flatten edges
    edges = edges.reduce((a,b) => a.concat(b), []);

    // Make all edges renderable
    edges = edges.map((e) => {
      return {
        id:     Math.random()*10000,
        source: e.out,
        target: e.in,
        type:   'curve'
      }
    })

    var graph = { nodes: nodes, edges: edges }; 
    var sgraph = JSON.stringify(graph);

    return sgraph
  })
}

function saveToJSON(outputPath){
  return function (sgraph){
    return new Promise((done,reject) => {
      var content = `function getGraph(){ return ${sgraph} }`;
      fs.writeFile(`./HTML/${outputPath}`,content,(err) => {
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
  }
}

//-------------------------------
// [OrientDB data] => [JSON data]
// mapping strategies
//-------------------------------
const dataMapping = {
  'vor': {
    'mapper': circularGraphMapper,
    'output': 'graph-data.js'
  }
  // },
  // 'vorindex': {
  //   'mapper': indexGraphMapper,
  //   'output': 'graph-index.js'
  // }
};

/**
 * Map [OrientDB data] => [renderable JSON]
 * by the predefined mapping strategies
 */
for (db in dataMapping){
  
  console.log('================================'.cyan)
  console.log('[Datasource] Processing : '.cyan, db)
  console.log('================================'.cyan)

  var mapToJSON = dataMapping[db].mapper;
  var outputPath = dataMapping[db].output;

  KB.connect(db,usrname,password)
    .catch((e) => {
      console.error(`[ERROR] connection to OrientDB [${db}] failed.`.red);
      console.error(e);
      process.exit(1);
    }) 
    .then((g) => {
      console.log(`[Connected] to OrientDB [${db}].`.green);

      // Read all nodes in
      var nodes = KB.nodes();
      console.log('All nodes retrieved...')

      // Fulfill the values and go on
      return Promise.resolve(nodes)
    })
    .then(mapToJSON)
    .then(saveToJSON(outputPath))
    //.then((_) => process.exit())
}