document.addEventListener("DOMContentLoaded", function () {

    const header = document.querySelector("header");
    const links = document.querySelectorAll(".nav-links a");

    // 1. Shadow on the header when scrolling
    window.addEventListener("scroll", function () {
        header.classList.toggle("scrolled", window.scrollY > 20);
    });

    // 2. Highlight the menu link of the page you are on
    links.forEach(function (link) {
        link.classList.toggle("active", link.pathname === window.location.pathname);
    });

    // 3. Filter buttons on the Opportunities page (All / Jobs / Vacancies / Attachments)
    const filterButtons = document.querySelectorAll(".filter-btn");
    const items = document.querySelectorAll(".opp-item");

    function applyFilter(filter) {
        // make the clicked button look active
        filterButtons.forEach(function (b) {
            b.classList.toggle("active", b.dataset.filter === filter);
        });
        // show only the cards of that category
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

    // Open with a filter from the homepage, e.g. /opportunities/?filter=job
    if (filterButtons.length) {
        const wanted = new URLSearchParams(window.location.search).get("filter");
        if (wanted) {
            applyFilter(wanted);
        }
    }

    // 4. Animated counters on the homepage
    const counters = document.querySelectorAll(".counter");

    function runCounter(el) {
        const target = +el.dataset.target;
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 60));
        const timer = setInterval(function () {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current.toLocaleString();
        }, 25);
    }

    // 5. Fade-in on scroll (the Opportunities cards are left out so the filter never hides them)
    const revealItems = document.querySelectorAll(
        ".offer-card, .step-card, .quote-card, .cta-banner .container"
    );
    revealItems.forEach(function (el) { el.classList.add("reveal"); });

    const observer = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            if (entry.target.classList.contains("counter")) {
                runCounter(entry.target);
            } else {
                entry.target.classList.add("show");
            }
            obs.unobserve(entry.target);
        });
    }, { threshold: 0.15 });

    counters.forEach(function (c) { observer.observe(c); });
    revealItems.forEach(function (el) { observer.observe(el); });

});