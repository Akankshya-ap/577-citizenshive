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

    $("form").submit(function(e){
        var dob = $("#dob").val();
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();

        var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
        
        var current_date = year + "-" + month + "-" + day;
        
        // alert("Start Date = " + start_date);
        // alert("End Date" + end_date);
        // alert("Current Date = " + current_date);
        if(dob < current_date) 
        {
            alert("Date of birth cannot precede the current date");
            e.preventDefault();
        }
        if(start_date < current_date) 
        {
            alert("Start date cannot precede the current date");
            e.preventDefault();
        }
        if(end_date < current_date)
        {
            alert("End date cannot precede the current date");
            e.preventDefault();
        }
        if(end_date < start_date)
        {
            alert("End date cannot precede start date");
            e.preventDefault();
        }

    });



});