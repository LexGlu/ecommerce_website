// get the phone input field
const phoneField = document.getElementById('phone');
const prefix = '+38 ';
const operatorCodes = [
  // Djuice (Astelit) - now merged with Kyivstar
  "039",
  // Vodafone Ukraine (MTC)
  "050",
  // Kyivstar (Golden Telecom)
  "063",
  // Kyivstar (Beeline Ukraine) - now merged with Kyivstar
  "066",
  // Kyivstar (Cosmos) - now merged with Kyivstar
  "067",
  // Kyivstar (Djuice) - now merged with Kyivstar
  "068",
  // Ukrtelecom CDMA
  "091",
  // PEOPLEnet (CDMA Ukraine)
  "092",
  // Vodafone Ukraine (Utel)
  "093",
  // Kyivstar (WellCom)
  "094",
  // Lifecell (Astelit)
  "095",
  // Beeline Ukraine - now merged with Kyivstar
  "096",
  // Kyivstar (Jeans) - now merged with Kyivstar
  "097",
  // Kyivstar (Parus) - now merged with Kyivstar
  "098",
  // Vodafone Ukraine (MTS)
  "099"
];


// add event listener for focus on the phone field
phoneField.addEventListener('focus', function () {
  // if the current value is not starting with the prefix
  if (!phoneField.value.startsWith(prefix)) {
    // set the initial value with the prefix
    phoneField.value = prefix;
  }
});

// allow only digits
phoneField.addEventListener("input", function() {
    let phoneValue = phoneField.value;
    phoneValue = prefix + phoneValue.substring(4, ).replace(/\D/g, '');
    phoneField.value = phoneValue;


    // apply formatting
    if (phoneValue.length > 7) {
    phoneValue = phoneValue.substring(0, 7) + ' ' + phoneValue.substring(7);
    }
    if (phoneValue.length > 11) {
    phoneValue = phoneValue.substring(0, 11) + ' ' + phoneValue.substring(11);
    }
    if (phoneValue.length > 14) {
    phoneValue = phoneValue.substring(0, 14) + ' ' + phoneValue.substring(14);
    }

    // truncate to 17 characters if necessary
    if (phoneValue.length > 17) {
    phoneValue = phoneValue.substring(0, 17);
    }

    phoneField.value = phoneValue;

    // validate the first three digits of the phone number against operator codes
    let code = phoneValue.substring(4, 7);
    const formSubmitElement = document.getElementById('signup');
    if (!operatorCodes.includes(code) && code.length === 3){
        document.getElementById('code_error_message').innerHTML = 'Code ' + code.toString() + ' is not a valid operator code';
        document.getElementById("code_error").classList.remove("hidden");
        formSubmitElement.disabled = true;
        formSubmitElement.style.backgroundColor = 'grey';
    } else {
        document.getElementById('code_error_message').innerHTML = '';
        document.getElementById("code_error").classList.add("hidden");
        formSubmitElement.disabled = false;
        formSubmitElement.style.backgroundColor = '#6dabe4';
    }

})

// add event listener to change phone number format on submit
document.getElementById('register-form').addEventListener('submit', function (e) {
    // remove spaces
    phoneField.value = phoneField.value.replace(/\s/g, '');
});