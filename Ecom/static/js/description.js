
var descBtns = document.getElementsByClassName( 'get-description' );

for(var i=0;i<descBtns.length;i++){
  descBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product;
    var action = this.dataset.action;
    getDescription(productId);
  });
}

function getDescription(productId){
  var url = '/product_description/';
  
  fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X_CSRFToken': csrftoken
      },
      body:JSON.stringify({'product_id':productId})
  })
  .then(( response ) => {
    return response.json();  
  })
  .then(( data ) => {
    console.log( data );  
  });
}