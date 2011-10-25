
//add listener to initialize ... which listens for onPageLoad
window.addEventListener("load", function() { SLPageInterpretor.init(); }, false);
function SLAction() {
  alert("Action");
//window._content.document.location  = "http://www.google.com/search?q=" + encodeURI(query);

}

function httpGet(theUrl) {
    var xmlHttp = null;

    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

var SLPageInterpretor = {
  init: function() {
    //Listen for onPageLoad so that we can submit request to server
    var appcontent = document.getElementById("appcontent");   // browser
    if(appcontent)
      appcontent.addEventListener("DOMContentLoaded", SLPageInterpretor.onPageLoad, true);
  },

  onPageLoad: function(aEvent) {
    var doc = aEvent.originalTarget; // doc is document that triggered "onload" event
    // do something with the loaded page.

    if (doc.location.href == "about:blank")
      return;

//    $.get(
//          "10.0.1.116",
//          {'location' : doc.location.href},
//          function(data) {
//             alert('response content: ' + data);
//          }
//      );


    $("#SLTextField").val(httpGet("http://10.0.1.116/"));

  },

  onPageUnload: function(aEvent) {
    // do something
  }
}