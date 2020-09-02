
    $(document).ready(function() {
     $('.form1').find('#d1').change(function(event) {
        event.preventDefault();

        
      /*var formdata = {
          'yy': $('#y1').val()
          'tt': $('#t1').val()
          'dd': $('#d1').val()
        }*/

        $.ajax({
          url: '/rating/',
          type: 'POST',
          data: formdata,
          success: function(result) {
            $('.rate').html(result);
         }
        });
     });
    });