$(document).ready(function() {
  $('#registerform').submit(function(e) {
    $('#status').text('');
    $.ajax({
      type: 'POST',
      data: $('#registerform').serialize(),
      success: show_status
    });
    return false;
  });
});

function show_status(status) {
  if (status == '1') {
    document.location = '/login';
  } else {
    $('#status').text('注册失败！');
  }
}
