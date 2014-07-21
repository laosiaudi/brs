// Javascript File
// AUTHOR:   LaoSi
// FILE:     communicate.js
// 2014 @laosiaudi All rights reserved
// CREATED:  2014-07-20 12:50:19
// MODIFIED: 2014-07-20 12:55:23
$(document).ready(function() {
  $('#cmform').submit(function(e) {
    $('#status').text('');
    $.ajax({
      type: 'POST',
      data: $('#cmform').serialize(),
      success: show_status
    });
    return false;
  });
});

function show_status(status) {
  if (status == '1') {
    window.location.reload();
  } else {
    $('#status').text('出错了...');
  }
}
