$(document).ready(function() {
  $('#groupform').submit(function(e) {
    $('#status').text('');
    $.ajax({
      type: 'POST',
      data: $('#groupform').serialize(),
      success: show_status
    });
    return false;
  });
});

function show_status(status) {
  if (status == '1') {
    $('#status').text('创建成功！');
  } else {
    $('#status').text('出错了...');
  }
}
