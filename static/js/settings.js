$(document).ready(function() {
  for (var i in tags) {
    $($('.checkbox input:checkbox')[tags[i]]).prop('checked', true)
  }

  $('#settingsform').submit(function(e) {
    $('#status').text('');
    $.ajax({
      type: 'POST',
      data: $('#settingsform').serialize(),
      success: show_status
    });
    return false;
  });
});

function show_status(status) {
  if (status == '1') {
    $('#status').text('修改成功！');
  } else {
    $('#status').text('修改失败！');
  }
}

