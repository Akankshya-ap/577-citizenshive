$(document).ready(function(){
    $('#edit_profile').click(function(){
        //alert('Edit button clicked');
        // $(':input[type="submit"]').prop('disabled', false);
        $(this).parent().find("input").prop('disabled', false);
        // $(this).parent().parent().parent().find("input").prop('disabled', false);
        $(this).parent().find("textarea").prop('disabled', false);
        $(this).parent().find("select").prop('disabled', false);
        //alert("Hey");
        $('.profile_image').prop('disabled',false);
        
    });
});