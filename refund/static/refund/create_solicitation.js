$(document).ready(function() {
  $('#add_item').click(function() {
    var next_id = $('#id_items-TOTAL_FORMS').val()
    $('form table').append($('#empty_form table tbody').html().replace(/__prefix__/g, next_id))
    $('#id_items-TOTAL_FORMS').val(parseInt(next_id)+1)
  })
})