function getInlineValues(form) {
    var url = form.url;
    var switch_inline_current = form.switch_inline_current;
    var switch_inline = form.switch_inline;
    var callback = form.callback;

    var change_list = [
        '<input type="url" name="url" class="form-control" placeholder="Url" id="id_url" readonly>',
        '<input type="text" name="switch_inline" class="form-control" placeholder="Switch Inline Query" maxlength="50" id="id_switch_inline" readonly>',
        '<input type="text" name="switch_inline_current" class="form-control" placeholder="Switch Inline Current Chat" maxlength="50" id="id_switch_inline_current" readonly>',
        '<input type="text" name="callback" class="form-control" placeholder="Callback Data" maxlength="64" id="id_callback" readonly>'
    ]

    var initial_list = [
        '<input type="url" name="url" class="form-control" placeholder="Url" id="id_url">',
        '<input type="text" name="switch_inline" class="form-control" placeholder="Switch Inline Query" maxlength="50" id="id_switch_inline">',
        '<input type="text" name="switch_inline_current" class="form-control" placeholder="Switch Inline Current Chat" maxlength="50" id="id_switch_inline_current">',
        '<input type="text" name="callback" class="form-control" placeholder="Callback Data" maxlength="64" id="id_callback">'
    ]

    if (url.value.trim() != "") {
        switch_inline.outerHTML = change_list[1];
        switch_inline_current.outerHTML = change_list[2];
        callback.outerHTML = change_list[3];
    }
    else if (switch_inline_current.value.trim() != "") {
        switch_inline.outerHTML = change_list[1];
        url.outerHTML = change_list[0];
        callback.outerHTML = change_list[3];
    }
    else if (switch_inline.value.trim() != "") {
        url.outerHTML = change_list[0];
        switch_inline_current.outerHTML = change_list[2];
        callback.outerHTML = change_list[3];
    }
    else if (callback.value.trim() != "") {
        switch_inline.outerHTML = change_list[1];
        switch_inline_current.outerHTML = change_list[2];
        url.outerHTML = change_list[0];
    }
    else if (url.value.trim() == "" || switch_inline_current.value.trim() == "" || switch_inline.value.trim() == "" || callback.value.trim() == "") {
        url.outerHTML = initial_list[0];
        switch_inline.outerHTML = initial_list[1];
        switch_inline_current.outerHTML = initial_list[2];
        callback.outerHTML = initial_list[3];
    }
}


function buttonClick() {
    var code = editor.getValue();
    document.getElementById('code_hello_world').value = code;
}


function onCheck() {
    document.getElementById('text').className += ' disabled';
    document.getElementById('reply').className += ' disabled';
    document.getElementById('inline').className += ' disabled';
    document.getElementById('id_menu_callback').className += ' disabled';
}


function changeSome() {
    var react = document.getElementById('react_text_text');
    if (react.value.trim().startsWith('/')) {
        react.outerHTML = '<div class="input-group"><div class="input-group-prepend"><div class="input-group-text">/</div></div>]' + react + '</div>';
    }
}

