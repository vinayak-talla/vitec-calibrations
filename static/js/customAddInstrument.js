document.addEventListener('DOMContentLoaded', function () {


    if(document.getElementById('instrumentTypeSelect').getAttribute('data-instrument-type') != "None") {
        toggleFields() 
    }

    $(document.getElementById('instrumentTypeSelect')).on('changed.bs.select', function () {
        toggleFields()
    });

    function toggleFields() {
        // Get the selected instrument type from the clicked dropdown item
        const instrumentType = document.getElementById('instrumentTypeSelect').value;

        // Get references to the fields that should be shown or hidden based on selection
        var pipetteFields = document.getElementById('pipette-fields');
        var rpmFields = document.getElementById('rpm-fields');
        var temperatureFields = document.getElementById('temperature-fields');
        
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

    if(document.getElementById('rpmTypeSelect').getAttribute('data-temperature-type') != "None") {
        toggleTempFields() 
    }

    $(document.getElementById('rpmTypeSelect')).on('changed.bs.select', function () {
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

    document.getElementById('toggleRpmButton').addEventListener('click', function (event) {
        event.preventDefault();
        const rpmCountInput = document.getElementById('rpmCountInput');
        const isInputVisible = rpmCountInput.style.display === 'block';

        if (isInputVisible) {
            // Get the number entered
            const fieldCount = parseInt(rpmCountInput.value, 10);
            
            // Clear the container before adding new fields
            rpmTestFields.innerHTML = '';
            rpmActualFields.innerHTML = '';

            if (!isNaN(fieldCount) && fieldCount > 0) {
                // Generate the specified number of input fields
                for (let i = 0; i < fieldCount; i++) {
                    const testInputField = document.createElement('input');
                    testInputField.type = 'text';
                    testInputField.className = 'form-control custom-input rpm-custom-size me-3 rpm-test-fields';
                    rpmTestFields.appendChild(testInputField);

                    const actualInputField = document.createElement('input');
                    actualInputField.type = 'text';
                    actualInputField.className = 'form-control custom-input rpm-custom-size me-3 rpm-actual-fields';
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



    // Combine the rpm fields into one field before submitting
    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {

        if (rpmTestFields.children.length === 0) {
            var rpmTest = '';
            var rpmActual = '';
        }
        else {
            var rpmTest = Array.from(rpmTestFields.querySelectorAll('input')).map(input => input.value.trim()).filter(value => value !== '').join(';');
            var rpmActual = Array.from(rpmActualFields.querySelectorAll('input')).map(input => input.value.trim()).filter(value => value !== '').join(';');
        }

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


    });



});
