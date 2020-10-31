

$( document ).ready(function() {
    $( ".show_comments" ).click(function() {
        $(this).parent().children(".comments_hidden").css("display", "block");
        $(this).parent().children(".hide_comments").css("display", "block");
        $(this).css("display", "none");
      });

      $( ".hide_comments" ).click(function() {
        $(this).parent().children(".comments_hidden").css("display", "none");
        $(this).css("display", "none");
        $(this).parent().children(".show_comments").css("display", "block");
      });

    $(".add_comment").click(function(){
       
    });
      

});