$(document).on('submit', '#text-form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "create_bot_second_step_text_url" token=token %}',
        data: {
            react_text: $('#id_react_text').val(),
            response_text: $('#id_response_text').val(),
            remove_reply: $('#id_remove_reply_markup_0').is(':checked'),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function (json) {
            var object = '';
            object += `<form method="POST" class="mt-3" onsubmit="sendAjaxUpdate(this); return false;">` +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + json.csrf + '">' +
                '<div class="form-row mb-3">' +
                '<div class="col-md-9">' +
                '<input class="form-control" name="react_text_' + json.len_text + '" value="' + json.react_text + '">' +
                '</div>' +
                '<div class="col-md-3">' +
                '<div class="form-row">' +
                '<div class="col-md-6">' +
                '<button type="submit" class="btn btn-outline-success btn-block">Update</button>' +
                '</div>' +
                '<div class="col-md-6">' +
                '<button type="button" id="id_delete_text_' + json.len_text + '" class="btn btn-outline-danger btn-block" onclick="sendAjaxDelete(this);">Delete</button>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-12">' +
                `<textarea class="form-control mt-2" style="height: 100%;" name="response_text_` + json.len_text + `" id="response_text_text">` + json.response_text + `</textarea>` +
                '</div>' +
                '<div class="col-md-12 mt-2">' +
                '<div class="custom-control custom-checkbox custom-control-inline">';

            if (json.remove_reply_markup) {
                object += '<input type="checkbox" name="remove_reply_markup_' + json.len_text + '" class="custom-control-input" id="remove_reply_markup_' + json.len_text + '" checked>' +
                    '<label for="remove_reply_markup_' + json.len_text + '" class="custom-control-label">Remove Reply Markup</label>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</form>';
            }
            else {
                object += '<input type="checkbox" name="remove_reply_markup_' + json.len_text + '" class="custom-control-input" id="remove_reply_markup_' + json.len_text + '">' +
                    '<label for="remove_reply_markup_' + json.len_text + '" class="custom-control-label">Remove Reply Markup</label>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</form>';
            }

            document.getElementById("text-form").reset();
            $("#id_no_element").remove();
            $(".text_fields").append(
                object
            );
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});

function sendAjaxDelete(button) {
    $.ajax({
        type: 'GET',
        url: '{% url "create_bot_second_step_text_delete_url" token=token %}',
        data: {
            button_id: button.id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'delete_text'
        },
        success: function (json) {
            var elements = $('.text_fields').find('form');
            elements[json.button_id].remove();
            var elements = $('.text_fields').find('form');

            for (var item = 0; item < elements.length; item++) {
                $(elements[item]).find('input')[1].name = `react_text_${item}`;
                $(elements[item]).find('button')[1].id = `id_delete_text_${item}`;
                $(elements[item]).find('input')[2].id = `remove_reply_markup_${item}`;
                $(elements[item]).find('input')[2].name = `remove_reply_markup_${item}`;
                $(elements[item]).find('textarea')[0].name = `response_text_${item}`;
                $(elements[item]).find('label')[0].outerHTML = `<label for="remove_reply_markup_${item}" class="custom-control-label">Remove Reply Markup</label>`;
            }

            if (elements.length == 0) {
                $('.text_fields').append(
                    '<div class="alert alert-success mt-3" role="alert" id="id_no_element"><h5 class="alert-heading mb-0 mt-0">No such elements added</h5><hr><p class="mt-0 mb-0">If you want to add new text response check the form below</p></div>'
                )
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function sendAjaxUpdate(form) {
    var react_text = $(form).find('input')[1];
    var remove_reply_markup = $(form).find('input')[2];
    var response_text = $(form).find('textarea')[0];

    $.ajax({
        type: 'POST',
        url: '{% url "create_bot_second_step_text_update_url" token=token %}',
        data: {
            react_text: [react_text.name, react_text.value],
            response_text: [response_text.name, response_text.value],
            remove_reply_markup: [remove_reply_markup.name, remove_reply_markup.checked],
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'update_text'
        },
        success: function (json) {

        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}