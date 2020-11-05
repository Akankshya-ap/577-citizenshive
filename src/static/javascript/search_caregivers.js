$(document).ready(function(){
    $("form").submit(function(e){

        var start_date = new Date($("#start_date").val());
        var end_date = new Date($("#end_date").val());
        var current_date = new Date();

        var start_date_str = start_date.getFullYear() + "-" + start_date.getMonth() + "-" + start_date.getDate();
        var end_date_str = end_date.getFullYear() + "-" + end_date.getMonth() + "-" + end_date.getDate();
        var current_date_str = current_date.getFullYear() + "-" + current_date.getMonth() + "-" + current_date.getDay();

        console.log("Current date = " , current_date_str);
        console.log("Start Date = ", start_date_str);
        console.log("End Date = ", end_date_str);
        
        //Check if the user input start date is less than the current date
        console.log(start_date_str<current_date_str , ", Start date is less than the current date");
        if(start_date_str < current_date_str)
        {
            alert("Start date cannot precede the current date");
            e.preventDefault();
        }


        //Check if the user input end date is less than the current date
        console.log(end_date_str<current_date_str , ", End date is less than the current date");
        if(end_date_str<current_date_str)
        {
            alert("End date cannot precede the current date");
            e.preventDefault();
        }

        //Check if the user input end date is less than user input start date
        console.log(end_date_str<start_date_str , ", End date is less than the start date");
        if(end_date_str<start_date_str)
        {
            alert("End date cannot precede the start date");
            e.preventDefault();
        }

    });

});