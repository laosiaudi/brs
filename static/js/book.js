$(document).ready(function() {
  $('#rateform').submit(function(e) {
    $('#status').text('');
    $.ajax({
      type: 'POST',
      data: $('#rateform').serialize(),
      success: show_status
    });
    return false;
  });
});

function show_status(status) {
  if (status == '1') {
    $('#status').text('打分成功！');
  } else {
    $('#status').text('出错了...');
  }
}
