document.addEventListener('DOMContentLoaded', function () {

    const forms = document.querySelectorAll('form[id^="valuesForm"]'); // Select all modals' forms

    forms.forEach(form => {
        const instrumentId = form.getAttribute('action').split('/')[3]; // Assuming instrument ID is in the URL
        const instrumentType = document.getElementById(`instrument_type${instrumentId}`).textContent.trim();

        form.addEventListener('submit', function (event) {
            event.preventDefault();

            // Run the specific handler if it exists
            if (instrumentType in instrumentHandlers) {
                instrumentHandlers[instrumentType](form,instrumentId); // Call the handler with the form
            }
            // Submit the form via modalSubmission
            modalSubmission(form, instrumentId);
        });

        if (instrumentType === "RPM") {

            const toggleRPM = document.getElementById(`toggleRpmButton${instrumentId}`)
            toggleRPM.addEventListener('click', function (event) {
                event.preventDefault();
                const rpmCountInput = document.getElementById(`rpmCountInput${instrumentId}`);
                const isInputVisible = rpmCountInput.style.display === 'block';

                if (isInputVisible) {
                    // Get the number entered
                    const fieldCount = parseInt(rpmCountInput.value, 10);
            
                    if (!isNaN(fieldCount) && fieldCount >= 0) {
                        const rpmTestFields = document.getElementById(`rpmTestFields${instrumentId}`);
                        const rpmActualFields = document.getElementById(`rpmActualFields${instrumentId}`);

                        // Preserve existing data
                        const existingRpmTestData = Array.from(rpmTestFields.querySelectorAll('input')).map(input => input.value);
                        const existingRpmActualData = Array.from(rpmActualFields.querySelectorAll('input')).map(input => input.value);

                        // Clear the container before adding new fields
                        rpmTestFields.innerHTML = '';
                        rpmActualFields.innerHTML = '';

                        // Generate the specified number of input fields
                        for (let i = 0; i < fieldCount; i++) {
                            const testInputField = document.createElement('input');
                            testInputField.type = 'text';
                            testInputField.className = 'form-control custom-input rpm-custom-size me-3 rpm-test-fields';
                            if (i < existingRpmTestData.length) {
                                testInputField.value = existingRpmTestData[i]; // Restore previous data
                            }
                            rpmTestFields.appendChild(testInputField);
                            

                            const actualInputField = document.createElement('input');
                            actualInputField.type = 'text';
                            actualInputField.className = 'form-control custom-input rpm-custom-size me-3 rpm-actual-fields';
                            if (i < existingRpmActualData.length) {
                                actualInputField.value = existingRpmActualData[i]; // Restore previous data
                            }
                            rpmActualFields.appendChild(actualInputField);
                        }
                    }
                    // Hide the input field after processing
                    rpmCountInput.style.display = 'none';
                    rpmCountInput.value = '';


                }
                else {
                    rpmCountInput.style.display = 'block';
                    rpmCountInput.focus();
                }

            });

        }

    });



});

const instrumentHandlers = {
    RPM: (form,instrumentId) => consolidateRPM(form,instrumentId), // Pass the form parameter
};
// Handle paste event (typically triggered by QR scanner)
function handlePaste(event) {
    setTimeout(() => {
        let inputField = document.getElementById('instrument-input');
        if (inputField.value.trim() !== "") {
            document.getElementById('id-form').submit();
        }
    }, 0);  // Wait for the paste event to populate the input field
}

// Allow manual submission when Enter is pressed
function submitOnEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevent default form submission behavior
        document.getElementById('id-form').submit();
    }
}

function consolidateRPM(form, instrumentId) {
    const rpmTestFields = document.getElementById(`rpmTestFields${instrumentId}`);
    const rpmActualFields = document.getElementById(`rpmActualFields${instrumentId}`);

    var rpmTest = Array.from(rpmTestFields.querySelectorAll('input')).map(input => input.value.trim()).filter(value => value !== '');
    var rpmActual = Array.from(rpmActualFields.querySelectorAll('input')).map(input => input.value.trim()).filter(value => value !== '');

    const rpmTestInput = document.createElement('input');
    rpmTestInput.type = 'hidden';
    rpmTestInput.name = 'rpm_test';
    rpmTestInput.id = 'rpm_test';
    rpmTestInput.value = rpmTest;
    form.appendChild(rpmTestInput);

    const rpmActualInput = document.createElement('input');
    rpmActualInput.type = 'hidden';
    rpmActualInput.name = 'rpm_actual';
    rpmActualInput.name = 'rpm_actual';
    rpmActualInput.value = rpmActual;
    form.appendChild(rpmActualInput);

}

function modalSubmission(form, instrumentId) {
    // Get the form data
    const formData = new FormData(form);

    const url = form.getAttribute('action');

    // Send the data using AJAX
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            $('#valuesModal').modal('hide'); // Assuming you're using Bootstrap modal
            // Optionally, you can reload the instrument list here or update the specific row.
            location.reload(); // Refresh the page to reflect the updated values
        } else {
            // If there were errors, display them below the input fields
            const errorContainer = document.getElementById(`formErrors${instrumentId}`);
            errorContainer.classList.add('border-top');
            errorContainer.style.display = 'block';
            errorContainer.innerHTML = '';
            for (let [field, errors] of Object.entries(data.errors)) {
                field = formatErrorTitle(field)
                const labelDiv = document.createElement('div');
                labelDiv.classList.add('custom-form-label', 'mt-3');
                labelDiv.textContent = `${field} Errors:`;
                errorContainer.appendChild(labelDiv);
                errors.forEach(error => {
                    const errorDiv = document.createElement('div');
                    errorDiv.classList.add('text-danger');
                    errorDiv.textContent = `${error}`; // Include field name for context
                    errorContainer.appendChild(errorDiv);
                });
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

}

function formatErrorTitle(inputString) {
    if (!inputString) {
      return ""; // Handle null or undefined input
    }
  
    const words = inputString.split("_");
    const formattedWords = words.map(word => {
      if (word.length === 0) {
          return "";
      }
      return word.charAt(0).toUpperCase() + word.slice(1);
    });
    return formattedWords.join(" ");
}
