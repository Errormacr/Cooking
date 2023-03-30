const server_url = sessionStorage.getItem('server_url');

let curr_ingredient = 0;

async function fetch_ingredients_list() {
    const query = server_url + 'ingredient/?limit=1000';

    const response = await fetch(query, {
        credentials: 'include'
    });
    console.log(response);

    const ingredients = await response.json();
    console.log(ingredients);

    ingredients.forEach(ingredient => {
        $('#ingredients_list').loadTemplate('templates/new_recipe/ingredient_option_tpl.html', {
            ingredient_id: ingredient['id'],
            value: ingredient['name']
        }, {
            append: true,
        })
    });
}

async function fetch_unit(element) {
    const ingredient_name = $(element).val();
    console.log(ingredient_name);

    const query = server_url + 'ingredient/?ingredient_name=' + encodeURIComponent(ingredient_name);

    const response = await fetch(query, {
        credentials: 'include'
    });
    console.log(response);

    const ingredients = await response.json();
    const ingredient = ingredients[0];
    console.log(ingredient);

    $('#ingredient_' + curr_ingredient + ' input[name=unit]').val(ingredient['unit']);
}

function on_add_ingr_click() {
    let can_add = true;
    $('#ingredient_' + curr_ingredient + ' input').each(function (index, element) {
        if ($(element).val().trim() == '' && can_add) {
            can_add = false;
            notification('Сначала заполните текущий ингредиент.', 2500);
        }
    });

    if (can_add) {
        curr_ingredient++;

        ingredients_container = $('#ingredients_container');
        ingredients_container.loadTemplate('templates/new_recipe/ingredient_tpl.html', {
            ingredient_id: 'ingredient_' + curr_ingredient,
            deletion_btn_id: 'delete_ingredient_' + curr_ingredient,
        }, {
            append: true,
            complete: function() {
                $('#ingredient_' + curr_ingredient + ' input[name=ingredient]').focus();
                $('#ingredient_' + curr_ingredient + ' input[name=ingredient]').change(function() {
                    fetch_unit(this);
                });
                $('#delete_ingredient_' + curr_ingredient + ' .delete-btn').click(function() {
                    const ingr_to_del = $(this).parents('.row').attr('id').split('_').pop();
                    $('#ingredient_' + ingr_to_del).remove();
                    $('#delete_ingredient_' + ingr_to_del).remove();
                });
            }
        });
    }
}

let curr_step = 0;

function on_add_step_click() {
    curr_step++;

    steps_container = $('#steps_container');
    steps_container.loadTemplate('templates/new_recipe/step_tpl.html', {
        step_id: 'step_' + curr_step,
        deletion_btn_id: 'delete_step_' + curr_step,
        step_media_id: 'step_media_container_' + curr_step
    }, {
        append: true,
        complete: function() {
            $('#step_' + curr_step + ' input[name=step]').focus();
            $('#step_' + curr_step + ' .timer-row input').focusout(function() {
                if(Number($(this).val()) > $(this).attr('max')) {
                    $(this).val($(this).attr('max'));
                } else if (Number($(this).val()) < $(this).attr('min')) {
                    $(this).val($(this).attr('min'));
                }
            });
            $('#delete_step_' + curr_step + ' .delete-btn').click(function() {
                const step_to_del = $(this).parents('.row').attr('id').split('_').pop();
                $('#step_' + step_to_del).remove();
                $('#delete_step_' + step_to_del).remove();
            });
            $('#step_media_container_' + curr_step + ' input').attr('id', 'step_media_' + curr_step);
            $('#step_media_container_' + curr_step + ' label:eq(1)').attr('for', 'step_media_' + curr_step);
            $('#step_media_container_' + curr_step + ' label:eq(1)').attr('id', 'step_media_label_container_' + curr_step);
            $('#step_media_container_' + curr_step).click(function() {
                const new_step_id = $(this).attr('id').split('_').pop();
                $('#step_media_container_' + new_step_id + ' input').change(function() {
                    const step_media = this.files[0];
                    console.log(step_media);
                    steps_files.set(new_step_id, step_media);

                    const step_media_url = URL.createObjectURL(step_media);
                    if (step_media.type.startsWith('image/')) {
                        $('#step_media_label_container_' + new_step_id).loadTemplate('templates/new_recipe/step_img_tpl.html', {
                            url: step_media_url
                        })
                    } else if (step_media.type.startsWith('video/')) {
                        $('#step_media_label_container_' + new_step_id).html('Видео...')
                    }
                })
            })
        }
    });
}

function on_add_rec_click() {
    recommendations_container = $('#recommendations_container');
    recommendations_container.loadTemplate('templates/new_recipe/recommendations_tpl.html');
    $('#add_rec').hide();
}

let curr_tag = 0;

async function fetch_tags_list() {
    const query = server_url + 'tag/?limit=1000';

    const response = await fetch(query, {
        credentials: 'include'
    });
    console.log(response);

    const tags = await response.json();
    console.log(tags);

    tags.forEach(tag => {
        $('#tags_list').loadTemplate('templates/new_recipe/tag_option_tpl.html', {
            tag_id: tag['id'],
            value: tag['name']
        }, {
            append: true,
        })
    });
}

