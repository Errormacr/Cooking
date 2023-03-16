function on_add_ingr_click() {
    ingredients_container = $('#ingredients_container');
    ingredients_container.loadTemplate('templates/new_recipe/ingredient_tpl.html', null, {
        append: true
    });
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
    $('#add_ingredient').click();
    $('#add_step').click();
});