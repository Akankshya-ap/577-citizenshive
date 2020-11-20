$(document).ready(function(){
    $("form").submit(function(e){

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
        
        var d = new Date();

        var month = d.getMonth()+1;
        var day = d.getDate();

        var output = d.getFullYear() + '-' +
            (month<10 ? '0' : '') + month + '-' +
            (day<10 ? '0' : '') + day;

        $('#start_date').val(output);
        $('#end_date').val(output);
        // alert("Start Date = " + start_date);
        // alert("End Date" + end_date);
        // alert("Current Date = " + current_date);

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
