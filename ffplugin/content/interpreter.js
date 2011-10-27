
function inspect(obj, maxLevels, level)
{
  var str = '', type, msg;

    // Start Input Validations
    // Don't touch, we start iterating at level zero
    if(level == null)  level = 0;

    // At least you want to show the first level
    if(maxLevels == null) maxLevels = 1;
    if(maxLevels < 1)
        return '<font color="red">Error: Levels number must be > 0</font>';

    // We start with a non null object
    if(obj == null)
    return '<font color="red">Error: Object <b>NULL</b></font>';
    // End Input Validations

    // Each Iteration must be indented
    str += '<ul>';

    // Start iterations for all objects in obj
    for(property in obj)
    {
      try
      {
          // Show "property" and "type property"
          type =  typeof(obj[property]);
          str += '<li>(' + type + ') ' + property +
                 ( (obj[property]==null)?(': <b>null</b>'):('')) + '</li>';

          // We keep iterating if this property is an Object, non null
          // and we are inside the required number of levels
          if((type == 'object') && (obj[property] != null) && (level+1 < maxLevels))
          str += inspect(obj[property], maxLevels, level+1);
      }
      catch(err)
      {
        // Is there some properties in obj we can't access? Print it red.
        if(typeof(err) == 'string') msg = err;
        else if(err.message)        msg = err.message;
        else if(err.description)    msg = err.description;
        else                        msg = 'Unknown';

        str += '<li><font color="red">(Error) ' + property + ': ' + msg +'</font></li>';
      }
    }

      // Close indent
      str += '</ul>';

    return str;
}

//add listener to initialize ... which listens for onPageLoad
window.addEventListener("load", function() { SLPageInterpretor.init(); SLFBConnect.init();}, false);
function SLAction() {
  alert("Action");
//window._content.document.location  = "http://www.google.com/search?q=" + encodeURI(query);

}



var SLPageInterpretor = {
  init: function() {

    //Listen for onPageLoad so that we can submit request to server
    var appcontent = document.getElementById("appcontent");   // browser
    if(appcontent)
      appcontent.addEventListener("load", SLPageInterpretor.onPageLoad, true);
  },


  handleResponse: function(responseText) {
    var response = JSON.parse(responseText);

    //remove all labels from previous interpretation
    var elem = document.getElementById("SLInterpretContent");
    while(elem.hasChildNodes()){
       elem.removeChild(elem.firstChild);
    }

    // add all new keyPhrases
    for (var i=0; i<response.length;++i){
        var item = response[i];
        if (item.keyPhrase != undefined) {
            var node = document.createElement('label');
            node.setAttribute('value', item.keyPhrase);
            elem.appendChild(node);
        }

    }
  },

  submitPage: function httpPost(theUrl, data) {
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", theUrl, true );

    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlHttp.setRequestHeader("Content-length", data.length);
    xmlHttp.setRequestHeader("Connection", "close");

    xmlHttp.onreadystatechange = function() {//Call a function when the state changes.
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            SLPageInterpretor.handleResponse(xmlHttp.responseText);
        }
    }

    xmlHttp.send( data );
    return xmlHttp.responseText;
  },

  onPageLoad: function(aEvent) {
    var doc = aEvent.originalTarget; // doc is document that triggered "onload" event
    // do something with the loaded page.
    if (doc.location.href == "about:blank")
      return;


    var htmlStr = doc.getElementsByTagName('html')[0].innerHTML;
    SLPageInterpretor.submitPage("http://10.0.1.116/", "activexml="+encodeURIComponent(htmlStr));

  },

  onPageUnload: function(aEvent) {
    // do something
  }
}