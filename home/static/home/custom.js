document.addEventListener("DOMContentLoaded", function () {

    // Filter buttons on the Opportunities page (All / Jobs / Vacancies / Attachments)
    const filterButtons = document.querySelectorAll(".filter-btn");
    const items = document.querySelectorAll(".opp-item");

    function applyFilter(filter) {
        filterButtons.forEach(function (b) {
            b.classList.toggle("active", b.dataset.filter === filter);
        });
        items.forEach(function (item) {
            const show = filter === "all" || item.dataset.category === filter;
            item.style.display = show ? "block" : "none";
        });
    }

    filterButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            applyFilter(btn.dataset.filter);
        });
    });

    // Open with a filter, e.g. /opportunities/?filter=job
    if (filterButtons.length) {
        const wanted = new URLSearchParams(window.location.search).get("filter");
        if (wanted) {
            applyFilter(wanted);
        }
    }
});