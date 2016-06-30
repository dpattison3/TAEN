window.onload = function() {
    var searchText = document.getElementById("searchText");
    var searchButtonLabel = document.getElementById("searchButtonLabel");
    var searchIcon = document.getElementById("searchIcon");
    var isSearchOpen = false;

    // check if there is an existing search request and populate the text field
    var url = window.location.href;
    var index = url.indexOf("search=");
    if (index != -1) {
        var searchQuery = url.substring(index + 7, url.length);
        openSearchInput();
        searchText.value = searchQuery;
    }


    document.onclick = function(obj) {
        if (searchButtonLabel.contains(obj.target) && isSearchOpen) {
            document.getElementById("searchForm").submit();
        } else if (searchButtonLabel.contains(obj.target)) {
            openSearchInput();
        } else if (isSearchOpen) {
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

    function openSearchInput() {
        searchText.style.maxWidth = "20em";
        searchText.style.paddingTop = ".1em";
        searchText.style.paddingBottom = ".1em";
        searchText.select();

        searchIcon.style.transition = "background-color .2s ease 0s";
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
}
