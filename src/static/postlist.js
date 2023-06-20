function changeSort() {
    var selectElement = document.querySelector("#postlist select[name=order]");
    for (var i = 0; i < this.children.length; i++) {
        this.children[i].classList.toggle("hidden");
    }
    selectElement.value = selectElement.value === "desc" ? "asc" : "desc";
}

// Sync text values between post tag pills and tag select select
// and trigger the submit event from the form to HTMX
function changeTag() {
    document.querySelector("#postlist select[name=tag]").value = this.textContent;
    htmx.trigger("#postlist-header form", "submit");
    handleTagChange();
}

// When the tag selection option is set to `All` (or an empty value)
// the `tag` parameter is excluded from the request made by HTMX
function handleTagChange() {
    var formElement = document.querySelector("#postlist-header form");
    var tagSelectElement = formElement.querySelector("select[name=tag]")
    formElement.setAttribute("hx-params", tagSelectElement.value === ""  ? "not tag" : "*");
}
