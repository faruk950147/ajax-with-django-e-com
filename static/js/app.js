  $(document).ready(function () {
    //categories
    $("#showHideCates").on("click", function(e){
        e.preventDefault()
        console.log('clicked');
        $(".catesToggle").stop().fadeToggle(1000)
      });

});
