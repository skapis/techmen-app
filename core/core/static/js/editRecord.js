$(document).ready(function(){
    $('#editRec').click(function(){
        var name = $('[name="name"]');
        var date = $('[name="date"]');
        var line = $('[name="line"]');
        var desc = $('[name="description"]');

        $('input, textarea, select').each(function(){
            $(this).prop('disabled', false)
        })


        $('.actions').hide() // remove buttons for edit and delete, when user edits customer data
        $('.edit').show();
        $('.addBtn').removeClass('d-none');
        
        var submit = $('<button/>')
            .text('Uložit')
            .addClass('btn btn-primary rounded-lg mr-2 mb-3')
            .on('click', () => {
                var name = $('[name="name"]').val();
                var date = $('[name="date"]').val();
                var internalId = $('[name="internalId"]').val();
                var line = $('[name="line"]').val();
                var desc = $('[name="description"]').val();
                var distance = $('[name="distance"]').val();
                var transportPrice = $('[name="transportPrice"]').val();
                var workPrice = $('[name="workPrice"]').val();

                var workArray = new Array()
                
                $('.workRow').each(function(){
                    var workId = $(this).attr('id')
                    var checkboxValue = $(this).find('[name="works"]').prop('checked')
                    var checkboxValueId = $(this).find('[name="works"]').val();
                    var itemDescription = $(this).find('[name="itemDesc"]').val();

                    workData = {
                        'workId': workId,  
                        'workDone': checkboxValue,
                        'workItemId': checkboxValueId,
                        'itemDescription': itemDescription
                    }

                    workArray.push(workData)
                });

                var issueArray = new Array()

                $('.issueRow').each(function(){
                    var issueId = $(this).attr('id')
                    var issueName = $(this).find('[name="issueName"]').val();
                    var fixTime = $(this).find('[name="fixTime"]').val();
                    var resolution = $(this).find('[name="resolution"]').val(); 

                    issueData = {
                        'issueId': issueId,
                        'issueName': issueName,
                        'fixTime': fixTime,
                        'resolution': resolution
                    }


                    issueArray.push(issueData)
                });

                var componentArray = new Array()

                $('.componentRow').each(function(){
                    var componentId = $(this).attr('id')
                    var componentName = $(this).find('[name="componentName"]').val();
                    var componentSerialNumber = $(this).find('[name="componentSerialNumber"]').val();
                    var componentChange = $(this).find('[name="componentChange"]').val();
                    var componentPrice = $(this).find('[name="componentPrice"]').val();
                    var componentOrdered =  $(this).find('[name="componentOrdered"]').prop('checked');

                    componentData = {
                        'componentId': componentId,
                        'componentName': componentName,
                        'componentSerialNumber': componentSerialNumber,
                        'componentChange': componentChange,
                        'componentOrdered': componentOrdered,
                        'componentPrice': componentPrice
                    }

                    componentArray.push(componentData)
                })

                var offerArray = new Array()

                $('.offerRow').each(function(){
                    var offerId = $(this).attr('id')
                    var offerDate = $(this).find('[name="offerDate"]').val();
                    var componentSerialNumber = $(this).find('[name="componentSerialNumber"]').val();
                    var workTime = $(this).find('[name="workTime"]').val();
                    var offerPrice = $(this).find('[name="offerPrice"]').val();
        
                    offerData = {
                        'offerId': offerId,
                        'offerDate': offerDate,
                        'componentSerialNumber': componentSerialNumber,
                        'workTime': workTime,
                        'offerPrice': offerPrice
                    }

                    offerArray.push(offerData)
                })

                formData = {
                    'name': name,
                    'date': date,
                    'internalId': internalId,
                    'line': line,
                    'description': desc,
                    'distance': distance,
                    'transportPrice': transportPrice,
                    'workPrice': workPrice,
                    'works': workArray,
                    'issues': issueArray,
                    'components': componentArray,
                    'offers': offerArray
                }
                console.log(formData)
                
                $.ajax({
                    type: 'POST',
                    url: '/record/'+ getUrlId() + '/edit',
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    data: JSON.stringify(formData),
                    success: function(data){
                        window.location.href = '/record/'+ getUrlId()
                    }
                });
            });
        var cancel = $('<button/>')
            .text('Storno')
            .addClass('btn btn-danger rounded-lg mb-3')
            .attr('id', 'cancel')
            .on('click', () => {

                $('input, textarea, select').each(function(){
                    $(this).prop('disabled', true)
                })
                $('.edit').hide();
                $('.actions').show();
                $('.addBtn').addClass('d-none');
            })
            ;
        if (!$('#cancel').length){
            $('.edit').append(submit);
            $('.edit').append(cancel);
        }

    });

    $('#addIssue').click(function(){
        var inputId = $('#issues').children().length + 1
        var item = 
        '<div class="row issueRow" id="issueRow-"'+ inputId +'>' +
            '<div class="col-md-10 col">' +
                '<div class="form-row">'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="issueName" class="font-weight-bold">Závada č.'+ inputId +'</label>'+
                        '<input type="text" name="issueName" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="fixTime">Čas</label>'+
                        '<input type="number" name="fixTime" class="form-control rounded-sm">'+
                    '</div>'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="resolution">Odstranění závady</label>'+
                        '<input type="text" name="resolution" class="form-control rounded-sm" required>'+
                    '</div>'+
                '</div>'+
            '</div>'+
            '<div class="col-md-2 col-12 d-flex align-items-end justify-content-center removeIssue">'+
                '<p class="btn btn-danger border-0 rounded-lg mb-0 mt-2" id="removeBtn'+ inputId +'">Odebrat</p>'
            '</div>'+
        '</div>'
        
        $('#issues').append(item)

        $('.removeIssue').click(function(){
            $(this).parent().remove()
        })
        
    });

    $('#addComponent').click(function(){
        var inputId = $('#components').children().length + 1
        var item = 
        '<div class="row componentRow" id="componentRow-"'+ inputId +'>' +
            '<div class="col-md-10 col">' +
                '<div class="form-row">'+
                    '<div class="col-lg col-md-2">'+
                        '<label for="componentName" class="font-weight-bold">Komponenta č.'+ inputId +'</label>'+
                        '<input type="text" name="componentName" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-2">'+
                        '<label for="componentSerialNumber">Číslo komponenty</label>'+
                        '<input type="text" name="componentSerialNumber" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-2">'+
                        '<label for="componentChange">Výměna komponenty</label>'+
                        '<input type="text" name="componentChange" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-2">'+
                        '<label for="componentPrice">Cena komponenty</label>'+
                        '<input type="number" step="0.01" name="componentPrice" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-2 mb-md-0 mb-2 d-flex align-items-center justify-content-center">'+
                        '<div class="mt-4">'+
                            '<input type="checkbox" class="form-check-input" name="componentOrdered" >'+
                            '<label for="componentOrdered" class="form-check-label">Objednáno</label>'+
                        '</div>'+
                    '</div>'+
                '</div>'+
            '</div>'+
            '<div class="col-md-2 col-12 d-flex align-items-end justify-content-center removeComponent">'+
                '<p class="btn btn-danger border-0 rounded-lg mb-0 mt-2" id="removeBtn'+ inputId +'">Odebrat</p>'
            '</div>'+
        '</div>'
        
        $('#components').append(item)

        $('.removeComponent').click(function(){
            $(this).parent().remove()
        });

    });

    $('#addOffer').click(function(){
        var inputId = $('#offers').children().length + 1
        var item = 
        '<div class="row offerRow" id="offerRow-"'+ inputId +'>' +
            '<div class="col-md-10 col">' +
                '<div class="form-row">'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="offerDate" class="font-weight-bold">Nabídka č.'+ inputId +'</label>'+
                        '<input type="date" name="offerDate" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="componentSerialNumber">Číslo dílu</label>'+
                        '<input type="text" name="componentSerialNumber" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="workTime">Čas výměny</label>'+
                        '<input type="text" name="workTime" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="offerPrice">Cena komponenty</label>'+
                        '<input type="number" step="0.01" name="offerPrice" class="form-control rounded-sm" required>'+
                    '</div>'+
                '</div>'+
            '</div>'+
            '<div class="col-md-2 col-12 d-flex align-items-end justify-content-center removeOffer">'+
                '<p class="btn btn-danger border-0 rounded-lg mb-0 mt-2" id="removeBtn'+ inputId +'">Odebrat</p>'
            '</div>'+
        '</div>'
        
        $('#offers').append(item)

        $('.removeOffer').click(function(){
            $(this).parent().remove()
        })
    });
});


function getUrlId(){
    var url = document.location.href
    var custId = url.split('/')[4]
    return custId
};


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

function getMessage(text, type, action){
    var message = 
        '<div class="messages">' +
            '<div class="row mx-0 align-items-center ' + action + ' alert alert-sm rounded-sm alert-'+ type +'">' +
                '<div>' + text + '</div>'+
                '<a class="bi bi-x ml-auto"></a>' + 
            '</div>'
        '</div>';
    
    return message
}



