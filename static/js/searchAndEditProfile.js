window.onload = start;

// portfolio variables
var numberOfLinks;
var portfolio;
var linkForms;
var deletedLinks;
// search variables
var searchText;
var searchButtonLabel;
var searchIcon;
var isSearchOpen;

function start() {
    portfolio();
    search();
}

// portfolio editing functionality
function portfolio() {
    numberOfLinks = document.getElementById("existingPortfolio").children.length;
    portfolio = document.getElementById("portfolio");
    linkForms = document.getElementById("linkForms");
    deletedLinks = [];
    var portfolioChildren = portfolio.children;

    var removeLink = document.getElementById("existingPortfolio").getElementsByTagName("SPAN");
    for (var i = 0; i < removeLink.length; ++i) {
        removeLink[i].onclick = deleteLink;
    }

    $('#editProfile').on('submit', function(event) {
        event.preventDefault();
        var validated = updateProfile();
        if (validated) {
            document.getElementById("editProfile").submit();
        }
    });

    document.getElementById("addToPortfolio").onclick = addToPortfolio;

    // submit form script on enter key
    $(window).keydown(function(event) {
        if(event.keyCode == 13) {
            event.preventDefault();
            var validated = updateProfile();
            if (validated) {
                document.getElementById("editProfile").submit();
            }
        }
    });
}

function updateProfile() {
    var forms = linkForms.children;
    var linksToSubmit = [];
    var titlesForLinks = [];
    var validated = true;
    for (var i = 0; i < forms.length; ++i) {
        var linkTxt = forms[i].elements.link.value;
        if ((linkTxt.length == 0) || (validateURL(linkTxt))) {
            if (linkTxt.length != 0) {
                linksToSubmit.push(linkTxt);
                titlesForLinks.push(forms[i].elements.title.value);
            }
        } else {
            if (!forms[i].getElementsByTagName("DIV")[0]) {
                var errormsg = document.createElement("DIV");
                errormsg.className += " alert alert-danger";
                errormsg.setAttribute("role", "alert");
                errormsg.innerHTML += "url is malformed or the domain is not supported";
                forms[i].appendChild(errormsg);
            }
            validated = false;
        }
    }
    if (validated) {
        submitForm(linksToSubmit, titlesForLinks);
    }
    return validated;
}

function submitForm(linksToSubmit, titlesForLinks) {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    $.ajax({
        url : "/update_portfolio/",
        type : "post",
        traditional: true,
        data : {
                deleted : deletedLinks,
                numberOfLinksToAdd : numberOfLinks,
                newLinks : linksToSubmit,
                titles : titlesForLinks
        },

        error : function(xhr,errmsg,err) {
            alert(errmsg);
        }
    });
}

function addToPortfolio() {
    if (numberOfLinks <= 10) {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", ".");

        var link = document.createElement("input");
        link.setAttribute('type', "text");
        link.setAttribute('name', "link");
        link.setAttribute("placeholder", "link url");

        var title = document.createElement("input");
        title.setAttribute('type', "text");
        title.setAttribute('name', "title");
        title.setAttribute("placeholder", "title");

        var deleteButton = document.createElement("span");
        deleteButton.className += " glyphicon glyphicon-remove-sign remove-portfolio-link";
        deleteButton.setAttribute("role", "button");
        deleteButton.onclick = function(obj) {
            obj.target.parentElement.parentElement.removeChild(obj.target.parentElement);
            --numberOfLinks;
        }

        form.appendChild(title);
        form.appendChild(link);
        form.appendChild(deleteButton);
        linkForms.appendChild(form);
        link.select();
        ++numberOfLinks;
    }
    if (numberOfLinks == 5) {
        var addLink = document.getElementById("addToPortfolio");
        portfolio.removeChild(addLink);
    }
}

function deleteLink(obj) {
    var linkParent = obj.target.parentElement;
    linkParent.parentElement.removeChild(linkParent);
    var link = linkParent.getElementsByTagName("A");
    deletedLinks.push(link[0]);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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

function validateURL(url) {
    var url_whitelist = [
            "https://www.youtube.com/.*",
            "http://www.youtube.com/.*",
            "www.youtube.com/.*",
            "youtube.com/.*",
            "https://soundcloud.com/.*",
            "http://soundcloud.com/.*",
            "https://www.soundcloud.com/.*",
            "http://www.soundcloud.com/.*",
            "www.soundcloud.com/.*",
            "soundcloud.com/.*",
            "https://www.spotify.com/.*",
            "https://www.spotify.com/.*",
            "www.spotify.com/.*",
            "spotify.com/.*",
            "http://www.apple.com/music/.*",
            "https://www.apple.com/music/.*",
            "www.apple.com/music/.*",
            "apple.com/music/.*",
            "https://twitter.com/.*",
            "http://twitter.com/.*",
            "https://www.twitter.com/.*",
            "http://www.twitter.com/.*",
            "www.twitter.com/.*",
            "twitter.com/.*",
            "https://www.facebook.com/.*",
            "http://www.facebook.com/.*",
            "https://facebook.com/.*",
            "https://facebook.com/.*",
            "www.facebook.com/.*",
            "facebook.com/.*",
            "https://www.pinterest.com/.*",
            "http://www.pinterest.com/.*",
            "https://pinterest.com/.*",
            "http://pinterest.com/.*",
            "www.pinterest.com/.*",
            "pinterest.com/.*",
            "https://www.tumblr.com/.*",
            "https://www.tumblr.com/.*",
            "https://tumblr.com/.*",
            "http://tumblr.com/.*",
            "www.tumblr.com/.*",
            "tumblr.com/.*",
            "https://www.instagram.com/.*",
            "http://www.instagram.com/.*",
            "https://instagram.com/.*",
            "http://instagram.com/.*",
            "www.instagram.com/.*",
            "instagram.com/.*",
    ]
    var regex = new RegExp(url_whitelist.join("|"), "i");
    return(url.match(regex) != null);
}
