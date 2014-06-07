$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });

  $('#btn-one').attr("disabled", true);
  $('#btn-two').attr("disabled", false);
  $('#by').val('title');
  $('#btn-two').click(function() {
    $('#btn-one').attr("disabled", false);
    $('#btn-two').attr("disabled", true);
    $('#by').val('author');
  });
  $('#btn-one').click(function() {
    $('#btn-one').attr("disabled", true);
    $('#btn-two').attr("disabled", false);
    $('#by').val('title');
  });
});

