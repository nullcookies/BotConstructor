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

var editor = ace.edit("editor");
editor.setTheme("ace/theme/github");
editor.session.setMode("ace/mode/python");
editor.setFontSize(15);

function buttonClick() {
    var code = editor.getValue();
    document.getElementById('code_hello_world').value = code;
}


function onCheck() {
    if (document.getElementById('id_templates_0').checked) {
        document.getElementById('text').className += ' disabled';
        document.getElementById('reply').className += ' disabled';
        document.getElementById('inline').className += ' disabled';
    }
}
