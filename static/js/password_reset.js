var url_elements = window.location.pathname.split('/');

if (url_elements.length == 6){
  var uid = url_elements[url_elements.length - 3];
  if (uid !== undefined){
    $('input[name=uid]').val(uid);
  }
  var token = url_elements[url_elements.length - 2];
  if (token !== undefined){
    $('input[name=token]').val(token);
  }
}