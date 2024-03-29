sessionStorage.setItem('server_url', 'http://localhost:8000/');
server_url = sessionStorage.getItem('server_url');

const WHITE = "#fff";
const PINK = "#ff2787";
const RED = "#e64343";
const GREEN = "#61b030";

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

function on_fav_recipes_btn_click() {
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

async function get_current_user() {
    const query = server_url + 'users/current/';

    const response = await fetch(query, {
        credentials: 'include',
    });
    console.log(response);

    const user = await response.json();
    console.log(user);

    console.log(user['id']);

    sessionStorage.setItem('user_id', user['id']);

    const img_src = server_url + 'users/photo?user_id=' + sessionStorage.getItem('user_id');
    $('.profile-pic img').attr('src', img_src);
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
            get_current_user().then(function() {
                $('.modal-back').click();
                sessionStorage.setItem('authorized', true);
                location.reload();
            })
        } else {
            $('#sign_in_modal .hint').html('Такого пользователя не существует.');
        }
    }
}

async function sign_up() {
    // предположение о корректности введенных данных
    $('#sign_up_modal .hint').html('');
    let approved = true;

    // проверка заполнения всех полей
    $('#sign_up_modal input').each(function(index, element) {
        if ($(element).val().trim() == '') {
            $('#sign_up_modal .hint').html('Все поля обязательны к заполнению.');
            approved = false;
        }
    })

    // проверка совпадения пароля и проверки
    const password = $('#sign_up_modal input[name="password"]').val();
    const password_confirmation = $('#sign_up_modal input[name="password_confirmation"]').val();
    if (password != password_confirmation) {
        $('#sign_up_modal .hint').html('Пароли должны совпадать.');
        approved = false;
    }

    // проверка корректности адреса электронной почты
    const EMAIL_REGEXP = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;

    const email = $('#sign_up_modal input[name="email"]').val();
    if (!EMAIL_REGEXP.test(email)) {
        $('#sign_up_modal .hint').html('Предложен некорректный адрес электронной почты.');
        approved = false;
    }

    // тут должны быть проверки

    //если все проверки пройдены, регистрационный запрос
    if (approved) {
        const query = server_url + 'auth/register';
        let fetch_params = {
            method: 'POST',
            credentials: 'include',
        }

        const headers = {
            "Content-Type": "application/json",
        };

        const body = {
            email: $('#sign_up_modal input[name="email"]').val(),
            password: $('#sign_up_modal input[name="password"]').val(),
            is_active: true,
            is_superuser: false,
            is_verified: false,
            login: $('#sign_up_modal input[name="login"]').val(),
        };


        fetch_params.headers = headers;
        fetch_params.body = JSON.stringify(body);

        const response = await fetch(query, fetch_params);
        console.log(response);

        const result = await response.json();
        console.log(result);

        if (response.ok) {
            $('.modal-back').click();

            notification('Вы успешно зарегистрировались!', 2500);
        } else {
            $('#sign_up_modal .hint').html('Такой пользователь уже существует.');
        }
    }
}

function authorized() {
    return (sessionStorage.getItem('user_id') != null ? true : false);
}

function notification(text, duration) {
    $('#notification').remove();
    $('body').loadTemplate('templates/main/notification_tpl.html', {
        text: text
    }, {
        append: true,
        complete: function() {
            const notification = $('#notification');
            setTimeout(function() {
                notification.remove();
            }, duration)
        }
    })
}

function close_menus() {
    $('.menu-block > div').each(function(index, element) {
        $(element).css('display', 'none');
    })
}

function limit_length(selector, limit) {
    $(selector).keyup(function() {
        const value = $(this).val();
        $(this).val(value.slice(0, limit))
    });
}

$('document').ready(function() { 
    var header_container = $('header');
    header_container.loadTemplate("templates/main/header_tpl.html", null, {
        complete: function() {
            const img_src = server_url + 'users/photo?user_id=' + sessionStorage.getItem('user_id');
            $('.profile-pic img').attr('src', img_src);
            $('#sidebar_btn').click(function(event) {
                event.preventDefault();
                $('.sidebar-block').css('top', $('header').height());
        
                if ($('.sidebar-menu').css('display') == 'none') {
                    close_menus();
                    $('.sidebar-menu').css('display', 'block');
                    $('.sidebar-menu').animate({opacity: 1}, 300);
                } else {
                    $('.sidebar-menu').animate({opacity: 0}, 300, function() {
                        $('.sidebar-menu').css('display', 'none');
                    });
                }
            })

            limit_length('.searchbar', 100);
        }
    });

    var footer_container = $('footer');
    footer_container.loadTemplate("templates/main/footer_tpl.html", null);

    $('#modals_container').loadTemplate('templates/main/sign_up_modal_tpl.html', null, {
        append: true,
        complete: function() {
            limit_length('#sign_up_modal input[name="login"]', 50);
            limit_length('#sign_up_modal input[name="password"]', 255);
            limit_length('#sign_up_modal input[name="password_confirmation"]', 255);
            limit_length('#sign_up_modal input[name="email"]', 100);
        }
    });
    
    $('#modals_container').loadTemplate('templates/main/sign_in_modal_tpl.html', null, {
        append: true,
        complete: function() {
            limit_length('#sign_in_modal input[name="login"]', 50);
            limit_length('#sign_in_modal input[name="password"]', 255);
        }
    });

    if(sessionStorage.getItem('unathorized_access')) {
        notification('Для доступа к этой странице необходима авторизация.', 3000);
        sessionStorage.removeItem('unathorized_access');
    }

    if(sessionStorage.getItem('cant_find')) {
        notification('Страница не найдена.', 2500);
        sessionStorage.removeItem('cant_find');
    }

    if(sessionStorage.getItem('authorized')) {
        notification('Вы успешно авторизовались!', 2500);
        sessionStorage.removeItem('authorized');
    }

    if(sessionStorage.getItem('no_rights')) {
        notification('У вас нет прав для доступа к этой странице.', 3000);
        sessionStorage.removeItem('no_rights');
    }

    $('.modal-back').click(function(){
        $('.auth-modal').fadeOut();
        $('.modal-back').fadeOut();
        $('body').css('overflow', 'auto');
    });
});