window.onload = function() {
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
