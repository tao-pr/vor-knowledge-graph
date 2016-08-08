/**
 * Knowledge graph query
 * @author TaoPR (github.com/starcolon)
 */

var Knw = {}
var OrientDB = require('orientjs');
var Promise = require('bluebird');

/**
 * Make a connection to the OrientDB
 * @param {string} database name
 * @param {string} username
 * @param {string} password
 * @return {Promise}
 */
Knw.connect = function(db,usrname,psw){
  // Do nothing if connected
  if (Knw.graph)
    return Promise.resolve(Knw.graph);

  Knw.server = OrientDB({
    host:       'localhost',
    port:       2424,
    username:   usrname,
    password:   psw
  });

  return Knw.server.use(db)
    .then((_db) => {
      console.log('[OrientDB] connected'.green);
      Knw.graph = _db;
      return Knw.graph; 
    })
}

/**
 * Release the database resources
 */
Knw.tearDown = function(){
  Knw.server.close();
}

Knw.topics = function(condition){
  
}

Knw.keywords = function(condition){}

Knw.expandFromTopic = function(topic,degree){}

Knw.expandFromKeyword = function(kw,degree){}


module.exports = Knw;