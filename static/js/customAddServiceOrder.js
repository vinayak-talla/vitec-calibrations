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
                const rpmTestFields = document.getElementById(`rpmTestFields${instrumentId}`);
                const rpmActualFields = document.getElementById(`rpmActualFields${instrumentId}`);
                toggleArrayFieldBtn([rpmTestFields, rpmActualFields], document.getElementById(`rpmCountInput${instrumentId}`))
               

            });

            const toggleTimer = document.getElementById(`toggleTimerButton${instrumentId}`)
            toggleTimer.addEventListener('click', function (event) {
                event.preventDefault();
                const timerTestFields = document.getElementById(`timerTestFields${instrumentId}`);
                const timerActualFields = document.getElementById(`timerActualFields${instrumentId}`);
                toggleArrayFieldBtn([timerTestFields, timerActualFields], document.getElementById(`timerCountInput${instrumentId}`))
               

            });

        }
        else if(instrumentType == "Temperature") {
            const toggleTemperature = document.getElementById(`toggleTemperatureButton${instrumentId}`)
            toggleTemperature.addEventListener('click', function (event) {
                event.preventDefault();
                const temperatureTestFields = document.getElementById(`temperatureTestFields${instrumentId}`);
                const temperatureActualFields = document.getElementById(`temperatureActualFields${instrumentId}`);
                toggleArrayFieldBtn([temperatureTestFields, temperatureActualFields], document.getElementById(`temperatureCountInput${instrumentId}`))
               

            });

        }
        else if (instrumentType === "Timer") {
            const toggleTimer = document.getElementById(`toggleTimerButton${instrumentId}`)
            toggleTimer.addEventListener('click', function (event) {
                event.preventDefault();
                const timerTestFields = document.getElementById(`timerTestFields${instrumentId}`);
                const timerActualFields = document.getElementById(`timerActualFields${instrumentId}`);
                toggleArrayFieldBtn([timerTestFields, timerActualFields], document.getElementById(`timerCountInput${instrumentId}`))
               

            });

        }
        else if (instrumentType === "ThermoRPM") {

            const toggleRPM = document.getElementById(`toggleRpmButton${instrumentId}`)
            toggleRPM.addEventListener('click', function (event) {
                event.preventDefault();
                const rpmTestFields = document.getElementById(`rpmTestFields${instrumentId}`);
                const rpmActualFields = document.getElementById(`rpmActualFields${instrumentId}`);
                toggleArrayFieldBtn([rpmTestFields, rpmActualFields], document.getElementById(`rpmCountInput${instrumentId}`))
               

            });
            const toggleTemperature = document.getElementById(`toggleTemperatureButton${instrumentId}`)
            toggleTemperature.addEventListener('click', function (event) {
                event.preventDefault();
                const temperatureTestFields = document.getElementById(`temperatureTestFields${instrumentId}`);
                const temperatureActualFields = document.getElementById(`temperatureActualFields${instrumentId}`);
                toggleArrayFieldBtn([temperatureTestFields, temperatureActualFields], document.getElementById(`temperatureCountInput${instrumentId}`))
               

            });
            const toggleTimer = document.getElementById(`toggleTimerButton${instrumentId}`)
            toggleTimer.addEventListener('click', function (event) {
                event.preventDefault();
                const timerTestFields = document.getElementById(`timerTestFields${instrumentId}`);
                const timerActualFields = document.getElementById(`timerActualFields${instrumentId}`);
                toggleArrayFieldBtn([timerTestFields, timerActualFields], document.getElementById(`timerCountInput${instrumentId}`))
               

            });

        }
        

    });

    const delForms = document.querySelectorAll('form[id^="delete-form"]'); // Select all modals' forms

    delForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            // Get the form data
            const formData = new FormData(form);

            const url = form.getAttribute('action');

            // Send the data using AJAX
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                location.reload(); 
            })
            .catch(error => {
                console.error('Error:', error);
            });


                    
        });

                
    });



});

