window.addEventListener("load", function() {
    var cookieBanner = document.getElementById("cookie-container");

    function handleClick(consent) {
        cookieBanner.classList.remove("active");
        localStorage.setItem("cookie_consent", consent);
    }

    document.querySelector("button#confirm")
            .addEventListener("click", handleClick.bind(null, true));

    document.querySelector("button#deny")
            .addEventListener("click", handleClick.bind(null, false));

    if (!localStorage.getItem("cookie_consent")) {
        setTimeout(function() {
            cookieBanner.classList.add("active");
        }, 1000);
    }
});
