window.onload = search;

var searchText;
var searchButtonLabel;
var searchIcon;
var isSearchOpen;

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
    searchText.style.maxWidth = "125px";
    searchText.style.paddingTop = "3px";
    searchText.style.paddingBottom = "3px";
    searchText.style.paddingRight = "17px";
    searchText.style.marginLeft = "-15em";
    searchText.focus();
    searchText.select();

    searchIcon.style.transition = "background-color .2s ease 0s, color .2s ease 0s";
    searchIcon.style.backgroundColor = "#fff";
    searchIcon.style.color = "#818181";

    isSearchOpen = true;
}

function closeSearchInput() {
    searchText.style.maxWidth = "0px";
    searchText.style.padding = "0px";

    searchIcon.style.transition = "background-color .2s ease .5s, color .2s ease .5s";
    searchIcon.style.paddingLeft = "5px";
    searchIcon.style.backgroundColor = "transparent";
    searchIcon.style.color = "#fff";

    isSearchOpen = false;
}
