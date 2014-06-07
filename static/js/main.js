$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });

  $('#loginform').submit(function(e) {
    $.ajax({
      type: 'POST',
      data: $('#loginform').serialize(),
      success: show_status
    });
    return false;
  });
});

function show_status() {
  $('#status').text('okkkkay');
}
