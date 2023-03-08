$('document').ready(function() {
    // var server_url = 'https://4faf-178-141-127-143.eu.ngrok.io/';

    // var recipes_request = new XMLHttpRequest();

    // recipes_request.open('GET', server_url + 'recipes/', true);

    // recipes_request.send();

    // console.log(recipes_request.responseText);

    // if (recipes_request.status = 200) {
    //     
    // }

    response = [{"recipe_id":3,"recipe_desc":{"name":"Котлеты морковные","photo":"/photo/recipe/3_recipe_photo.jpg","servings_cout":4,"cook_time":30,"rating":0,"recommend":"Берите свежую морковь","author":1}},{"recipe_id":4,"recipe_desc":{"name":"Борщ со сметаной","photo":"/photo/recipe/4_recipe_photo.jpg","servings_cout":3,"cook_time":280,"rating":0,"recommend":null,"author":1}}]

    var recipe_cards_container = $('#recipe-cards');

    var recipe_cards = [];

    response.forEach(recipe => {
        var time = Number(recipe['recipe_desc']['cook_time']);
        var hours = Math.floor(time / 60)

        if (hours != 0) {
            time = String(hours) + ' ч ' + String(time % 60 + ' мин');
        } else {
            time = String(time) + ' мин';
        }
        recipe_cards.push(
            {
                name: recipe['recipe_desc']['name'],
                time: time,
                img_src: recipe['recipe_desc']['photo']
            }
        )
    });

    recipe_cards_container.loadTemplate('templates/recipe_card_tpl.html', recipe_cards);
});