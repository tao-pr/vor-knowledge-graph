/**
 * Knowledge graph query
 * @author TaoPR (github.com/starcolon)
 */

var Knw = {}
var ODatabase = require('orientjs').ODatabase;
var Promise = require('bluebird');

/**
 * Make a connection to the OrientDB
 * @param {string} database name
 * @param {string} username
 * @param {string} password
 * @param {bool} force reconnect?
 * @return {Promise} which wraps a [db] variable
 */
Knw.connect = function(db,usrname,psw,reconnect=false){
  // Do nothing if connected
  if (Knw.db && !reconnect)
    return Promise.resolve(Knw.db);

  Knw.db = new ODatabase({
    host:       'localhost',
    port:       2424,
    username:   usrname,
    password:   psw,
    name:       db
  });

  return Knw.db.open();
}


/**
 * List all vertices where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.nodes = function(condition){
  if (condition)
    return Knw.db.select().from('V').where(condition).all();
  return Knw.db.select().from('V').all();
}

Knw.allTopics = () => Knw.nodes({'@class': 'TOPIC'})
Knw.allKeywords = () => Knw.nodes({'@class': 'KEYWORD'})

/**
 * List all edges where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.edges = function(condition){
  if (condition)
    return Knw.db.select().from('E').where(condition).all();
  return Knw.db.select().from('E').all();
}

/**
 * List all outbound edges from the specified node
 * @param {Object} node object
 * @return {Promise}
 */
Knw.getOutE = function(limit){
  return function(node){
    var linked = {'out': node.id}
    var output = (node.type=='TOPIC') ? 
      Knw.db.select().from('has').where(linked) :
      Knw.db.select().from('rel').where(linked);

    if (limit){
      return output.limit(limit).all();
    }
    else
      return output.all();
  }
}

/**
 * List all outbound index edges from the specified node
 * @param {Object} node object
 * @return {Promise}
 */
Knw.getOutIndex = function(limit){
  return function(node){
    // TAODEBUG:
    console.log(`...edges from node #${node.id}`)

    var linked = {'out': node.id}
    var output = Knw.db
      .select().from('e')
      .where(linked)
      .order('weight desc')

    if (limit){
      return output.limit(limit).all();
    }
    else
      return output.all();
  }
}

module.exports = Knw;