const instrumentHandlers = {
    RPM: (form,instrumentId) => consolidateRPM(form,instrumentId), // Pass the form parameter
    Temperature: (form, instrumentId) => consolidateTemperature(form, instrumentId),
    Timer: (form, instrumentId) => consolidateTimer(form,instrumentId),
    ThermoRPM: (form, instrumentId) => consolidateThermoRPM(form, instrumentId)
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

    const timerTestFields = document.getElementById(`timerTestFields${instrumentId}`);
    const timerActualFields = document.getElementById(`timerActualFields${instrumentId}`);

    consolidateArrayFields(form, rpmTestFields,'rpm_test')
    consolidateArrayFields(form, rpmActualFields,'rpm_actual')

    consolidateArrayFields(form, timerTestFields, 'timer_test')
    consolidateArrayFields(form, timerActualFields, 'timer_actual')

}

function consolidateTemperature(form, instrumentId) {
    const temperatureTestFields = document.getElementById(`temperatureTestFields${instrumentId}`);
    const temperatureActualFields = document.getElementById(`temperatureActualFields${instrumentId}`);

    consolidateArrayFields(form, temperatureTestFields, 'temperature_test')
    consolidateArrayFields(form, temperatureActualFields, 'temperature_actual')
}

function consolidateTimer(form, instrumentId) {
    const timerTestFields = document.getElementById(`timerTestFields${instrumentId}`);
    const timerActualFields = document.getElementById(`timerActualFields${instrumentId}`);

    consolidateArrayFields(form, timerTestFields, 'timer_test')
    consolidateArrayFields(form, timerActualFields, 'timer_actual')


}

function consolidateThermoRPM(form, instrumentId) {
    const rpmTestFields = document.getElementById(`rpmTestFields${instrumentId}`);
    const rpmActualFields = document.getElementById(`rpmActualFields${instrumentId}`);

    const timerTestFields = document.getElementById(`timerTestFields${instrumentId}`);
    const timerActualFields = document.getElementById(`timerActualFields${instrumentId}`);

    const temperatureTestFields = document.getElementById(`temperatureTestFields${instrumentId}`);
    const temperatureActualFields = document.getElementById(`temperatureActualFields${instrumentId}`);

    consolidateArrayFields(form, temperatureTestFields, 'temperature_test')
    consolidateArrayFields(form, temperatureActualFields, 'temperature_actual')

    consolidateArrayFields(form, timerTestFields, 'timer_test')
    consolidateArrayFields(form, timerActualFields, 'timer_actual')

    consolidateArrayFields(form, rpmTestFields,'rpm_test')
    consolidateArrayFields(form, rpmActualFields,'rpm_actual')


}

function modalSubmission(form, instrumentId) {
    // Get the form data
    const formData = new FormData(form);

    const url = form.getAttribute('action');

    // Send the data using AJAX
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
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

function toggleArrayFieldBtn(fields, countInput) {
    const isInputVisible = countInput.style.display === 'block';

    if (isInputVisible) {
        // Get the number entered
        const fieldCount = parseInt(countInput.value, 10);

        if (!isNaN(fieldCount) && fieldCount >= 0) {
            fields.forEach( field => {
                // Preserve existing data
                const existingFieldData = Array.from(field.querySelectorAll('input')).map(input => input.value);

                // Clear the container before adding new fields
                field.innerHTML = '';

                // Generate the specified number of input fields
                for (let i = 0; i < fieldCount; i++) {
                    const testInputField = document.createElement('input');
                    testInputField.type = 'text';
                    testInputField.className = 'form-control custom-input rpm-custom-size me-3';
                    if (i < existingFieldData.length) {
                        testInputField.value = existingFieldData[i]; // Restore previous data
                    }
                    field.appendChild(testInputField);
                }
            });
        }
        // Hide the input field after processing
        countInput.style.display = 'none';
        countInput.value = '';


    }
    else {
        countInput.style.display = 'block';
        countInput.focus();
    }
}

function consolidateArrayFields(form, field, name) {
    var array = Array.from(field.querySelectorAll('input')).map(input => input.value.trim()).filter(value => value !== '');

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.id = name;
    input.value = array;
    form.appendChild(input);

}