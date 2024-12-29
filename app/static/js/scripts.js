// app/static/js/scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const themeLinks = document.querySelectorAll('[data-theme]');
    const currentTheme = localStorage.getItem('theme') || 'light-mode';
    setTheme(currentTheme);

    themeLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const selectedTheme = link.getAttribute('data-theme');
            setTheme(selectedTheme);
            localStorage.setItem('theme', selectedTheme);
        });
    });

    function setTheme(theme) {
        const body = document.body;
        // Remove existing theme classes
        body.classList.remove('light-mode', 'dark-mode', 'contrast-mode');
        // Add the selected theme class
        body.classList.add(theme);
    }
});