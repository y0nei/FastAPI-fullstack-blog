function changeSort() {
    var selectElement = document.querySelector("#postlist select[name=order]");
    for (var i = 0; i < this.children.length; i++) {
        this.children[i].classList.toggle("hidden");
    }
    selectElement.value = selectElement.value === "desc" ? "asc" : "desc";
}

// When the tag selection option is set to `All` (or an empty value)
// the `tag` parameter is excluded from the request made by HTMX
function handleTagChange() {
    var formElement = document.querySelector("#postlist-header form");
    formElement.setAttribute('hx-params', this.value === "" ? "not tag" : "*");
}
