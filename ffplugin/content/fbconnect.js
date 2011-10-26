
// Not sure how to use the standard facebook connect and obtain to the access token
// initialize the library with the API key
//FB.init({ apiKey: '309628079050942' });

// fetch the status on load
//FB.getLoginStatus(handleSessionResponse);


//TODO Need to detect if the user is already logged in
//     if we store the accessToken and hasSiteCookie == True we can avoid the login step
//TODO Need to detect if the user logs in via www.facebook.com

var SLFBConnect = {
    _accessToken:"",

    init: function() {
      //Listen for onPageLoad so that we can attempt to detect the auth code
      //TODO see if there is a better listener for detecting the AuthPage
      var appcontent = document.getElementById("appcontent");   // browser
      if(appcontent)
        appcontent.addEventListener("load", SLFBConnect.onAuthLoad, true);
    },
    
    hasSiteCookie: function (){
        //cycles through the cookies looking for the facebook.com cookie
        var cookieMgr = Components.classes["@mozilla.org/cookiemanager;1"]
            .getService(Components.interfaces.nsICookieManager);

        for (var e = cookieMgr.enumerator; e.hasMoreElements();) {
            var cookie = e.getNext().QueryInterface(Components.interfaces.nsICookie);
            if ((cookie.host == ".facebook.com" || cookie.host == "facebook.com") && cookie.name == 'c_user')
                return true;
        }

        return false;
    },

    toggleLogin: function(event) {
        //TODO be able to logout as well as login
        var askUrl = "https://www.facebook.com/dialog/oauth?client_id=" + 309628079050942 + "&redirect_uri=http://www.facebook.com/&scope=publish_stream&response_type=token";
        gBrowser.selectedTab = gBrowser.addTab(askUrl);
    },

    onAuthLoad: function (event) {
        //looks for a facebook.com url with the access_token
        // TODO: find more robust way to find valid facebook url
        if (event.originalTarget.location.href.indexOf('facebook.com') == -1)
            return;

        if (event.originalTarget.location.href.indexOf("access_token") > 0)
        {
            alert("Attempting session:" + event.originalTarget.location.href);
            // if the page loads to a facebook.com/#access_token=xx then we've authenticated successfully
            // we may want to add some additional error checking to make sure access_token is valid

            var pList = event.originalTarget.location.hash.substring(1).split('&');

            for (var i=0; i<pList.length; i++)
            {
                var tup = pList[i].split('=');

                if (tup[0] == "access_token")
                {
                    //alert ("auth token is:" + tup[1]);
                    SLFBConnect.sessionWithAuth(tup[1])
                }
            }
        }
    },

    fetchGraphObject: function(method, callback)
    {

        var req = Components.classes["@mozilla.org/xmlextras/xmlhttprequest;1"]
            .createInstance(Components.interfaces.nsIXMLHttpRequest);
        req.onreadystatechange = function(e)
        {
            try
            {
                if (req.readyState != 4) { return; }

//                alert("finished graph call, status = " + req.status);
                alert("graph response: " + req.responseText);

                if (req.status != 200)
                    return;

                var jsObject = JSON .parse(req.responseText);

                callback(jsObject);
            }
            catch (e)
            {
                //TODO: Need better solution
                alert("graph error: " + e);
                return;
            }

        };
        req.open("GET", "https://graph.facebook.com/" + method + "?access_token=" + this._accessToken, true);
        req.send(null);
    },


    sessionWithAuth: function(accessToken) {

        this._accessToken   = accessToken;

        this.fetchGraphObject("me", function(response)
        {
            if (response.id)
            {
                //debug("SAVING ACCESS TOKEN: " + accessToken);
                $("#SLFBName").val(response.name);
                $("#SLActionButton").attr("label", "Log out")

//                fbSvc._uid = response.id;
//                fbSvc._loggedIn      = true;
//                fbSvc._prefService.setCharPref('extensions.facebook.access_token', accessToken)
//                fbSvc._prefService.setCharPref('extensions.facebook.uid', response.id)
            }
            else
            {
                alert("missing id in 'me' graph call");
                return;
            }

        });
    }


};