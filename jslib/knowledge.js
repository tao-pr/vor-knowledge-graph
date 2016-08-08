/**
 * Knowledge graph query
 * @author TaoPR (github.com/starcolon)
 */

var Knw = {}
var orient = require('orientdb-js');
var Promise = require('bluebird');

/**
 * Make a connection to the OrientDB
 * @param {string} database name
 * @param {string} username
 * @param {string} password
 */
Knw.connect = function(db,usrname,psw){
  // Do nothing if connected
  if (Knw.__db)
    return;

  Knw.__db = orient.connect({
    'database': db,
    'user':     usrname,
    'psw':      psw
  })
}

Knw.topics = function(condition){}

Knw.keywords = function(condition){}

Knw.expandFromTopic = function(topic,degree){}

Knw.expandFromKeyword = function(kw,degree){}


module.exports = Knw;