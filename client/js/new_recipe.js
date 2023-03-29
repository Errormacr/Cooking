const server_url = sessionStorage.getItem('server_url');

let curr_ingredient = 0;

async function fetch_ingredients() {
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
    })

    if (can_add) {
        curr_ingredient++;

    ingredients_container = $('#ingredients_container');
    ingredients_container.loadTemplate('templates/new_recipe/ingredient_tpl.html', {
        ingredient_id: 'ingredient_' + curr_ingredient,
    }, {
        append: true,
        complete: function() {
            $('#ingredient_' + curr_ingredient + ' input[name=ingredient]').change(function() {
                fetch_unit(this);
            });
        }
    });
    }
}

function on_add_step_click() {
    steps_container = $('#steps_container');
    steps_container.loadTemplate('templates/new_recipe/step_tpl.html', null, {
        append: true
    });
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

$('document').ready(function() {
    fetch_ingredients();
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
});