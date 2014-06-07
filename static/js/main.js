$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });

  $('#loginform').submit(function(e) {
    $('#status').text('');
    $.ajax({
      type: 'POST',
      data: $('#loginform').serialize(),
      success: show_status
    });
    return false;
  });
});

function show_status(status) {
  if (status == '1') {
    document.location = '/';
  } else {
    $('#status').text('登录失败！');
  }
}
