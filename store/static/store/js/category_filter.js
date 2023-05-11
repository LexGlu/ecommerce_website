document.addEventListener('DOMContentLoaded', function () {
  let filterForm = document.getElementById('filter-form');
  let sortSelect = document.getElementById('sort-select');
  let brandCheckboxes = document.querySelectorAll('input[name="brand"]');
  let minPriceInput = document.querySelector('input[name="min_price"]');
  let maxPriceInput = document.querySelector('input[name="max_price"]');
  let urlParams = new URLSearchParams(window.location.search);
  let dropdownMenuOpened = window.localStorage.getItem('dropdownMenuOpened');
  

  function toggleDropdownMenu() {
    let filterDropdown = document.getElementById('filter-dropdown');
    let dropdownMenu = document.getElementById('dropdown-menu');
    if (dropdownMenuOpened === 'true') {
      filterDropdown.classList.add('show');
      filterDropdown.attributes['aria-expanded'].value = 'true';
      dropdownMenu.classList.add('show');
      localStorage.removeItem('dropdownMenuOpened');
    } else {
      dropdownMenu.classList.remove('show');
    }
  }

  toggleDropdownMenu();

  // Initialize brand checkboxes
  brandCheckboxes.forEach(function (checkbox) {
    let brandValue = checkbox.value;
    let selectedBrands = urlParams.get('brand');
    if (selectedBrands) {
      let selectedBrandsArray = selectedBrands.split(',');
      checkbox.checked = selectedBrandsArray.includes(brandValue);
    }
  });

  // Initialize price inputs but add spaces for better formatting (e.g. 1 000)
  let minPrice = urlParams.get('min_price');
  if (minPrice) {
    minPrice = minPrice.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    minPriceInput.value = minPrice;
  }

  let maxPrice = urlParams.get('max_price');
  if (maxPrice) {
    maxPrice = maxPrice.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    maxPriceInput.value = maxPrice;
  }

  // Initialize sort select
  let sortParam = urlParams.get('sort');
  if (sortParam) {
    sortSelect.value = sortParam;
  }

  let priceFormat = function (event) {
    let value = event.target.value;
    if (value.length > 17) {
      value = value.substring(0, 17);
    } else {
      value = value.replace(/\D/g, '').replace(/^0+/, '').replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    }
    event.target.value = value;
  }

  filterForm.addEventListener('submit', function (event) {
    event.preventDefault();
    applyPriceFilters();
  });

  sortSelect.addEventListener('change', function (event) {
    applySort();
  });

  brandCheckboxes.forEach(function (checkbox) {
    checkbox.addEventListener('change', function (event) {
      applyFilters();
    });
  });

  let priceOkButton = document.getElementById('price-ok-btn');

  function checkPriceInputs() {
    let minPriceInputInt = parseInt(minPriceInput.value.replace(/\s/g, ''));
    let maxPriceInputInt = parseInt(maxPriceInput.value.replace(/\s/g, ''));
    if (minPriceInputInt > maxPriceInputInt) {
      priceOkButton.disabled = true;
    } else {
      priceOkButton.disabled = false;
    }
  }


  minPriceInput.addEventListener('input', function (event) {
    priceFormat(event);
    checkPriceInputs();
  });

  maxPriceInput.addEventListener('input', function (event) {
    priceFormat(event);
    checkPriceInputs();
  });

  function applyPriceFilters() {
    // get all query params from the URL
    let queryParams = [];

    // get min_price and max_price values from the inputs but replace spaces with empty strings
    let minPrice = minPriceInput.value.replace(/\s/g, '');
    let maxPrice = maxPriceInput.value.replace(/\s/g, '');

    // remove min_price from the URL
    urlParams.delete('min_price');

    // remove max_price from the URL
    urlParams.delete('max_price');

    // add min_price to the URL if it's not empty
    if (minPrice !== '') {
      urlParams.append('min_price', minPrice);
    }
    
    // add max_price to the URL if it's not empty
    if (maxPrice !== '') {
      urlParams.append('max_price', maxPrice);
    }

    // add all query params to the array
    for (let pair of urlParams.entries()) {
      queryParams.push(pair[0] + '=' + pair[1]);
    }

    // set dropdownMenuOpened to true in localStorage so that the dropdown menu is opened when the page is reloaded
    localStorage.setItem('dropdownMenuOpened', 'true');

    window.location.href = window.location.pathname + '?' + queryParams.join('&');
  }

  function applyFilters() {
    let queryParams = [];

    let selectedBrands = Array.from(brandCheckboxes)
      .filter(function (checkbox) {
        return checkbox.checked;
      })
      .map(function (checkbox) {
        return checkbox.value;
      });

    urlParams.delete('brand');

    if (selectedBrands.length > 0) { 
      queryParams.push('brand=' + encodeURIComponent(selectedBrands.join(',')));
    }

    // remove min_price and max_price from the URL
    urlParams.delete('min_price');
    urlParams.delete('max_price');

    // add min_price to the URL if it's not empty
    if (minPriceInput.value !== '') {
      urlParams.append('min_price', minPriceInput.value.replace(/\s/g, ''));
    }

    // add max_price to the URL if it's not empty
    if (maxPriceInput.value !== '') {
      urlParams.append('max_price', maxPriceInput.value.replace(/\s/g, ''));
    }

    // add all query params to the array
    for (let pair of urlParams.entries()) {
      queryParams.push(pair[0] + '=' + pair[1]);
    }

    // set dropdownMenuOpened to true in localStorage so that the dropdown menu is opened when the page is reloaded
    window.localStorage.setItem('dropdownMenuOpened', 'true');


    
    if (queryParams.length === 0) {
      window.location.href = window.location.pathname;
    } else {
    window.location.href = window.location.pathname + '?' + queryParams.join('&');
    }
  }

  function applySort() {
    let sortParam = sortSelect.value;
    let queryParams = [];

    urlParams.delete('sort');
    for (let pair of urlParams.entries()) {
      queryParams.push(pair[0] + '=' + pair[1]);
    }

    if (sortParam) {
      queryParams.push('sort=' + encodeURIComponent(sortParam));
    }

    window.location.href = window.location.pathname + '?' + queryParams.join('&');
  }
});
