/*!
 * refreshing page on 30 sec
 */

$(document).ready(function(){
  setInterval(function(){
    $('.refresh-page').load('/');
  },30000);
});