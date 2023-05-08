document.addEventListener('DOMContentLoaded', function() {
  let filterForm = document.getElementById('filter-form');
  let sortSelect = document.getElementById('sort-select');
  let brandCheckboxes = document.querySelectorAll('input[name="brand"]');
  let minPriceInput = document.querySelector('input[name="min_price"]');
  let maxPriceInput = document.querySelector('input[name="max_price"]');

  let urlParams = new URLSearchParams(window.location.search);

  // Initialize brand checkboxes
  brandCheckboxes.forEach(function(checkbox) {
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

  let priceFormat = function(event) {
    let value = event.target.value;
    if (value.length > 17) {
        value = value.substring(0, 17);
    } else {
      value = value.replace(/\D/g, '').replace(/^0+/, '').replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    }
    event.target.value = value;
  }

  filterForm.addEventListener('submit', function(event) {
    event.preventDefault();
    applyPriceFilters();
  });

  sortSelect.addEventListener('change', function(event) {
    applySort();
  });

  brandCheckboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function(event) {
      applyFilters();
    });
  });

  minPriceInput.addEventListener('input', function(event) {
      priceFormat(event);
  });

  maxPriceInput.addEventListener('input', function(event) {
      priceFormat(event)
  });

  function applyPriceFilters() {
    // get all query params from the URL
    let queryParams = [];

    // get min_price and max_price values from the inputs but replace spaces with empty strings
    let minPrice = minPriceInput.value.replace(/\s/g, '')
    let maxPrice = maxPriceInput.value.replace(/\s/g, '')

    // remove min_price from the URL
    urlParams.delete('min_price');
    urlParams.delete('max_price');

    // add min_price to the URL if it's not empty
    if (minPrice !== '') {
      urlParams.append('min_price', minPrice);
    }
    if (maxPrice !== '') {
      urlParams.append('max_price', maxPrice);
    }

    // add all query params to the array
    for (let pair of urlParams.entries()) {
        queryParams.push(pair[0] + '=' + pair[1]);
    }

    window.location.href = window.location.pathname + '?' + queryParams.join('&');
  }

  function applyFilters() {
    let queryParams = [];

    let selectedBrands = Array.from(brandCheckboxes)
      .filter(function(checkbox) {
        return checkbox.checked;
      })
      .map(function(checkbox) {
        return checkbox.value;
      });

    if (selectedBrands.length > 0) {
      queryParams.push('brand=' + encodeURIComponent(selectedBrands.join(',')));
    }

    //
    if (minPrice) {
      queryParams.push('min_price=' + encodeURIComponent(minPrice.replace(/\s/g, '')));
    }

    if (maxPrice) {
      queryParams.push('max_price=' + encodeURIComponent(maxPrice.replace(/\s/g, '')));
    }

    if (sortSelect.value !== '') {
      queryParams.push('sort=' + encodeURIComponent(sortSelect.value));
    }

    window.location.href = window.location.pathname + '?' + queryParams.join('&');
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
