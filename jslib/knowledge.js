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
 * List all vertices where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.nodes = function(condition){
  if (condition)
    return Knw.db.select().from('V').where(condition).all();
  return Knw.db.select().from('V').all();
}

/**
 * List all edges where condition is met
 * @param {Object} must satisfy OrientDB query format
 */
Knw.edges = function(condition){
  if (condition)
    return Knw.db.select().from('E').where(condition).all();
  return Knw.db.select().from('E').all();
}

module.exports = Knw;