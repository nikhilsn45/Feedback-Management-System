  
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

    $(document).ready(function() {
      $('.form2').find('#prac').change(function(event){
        event.preventDefault();

        $.ajax({
          url: '/getbatch/',
          type: 'POST',
          data: formdata,
          success: function(result) {
            $('.batch2').html(result);
         }
        });
      })
    });

    $(document).ready(function() {
     $('.form2').find('.year1').change(function(event) {
        event.preventDefault();

        var formdata = {
          'year': $('.year1').val()
        }

        $.ajax({
          url: '/getdiv/',
          type: 'POST',
          data: formdata,
          success: function(result) {
            $('.div1').html(result);
         }
        });
     });
     });

    $(document).ready(function() {
     $('.form2').find('.year1').change(function(event) {
        event.preventDefault();

        var formdata = {
          'year': $('.year1').val()
        }

        $.ajax({
          url: '/getsub1/',
          type: 'POST',
          data: formdata,
          success: function(result) {
            $('.subject1').html(result);
         }
        });
     });
     });



    $(document).ready(function() {
      $('.form2').find('#theo').change(function(event){
        $('.batch2').hide();
      })
    });

    $(document).ready(function() {
      $('.form2').find('#prac').change(function(event){
        $('.batch2').show();
      })
    });