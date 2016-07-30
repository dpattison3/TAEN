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
        var searchQuery = url.substring(searchIndex + 7, url.length);
        var ampIndex = searchQuery.indexOf("&");
        if (ampIndex != -1) {
            searchQuery = searchQuery.substring(0, ampIndex);
        }
        openSearchInput();
        searchText.value = searchQuery;
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
            searchIcon.style.color = "#5a5a5a";
        } else {
            searchIcon.style.color = "#818181";
        }
    }

    searchButtonLabel.onmouseleave = function() {
        if (isSearchOpen) {
            searchIcon.style.color = "#818181";
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
    searchText.style.maxWidth = "15em";
    searchText.style.paddingTop = ".1em";
    searchText.style.paddingBottom = ".1em";
    searchText.style.paddingRight = ".9em";
    searchText.style.marginLeft = "-15em";
    searchText.focus();

    searchIcon.style.transition = "background-color .2s ease 0s, color .2s ease 0s";
    searchIcon.style.backgroundColor = "#fff";
    searchIcon.style.color = "#818181";

    isSearchOpen = true;
}

function closeSearchInput() {
    searchText.style.maxWidth = "0em";
    searchText.style.padding = "0em";

    searchIcon.style.transition = "background-color .2s ease .5s, color .2s ease .5s";
    searchIcon.style.paddingLeft = ".125em";
    searchIcon.style.backgroundColor = "transparent";
    searchIcon.style.color = "#fff";

    isSearchOpen = false;
}

var youtubePattern = [
        "https://www.youtube.com/.*",
        "http://www.youtube.com/.*",
        "www.youtube.com/.*",
        "youtube.com/.*",
];
var youtubeRegex = new RegExp(youtubePattern.join("|"), "i");

var soundcloudPattern = [
    "https://soundcloud.com/.*",
    "http://soundcloud.com/.*",
    "https://www.soundcloud.com/.*",
    "http://www.soundcloud.com/.*",
    "www.soundcloud.com/.*",
    "soundcloud.com/.*",
];
var soundcloudRegex = new RegExp(soundcloudPattern.join("|"), "i");

var spotifyPattern = [
    "https://www.spotify.com/.*",
    "https://www.spotify.com/.*",
    "www.spotify.com/.*",
    "spotify.com/.*",
];
var spotifyRegex = new RegExp(spotifyPattern.join("|"), "i");

var applePattern = [
    "http://www.apple.com/music/.*",
    "https://www.apple.com/music/.*",
    "www.apple.com/music/.*",
    "apple.com/music/.*",
];
var appleRegex = new RegExp(applePattern.join("|"), "i");

var twitterPattern = [
    "https://twitter.com/.*",
    "http://twitter.com/.*",
    "https://www.twitter.com/.*",
    "http://www.twitter.com/.*",
    "www.twitter.com/.*",
    "twitter.com/.*",
];
var twitterRegex = new RegExp(twitterPattern.join("|"), "i");

var facebookPattern = [
    "https://www.facebook.com/.*",
    "http://www.facebook.com/.*",
    "https://facebook.com/.*",
    "https://facebook.com/.*",
    "www.facebook.com/.*",
    "facebook.com/.*",
];
var facebookRegex = new RegExp(facebookPattern.join("|"), "i");

var pinterestPattern = [
    "https://www.pinterest.com/.*",
    "http://www.pinterest.com/.*",
    "https://pinterest.com/.*",
    "http://pinterest.com/.*",
    "www.pinterest.com/.*",
    "pinterest.com/.*",
];
var pinterestRegex = new RegExp(pinterestPattern.join("|"), "i");

var tumblrPattern = [
    "https://www.tumblr.com/.*",
    "https://www.tumblr.com/.*",
    "https://tumblr.com/.*",
    "http://tumblr.com/.*",
    "www.tumblr.com/.*",
    "tumblr.com/.*",
];
var tumblrRegex = new RegExp(tumblrPattern.join("|"), "i");

var instagramPattern = [
    "https://www.instagram.com/.*",
    "http://www.instagram.com/.*",
    "https://instagram.com/.*",
    "http://instagram.com/.*",
    "www.instagram.com/.*",
    "instagram.com/.*",
];
var instagramRegex = new RegExp(instagramPattern.join("|"), "i");

var socialPattern = instagramPattern.concat(tumblrPattern, pinterestPattern,
        facebookPattern, twitterPattern);
var socialRegex = new RegExp(socialPattern.join("|"), "i");

var portfolioPattern = youtubePattern.concat(applePattern, spotifyPattern,
        soundcloudPattern);
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
