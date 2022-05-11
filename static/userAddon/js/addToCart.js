// incement and decrement button for change quantity of cart item
var updateBtn = $(".update-btn");
for (var i = 0; i < updateBtn.length; i++) {
     updateBtn[i].addEventListener("click", function () {
          let Type = this.dataset.type;
          let b = this.getAttribute("data-cartId");

          // incOrDec(Type, b);
          incOrDec(Type, b);
     });
}


function incOrDec(Type, c_id) {
     var data = {
          c_id: c_id,
          type: Type,
     };
     $.ajax({
          url: "/cart/changequantity",
          method: "GET",
          data: data,
          dataType: "json",
          success: function (data) {
               if (data.success) {
                    $("#qty-input" + c_id).val(data.quantity);
                    $("#Subtotal" + c_id).html(data.subtotal);
                    $("#cart_total").html(data.cart_subtotal);
                    $("#Cart_Subtotal").html(data.cart_subtotal);
               } else {
                    console.log("failed");
               }
          },
     });
}

// remove item from cart
function remove(cart_id) {
     var data = {
          c_id: cart_id,
     };
     $.ajax({
          url: "/cart/remove_item_cart",
          method: "GET",
          data: data,
          dataType: "json",
          success: function (data) {
               if (data.success) {
                    $("#product" + cart_id).remove();
                    $("#cart_total").html(data.cart_subtotal) && $("#Cart_Subtotal").html(data.cart_subtotal);
                    $("#cart-count").html(data.cartCount);
                    if (data.cartCount == 0){
                         $("#cart_status").html("No Products IN Cart")
                    }
                    console.log("success");
                    if (data.cart_subtotal <= 0) {
                         $("#checkout-btn").remove();
                         console.log("remmoved");
                    }

                    const Toast = Swal.mixin({
                         toast: true,
                         position: "bottum",
                         showConfirmButton: false,
                         timer: 3000,
                         timerProgressBar: true,
                         didOpen: (toast) => {
                              toast.addEventListener("mouseenter", Swal.stopTimer);
                              toast.addEventListener("mouseleave", Swal.resumeTimer);
                         },
                    });

                    Toast.fire({
                         icon: "success",
                         title: "Item removed from cart",
                    });
               } else {
                    alert("failed");
               }
          },
     });
}



// add to cart item onclick the add to cart button
function addToCart(v_id) {
     var data = {
          vari_id: v_id,
     };

     $.ajax({
          url: "/cart/addtocart",
          method: "GET",
          data: data,
          dataType: "json",
          success: function (data) {
               if (data.success) {
                    $("#cart-count").html(data.cart_count);
                    const Toast = Swal.mixin({
                         toast: true,
                         position: "top",
                         showConfirmButton: false,
                         timer: 3000,
                         timerProgressBar: true,
                         didOpen: (toast) => {
                              toast.addEventListener("mouseenter", Swal.stopTimer);
                              toast.addEventListener("mouseleave", Swal.resumeTimer);
                         },
                    });
               
                    Toast.fire({
                         icon: "success",
                         title: 'item added into cart',
                    });
               }
          },
     });
}

function delCartItem(item_id) {
     const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
               confirmButton: "btn btn-success",
               cancelButton: "btn btn-danger",
          },
          buttonsStyling: false,
     });

     swalWithBootstrapButtons
          .fire({
               title: "Are you sure?",
               text: "You won't be able to revert this!",
               icon: "warning",
               showCancelButton: true,
               confirmButtonText: "Yes, delete it!",
               cancelButtonText: "No, cancel!",
               reverseButtons: true,
          })
          .then((result) => {
               if (result.isConfirmed) {
                    // swalWithBootstrapButtons.fire("Deleted!", "Your file has been deleted.", "success");
                    remove(item_id);
               } else if (
                    /* Read more about handling dismissals below */
                    result.dismiss === Swal.DismissReason.cancel
               ) {
                    swalWithBootstrapButtons.fire("Cancelled", "Your imaginary file is safe :)", "error");
               }
          });
}

function delAddress(id) {
     const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
               confirmButton: "btn btn-success",
               cancelButton: "btn btn-danger",
          },
          buttonsStyling: false,
     });

     swalWithBootstrapButtons
          .fire({
               title: "Are you sure?",
               text: "You won't be able to revert this!",
               icon: "warning",
               showCancelButton: true,
               confirmButtonText: "Yes, delete it!",
               cancelButtonText: "No, cancel!",
               reverseButtons: true,
          })
          .then((result) => {
               if (result.isConfirmed) {
                    swalWithBootstrapButtons.fire("Deleted!", "Your file has been deleted.", "success");

                    data = {
                         address_id: id,
                    };
                    $.ajax({
                         url: "/checkout/DelAddressFromCheckout",
                         method: "GET",

                         data: data,
                         dataType: "json",
                         success: function (data) {
                              if (data.success) {
                                   //alert('success')
                                   $("#add" + id).remove();
                              } else {
                                   console.log("fail");
                              }
                         },
                    });
               } else if (
                    /* Read more about handling dismissals below */
                    result.dismiss === Swal.DismissReason.cancel
               ) {
                    swalWithBootstrapButtons.fire(
                         "Cancelled"
                         //'Your imaginary file is safe :)',
                         //'error'
                    );
               }
          });
}

// // add to whislist item onclick the add to cart button
// function  addToWhishlist(v_id) {
//      var data = {
//           vari_id: v_id,
//      };

//      $.ajax({
//           url: "/addtowhishlist",
//           method: "GET",
//           data: data,
//           dataType: "json",
//           success: function (data) {
//                if (data.status) {
//                     $("#whishlist_count").html(data.whishlist_count);
//                     const Toast = Swal.mixin({
//                          toast: true,
//                          position: "top",
//                          showConfirmButton: false,
//                          timer: 3000,
//                          timerProgressBar: true,
//                          didOpen: (toast) => {
//                               toast.addEventListener("mouseenter", Swal.stopTimer);
//                               toast.addEventListener("mouseleave", Swal.resumeTimer);
//                          },
//                     });

//                     Toast.fire({
//                          icon: "success",
//                          title: "add to whishlist",
//                     });
//                } else {
//                     window.location = '/login'
//                }
//           },
//      });
// }
