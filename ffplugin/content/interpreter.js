
//add listener to initialize ... which listens for onPageLoad
window.addEventListener("load", function() { SLPageInterpretor.init(); }, false);
function SLAction() {
  alert("Action");
//window._content.document.location  = "http://www.google.com/search?q=" + encodeURI(query);

}

function httpPost(theUrl, data) {
    var xmlHttp = null;

    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", theUrl, true );

    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlHttp.setRequestHeader("Content-length", data.length);
    xmlHttp.setRequestHeader("Connection", "close");

    xmlHttp.onreadystatechange = function() {//Call a function when the state changes.
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            $("#SLTextField").val(xmlHttp.responseText);
            //alert(xmlHttp.responseText);
        }
    }

    xmlHttp.send( data );
    return xmlHttp.responseText;
}

var SLPageInterpretor = {
  init: function() {
    //Listen for onPageLoad so that we can submit request to server
    var appcontent = document.getElementById("appcontent");   // browser
    if(appcontent)
      appcontent.addEventListener("load", SLPageInterpretor.onPageLoad, true);
  },

  onPageLoad: function(aEvent) {
    var doc = aEvent.originalTarget; // doc is document that triggered "onload" event
    // do something with the loaded page.

    if (doc.location.href == "about:blank")
      return;

    var htmlStr = doc.getElementsByTagName('html')[0].innerHTML;
    httpPost("http://10.0.1.116/", "activexml="+encodeURIComponent(htmlStr));

  },

  onPageUnload: function(aEvent) {
    // do something
  }
}