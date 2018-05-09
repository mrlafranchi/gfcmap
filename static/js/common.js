var error_response = function(data){
  var message;

  if (data.status == 500) {
    message = "Something is wrong on server. please contact server administrator.";
  } else {
    var key = Object.keys(data.responseJSON)[0];
    message = data.responseJSON[key];
  }
  
  $('.api-response').html(message);
  endLoading();
}

var susccess_response = function(data){
  endLoading();
  var RES = ['Password reset e-mail has been sent.', 
             'Password has been reset with the new password.'];

  if (data.detail == 'Verification e-mail sent.') {
    $('.api-response').html('<span class="text-success">Verification e-mail sent. Check spam folder.</span>');      
  } else if (RES.indexOf(data.detail) > -1) {
    $('.api-response').html('<span class="text-success">'+data.detail+'</span>');
  } else {
    location.href = redirect_url;
  }
}

$().ready(function() {
  if (!localStorage.getItem("is_visited")) {
    $('#welcome-modal').modal();
  }
  localStorage.setItem("is_visited", true);

  $('.nav-link').click(function() {
    $('.api-response').html('');   
  });

  $('form.ajax-post').submit(function(e){
    startLoading();
    e.preventDefault();

    var form = $(this);

    if (form.attr('class').indexOf('event ') > -1) {
      var date = $('input[name=datetime]').val();
      var time = $('input[name=time]').val();
      $('input[name=datetime]').val(date+'T'+time);
    }

    if ($('#method').val()) { // edit
      $.ajax({ 
        url: $('#method').val(), 
        data: form.serialize(),
        method: 'PATCH',
        headers: {
          'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        }
       })
      .fail(function(data){error_response(data);})
      .done(function(data){susccess_response(data);});        
    } else {
      $.post(form.attr('action'), form.serialize())
      .fail(function(data){error_response(data);})
      .done(function(data){susccess_response(data);});        
    }

    return false;
  });

  $('.btn-game-edit').click(function() {
    $('form.event')[0].reset();
    $('.api-response').html('');
    $('#location-id').val($(this).data('loc_id'));
    $('#location-name').val($(this).data('loc_name'));
    $('form.event input[name=datetime]').val($(this).data('date'));
    $('form.event input[name=time]').val($(this).data('time'));
    $('form.event input[name=description]').val($(this).data('description'));
    $("form.event select[name=players]").val($(this).data('players').split(','));
    $('form.event input[name=url]').val($(this).data('url'));

    $('#event-modal').modal();
  });

  $('.btn-logout').click(function() {
    var form = $('form.logout');
    $.post('/rest-auth/logout/', form.serialize()).done(function(data) {
      location.reload();
    });
  })

  $('.btn-game').click(function() {
    startLoading();
    $.ajax({
      url: $(this).data('url'),
      type: 'POST',
      headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
      },
      data: {},
      success: function(data){ 
        endLoading();
        location.reload();
      },
    });
  });       

  $('.tmap').click(function() {
    $('.tmap').toggleClass('d-none');
    $('#mapid').toggleClass('d-none');
  })
});

function delete_game(game_id) {
  var r = confirm("Are you sure to delete this game?");
  if (r == true) {
    startLoading();
    $.ajax({
      url: '/api/gameevent/'+game_id+'/',
      type: 'DELETE',
      headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
      },
      data: {},
      success: function(data){ 
        endLoading();
        location.reload();
      },
    });
  }
}

function delete_location(location_id) {
  var r = confirm("Are you sure to delete this location? \nGames in this field would be deleted too.");
  if (r == true) {
    startLoading();
    $.ajax({
      url: '/api/location/'+location_id+'/',
      type: 'DELETE',
      headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
      },
      data: {},
      success: function(data){ 
        endLoading();
        location.reload();
      },
    });
  }
}

function toggleBody(obj) {
  $(obj).parent().find('.card-body.player').toggleClass('d-none');
}

function startLoading() {
  $('.spinner').show();    
}

function endLoading() {
  $('.spinner').hide();    
}
