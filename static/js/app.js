 
 $(document).ready(function () {
    //categories
    $("#showHideCates").on("click", function(e){
        e.preventDefault()
        $(".catesToggle").stop().fadeToggle(1000)
      });
      // //color change active
      $(document).ready(function () {
        console.log($('input[name="color"]').val());
        $('input[name="color"]').change(function () {
            var newImage = $(this).val(); // Get the value of the selected radio button
            $('#main-product-image').attr('src', newImage); // Update the main product image
        });
    });
      
    
  });
