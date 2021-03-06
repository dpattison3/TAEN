window.onload = start;

// portfolio variables
var portfoliotable;
var socialTable;
var linkDiv;
var links
var numSocialLinks;
var numPortfolioLinks;
// search variables
var searchText;
var searchButtonLabel;
var searchIcon;
var isSearchOpen;

function start() {
    if (window.innerWidth <= 768) {
        searchTextWidth = "125";
    } else if (window.innerWidth <= 992) {
        searchTextWidth = "150";
    } else {
        searchTextWidth = "200";
    }
    
    profile();
    search();
}

// portfolio markup functionality
function profile() {
    numSocialLinks = 0;
    numPortfolioLinks = 0;

    linkDiv = document.getElementById("links");
    links = linkDiv.children;
    linkDiv.parentElement.removeChild(linkDiv);

    portfoliotable = document.getElementById("profilePortfolioTable");
    socialTable = document.getElementById("profileSocialTable");

    for (var i = 0; links.length > 0; ++i) {
        addURLToTable(links[0]);
    }
    if (numSocialLinks == 0) {
        var emptymsg = document.createTextNode("No social media links have been added");
        socialTable.parentElement.appendChild(emptymsg);
    }
    if (numPortfolioLinks == 0) {
        var emptymsg = document.createTextNode("No portfolio links have been added");
        portfoliotable.parentElement.appendChild(emptymsg);
    }
}

// search functionality
function search() {
    searchText = document.getElementById("searchText");
    searchButtonLabel = document.getElementById("searchButtonLabel");
    searchIcon = document.getElementById("searchIcon");
    isSearchOpen = false;

    // check if there is an existing search request and populate the text field
    var url = window.location.href;
    var searchIndex = url.indexOf("search=");
    if (searchIndex != -1) {
        openSearchInput();
    }

    document.onclick = function(obj) {
        if (searchButtonLabel.contains(obj.target) && isSearchOpen) {
            document.getElementById("searchForm").submit();
        } else if (searchButtonLabel.contains(obj.target)) {
            openSearchInput();
        } else if (isSearchOpen && !searchText.contains(obj.target)) {
            closeSearchInput();
        }
    }

    searchButtonLabel.onmouseover = function() {
        searchIcon.style.transition = "0s";
        if (isSearchOpen) {
            searchIcon.style.backgroundColor = "#bdbdbd";
        } else {
            searchIcon.style.color = "#818181";
        }
    }

    searchButtonLabel.onmouseleave = function() {
        if (isSearchOpen) {
            searchIcon.style.backgroundColor = "#cecece";
        } else {
            searchIcon.style.color = "#fff";
        }
    }

    searchButtonLabel.onmousedown = function () {
        if (isSearchOpen) {
            searchIcon.style.color = "#3b3b3b";
        } else {
            searchIcon.style.color = "#5a5a5a";
        }
    }
}

function openSearchInput() {
    $("#searchText").width(searchTextWidth);
    searchText.style.paddingTop = ".1em";
    searchText.style.paddingBottom = ".1em";
    searchText.style.paddingRight = ".35em";
    searchText.select();

    searchIcon.style.transition = "background-color .2s ease 0s, color .2s ease 0s";
    searchIcon.style.backgroundColor = "#cecece";
    searchIcon.style.color = "#5a5a5a";

    isSearchOpen = true;
}

function closeSearchInput() {
    $("#searchText").width("0");
    searchText.style.width = "0px";
    searchText.style.padding = "0px";

    searchIcon.style.transition = "background-color .2s ease .5s, color .2s ease .5s";
    searchIcon.style.paddingLeft = ".125em";
    searchIcon.style.backgroundColor = "transparent";
    searchIcon.style.color = "#fff";

    isSearchOpen = false;
}

var youtubeRegex = "^.*(youtube\.com).*$";
var soundcloudRegex = "^.*(soundcloud\.com).*$";
var spotifyRegex = "^.*(spotify\.com).*$";
var appleRegex = "^.*(apple\.com).*$";
var twitterRegex = "^.*(twitter\.com).*$";
var facebookRegex = "^.*(facebook\.com).*$";
var pinterestRegex = "^.*(pinterest\.com).*$";
var tumblrRegex = "^.*(tumblr\.com).*$";
var instagramRegex = "^.*(instagram\.com).*$";
var linkedinRegex = "^.*(linkedin\.com).*$";
var bandcampRegex = "^.*(bandcamp\.com).*$";

var socialPattern = [
        twitterRegex,
        facebookRegex,
        pinterestRegex,
        tumblrRegex,
        instagramRegex
]
var socialRegex = new RegExp(socialPattern.join("|"), "i");

var portfolioPattern = [
        youtubeRegex,
        soundcloudRegex,
        spotifyRegex,
        appleRegex,
        linkedinRegex,
        bandcampRegex
]
var portfolioRegex = new RegExp(portfolioPattern.join("|"), "i");

function urlToIconStyle(url, element) {
    var newElement = document.createElement("I");
    newElement.style.fontSize = "2.5em";
    if (url.match(youtubeRegex) != null) {
        newElement.style.color = "#e52d27";
        newElement.className = "fa fa-youtube-play";
    } else if (url.match(soundcloudRegex) != null) {
        newElement.style.color = "#ff3a00";
        newElement.className = "fa fa-soundcloud";
    } else if (url.match(spotifyRegex) != null) {
        newElement.style.color = "#2ebd59";
        newElement.className = "fa fa-spotify";
    } else if (url.match(appleRegex) != null) {
        newElement.style.color = "#000";
        newElement.className = "fa fa-apple";
    } else if (url.match(twitterRegex) != null) {
        newElement.style.color = "#00aced";
        newElement.className = "fa fa-twitter";
    } else if (url.match(facebookRegex) != null) {
        newElement.className = "fa fa-facebook-square";
        newElement.style.color = "#3b5998";
    } else if (url.match(pinterestRegex) != null) {
        newElement.className = "fa fa-pinterest-square";
        newElement.style.color = "#bd081c";
    } else if (url.match(tumblrRegex) != null) {
        newElement.className = "fa fa-tumblr-square";
        newElement.style.color = "#35465c";
    } else if (url.match(instagramRegex) != null) {
        newElement.className = "fa fa-instagram";
        newElement.style.color = "#517fa4";
    } else if (url.match(linkedinRegex) != null) {
        newElement.className = "fa fa-linkedin-square";
        newElement.style.color = "#4875B4";
    }

    element.appendChild(newElement);
}

function addURLToTable(a) {
    var url = a.href;
    var title = a.innerHTML;
    a.innerHTML = "";

    var newTr = document.createElement("TR");
    var newTh = document.createElement("TH");
    var newTd = document.createElement("TD");
    newTd.innerHTML = title;
    urlToIconStyle(url, a);
    newTh.appendChild(a);
    newTr.appendChild(newTh);
    newTr.appendChild(newTd);
    socialTable.appendChild(newTr);

    if (url.match(socialRegex) != null) {
        socialTable.appendChild(newTr);
        numSocialLinks++;
    } else if (url.match(portfolioRegex) != null) {
        portfoliotable.appendChild(newTr);
        numPortfolioLinks++;
    }
}
