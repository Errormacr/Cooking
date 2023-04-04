const server_url = sessionStorage.getItem('server_url');

function set_photo() {
    const img_src = server_url + 'users/photo?user_id=' + sessionStorage.getItem('user_id');
    $('.round-img').attr('src', img_src);
}

async function fetch_user() {
    const query = server_url + 'users/?user_id=' + sessionStorage.getItem('user_id');
    
    const response = await fetch(query, {
        credentials: 'include'
    })
    console.log(response);

    const user = await response.json();
    console.log(user);

    $('input[name="login"]').val(user['login']);
    $('input[name="firstname"]').val(user['name']);
    $('input[name="lastname"]').val(user['s_name']);
    $('input[name="date_of_birth"]').val(user['b_day']);
    $('input[name="sex"]').val(user['gender']);
    $('input[name="email"]').val(user['email']);
}

async function update_user() {
    let approved = true;
    
    $('#profile_data input').each(function(index, element) {
        if ($(element).val().trim() == '') {
            approved = false;
        }
    })

    // тут должны быть проверки

    if (approved) {
        const details = {
            login: $('input[name="login"]').val(),
            email: $('input[name="email"]').val(),
            name: $('input[name="firstname"]').val(),
            s_name: $('input[name="lastname"]').val(),
            b_day: $('input[name="date_of_birth"]').val()+'T00:00',
            gender: ($('input[name="sex"]').val() == 'Мужской' ? 'М' : 'Ж'),
        };
    
        let url_params = [];
        for (const property in details) {
            const encoded_key = encodeURIComponent(property);
            const encoded_value = encodeURIComponent(details[property]);
            url_params.push(encoded_key + '=' + encoded_value); 
        }
        url_params = url_params.join('&');

        let fetch_params = {
            method: 'PUT',
            credentials: 'include',
        }

        if (profile_photo) {
            let body = new FormData();
            body.append('photo', profile_photo);
            fetch_params.body = body;
        }

        const query = server_url + 'users?' + url_params;
        
        const response = await fetch(query, fetch_params);
        console.log(response);

        $('#save_btn').hide();
    } else {
        notification('Пожалуйста, укажите всю личную информацию.', 3000);
    }
}

async function logout() {
    const query = server_url + 'auth/jwt/logout';
        
    const response = await fetch(query, {
        method: 'POST',
        credentials: 'include',
    });
    console.log(response);

    sessionStorage.removeItem('user_id');
    $(location).attr('href', 'index.html');
}

function on_prof_data_click() {
    $('.menu').css('background', 'linear-gradient(to right, #61b030 33%, #d9d9d9 33%)');
    $('#profile_data').css('color', '#fff');
    $('#favourite_recipes').css('color', '');
    $('#users_recipes').css('color', '');

    $('.change-photo').show();

    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/profile_data_tpl.html', null, {
        complete: function() {
            $('#save_btn').hide();
            $('#profile_data input').focus(function() {
                $('#save_btn').show();
            });
            fetch_user();
        }
    });
}



async function fetch_fav_recipes() {
    const query = server_url + 'users/' + sessionStorage.getItem('user_id') + '/favourite';

    const response = await fetch(query, {
        credentials: 'include'
    });
    console.log(response);

    const recipes = await response.json();
    console.log(recipes);

    let fav_recipes_data = [];

    recipes.forEach(recipe => {
        const recipe_desc = recipe['recipe_desc'];

        let time = Number(recipe_desc['cook_time']);
        const hours = Math.floor(time / 3600);
        const minutes = time % 3600 / 60;
        
        time = (hours != 0 ? hours + ' ч' : "") + " " + (minutes != 0 ? minutes + ' мин' : "");

        const img_src = server_url + 'recipes/photo/' + recipe['recipe_id'];


        fav_recipes_data.push(
            {
                fav_alt: recipe['recipe_id'],
                name: recipe_desc['name'],
                rating: recipe_desc['rating'],
                time: time,
                img_src: img_src,
                href: 'recipe.html?id=' + recipe['recipe_id']
            }
        )
    });

    $('#recipes_container').loadTemplate('templates/profile/fav_recipe_card_tpl.html', fav_recipes_data);

}

