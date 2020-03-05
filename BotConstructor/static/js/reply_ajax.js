$(document).on('submit', '#id_reply_markup_create_form', function (e) {
    e.preventDefault();
    var checkboxes = $('#id_reply_checkboxes').find('input');
    var resize_keyboard = checkboxes[0].checked;
    var one_time_keyboard = checkboxes[1].checked;
    var selective_keyboard = checkboxes[2].checked;
    console.log(resize_keyboard, one_time_keyboard, selective_keyboard);

    $.ajax({
        type: 'POST',
        url: '{% url "create_bot_second_step_reply_markup_url" token=token %}',
        data: {
            react_text: $('#id_react_text').val(),
            row_width: $('#id_row_width').val(),
            response_text_markup: $('#id_response_text_markup').val(),
            resize_keyboard: resize_keyboard,
            one_time_keyboard: one_time_keyboard,
            selective_keyboard: selective_keyboard,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'create_reply_markup'
        },
        success: function (json) {
            var resize = json.resize_keyboard;
            var one_time = json.one_time_keyboard;
            var selective = json.selective;

            if (resize == true) {
                resize = 'checked';
            }
            else {
                resize = '';
            }

            if (one_time == true) {
                one_time = 'checked';
            }
            else {
                one_time = '';
            }

            if (selective == true) {
                selective = 'checked';
            }
            else {
                selective = '';
            }

            var object = '<div class="form-row mt-3" id="' + json.len_text + '_reply_element">' +
                '<div class="col-md-5">' +
                '<form onsubmit="sendAjaxUpdateReply(this); return false;" method="POST" class="mb-3">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + json.csrf + '">' +
                '<div class="form-row row">' +
                '<div class="col-md-8">' +
                '<div class="input-group">' +
                '<div class="input-group-prepend">' +
                '<div class="input-group-text">React</div>' +
                '</div>' +
                '<input class="form-control" name="react_text_' + json.len_text + '" value="' + json.react_text + '">' +
                '</div>' +
                '</div>' +
                '<div class="col-md-4">' +
                '<input class="form-control" name="row_width_' + json.len_text + '" value="' + json.row_width + '">' +
                '</div>' +
                '</div>' +
                '<div class="input-group">' +
                '<div class="input-group-prepend">' +
                '<div class="input-group-text mt-2">Response</div>' +
                '</div>' +
                '<input class="form-control mt-2" name="response_text_markup_' + json.len_text + '" value="asdasd">' +
                '</div>' +
                '<div class="form-row mt-2 mb-2">' +
                '<div class="ml-1">' +
                '<div class="custom-control custom-checkbox custom-control-inline">' +
                '<input type="checkbox" name="resize_keyboard_' + json.len_text + '" class="custom-control-input" ' + resize + ' id="res_key_' + json.len_text + '">' +
                '<label for="res_key_' + json.len_text + '" class="custom-control-label">Resize keyboard</label>' +
                '</div>' +
                '</div>' +
                '<div class="ml-1">' +
                '<div class="custom-control custom-checkbox custom-control-inline">' +
                '<input type="checkbox" name="one_time_keyboard_' + json.len_text + '" class="custom-control-input" ' + one_time + ' id="o_t_k_' + json.len_text + '">' +
                '<label for="o_t_k_' + json.len_text + '" class="custom-control-label">One time keyboard</label>' +
                '</div>' +
                '</div>' +
                '<div class="ml-1">' +
                '<div class="custom-control custom-checkbox custom-control-inline">' +
                '<input type="checkbox" name="selective_' + json.len_text + '" class="custom-control-input" ' + selective + ' id="s_' + json.len_text + '">' +
                '<label for="s_' + json.len_text + '" class="custom-control-label">Selective</label>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="form-row">' +
                '<div class="col-md-4">' +
                '<button type="submit" class="btn btn-outline-warning btn-sm btn-block">Update keyboard</button>' +
                '</div>' +
                '<div class="col-md-4">' +
                '<button type="button" id="reply_markup_' + json.len_text + '" onclick="sendAjaxDeleteReply(this); " class="btn btn-outline-danger btn-sm btn-block">Delete keyboard</button>' +
                '</div>' +
                '<div class="col-md-4">' +
                '<a href="/createBot/secondStep/944380578:AAEFvaqShiw164lLumAu2wI6w2ZnzSAJ7lM/replyMarkup/replyButtons/" class="btn btn-outline-dark btn-sm btn-block">Add button</a>' +
                '</div>' +
                '</div>' +
                '</form>' +
                '</div>' +
                '<div class="col-md-7"></div>' +
                '</div>';

            document.getElementById("id_reply_markup_create_form").reset();
            document.getElementById("id_reply_form").outerHTML = '<form id="id_reply_buttons_form" method="POST">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + json.csrf + '">' +
                '<div class="form-row">' +
                '<div class="col-md-10">' +
                '<input type="text" name="response_text" class="form-control" placeholder="Response Text" required="" id="id_response_text">' +
                '</div>' +
                '<div class="col-md-2">' +
                '<button type="submit" class="btn btn-outline-primary btn-block">Create Button</button>' +
                '</div>' +
                '</div>' +
                '<div class="form-row ml-0 mt-1">' +
                '<div class="custom-control custom-radio custom-control-inline">' +
                '<input id="id_radio_buttons_0" name="radio_buttons" type="radio" value="request_contact" class="custom-control-input">' +
                '<label for="id_radio_buttons_0" class="custom-control-label">Request Contact</label>' +
                '</div>' +
                '<div class="custom-control custom-radio custom-control-inline">' +
                '<input id="id_radio_buttons_1" name="radio_buttons" type="radio" value="request_location" class="custom-control-input">' +
                '<label for="id_radio_buttons_1" class="custom-control-label">Request Location</label>' +
                '</div>' +
                '</div>' +
                '</form>';

            $('#id_no_element').remove();
            $('#id_reply_elements').append(object);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});

function sendAjaxUpdateReply(form) {
    var react_text = $(form)[0][1];
    var row_width = $(form)[0][2];
    var response_text_markup = $(form)[0][3];
    var resize_keyboard = $(form)[0][4];
    var one_time_keyboard = $(form)[0][5];
    var selective = $(form)[0][6];


    $.ajax({
        type: 'POST',
        url: '{% url "create_bot_second_step_reply_markup_update_url" token=token %}',
        data: {
            react_text: react_text.value,
            row_width: row_width.value,
            response_text: response_text_markup.value,
            resize_keyboard: resize_keyboard.checked,
            one_time_keyboard: one_time_keyboard.checked,
            selective: selective.checked,
            index: react_text.name.split('_')[2],
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'update_reply_markup'
        },
        success: function (json) {

        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function sendAjaxDeleteReply(button) {
    var button_id = button.id.split('_');

    $.ajax({
        type: 'GET',
        url: '{% url "create_bot_second_step_reply_markup_delete_url" token=token %}',
        data: {
            button_id: button_id[2],
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'delete_reply_markup'
        },
        success: function (json) {
            var elements = $('#id_reply_elements').find('div[class^="form-row mt-3"]');
            elements[json.markup_id].remove();
            var elements = $('#id_reply_elements').find('div[class^="form-row mt-3"]');
            console.log(elements);

            for (var item = 0; item < elements.length; item++) {
                $(elements[item]).find('input')[1].name = `react_text_${item}`;
                $(elements[item]).find('input')[2].name = `row_width_${item}`;
                $(elements[item]).find('input')[3].name = `response_text_markup_${item}`;
                $(elements[item]).find('input')[4].name = `resize_keyboard_${item}`;
                $(elements[item]).find('input')[4].id = `res_key_${item}`;
                $(elements[item]).find('input')[5].name = `one_time_keyboard_${item}`;
                $(elements[item]).find('input')[5].id = `o_t_k_${item}`;
                $(elements[item]).find('input')[6].name = `selective_${item}`;
                $(elements[item]).find('input')[6].id = `s_${item}`;
                $(elements[item]).find('label')[0].outerHTML = `<label for="res_key_${item}" class="custom-control-label">Resize keyboard</label>`;
                $(elements[item]).find('label')[1].outerHTML = `<label for="o_t_k_${item}" class="custom-control-label">One time keyboard</label>`;
                $(elements[item]).find('label')[2].outerHTML = `<label for="s_${item}" class="custom-control-label">Selective</label>`;
                $(elements[item]).find('div').prevObject[0].id = `${item}_reply_element`;
                $(elements[item]).find('button')[1].id = `reply_markup_${item}`;
            }

            if (elements.length == 0) {
                $('#id_reply_elements').append(
                    '<div class="alert alert-success mt-3" role="alert" id="id_no_element"><h5 class="alert-heading mb-0 mt-0">No such elements added</h5><hr><p class="mt-0 mb-0">If you want to add new text response check the form below</p></div>'
                );
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

$(document).on('submit', '#id_reply_buttons_form', function (e) {
    e.preventDefault();

    if ($('#id_radio_buttons_0').is(':checked') == true) {
        request_contact = 'checked';
    }
    else {
        request_contact = '';
    }

    if ($('#id_radio_buttons_1').is(':checked') == true) {
        request_location = 'checked';
    }
    else {
        request_location = '';
    }

    $.ajax({
        type: 'POST',
        url: '',
        data: {
            response_text: $('#id_response_text').val(),
            request_contact: $('#id_radio_buttons_0').is(':checked'),
            request_location: $('#id_radio_buttons_1').is(':checked'),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'create_reply_button'
        },
        success: function (json) {
            console.log(json);
            var object = '<form action="/createBot/secondStep/812889787:AAGLeU_UBeNkGGHTZ1bJWXsfnnlTeBwE0ZU/replyMarkup/updateReplyButtons/" method="POST" class="mb-3">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + json.csrf + '">' +
                '<div class="input-group">' +
                '<div class="input-group-prepend">' +
                '<div class="input-group-text">Text</div>' +
                '</div>' +
                '<input class="form-control" name="response_text_' + json.len_text + '_' + json.len_button + '" value="' + json.response_text + '">' +
                '</div>' +
                '<div class="form-row mt-1 mb-1 ml-0">' +
                '<div class="custom-control custom-radio custom-control-inline">' +
                '<input type="radio" name="radio_buttons_' + json.len_text + '_' + json.len_button + '" value="request_contact" ' + request_contact + ' class="custom-control-input" id="req_con_' + json.len_button + '">' +
                '<label for="req_con_' + json.len_button + '" class="custom-control-label">Request contact</label>' +
                '</div>' +
                '<div class="custom-control custom-radio custom-control-inline">' +
                '<input type="radio" name="radio_buttons_' + json.len_text + '_' + json.len_button + '" value="request_location" ' + request_location + ' class="custom-control-input" id="req_loc_' + json.len_button + '">' +
                '<label for="req_loc_' + json.len_button + '" class="custom-control-label">Request location</label>' +
                '</div>' +
                '</div>' +
                '<div class="form-row">' +
                '<div class="col-md-6">' +
                '<button type="submit" class="btn btn-outline-warning btn-sm btn-block">Update button</button>' +
                '</div>' +
                '<div class="col-md-6">' +
                '<a href="/createBot/secondStep/812889787:AAGLeU_UBeNkGGHTZ1bJWXsfnnlTeBwE0ZU/replyMarkup/deleteReplyButton/' + json.len_text + '/' + json.len_button + '/" class="btn btn-outline-danger btn-sm btn-block">Delete button</a>' +
                '</div>' +
                '</div>' +
                '</form>';

            document.getElementById('id_reply_buttons_form').reset();
            $('#' + json.len_text + '_reply_element').find('div.col-md-7').append(object);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});