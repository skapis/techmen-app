$(document).ready(function(){
    $('[name="name"]').on('input', function() {
        var inputValue = $(this).val();

        if (!inputValue.trim()) {
        return;
        }

        $.ajax({
        url: '/lines/check',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        data: JSON.stringify({
            'name': inputValue
        }),
        success: function(data) {
            $('#invalid_line').empty();
            $('#invalid_line').removeClass('d-block');
            $('#submitBtn').prop('disabled', false)
        },
        error: function(xhr) {
            var errText = $('<p/>').text(xhr.responseJSON.duplicate_check);
            $('#invalid_line').addClass('d-block')
            $('#invalid_line').empty().append(errText);
            $('#submitBtn').prop('disabled', true)
        }
        });
    })
});


  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}