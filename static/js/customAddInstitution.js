// JavaScript to toggle password visibility with text
document.addEventListener('DOMContentLoaded', function () {
    const phoneParts = [
        document.getElementById('phone-part1'),
        document.getElementById('phone-part2'),
        document.getElementById('phone-part3')
    ];

    phoneParts.forEach((input, index) => {
        input.addEventListener('input', function () {
            // Automatically move to the next input when the field is filled
            if (input.value.length === input.maxLength) {
                if (index < phoneParts.length - 1) {
                    phoneParts[index + 1].focus();
                }
            }
            // Automatically move to the previous input when the field is emptied
            else if (input.value.length === 0 && index > 0) {
                phoneParts[index - 1].focus();
            }
        });
    });

    // Combine the phone number parts into one field before submitting
    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        const phoneNumber = phoneParts.map(input => input.value).join('');
        const phoneInput = document.createElement('input');
        phoneInput.type = 'hidden';
        phoneInput.name = 'phone_number';
        phoneInput.value = phoneNumber;
        form.appendChild(phoneInput);

    });

});
