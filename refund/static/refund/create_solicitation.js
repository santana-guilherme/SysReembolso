$(document).ready(function() {

  $('#add_item').click(function() {
    var next_id = $('#id_items-TOTAL_FORMS').val()
    $('form table').append($('#empty_form table tbody').html().replace(/__prefix__/g, next_id))
    $('#id_items-TOTAL_FORMS').val(parseInt(next_id)+1)
  })

  $('#remove_last').click(function() {
      var id = $('#id_items-TOTAL_FORMS').val()
      const fields = $('#empty_form table tbody tr').length

      if(id > 1) {
        for(let i = fields; i > 0; i--){
            $('form table tbody tr:last-child').remove()
        }
        $('#id_items-TOTAL_FORMS').val(parseInt(id)-1)
      }
  })
})