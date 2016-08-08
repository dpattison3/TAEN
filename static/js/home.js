window.onload = start;

// search variables
var searchText;
var searchButtonLabel;
var searchIcon;
var isSearchOpen;

function start() {
    profileHeightAdjustment();
    search();
}

function profileHeightAdjustment() {
    var profileList = document.getElementsByClassName("profile-preview");
    var max = 0;
    for (var i = 0; i < profileList.length; ++i) {
        max = (profileList[i].clientHeight > max) ? profileList[i].clientHeight
                : max;
    }
    for (var i = 0; i < profileList.length; ++i) {
        profileList[i].style.height = max.toString() + "px";
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
    searchText.style.marginLeft = "-200px";
    searchText.select();

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
