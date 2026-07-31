(function () {
    var STORAGE_KEY = 'shotz_cookie_consent';
    var banner = document.getElementById('cookieConsentBanner');

    if (!banner) {
        return;
    }

    function getConsent() {
        try {
            return localStorage.getItem(STORAGE_KEY);
        } catch (error) {
            return null;
        }
    }

    function setConsent(value) {
        try {
            localStorage.setItem(STORAGE_KEY, value);
        } catch (error) {
            /* ignore storage failures */
        }
        document.documentElement.dataset.cookieConsent = value;
        banner.hidden = true;
        banner.classList.remove('is-visible');
    }

    function showBanner() {
        banner.hidden = false;
        requestAnimationFrame(function () {
            banner.classList.add('is-visible');
        });
    }

    var existingConsent = getConsent();
    if (existingConsent) {
        document.documentElement.dataset.cookieConsent = existingConsent;
    } else {
        showBanner();
    }

    var acceptBtn = banner.querySelector('.cookie-consent-accept');
    var declineBtn = banner.querySelector('.cookie-consent-decline');

    if (acceptBtn) {
        acceptBtn.addEventListener('click', function () {
            setConsent('accepted');
        });
    }

    if (declineBtn) {
        declineBtn.addEventListener('click', function () {
            setConsent('essential');
        });
    }
})();
