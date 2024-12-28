// app/static/js/scripts.js

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Theme Dropdown Functionality
    const themeDropdownItems = document.querySelectorAll('[data-theme]');
    const currentTheme = localStorage.getItem('theme') || 'light';
    applyTheme(currentTheme);

    themeDropdownItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const selectedTheme = item.getAttribute('data-theme');
            applyTheme(selectedTheme);
            localStorage.setItem('theme', selectedTheme);
        });
    });

    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode', 'contrast-mode');
        } else if (theme === 'contrast') {
            document.body.classList.add('contrast-mode');
            document.body.classList.remove('light-mode', 'dark-mode');
        } else {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode', 'contrast-mode');
        }
    }
});