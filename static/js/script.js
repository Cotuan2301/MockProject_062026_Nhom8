document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggle-sidebar-btn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    // Automatically collapse the sidebar when opened on a mobile phone.
    if (window.innerWidth < 768) {
        document.body.classList.add('sidebar-collapsed');
    }
});
