window.onload = onloadFunction;

var numberOfLinks;
var portfolio;
var linkForms;
var deletedLinks;

function onloadFunction() {
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
        updateProfile();
        //document.getElementById("editProfile").submit();
    });

    document.getElementById("addToPortfolio").onclick = addToPortfolio;
}

function updateProfile() {
    var forms = linkForms.children;
    var linksToSubmit = [];
    var validated = true;
    for (var i = 0; i < forms.length; ++i) {
        var linkTxt = forms[i].elements.link.value;
        if ((linkTxt.length == 0) || (validateURL(linkTxt))) {
            if (linkTxt.length != 0) {
                linksToSubmit.push(linkTxt);
            }
        } else {
            alert("bad!");
            validated = false;
        }
    }
    if (validated) {
        submitForm(linksToSubmit);
    }
}

function submitForm(linksToSubmit) {
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
                newLinks : linksToSubmit
        },

        success: function () {
            alert("Saved!");
        },

        error : function(xhr,errmsg,err) {
            alert(errmsg);
        }
    });
}

function addToPortfolio() {
    if (numberOfLinks <= 5) {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", ".");

        var link = document.createElement("input");
        link.setAttribute('type', "text");
        link.setAttribute('name', "link");
        link.setAttribute("placeholder", "link url");

        var deleteButton = document.createElement("span");
        deleteButton.className += " glyphicon glyphicon-remove-sign remove-portfolio-link";
        deleteButton.setAttribute("role", "button");
        deleteButton.onclick = function(obj) {
            obj.target.parentElement.parentElement.removeChild(obj.target.parentElement);
            --numberOfLinks;
        }

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

function validateURL(url) {
    if ((url.length > 23) && (url.substring(0, 24).valueOf() === "https://www.youtube.com/")) {
        return true;
    } else if ((url.length > 22)
            && (url.substring(0, 23).valueOf() === "http://www.youtube.com/")) {
        return true;
    } else if ((url.length > 15) && (url.substring(0, 15).valueOf() === "www.youtube.com/")) {
        return true;
    } else if ((url.length > 11) && (url.substring(0, 11).valueOf() === "youtube.com/")) {
        return true;
    }
    return false;
}
