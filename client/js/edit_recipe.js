const server_url = sessionStorage.getItem('server_url');

async function update_recipe() {
    //сбор основной информации о рецепте
    const servings_cout = $('input[name="servings"]').val();
    const cook_time = $('input[name="hours"]').val() * 3600 + $('input[name="minutes"]').val() * 60;

    const details = {
        servings_cout: servings_cout,
        cook_time: cook_time,
    }

    const name = $('input[name="name"]').val().trim();

    if (name != recipe_name) {
        details.name = name;
    }

    if ($('textarea[name="recommendations"]').length) {
        const recommend = $('textarea[name="recommendations"]').val().trim();
        if (recommend) {
            details.recommend = recommend;
        } else {
            details.recomend_to_null = true;
        }
    }

    if (!name || !cook_time) {
        notification('Укажите основную информацию о рецепте.', 3000);
        return 0;
    }

    console.log(details);

    //подготовка основной информации к отправке
    let url_params = [];
    for (const property in details) {
        const encoded_key = encodeURIComponent(property);
        const encoded_value = encodeURIComponent(details[property]);
        url_params.push(encoded_key + '=' + encoded_value); 
    }
    url_params = url_params.join('&');

    const fetch_params = {
        method: 'PUT',
        credentials: 'include',
    }

    // получение фотографии рецепта
    let body = new FormData();
    if (recipe_photo) {
        body.append('photo', recipe_photo);
        fetch_params.body = body;
    }

    const query = server_url + 'recipes/' + $.urlParam('id') + '?' + url_params;

    const response = await fetch(query, fetch_params);
    console.log(response);

    if (response.ok) {
        const recipe = await response.json();
        console.log(recipe);

        $(location).attr('href', 'profile.html?tab=3');
    } else {
        notification('Рецепт с таким именем уже существует.', 3000);
    }
}

let recipe_name;

async function fill_recipe_info() {
    const query = server_url + 'recipes/' + $.urlParam('id');

    const response = await fetch(query, {
        credentials: 'include'
    });
    console.log(response);

    if (!response.ok) {
        sessionStorage.setItem('cant_find', true);
        $(location).attr('href', 'index.html');
    }

    const recipes = await response.json();
    const recipe = recipes[0]
    console.log(recipe);

    const recipe_desc = recipe['recipe_desc'];

    if (recipe_desc['author'] != sessionStorage.getItem('user_id')) {
        sessionStorage.setItem('no_rights', true);
        $(location).attr('href', 'index.html');
    }

    const img_src = server_url + 'recipes/photo/' + $.urlParam('id'); 
    $('#recipe_data img').attr('src', img_src);

    $('input[name="name"]').val(recipe_desc['name']);

    recipe_name = recipe_desc['name'];

    $('input[name="servings"]').val(recipe_desc['servings_cout']);

    if (recipe_desc['recommend']) {
        recommendations_container = $('#recommendations_container');
        recommendations_container.loadTemplate('templates/new_recipe/recommendations_tpl.html', null, {
            complete: function() {
                $('textarea[name="recommendations"]').val(recipe_desc['recommend']);
            }
        });
        $('#add_rec').hide();
    }

    const time = Number(recipe_desc['cook_time']);
    const hours = Math.floor(time / 3600);
    const minutes = time % 3600 / 60;

    $('input[name="hours"]').val(hours);
    $('input[name="minutes"]').val(minutes);
}

function on_add_rec_click() {
    recommendations_container = $('#recommendations_container');
    recommendations_container.loadTemplate('templates/new_recipe/recommendations_tpl.html');
    $('#add_rec').hide();
}

function on_decr_serv_click() {
    servings_input = $('#servings');
    servs = Number(servings_input.val());
    if (servs > servings_input.attr("min")) {
        servings_input.val(servs - 1);
    };
}

function on_incr_serv_click() {
    servings_input = $('#servings');
    servs = Number(servings_input.val());
    if (servs < servings_input.attr("max")) {
        servings_input.val(servs + 1);
    };
}

let recipe_photo;

$('document').ready(function() {
    if (!authorized()) {
        sessionStorage.setItem('unathorized_access', true);
        $(location).attr('href', 'index.html');
    }

    fill_recipe_info();

    $('#hours').focusout(function() {
        const hours_input = $('#hours');

        if(Number(hours_input.val()) > hours_input.attr('max')) {
            hours_input.val(hours_input.attr('max'));
        } else if (Number(hours_input.val()) < hours_input.attr('min')) {
            hours_input.val(hours_input.attr('min'));
        }
    });

    $('#minutes').focusout(function() {
        const minutes_input = $('#minutes');

        if(Number(minutes_input.val()) > minutes_input.attr('max')) {
            minutes_input.val(minutes_input.attr('max'));
        } else if (Number(minutes_input.val()) < minutes_input.attr('min')) {
            minutes_input.val(minutes_input.attr('min'));
        }
    });

    $('#recipe_photo').change(function() {
        recipe_photo = this.files[0];
        if (recipe_photo) {
            console.log(recipe_photo);

            $('#recipe_photo_img').attr('src', URL.createObjectURL(recipe_photo));
        }
    });

    limit_length('input[name="name"]', 100);
});