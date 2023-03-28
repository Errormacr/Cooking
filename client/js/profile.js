const server_url = sessionStorage.getItem('server_url');

async function fetch_user() {
    const query = server_url + 'users/?user_id=' + sessionStorage.getItem('user_id');
    
    const response = await fetch(query, {
        credentials: 'include'
    })
    console.log(response);

    const user = await response.json();
    console.log(user);
    
    const img_src = server_url + 'users/photo?user_id=' + sessionStorage.getItem('user_id');
    $('.round-img').attr('src', img_src);

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
            $('.hint').html('Пожалуйста, укажите личную информацию.');
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
    
        const query = server_url + 'users?' + url_params;
        
        const response = await fetch(query, {
            method: 'PUT',
            credentials: 'include',
            // body: фотография
        });
        console.log(response);

        $('#save_btn').hide();
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

    fav_recipes_data = [];

    recipes.forEach(recipe => {
        const recipe_desc = recipe['recipe_desc'];

        let time = Number(recipe_desc['cook_time']);
        const hours = Math.floor(time / 3600);
        const minutes = time % 3600 / 60;
        
        time = (hours != 0 ? hours + ' ч' : "") + " " + (minutes != 0 ? minutes + ' мин' : "");

        const img_src = server_url + 'recipes/photo/' + recipe['recipe_id'];


        fav_recipes_data.push(
            {
                name: recipe_desc['name'],
                time: time,
                img_src: img_src,
                href: 'recipe.html?id=' + recipe['recipe_id']
            }
        )
    });

    $('#recipes_container').loadTemplate('templates/profile/fav_recipe_card_tpl.html', fav_recipes_data);

}

function on_fav_recipes_click() {
    $('.menu').css('background', 'linear-gradient(to right, #d9d9d9 33%, #61b030 33% 66%, #d9d9d9 66%)');
    $('#profile_data').css('color', '');
    $('#favourite_recipes').css('color', '#fff');
    $('#users_recipes').css('color', '');
    
    


    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/recipes_container_tpl.html', null, {
        complete: function() {
            fetch_fav_recipes();
        }
    });
}

function on_users_recipes_click() {
    $('.menu').css('background', 'linear-gradient(to right, #d9d9d9 66%, #61b030 66%)');
    $('#profile_data').css('color', '');
    $('#favourite_recipes').css('color', '');
    $('#users_recipes').css('color', '#fff');

    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/users_recipe_card_tpl.html');
}

$('document').ready(function() {
    if (!authorized()) {
        $(location).attr('href', 'index.html');
    }

    tab = $.urlParam('tab')
    if (tab == 1) {
        $('#profile_data').click();
    } else if (tab == 2) {
        $('#favourite_recipes').click();
    }
});