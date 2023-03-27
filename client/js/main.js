sessionStorage.setItem('server_url', 'http://localhost:8000/');

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}

function search_btn_click() {
    if ($('.searchbar').val()) {
        let href = 'search.html?query=';
        href += $('.searchbar').val();
        $(location).attr('href', href);
    }
};

$.fn.popup = function() {
    this.css('position', 'absolute').fadeIn();
    this.css('top', ($(window).height() - this.height()) / 2 + $(window).scrollTop() - $('header').height() + 'px');
    $('.modal-back').fadeIn();
    $('body').css('overflow', 'hidden');
}

function on_profile_btn_click() {
    if (authorized()) {
        const href = "profile.html?tab=1";
        $(location).attr('href', href);
    } else {
        $('#sign_in_modal').popup();
    }
}

function on_fav_btn_click() {
    if (authorized()) {
        const href = "profile.html?tab=2";
        $(location).attr('href', href);
    } else {
        $('#sign_in_modal').popup();
    }
}

function on_add_recipe_btn_click() {
    if (authorized()) {
        const href = "new_recipe.html";
        $(location).attr('href', href);
    } else {
        $('#sign_in_modal').popup();
    }
}

function on_sign_up_click() {
    event.preventDefault();
    $('.auth-modal').fadeOut();
    $('#sign_up_modal').popup();
}

function on_sign_in_click() {
    event.preventDefault();
    $('.auth-modal').fadeOut();
    $('#sign_in_modal').popup();
}

async function sign_in() {
    // предположение о корректности введенных данных
    $('#sign_in_modal .hint').html('');
    let approved = true;

    // проверка заполнения всех полей
    $('#sign_in_modal input').each(function(index, element) {
        if ($(element).val().trim() == '') {
            $('#sign_in_modal .hint').html('Все поля обязательны к заполнению.');
            approved = false;
        }
    })

    // тут должны быть проверки

    //если все проверки пройдены, авторизационный запрос
    if (approved) {
        const query = server_url + 'auth/jwt/login';
        let fetch_params = {
            method: 'POST',
            credentials: 'include',
        }

        const headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        };

        // приведение body к типу x-www-form-urlencoded
        const details = {
            username: $('#sign_in_modal input[name="login"]').val(),
            password: $('#sign_in_modal input[name="password"]').val()
        };

        let body = [];
        for (const property in details) {
            const encoded_key = encodeURIComponent(property);
            const encoded_value = encodeURIComponent(details[property]);
            body.push(encoded_key + '=' + encoded_value); 
        }
        body = body.join('&');

        fetch_params.headers = headers;
        fetch_params.body = body;

        const response = await fetch(query, fetch_params);
        console.log(response);

        const result = await response.json();
        console.log(result);

        if (response.ok) {
            // при успешной авторизации создаем в хранилище флаг "авторизован"
            sessionStorage.setItem('authorized', true);
        } else {
            $('#sign_in_modal .hint').html('Такого пользователя не существует.');
        }
        
        $('.modal-back').click();

    }
}

function authorized() {
    return (sessionStorage.getItem('authorized') ? true : false);
}

$('document').ready(function() { 
    var header_container = $('header');
    header_container.loadTemplate("templates/main/header_tpl.html", {});

    if (authorized()) {
        var footer_container = $('footer');
        footer_container.loadTemplate("templates/main/footer_tpl.html", {});
    }
    

    $('#modals_container').loadTemplate('templates/main/sign_up_modal_tpl.html', null, {
        append: true
    });
    
    $('#modals_container').loadTemplate('templates/main/sign_in_modal_tpl.html', null, {
        append: true
    });

    $('.modal-back').click(function(){
        $('.auth-modal').fadeOut();
        $('.modal-back').fadeOut();
        $('body').css('overflow', 'auto');
    });
});