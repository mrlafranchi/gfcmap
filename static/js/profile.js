$(function () {
  $('#datetimepicker1').datetimepicker({
    format: 'YYYY-MM-DD',
    minDate: new Date(new Date().getTime() + 24 * 60 * 60 * 1000)
  });

  $('#datetimepicker2').datetimepicker({
      format: 'LT'
  });  
    
  $('#datetimepicker12').datetimepicker({
    format: 'YYYY-MM-DD'
  });

  $('form.profile').submit(function(e){
    e.preventDefault();
    var form = $(this);
    startLoading();

    $.ajax({
      url: form.attr('action'),
      type: 'PUT',
      headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
      },
      data: $(this).serialize(),
      success: function(data){ 
        endLoading();
        alert('Your profile saved successfully.'); 
      },
    });

    return false;
  });  

  $("body").on("click", ".upload-avatar", function(e) {
    e.preventDefault();
    jQuery("#inputfile").click();
  });

  $("#inputfile").change(function() {
      var fd = new FormData();
      var file = this.files;
      fd.append("images", file[0]);
      fd.append('type', 'avatar');

      jQuery.ajax({
          type: 'POST',
          url: '/upload-image',
          data: fd,
          contentType: false,
          dataType: "json",
          processData: false,
          success: function(response) {
              jQuery(".upload-image").find('input[class="uploded_id"]').val(response.image_name);
              jQuery(".upload-image").find('input[class="uploded_id1"]').val(response.image_name);
              jQuery(".avatar").attr('src', response.image_url);
          }
      });
  });
  $('.card-header.profile').click(function() {
    $('.card-body.profile').toggleClass('d-none');
    $('.fa-window-minimize').toggleClass('d-none');
    $('.fa-window-maximize').toggleClass('d-none');    
  });
});
