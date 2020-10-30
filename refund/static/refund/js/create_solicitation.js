$(document).ready(function () {

    $('#add_item').click(function () {
        var next_id = $('#id_items-TOTAL_FORMS').val()
        $('.multiField').append($('#empty_form').html().replace(/__prefix__/g, next_id))
        $('#id_items-TOTAL_FORMS').val(parseInt(next_id) + 1)
    })

    $('#remove_last').click(() => {
        var id = $('#id_items-TOTAL_FORMS').val()
        const fields = $('#empty_form > div').length
        if (id > 1) {
            for (let i = fields; i > 0; i--) {
                $('.multiField > div:last').remove()
            }
            $('.multiField > input:last').remove()
            $('#id_items-TOTAL_FORMS').val(parseInt(id) - 1)
        }
    })

    $('#img_preview').on('load',() => {
        $('.zoomImg').remove()
        $('#img_preview_container').zoom()
    })

    $('#id_claim_check').change(() => {
        var file = document.getElementById('id_claim_check').files[0];
        if (file === undefined) {
            return
        }
        var reader = new FileReader();
        reader.onload = (e) => {
            image = document.getElementById('img_preview')
            image.src = e.target.result
            $(image).css('display', 'inline-block')
        }
        reader.readAsDataURL(file)
    })
})