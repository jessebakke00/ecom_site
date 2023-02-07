var updateBtns = document.getElementsByClassName('update-cart');

for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('product:', productId, 'action:', action);
        console.log('USER:', user);
        if(user === 'AnonymousUser' ){
            console.log('Not Logged In');
        }else{
            updateUserOrder(productId, action);
        }
    });
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