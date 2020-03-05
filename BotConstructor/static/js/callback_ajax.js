$(document).on('submit', '#id_create_callback', function (e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '{% url "create_callback_url" token=token %}',
        data: {
            callback_text: $('#id_callback_text').val(),
            react_text: $('#id_react_text').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'create_callback'
        },
        success: function (json) {
            if (json.callback_error == null) {
                var object = '<form onsubmit="sendAjaxUpdateCallback(this); return false;" method="POST">' +
                    '<input type="hidden" name="csrfmiddlewaretoken" value="' + json.csrf + '">' +
                    '<div class="form-row mt-3">' +
                    '<div class="col-md-12">' +
                    '<div class="input-group">' +
                    '<div class="input-group-prepend">' +
                    '<div class="input-group-text">React</div>' +
                    '</div>' +
                    '<input type="text" class="form-control" name="callback_text_' + json.len_text + '" value="' + json.callback + '">' +
                    '</div>' +
                    '</div>' +
                    '<div class="col-md-12 mt-2">' +
                    '<div class="form-row">' +
                    '<div class="col-md-8">' +
                    '<div class="input-group">' +
                    '<div class="input-group-prepend">' +
                    '<div class="input-group-text">Callback</div>' +
                    '</div>' +
                    '<input type="text" class="form-control" name="react_text_' + json.len_text + '" value="' + json.react_text + '">' +
                    '</div>' +
                    '</div>' +
                    '<div class="col-md-2">' +
                    '<button type="submit" class="btn btn-outline-warning btn-block">Update callback</button>' +
                    '</div>' +
                    '<div class="col-md-2">' +
                    '<button id="callback_element_for_' + json.len_text + '" onclick="sendAjaxDeleteCallback(this);" type="button" class="btn btn-outline-danger btn-block">Delete callback</button>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</form>';

                document.getElementById("id_create_callback").reset();
                $('#id_no_element').remove();
                $('#id_callback_fields').append(object);
                var errors = $('#errors').find('div');

                for (var item = 0; item < errors.length; item++) {
                    errors[item].remove();
                }
            }
            else {
                var error = '<div class="alert alert-warning mt-2">' +
                    json.callback_error.react_text[0] +
                    '</div>';
                document.getElementById("id_create_callback").reset();
                $('#errors').append(error);
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});

function sendAjaxUpdateCallback(form) {
    console.log(form[1]);
    var callback_text = form[1];
    var react_text = form[2];

    $.ajax({
        type: 'POST',
        url: '{% url "update_callback_url" token=token %}',
        data: {
            callback_text: callback_text.value,
            react_text: react_text.value,
            index: react_text.name.split('_')[2],
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'update_callback'
        },
        success: function (json) {

        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function sendAjaxDeleteCallback(button) {
    var button_id = button.id.split('_')[3];
    console.log(button_id);

    $.ajax({
        type: 'GET',
        url: '{% url "delete_callback_url" token=token %}',
        data: {
            button_id: button_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'delete_callback'
        },
        success: function (json) {
            var elements = $('#id_callback_fields').find('form');
            elements[json.button_id].remove();
            var elements = $('#id_callback_fields').find('form');
            console.log(elements);

            for (var item = 0; item < elements.length; item++) {
                $(elements[item]).find('input')[1].name = `callback_text_${item}`;
                $(elements[item]).find('input')[2].name = `react_text_${item}`;
                $(elements[item]).find('button')[1].name = `callback_element_for_${item}`;
            }

            if (elements.length == 0) {
                $('#id_callback_fields').append(
                    '<div class="alert alert-success mt-3" role="alert" id="id_no_element"><h5 class="alert-heading mb-0 mt-0">No such elements added</h5><hr><p class="mt-0 mb-0">If you want to add new text response check the form below</p></div>'
                );
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    })
}