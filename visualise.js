/**
 * Knowledge graph visualiser module
 * @author TaoPR (github.com/starcolon)
 */

var args    = process.argv.slice(2);
var colors  = require('colors');
var fs      = require('fs');
var Promise = require('bluebird');

const MAX_LINKS = 100;


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

var indexGraphMapper = function(KB){
  return function(nodes){
    var nodeHash = new Set();
    var nodes = nodes.map(n => {
      nodeHash.add(n['@rid'].toString());
      return {
        id:    n['@rid'],
        type:  n['@class'],
        label: n['@class']=='TOPIC' ? n.title : n.w,
        color: n['@class']=='TOPIC' ? '#F00000' : '#FFAAAA',
        value: n['@class']=='TOPIC' ? 5 : 3,
        borderWidth: n['@class']=='TOPIC' ? 3 : 1
      }
    })

    nodeHash = Array.from(nodeHash)

    var topicOnly   = (n) => n.type == 'TOPIC';
    var keywordOnly = (n) => n.type == 'KEYWORD';
    var allKeywords = nodes.filter(keywordOnly);
    var allTopics   = nodes.filter(topicOnly);

    // Enumurate index between [nodes] <==> [keywords]
    console.log('Enurating edges...');
    var edges = [];
    var collectEdges = (iter) => iter.then((es) => {
      es.forEach(e => {

        var _in = e['in'].toString();
        var _out = e['out'].toString();

        edges.push({
          from:  nodeHash.indexOf(_in),
          to:    nodeHash.indexOf(_out),
          value: e['weight']
        });
      })
    });

    // Prepare edge enumuration jobs
    var jobs = allTopics
      .map(KB.getInboundIndex(MAX_LINKS)) 
      .map(collectEdges);

    return Promise
      .all(jobs).then(() => [nodes,edges])
      .then((p) => {

        var [nodes, edges] = p;

        console.log('Remapping nodes...')
        nodes = nodes.map( n => {
          n.id = nodeHash.indexOf(n.id.toString()); // @rid => integer
          return n
        })

        // Remove unlinked nodes from the graph
        var allInboundNodes = new Set(edges.map(e => e.to));
        var allOutboundNodes = new Set(edges.map(e => e.from));
        nodes = nodes.filter(n => 
          allOutboundNodes.has(n.id) ||
          allInboundNodes.has(n.id));

        var graph = { nodes: nodes, edges: edges }; 
        var sgraph = JSON.stringify(graph);

        return [graph,sgraph]
      });
  }
}
  
var circularGraphMapper = function(KB){
  return function(nodes){
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
    var collectEdges = (node) => node.then((e) => {
      edges.push(e);
    });
    var topic = (n) => n.type=='TOPIC';

    // Prepare edge enumuration jobs
    var jobs = nodes
      .filter(topic)
      .map(KB.getOutE(MAX_LINKS))
      .map(collectEdges);

    // Make sure edges of all underlying nodes are processed.
    return Promise
      .all(jobs).then(() => [nodes,edges])
      .then((p) => {

        console.log('Transforming nodes & edges ...')
        var [nodes, edges] = p;

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

        return [graph,sgraph]
      })
  }
}

function saveToJSON(outputPath){
  return function (graphArray){
    
    var graph = graphArray[0];
    var sgraph = graphArray[1];

    return new Promise((done,reject) => {
      console.log('Initialising I/O ...');
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
const dataMapping = [
  {
    'name':  'vor',
    'mapper': circularGraphMapper,
    'output': 'graph-data.js'
  },
  {
    'name': 'vorindex',
    'mapper': indexGraphMapper,
    'output': 'graph-index.js'
  }
]

/**
 * Map [OrientDB data] => [renderable JSON]
 * by the predefined mapping strategies
 */

Promise.mapSeries(dataMapping, (db) => {
  
  console.log('================================'.cyan)
  console.log('[Datasource] Processing : '.cyan, db)
  console.log('================================'.cyan)

  var KB      = require('./jslib/knowledge.js');
  var reconnect = true
  var mapToJSON = db.mapper;
  var outputPath = db.output;

  return KB
    .connect(db.name,usrname,password,reconnect)
    .catch((e) => {
      console.error(`[ERROR] connection to OrientDB [${db.name}] failed.`.red);
      console.error(e);
      process.exit(1);
    }) 
    .then((g) => {
      console.log(`[Connected] to OrientDB [${db.name}].`.green);

      // Read all nodes in
      var nodes = KB.nodes();
      console.log('All nodes retrieved...')

      // Fulfill the values and go on
      return Promise.resolve(nodes)
    })
    .then(mapToJSON(KB))
    .then(saveToJSON(outputPath))
  })
.then((_) => process.exit())