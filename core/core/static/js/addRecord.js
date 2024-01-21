$(document).ready(function(){
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
                        '<label for="fixTime">Čas (min)</label>'+
                        '<input type="number" name="fixTime" class="form-control rounded-sm" value="0">'+
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
                        '<label for="componentPrice">Cena komponenty (Kč)</label>'+
                        '<input type="number" step="0.01" value="0" name="componentPrice" class="form-control rounded-sm" required>'+
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
                        '<label for="workTime">Čas výměny (min)</label>'+
                        '<input type="text" name="workTime" value="0" class="form-control rounded-sm" required>'+
                    '</div>'+
                    '<div class="col-lg col-md-3">'+
                        '<label for="offerPrice">Cena komponenty (Kč)</label>'+
                        '<input type="number" step="0.01" value="0" name="offerPrice" class="form-control rounded-sm" required>'+
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
    })

    $("form").on("submit", function(event){
        event.preventDefault();

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
            var checkboxValue = $(this).find('[name="works"]').prop('checked')
            var checkboxValueId = $(this).find('[name="works"]').val();
            var itemDescription = $(this).find('[name="itemDesc"]').val();

            workData = {
                'workDone': checkboxValue,
                'workId': checkboxValueId,
                'itemDescription': itemDescription
            }

            workArray.push(workData)
        });

        var issueArray = new Array()

        $('.issueRow').each(function(){
            var issueName = $(this).find('[name="issueName"]').val();
            var fixTime = $(this).find('[name="fixTime"]').val();
            var resolution = $(this).find('[name="resolution"]').val(); 

            issueData = {
                'issueName': issueName,
                'fixTime': fixTime,
                'resolution': resolution
            }


            issueArray.push(issueData)
        });

        var componentArray = new Array()

        $('.componentRow').each(function(){
            var componentName = $(this).find('[name="componentName"]').val();
            var componentSerialNumber = $(this).find('[name="componentSerialNumber"]').val();
            var componentChange = $(this).find('[name="componentChange"]').val();
            var componentPrice = $(this).find('[name="componentPrice"]').val();
            var componentOrdered =  $(this).find('[name="componentOrdered"]').prop('checked');

            componentData = {
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
            var offerDate = $(this).find('[name="offerDate"]').val();
            var componentSerialNumber = $(this).find('[name="componentSerialNumber"]').val();
            var workTime = $(this).find('[name="workTime"]').val();
            var offerPrice = $(this).find('[name="offerPrice"]').val();
 
            offerData = {
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

        $.ajax({
            type: 'POST',
            url: '/record/add',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: JSON.stringify(formData)

            })


    })

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