function on_add_tag_click() {
    $('#add_tag').css('margin-top', '40px');
    curr_tag++;

    tags_container = $('#tags_container');
    tags_container.loadTemplate('templates/new_recipe/tag_tpl.html', {
        tag_id: 'tag_' + curr_tag,
        deletion_btn_id: 'delete_tag_' + curr_tag
    }, {
        append: true,
        complete: function() {
            $('#tag_' + curr_tag + ' input[name=tag]').focus();
            
            $('#delete_tag_' + curr_tag + ' .delete-btn').click(function() {
                const tag_to_del = $(this).parents('.row').attr('id').split('_').pop();
                $('#tag_' + tag_to_del).remove();
                $('#delete_tag_' + tag_to_del).remove();
            });
        }
    });
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

async function post_ingredient_recipe_relation(ingredient_id, recipe_id, quantity) {
    const query = server_url + 'recipes' + recipe_id + '/' + ingredient_id + '?count=' + quantity;

    const response = await fetch(query, {
        method: 'POST',
        credentials: 'include'
    });
    console.log(response);

    const relation = await response.json();
    console.log(relation);
}

async function post_ingredient_recipe(recipe_id) {
    let ingredients_data = [];

    const ingredients_count = $('#ingredients_container input[name=ingredient]').length;

    for (let i = 0; i < ingredients_count; i++) {
        const name = $('#ingredients_container input[name=ingredient]:eq(' + i + ')').val().trim();
        const quantity = $('#ingredients_container input[name=quantity]:eq(' + i + ')').val().trim();

        const query = server_url + 'ingredient/?ingredient_name=' + encodeURIComponent(name);

        const response = await fetch(query, {
            credentials: 'include'
        });
        console.log(response);

        const ingredients = await response.json();
        const ingredient = ingredients[0];
        console.log(ingredient);

        ingredients_data.push({
            id: ingredient['id'],
            quantity: quantity,
        })
    }

    console.log(ingredients_data);
    
    ingredients_data.forEach(ingredient => {
        post_ingredient_recipe_relation(ingredient.id, recipe_id, ingredient.quantity);
    });
}

let steps_files = new Map();

async function post_steps(recipe_id) {
    const steps_count = $('#steps_container input[name=step]').length;

    for (let i = 0; i < steps_count; i++) {
        const description = $('#steps_container input[name=step]:eq(' + i + ')').val().trim();
        const time = $('#steps_container input[name=hours]:eq(' + i + ')').val() * 3600 + $('#steps_container input[name=minutes]:eq(' + i + ')').val() * 60;

        const details = {
            description: description,
            timer: time,
        }

        let url_params = [];
        for (const property in details) {
            const encoded_key = encodeURIComponent(property);
            const encoded_value = encodeURIComponent(details[property]);
            url_params.push(encoded_key + '=' + encoded_value); 
        }
        url_params = url_params.join('&');        

        const query = server_url + 'recipes/' + recipe_id + '/step?' + url_params;
        const fetch_params = {
            method: 'POST',
            credentials: 'include',
            body: null
        }

        const step_id = $('input[name="media"]').parents(".step-container").attr('id').split('_').pop();

        let body = new FormData();
        body.append('media', steps_files.get(step_id));
        fetch_params.body = body;

        const response = await fetch(query, fetch_params);
        console.log(response);

        const step = await response.json();
        console.log(step);
    }
}

async function post_recipe() {
    //сбор основной информации о рецепте
    const name = $('input[name="name"]').val().trim();
    const servings_cout = $('input[name="servings"]').val();
    const cook_time = $('input[name="hours"]').val() * 3600 + $('input[name="minutes"]').val() * 60;
    const recommend = $('textarea[name="recommendations"]').val();

    let main_info_check = true;
    if (!name || !cook_time) {
        main_info_check = false;
    }

    const details = {
        name: name,
        servings_cout: servings_cout,
        cook_time: cook_time,
        recommend: (recommend ? recommend : null),
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

    //получение фотографии рецепта
    let recipe_photo_check = true;

    let body = new FormData();
    if (recipe_photo) {
        body.append('photo', recipe_photo);
    } else {
        recipe_photo_check = false;
    }
    
    //проверка ингредиентов
    let ingredients_check = true;
    
    if ($('#ingredients_container input').length == 0) {
        ingredients_check = false;
    }

    $('#ingredients_container input').each(function(index, element) {
        if($(element).val().trim() == '') {
            ingredients_check = false;
        }
    })

    //проверка шагов
    let steps_check = true;
    
    if ($('#steps_container input').length == 0) {
        steps_check = false;
    }

    $('#steps_container input[name=step]').each(function(index, element) {
        if($(element).val().trim() == '') {
            steps_check = false;
        }
    })

    $('#steps_container input[name=media]').each(function(index, element) {
        if($(element).val().trim() == '') {
            steps_check = false;
        }
    })

    //проверка собранных данных
    if (!main_info_check) {
        notification('Укажите основную информацию о рецепте.', 3000);
    } else if (!recipe_photo_check) {
        notification('Приложите фотографию готового блюда.', 3000);
    } else if (!ingredients_check) {
        notification('Укажите ингредиенты.', 2500);
    } else if (!steps_check) {
        notification('Укажите шаги.', 2500);
    } else {
        const fetch_params = {
            method: 'POST',
            credentials: 'include',
            body: body
        }

        const query = server_url + 'recipes/?' + url_params;

        const response = await fetch(query, fetch_params);
        console.log(response);

        if (response.ok) {
            const recipe = await response.json();
            console.log(recipe);

            const new_recipe_id = recipe[1];

            post_ingredient_recipe(new_recipe_id);
            
            post_steps(new_recipe_id);

            // редирект "мои рецепты"
        } else {
            notification('Рецепт с таким именем уже существует.', 3000);
        }
    }
}

let recipe_photo;

$('document').ready(function() {
    fetch_ingredients_list();
    fetch_tags_list()
    $('#add_ingredient').click();
    $('#add_step').click();

    if (!authorized()) {
        sessionStorage.setItem('unathorized_access', true);
        $(location).attr('href', 'index.html');
    }

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
});