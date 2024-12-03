document.addEventListener('DOMContentLoaded', function () {

    const clearButton = document.getElementById('clear-btn');
    if (clearButton) {
        clearButton.addEventListener('click', function (event) {
            event.preventDefault();  // Prevent form submission
            const searchInput = document.getElementById('search-input');
            searchInput.value = '';  // Clear the input field

            // Reload the page without the search parameter
            window.location.href = window.location.pathname;
        });
    }
});
