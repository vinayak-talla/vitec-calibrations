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
        var microscopeFields = document.getElementById('microscope-fields');
        var timerFields = document.getElementById('timer-fields');
        var thermoRPMFields = document.getElementById('thermoRPM-fields');
        var balanceFields = document.getElementById('balance-fields');
        var pHMeterFields = document.getElementById('pH-meter-fields');
        var airflowFields = document.getElementById('airflow-fields');
        var refrigerationFields = document.getElementById('refrigeration-fields');

        console.log(instrumentType)
        // Toggle child form display
        if (instrumentType === 'Pipette') {
            pipetteFields.style.display = 'block';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        } else if (instrumentType === 'RPM') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'block';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        } else if (instrumentType === 'Temperature') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'block';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        } else if (instrumentType === 'Microscope') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'block'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        }else if (instrumentType === 'Timer') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'block'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        }else if (instrumentType === 'ThermoRPM') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'block'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        }else if (instrumentType === 'Balance') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'block'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        }else if (instrumentType === 'pH Meter') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'block'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
        }else if (instrumentType === 'Airflow') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'block'
            refrigerationFields.style.display = 'none'
        }else if (instrumentType === 'Refrigeration') {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'block'
        } else {
            pipetteFields.style.display = 'none';
            rpmFields.style.display = 'none';
            temperatureFields.style.display = 'none';
            microscopeFields.style.display = 'none'
            timerFields.style.display = 'none'
            thermoRPMFields.style.display = 'none'
            balanceFields.style.display = 'none'
            pHMeterFields.style.display = 'none'
            airflowFields.style.display = 'none'
            refrigerationFields.style.display = 'none'
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

    if(document.getElementById('airflowTypeSelect').getAttribute('data-airflow-type') != "None") {
        togglePCRAirflowFields() 
    }

    $(document.getElementById('airflowTypeSelect')).on('changed.bs.select', function () {
        togglePCRAirflowFields()
    });

    function togglePCRAirflowFields() {
        // Get the selected instrument type from the clicked dropdown item
        const airflowType = document.getElementById('airflowTypeSelect').value;
        
        // Get references to the fields that should be shown or hidden based on selection
        var pcrFields = document.getElementById('pcr-fields');

        // Toggle child form display
        if (airflowType === 'PCR Work Station') {
            pcrFields.style.display = 'block';
        } else {
            pcrFields.style.display = 'none';
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

    const rpmTimerTestFields = document.getElementById('rpmTimerTestFields');
    const rpmTimerActualFields = document.getElementById('rpmTimerActualFields');

    const timerTestFields = document.getElementById('timerTestFields');
    const timerActualFields = document.getElementById('timerActualFields');

    const temperatureTestFields = document.getElementById('temperatureTestFields');
    const temperatureActualFields = document.getElementById('temperatureActualFields');

    const thermoRPMTimerTestFields = document.getElementById('thermoRPMTimerTestFields');
    const thermoRPMTimerActualFields = document.getElementById('thermoRPMTimerActualFields');

    const thermoRPMTestFields = document.getElementById('thermoRPMTestFields');
    const thermoRPMActualFields = document.getElementById('thermoRPMActualFields');

    const thermoRPMTemperatureTestFields = document.getElementById('thermoRPMTemperatureTestFields');
    const thermoRPMTemperatureActualFields = document.getElementById('thermoRPMTemperatureActualFields');

    const weightTestFields = document.getElementById('weightTestFields');
    const weightActualFields = document.getElementById('weightActualFields');

    const downflowFields = document.getElementById('downflowFields');
    const inflowFields = document.getElementById('inflowFields');

    const pcrAirflowFields = document.getElementById('pcrAirflowFields');
    const particleSizeFields = document.getElementById('particleSizeFields');




    document.getElementById('toggleRpmButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([rpmTestFields, rpmActualFields], document.getElementById('rpmCountInput'))
  
    });

    document.getElementById('toggleRPMTimerButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([rpmTimerTestFields, rpmTimerActualFields], document.getElementById('rpmTimerCountInput'))
  
    });

    document.getElementById('toggleTimerButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([timerTestFields, timerActualFields], document.getElementById('timerCountInput'))
  
    });

    document.getElementById('toggleTemperatureButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([temperatureTestFields, temperatureActualFields], document.getElementById('temperatureCountInput'))
  
    });
    

    document.getElementById('toggleThermoRpmButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([thermoRPMTestFields, thermoRPMActualFields], document.getElementById('thermoRPMCountInput'))
  
    });

    document.getElementById('toggleThermoRPMTemperatureButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([thermoRPMTemperatureTestFields, thermoRPMTemperatureActualFields], document.getElementById('thermoRPMTemperatureCountInput'))
  
    });

    document.getElementById('togglethermoRPMTimerButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([thermoRPMTimerTestFields, thermoRPMTimerActualFields], document.getElementById('thermoRPMTimerCountInput'))
  
    });

    document.getElementById('toggleWeightButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([weightTestFields, weightActualFields], document.getElementById('weightCountInput'))
  
    });

    document.getElementById('toggleDownflowButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([downflowFields], document.getElementById('downflowCountInput'))
  
    });

    document.getElementById('toggleInflowButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([inflowFields], document.getElementById('inflowCountInput'))
  
    });

    document.getElementById('togglePCRAirflowButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([pcrAirflowFields], document.getElementById('pcrAirflowCountInput'))
  
    });

    document.getElementById('toggleParticleSizeButton').addEventListener('click', function (event) {
        event.preventDefault();
        toggleArrayFieldBtn([particleSizeFields], document.getElementById('particleSizeCountInput'))
  
    });

    
    



    // Combine the rpm fields into one field before submitting
    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {

        const instrumentType = document.getElementById('instrumentTypeSelect').value;

        if(instrumentType === "RPM") {
            consolidateArrayFields(form, rpmTestFields,'rpm_test')
            consolidateArrayFields(form, rpmActualFields,'rpm_actual')

            consolidateArrayFields(form, rpmTimerTestFields, 'timer_test')
            consolidateArrayFields(form, rpmTimerActualFields, 'timer_actual')
        } else if(instrumentType === "Timer") {
            consolidateArrayFields(form, timerTestFields, 'timer_test')
            consolidateArrayFields(form, timerActualFields, 'timer_actual')
        } else if(instrumentType === "Temperature") {
            consolidateArrayFields(form, temperatureTestFields, 'temperature_test')
            consolidateArrayFields(form, temperatureActualFields, 'temperature_actual')
        } else if(instrumentType === "ThermoRPM") {
            consolidateArrayFields(form, thermoRPMTestFields,'rpm_test')
            consolidateArrayFields(form, thermoRPMActualFields,'rpm_actual')
            consolidateArrayFields(form, thermoRPMTemperatureTestFields, 'temperature_test')
            consolidateArrayFields(form, thermoRPMTemperatureActualFields, 'temperature_actual')
            consolidateArrayFields(form, thermoRPMTimerTestFields, 'timer_test')
            consolidateArrayFields(form, thermoRPMTimerActualFields, 'timer_actual')
        } else if(instrumentType === "Balance") {
            consolidateArrayFields(form, weightTestFields, 'weight_test')
            consolidateArrayFields(form, weightActualFields, 'weight_actual')
        }else if(instrumentType === "Airflow") {
            consolidateArrayFields(form, downflowFields, 'downflow')
            consolidateArrayFields(form, inflowFields, 'inflow')
            consolidateArrayFields(form, pcrAirflowFields, 'pcr_airflow')
            consolidateArrayFields(form, particleSizeFields, 'particle_size')
        }


        
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