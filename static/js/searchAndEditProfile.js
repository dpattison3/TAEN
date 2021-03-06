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
    if (window.innerWidth <= 768) {
        searchTextWidth = "125";
    } else if (window.innerWidth <= 992) {
        searchTextWidth = "150";
    } else {
        searchTextWidth = "200";
    }
    
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
    if (numberOfLinks >= 10) {
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

var url_whitelist = [
        "^.*(youtube\.com).*$",
        "^.*(soundcloud\.com).*$",
        "^.*(spotify\.com).*$",
        "^.*(apple\.com).*$",
        "^.*(twitter\.com).*$",
        "^.*(facebook\.com).*$",
        "^.*(pinterest\.com).*$",
        "^.*(tumblr\.com).*$",
        "^.*(tumblr\.com).*$",
        "^.*(instagram\.com).*$",
        "^.*(linkedin\.com).*$",
        "^.*(bandcamp\.com).*$"
]
var regex = new RegExp(url_whitelist.join("|"), "i");

function validateURL(url) {
    return (url.match(regex) != null);
}


$("#pictureInput").change(function(e) {
    for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {
        var file = e.originalEvent.srcElement.files[i];
        var img = document.getElementById("profileImage");
        var reader = new FileReader();
        reader.onloadend = function() {
            img.src = reader.result;
        }
        reader.readAsDataURL(file);
    }
});
