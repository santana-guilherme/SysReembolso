$(document).ready(() => {

    $('#id_refund_memo').change(() => {
        var file = document.getElementById('id_refund_memo').files[0];
        if (file === undefined) {
            return
        }
        var reader = new FileReader();
        reader.onload = (e) => {
            image = document.getElementById('refund-memo-img')
            image.src = e.target.result
            $(image).css('display', 'inline-block')
        }
        reader.readAsDataURL(file)
    })
})