document.addEventListener("DOMContentLoaded", function () {

    const header = document.querySelector("header");
    const links = document.querySelectorAll(".nav-links a");

    // 1. Shadow on the header when scrolling
    window.addEventListener("scroll", function () {
        header.classList.toggle("scrolled", window.scrollY > 20);
    });

    // 2. Highlight the menu link of the page you are on
    let currentPage = window.location.pathname.split("/").pop();
    if (currentPage === "") {
        currentPage = "index.html";
    }
    links.forEach(function (link) {
        link.classList.toggle("active", link.getAttribute("href") === currentPage);
    });

    // 3. Filter opportunities (only runs on opportunities.html)
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

    if (filterButtons.length) {
        const wanted = new URLSearchParams(window.location.search).get("filter");
        if (wanted) {
            applyFilter(wanted);
        }
    }
    // 4. Animated counters
    const counters = document.querySelectorAll(".counter");

    function runCounter(el) {
        const target = +el.dataset.target;
        let current = 0;
        const step = Math.ceil(target / 60);
        const timer = setInterval(function () {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current.toLocaleString();
        }, 25);
    }

    // 5. Fade-in on scroll
    const revealItems = document.querySelectorAll(
        ".offer-card, .step-card, .quote-card, .opp-card, .cta-banner .container"
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
        // 4. Animated counters
    const counters = document.querySelectorAll(".counter");

    function runCounter(el) {
        const target = +el.dataset.target;
        let current = 0;
        const step = Math.ceil(target / 60);
        const timer = setInterval(function () {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current.toLocaleString();
        }, 25);
    }

    // 5. Fade-in on scroll
    const revealItems = document.querySelectorAll(
        ".offer-card, .step-card, .quote-card, .opp-card, .cta-banner .container"
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