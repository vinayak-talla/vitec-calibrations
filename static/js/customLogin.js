// JavaScript to toggle password visibility with text
document.addEventListener('DOMContentLoaded', function () {
    // Check if the togglePasswordText element exists before adding an event listener
    const togglePasswordText = document.getElementById('togglePasswordText');
    if (togglePasswordText) {
        togglePasswordText.addEventListener('click', function () {
            const passwordField = document.getElementById('password');
            
            if (passwordField) {
                if (passwordField.type === 'password') {
                    passwordField.type = 'text';  // Show password
                    togglePasswordText.textContent = 'Hide';  // Change text to 'Hide'
                } else {
                    passwordField.type = 'password';  // Hide password
                    togglePasswordText.textContent = 'Show';  // Change text to 'Show'
                }
            }
        });
    }
});
