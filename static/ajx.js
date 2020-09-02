
    $(document).ready(function() {
     $('.form1').find('#data').change(function(event) {
        event.preventDefault();

        var formdata = {
          't': $('#data').val()
        }

        $.ajax({
          url: '/getdata/',
          type: 'POST',
          data: formdata,
          success: function(result) {
            $('.year').html(result);
         }
        });
     });
    });