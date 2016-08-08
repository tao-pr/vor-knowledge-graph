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


Knw.topics = function(condition){
  
}

Knw.keywords = function(condition){}

Knw.expandFromTopic = function(topic,degree){}

Knw.expandFromKeyword = function(kw,degree){}


module.exports = Knw;