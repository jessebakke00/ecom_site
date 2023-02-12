var updateBtns = document.getElementsByClassName('update-cart');

for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('product:', productId, 'action:', action);
        console.log('USER:', user);
        if(user === 'AnonymousUser' ){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action);
        }
    });
}

function addCookieItem(productId, action){
    console.log('User is not authenticated!');
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1};
        }else{
            cart[productId]['quantity'] += 1;
        }
        
        if(action == 'remove'){
            cart[productId]['quantity'] -= 1;
            console.log('product should be deleted');
            delete cart[productId];
        }
    }
    console.log('cart: ', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    updateCart();
}

function updateUserOrder(productId, action){
    console.log('User is authenticated. Sending data ...');
    
    var url = '/update_item/';
    
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'XCSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json();    
    })
    .then((data) => {
        //console.log('action:', data.action, 'product:', data.productId);
        location.reload();   
    });
}

function updateCookie(productId, action){
    console.log('whiskey');
    
}

function updateCart(){
    var url = '/update_cookie/';
    console.log('whiskey!', cart);
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'XCSRFToken':csrftoken,
        },
        body:JSON.stringify({'cart':cart})
    })
    .then((response) => {
        return response.json();    
    })
    .then((data) => {
        //console.log('action:', data.action, 'product:', data.productId);
        console.log('YESS!!');
    });
}


//function getToken(name){
//    var cookieValue = null;
//    if(document.cookie && document.cookie != ''){
//        var cookies = document.cookie.split(';');
//        for(var i=0; i<cookies.length; i++){
//            var cookie = cookies[i].trim();
//            if(cookie.substring(0, name.length - 1) === (name + '=')){
//                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                break;
//            }
//        }
//    }
//    return cookieValue;
//}