async function delete_fav(recipe_id) {
    // окна "вы уверены..."

    const query = server_url + 'users/favourite?recipe_id=' + recipe_id;

    const response = await fetch(query, {
        method: 'DELETE',
        credentials: 'include'
    });
    console.log(response);
}

function on_delete_fav_click(element) {
    $(element).parents('.recipe-card').animate({
        opacity: 0
    }, 400, function() {
        const recipe_id = $(element).attr('alt');

        delete_fav(recipe_id).then(function() {
            notification('Рецепт удален из избранного.', 2500);

            $('#favourite_recipes').click();
        });
    });
}

function on_fav_recipes_click() {
    $('.menu').css('background', 'linear-gradient(to right, #d9d9d9 33%, #61b030 33% 66%, #d9d9d9 66%)');
    $('#profile_data').css('color', '');
    $('#favourite_recipes').css('color', '#fff');
    $('#users_recipes').css('color', '');

    $('.change-photo').hide();

    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/recipes_container_tpl.html', null, {
        complete: function() {
            fetch_fav_recipes();
        }
    });
}



async function fetch_users_recipes() {
    const query = server_url + 'recipes/get/?limit=100&author=' + sessionStorage.getItem('user_id');

    const response = await fetch(query, {
        method: 'POST',
        credentials: 'include'
    });
    console.log(response);

    const recipes = await response.json();
    console.log(recipes);

    let users_recipes_data = [];

    recipes.forEach(recipe => {
        let time = Number(recipe['cook_time']);
        const hours = Math.floor(time / 3600);
        const minutes = time % 3600 / 60;
        
        time = (hours != 0 ? hours + ' ч' : "") + " " + (minutes != 0 ? minutes + ' мин' : "");

        const img_src = server_url + 'recipes/photo/' + recipe['recipe_id'];


        users_recipes_data.push(
            {
                edit_alt: recipe['recipe_id'],
                delete_alt: recipe['recipe_id'],
                name: recipe['name'],
                rating: recipe['rating'],
                time: time,
                img_src: img_src,
                href: 'recipe.html?id=' + recipe['recipe_id']
            }
        )
    });

    $('#recipes_container').loadTemplate('templates/profile/users_recipe_card_tpl.html', users_recipes_data);
}

function edit_recipe(element) {
    // редирект на стр редактирования рецепта + id рецепта
    console.log('edit ', $(element).attr('alt'));
}

async function delete_recipe(element) {
    // окна "вы уверены..."
    console.log('delete ', $(element).attr('alt'))
    
    const recipe_id = $(element).attr('alt');
    
    const query = server_url + 'recipes/' + recipe_id;
    
    const response = await fetch(query, {
        method: 'DELETE',
        credentials: 'include'
    });
    console.log(response);

    notification('Рецепт удален.', 2500);
    $('#users_recipes').click();
}

function on_users_recipes_click() {
    $('.menu').css('background', 'linear-gradient(to right, #d9d9d9 66%, #61b030 66%)');
    $('#profile_data').css('color', '');
    $('#favourite_recipes').css('color', '');
    $('#users_recipes').css('color', '#fff');

    $('.change-photo').hide();

    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/recipes_container_tpl.html', null, {
        complete: function() {
            fetch_users_recipes();
        }
    });
}

let profile_photo;

$('document').ready(function() {
    if (!authorized()) {
        sessionStorage.setItem('unathorized_access', true);
        $(location).attr('href', 'index.html');
    }

    set_photo();

    tab = $.urlParam('tab')
    if (tab == 1) {
        $('#profile_data').click();
    } else if (tab == 2) {
        $('#favourite_recipes').click();
    } else if (tab == 3) {
        $('#users_recipes').click();
    }

    $('#profile_photo').change(function() {
        $('#save_btn').show();
        profile_photo = this.files[0];
        if (profile_photo) {
            $('.round-img').attr('src', URL.createObjectURL(profile_photo));
        }
    });

});
