let updateButtons = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('User is not authenticated')
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
        const cartCountElement = document.getElementById('cart-count')
        if (cartCountElement) {
        cartCountElement.textContent = data['cart-count']
            if(cartCountElement.textContent === '0'){
                document.getElementById("cart-count-form").classList.add("hidden")
                console.log("count is now hidden anymore")
                console.log(cartCountElement.textContent)
                document.getElementById("cart-with-items").classList.add("hidden")
                document.getElementById("cart-without-items").classList.remove("hidden")

            }else {
                document.getElementById("cart-count-form").classList.remove("hidden")
                console.log("count is now NOT hidden anymore")
                console.log(cartCountElement.textContent)
            }
        }
    })
}
