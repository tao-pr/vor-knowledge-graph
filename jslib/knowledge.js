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
 * @return {Promise} which wraps a [db] variable
 */
Knw.connect = function(db,usrname,psw){
  // Do nothing if connected
  if (Knw.db)
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
 * List all topic vertices where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.topics = function(condition){
  if (condition)
    return Knw.db.select('title').from('topic').where(condition).all();
  return Knw.db.select('title').from('topic').all();
}

/**
 * List all keyword vertices where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.keywords = function(condition){
  if (condition)
    return Knw.db.select('w').from('keyword').where(condition).all();
  return Knw.db.select('w').from('keyword').all();
}

/**
 * List all has(es) edges where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.hases = function(condition){
  if (condition)
    return Knw.db.select().from('has').where(condition).all();
  return Knw.db.select().from('has').all();
}

/**
 * List all rel(s) edges where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.rels = function(condition){
  if (condition)
    return Knw.db.select().from('rel').where(condition).all();
  return Knw.db.select().from('rel').all();
}


module.exports = Knw;