let updateButtons = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action

        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        if(user === 'AnonymousUser'){
            addCookieItem(productId, action)
            updateUserOrder(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}


function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...')

    let url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {

        console.log('Data:', data)

        // Update cart count and subtotal
        let cartCountElement = document.getElementById('cart-count')
        if (cartCountElement) {

        let cartItemValue = document.getElementById('cart-item-value-'+data['product-id'])
        if (cartItemValue) {
            console.log('cartItemValue:', cartItemValue)
            let preFormattedItemValue = data['item-total']
            let formattedItemValue = numeral(preFormattedItemValue).format('0,0.00').replace(/,/g, ' ');
            cartItemValue.innerHTML = '\u20B4 ' + formattedItemValue
        }

        let cartItemCount = document.getElementById('cart-item-count-'+data['product-id'])
        if (cartItemCount) {
            cartItemCount.innerHTML = '<strong>' + data['item-count'] + '</strong>'
        }



        cartCountElement.textContent = data['cart-count'];
        let cartSubCountElement = document.getElementById('cart-sub-count')
            if (cartSubCountElement) {
                cartSubCountElement.innerHTML = '<h5><strong>' + data['cart-count'] + '</strong></h5>'
            }
            if(cartCountElement.textContent === '0'){
                document.getElementById("cart-count-form").classList.add("hidden")
                console.log(cartCountElement.textContent)
                document.getElementById("cart-with-items").classList.add("hidden")
                document.getElementById("cart-without-items").classList.remove("hidden")

            }else {
                document.getElementById("cart-count-form").classList.remove("hidden")
                console.log(cartCountElement.textContent)
            }
        }
        let cartSubtotalElement = document.getElementById('cart-subtotal')
        if (cartSubtotalElement) {
            let subtotalValue = data['cart-subtotal']
            let formattedValue = numeral(subtotalValue).format('0,0.00').replace(/,/g, ' ');
            cartSubtotalElement.innerHTML = '<h5><strong>' + '\u20B4 ' + formattedValue + '</strong></h5>';
        }

        if (data['item-count'] === 0){
            document.getElementById('cart-row-' + data['product-id']).classList.add('hidden')
        }

    })
}

function addCookieItem(productId, action) {
    if (action === 'add') {
        if (cart[productId] === undefined || cart[productId] === null) {
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if (action === 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    if (action === 'delete') {
        delete cart[productId]
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    console.log('Cart:', cart)

}
