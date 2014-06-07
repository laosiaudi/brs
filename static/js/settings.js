$(document).ready(function() {
  for (var i in tags) {
    $($('.checkbox input:checkbox')[tags[i]]).prop('checked', true)
  }
});

