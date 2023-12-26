var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(e){
        e.preventDefault();
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log("productId:", productId, 'Action:', action)
        console.log("user:", user)

        if(user === "AnonymousUser"){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)

        }
    })
}

function addCookieItem(productId, action){
    console.log('User is not authenticated')

    if (action == "add"){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == "remove"){
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0){
            console.log("Item should be deleted")
            //delete cart[productId];
            
        }
    }
    console.log("Cart:", cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    //location.reload()
    updateCartDisplay()
}


function updateCartDisplay() {

    // Assuming you have an element with id "cart-display" to show the cart information
    var cartDisplays = document.getElementsByClassName("cart-basket");
    
    var totalQuantity = Object.values(cart).reduce((acc, item) => acc + item.quantity, 0);
    // Update the content of the cart display
    
    for (var i = 0; i < cartDisplays.length; i++) {
        cartDisplays[i].textContent = totalQuantity.toString();
    }

    // Update Cart displayed items
    var cartItems = Array.from(document.getElementsByClassName("cart-row-item"));

    // Initialize variables for overall total quantity and cost
    var overallTotalQuantity = 0;
    var overallTotalCost = 0;
 
    for (var i = 0; i < cartItems.length; i++) {
        var productId = cartItems[i].dataset.productId;

        // Check if the item is still in the cart
        if (cart[productId] !== undefined) {
            // Update the quantity display
            var quantityDisplay = cartItems[i].querySelector('.quantity-number');
            
            if (quantityDisplay) {
                quantityDisplay.textContent = cart[productId].quantity.toString();
            }


            // Update the total price display
            var totalPriceDisplay = cartItems[i].querySelector('.total-price');
            if (totalPriceDisplay) {
                var productPrice = parseFloat(cartItems[i].querySelector(".unit-price").textContent)
                
                if (!isNaN(productPrice)) {
                    var totalPrice = cart[productId].quantity * productPrice;
                    totalPriceDisplay.textContent = 'GH₵ ' + totalPrice.toFixed(2);
                } else {
                    console.error('Invalid product price format:', "{{item.product.price}}");
                }

            }
            
            //Remove the Element if the quantity is 0 or less
            if (cart[productId].quantity <= 0) {
                cartItems[i].remove()
                
            }

            // Accumulate quantity and cost for overall total
            overallTotalQuantity += cart[productId].quantity;
            overallTotalCost += totalPrice;

           
        }

        
    }

    // Update the overall total quantity and total cost in the HTML
    var overallTotalQuantityElement = document.getElementById("overall-total-quantity");
    var overallTotalCostElement = document.getElementById("overall-total-cost");

    if (overallTotalQuantityElement) {
        overallTotalQuantityElement.textContent = overallTotalQuantity.toString();
    }

    if (overallTotalCostElement) {
        overallTotalCostElement.textContent = 'GH₵ ' + overallTotalCost.toFixed(2);
      
    }


}



function updateUserOrder(productId, action){
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({
            'productId': productId,
            'action': action
        })
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log(data)
       
        location.reload()
    })
}

function update2UserOrder(productId, action){
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({
            'productId': productId,
            'action': action
        })
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log(data)
        window.location.href = "/checkout/"
        
    })
}

document.addEventListener("DOMContentLoaded", function () {
    updateCartDisplay();


});


//Buy now Feature

var buyBtns = document.getElementsByClassName('buy-now')

for (i = 0; i < buyBtns.length; i++){
    buyBtns[i].addEventListener('click', function(e){
        e.preventDefault();
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log("productId:", productId, 'Action:', action)
        console.log("user:", user)

        if(user === "AnonymousUser"){
            addCookieItem(productId, action)
            window.location.href = "/checkout/"
        }else{
            update2UserOrder(productId, action)
            

        }
        
    })
}