document.addEventListener("DOMContentLoaded", function () {

    // Shadow on the navbar when scrolling
    const nav = document.querySelector(".site-nav");
    window.addEventListener("scroll", function () {
        if (nav) nav.classList.toggle("scrolled", window.scrollY > 20);
    });

    // Count up from 0 to the real number
    function runCounter(el) {
        const target = parseInt(el.dataset.target, 10) || 0;
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 50));
        el.textContent = "0";
        const timer = setInterval(function () {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current.toLocaleString();
        }, 30);
    }
       // Back-to-top button: appears after scrolling down, scrolls smoothly to the top
    const backToTop = document.getElementById("backToTop");
    if (backToTop) {
        window.addEventListener("scroll", function () {
            backToTop.classList.toggle("show", window.scrollY > 300);
        });
        backToTop.addEventListener("click", function (event) {
            event.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
    // Fade elements in as they scroll into view
    if (!("IntersectionObserver" in window)) {
        document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("show"); });
        return;
    }

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            if (entry.target.classList.contains("counter")) {
                runCounter(entry.target);
            } else {
                entry.target.classList.add("show");
            }
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.15 });

    document.querySelectorAll(".reveal, .counter").forEach(function (el) { observer.observe(el); });
});