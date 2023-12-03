// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// owl carousel 

$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    autoplay: true,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 6
        }
    }
})


//Cookies

function getCookie(name){
    var cookieArr = document.cookie.split(";");

    for (var i = 0; i < cookieArr.length; i++){
        var cookiePair = cookieArr[i].split("=");

        if (name == cookiePair[0].trim()){
            return decodeURIComponent(cookiePair[1]);
        }
    }

    return null;
}
var cart = JSON.parse(getCookie('cart'))

if (cart == undefined){
    cart = {}
    console.log('Cart Created!', cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
}
console.log("Cart:", cart)

