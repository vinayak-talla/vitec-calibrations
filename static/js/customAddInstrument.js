document.addEventListener('DOMContentLoaded', function () {

    if(document.getElementById('instrumentTypeSelect').getAttribute('data-instrument-type') != "None") {
        toggleFields() 
    }

    $(document.getElementById('instrumentTypeSelect')).on('changed.bs.select', function () {
        toggleFields()
    });
    console.log(document.getElementById('instrumentTypeSelect').value)

    function toggleFields() {
        // Get the selected instrument type from the clicked dropdown item
        const instrumentType = document.getElementById('instrumentTypeSelect').value;

        // Get references to the fields that should be shown or hidden based on selection
        var pipetteFields = document.getElementById('pipette-fields');
        var rpmFields = document.getElementById('rpm-fields');
        var temperatureFields = document.getElementById('temperature-fields');
        console.log(instrumentType)
        // Toggle child form display
        if (instrumentType === 'Pipette') {
            pipetteFields.style.display = 'block';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
        } else if (instrumentType === 'RPM') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'block';
            temperatureFields.style.display = 'none';
        } else if (instrumentType === 'Temperature') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'block';
        } else {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
        }
    }

    if(document.getElementById('temperatureTypeSelect').getAttribute('data-temperature-type') != "None") {
        toggleTempFields() 
    }

    $(document.getElementById('temperatureTypeSelect')).on('changed.bs.select', function () {
        toggleTempFields()
    });

    function toggleTempFields() {
        // Get the selected instrument type from the clicked dropdown item
        const temperatureType = document.getElementById('temperatureTypeSelect').value;
        
        // Get references to the fields that should be shown or hidden based on selection
        var humidityFields = document.getElementById('humidity-fields');

        // Toggle child form display
        if (temperatureType === 'DTH') {
            humidityFields.style.display = 'block';
        } else {
            humidityFields.style.display = 'none';
        }
       
    }

    document.querySelectorAll('.dropdown-container').forEach(container => {
        const dropdownKey = container.dataset.dropdownKey;
        const addButton = container.querySelector('.add-option-btn');
        const inputField = container.querySelector('.new-option-input');
        const selectElement = container.querySelector('select');
        const addDropdownOptionURL = document.getElementById('urls').getAttribute('data-add-dropdown-option-url');
        const csrfToken = document.getElementById('urls').getAttribute('data-csrf');

        addButton.addEventListener('click', function (event) {
            event.preventDefault();
            const isInputVisible = inputField.style.display === 'block';

            if (isInputVisible) {
                const newOption = inputField.value.trim();

                if (newOption) {
                    fetch(addDropdownOptionURL, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-CSRFToken": csrfToken
                        },
                        body: `dropdown_key=${encodeURIComponent(dropdownKey)}&new_option=${encodeURIComponent(newOption)}`
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                const option = document.createElement('option');
                                option.value = newOption;
                                option.textContent = newOption;
                                selectElement.appendChild(option);
                                option.selected = true;
                                $(selectElement).selectpicker('refresh');

                                inputField.style.display = 'none';
                                inputField.value = '';

                            }
                            else {
                                inputField.style.display = 'none';
                                inputField.value = '';
                            } 
                        })
                        .catch(error => {
                            console.error("Error:", error);
                        });
                }
                else {
                    inputField.style.display = 'none';
                } 
            } else {
                inputField.style.display = 'block';
                inputField.focus();
            }
        });
    });

    

    const rpmTestFields = document.getElementById('rpmTestFields');
    const rpmActualFields = document.getElementById('rpmActualFields');

    const timerTestFields = document.getElementById('timerTestFields');
    const timerActualFields = document.getElementById('timerActualFields');

    document.getElementById('toggleRpmButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([rpmTestFields, rpmActualFields], document.getElementById('rpmCountInput'))
  
    });

    document.getElementById('toggleTimerButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([timerTestFields, timerActualFields], document.getElementById('timerCountInput'))
  
    });



    // Combine the rpm fields into one field before submitting
    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {

        consolidateArrayFields(form, rpmTestFields,'rpm_test')
        consolidateArrayFields(form, rpmActualFields,'rpm_actual')

        consolidateArrayFields(form, timerTestFields, 'timer_test')
        consolidateArrayFields(form, timerActualFields, 'timer_actual')

    });



});


function consolidateArrayFields(form, field, name) {
    var array = Array.from(field.querySelectorAll('input')).map(input => input.value.trim()).filter(value => value !== '');

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.id = name;
    input.value = array;
    form.appendChild(input);

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