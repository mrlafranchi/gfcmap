$(function () {
  $('.btn-location-edit').click(function() {
    $('form.location')[0].reset();
    $('.api-response').html('');
    $('form.location input[name=name]').val($(this).data('name'));
    $('form.location input[name=address]').val($(this).data('address'));
    $('form.location input[name=url]').val($(this).data('link'));
    $("form.location select[name=facility_type]").val($(this).data('facility_type'));
    $("form.location select[name=field_type]").val($(this).data('field_type'));    
    $('form.event input[name=url]').val($(this).data('url'));

    $('#location-modal').modal();
  });
    
  $('.add-event').click(function() {
    $('form.event')[0].reset();
    $('.api-response').html('');
    $('#location-id').val($(this).data('id'));
    $('#location-name').val($(this).data('location'));
    $('form.event input[name=url]').val('');
    $('#event-modal').modal();
  });

  $('#datetimepicker1').datetimepicker({
    format: 'YYYY-MM-DD',
    minDate: new Date(new Date().getTime() + 24 * 60 * 60 * 1000)
  });

  $('#datetimepicker2').datetimepicker({
      format: 'LT'
  });  
});
