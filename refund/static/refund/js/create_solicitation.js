$(document).ready(function () {

    $('#add_item').click(function () {
        var next_id = $('#id_items-TOTAL_FORMS').val()
        $('#itemsolicitation_form').append("<div id='form_item'></div>")
        $('#itemsolicitation_form #form_item:last-child').append($('#empty_form').html().replace(/__prefix__/g, next_id))
        $('#id_items-TOTAL_FORMS').val(parseInt(next_id) + 1)
    })

    $('#remove_last').click(() => {
        var id = $('#id_items-TOTAL_FORMS').val()
        $('#itemsolicitation_form #form_item:last-child').remove()
        $('#id_items-TOTAL_FORMS').val(parseInt(id) - 1)
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

    $('#id_claim_check').parent().ready(() => {
        const imgURL = $('#id_claim_check').parent().children('a').attr('href')
        //TODO: improove this
        if (imgURL === undefined || imgURL === '') {
            return
        }
        console.log("asdf", $('#img_preview'))
        img = $('#img_preview')
        img.attr('src', imgURL)
        img.css('display', 'inline-block')
        console.log("executed")
    })
})