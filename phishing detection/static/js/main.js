  
$(document).ready(function(){
    $('#url_form').submit(function(event){
        event.preventDefault();
        $('.loading').show(); // Show loading animation
        $.ajax({
            type: 'POST',
            url: '/',
            data: $(this).serialize(),
            success: function(response){
                $('#prediction_result').html(response);
                $('.loading').hide(); // Hide loading animation
            }
        });
    });
});
 