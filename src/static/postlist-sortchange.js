function changeSort() {
    var selectElement = document.querySelector("#postlist select[name=order]");
    for (var i = 0; i < this.children.length; i++) {
        this.children[i].classList.toggle("hidden");
    }
    selectElement.value = selectElement.value === "desc" ? "asc" : "desc";
}
