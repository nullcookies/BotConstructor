var countHover = 0;
var params = {};
var currentToken = '';

function getCredentialsOfBot(form) {
    var token = $(form).find('#id_access_token').val();

    if (token !== currentToken) {
        currentToken = token;
        params = {};
        countHover = 0;
    }

    if (token !== '' && token.length >= 44) {
        if (countHover === 0) {
            document.getElementById('input_access').innerHTML = `<div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text">
                        <div class="spinner-border text-dark" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                    </span>
                </div>
                <input type="text" name="access_token" class="form-control shadow-sm" placeholder="Access Token" required="" id="id_access_token" value="` + token + `">
            </div>`;
            countHover += 1;
        }

        if (Object.keys(params).length === 0) {
            $.ajax({
                type: 'POST',
                url: '/until-first-step/',
                data: {
                    token: token,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (json) {
                    if ('title' in json && "username" in json) {
                        document.getElementById('id_title').value = json.title;
                        document.getElementById('id_username').value = json.username;
                        if (!(json.button)) {
                            document.getElementById('id_button_nxt').setAttribute('disabled', 'disabled');
                        }
                        else {
                            document.getElementById('id_button_nxt').removeAttribute('disabled');
                            document.getElementById('input_access').innerHTML = `<input type="text" name="access_token" class="form-control shadow-sm" placeholder="Access Token" required="" id="id_access_token" value="` + token + `">`;
                            params = json;
                            currentToken = token;
                        }
                    }
                    else {
                        document.getElementById('id_button_nxt').setAttribute('disabled', 'disabled');
                    }
                },
                error: function (xhr, errmsg, err) {

                }
            });
        }
    }
}