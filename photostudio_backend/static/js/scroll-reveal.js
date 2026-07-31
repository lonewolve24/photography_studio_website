(function () {
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function markVisible(elements) {
        elements.forEach(function (el) {
            el.classList.add('is-visible');
        });
    }

    function setupStaggerContainers() {
        document.querySelectorAll('.scroll-reveal-stagger').forEach(function (container) {
            var children = container.children;
            for (var i = 0; i < children.length; i++) {
                var child = children[i];
                if (!child.classList.contains('scroll-reveal')) {
                    child.classList.add('scroll-reveal');
                }
                child.style.setProperty('--reveal-delay', (i * 100) + 'ms');
            }
        });
    }

    function setupDelays() {
        document.querySelectorAll('[data-reveal-delay]').forEach(function (el) {
            el.style.setProperty('--reveal-delay', el.getAttribute('data-reveal-delay') + 'ms');
        });
    }

    setupStaggerContainers();
    setupDelays();

    var revealElements = document.querySelectorAll('.scroll-reveal');

    if (!revealElements.length) {
        return;
    }

    if (reducedMotion) {
        markVisible(revealElements);
        return;
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -30px 0px'
    });

    revealElements.forEach(function (el) {
        observer.observe(el);
    });
})();
