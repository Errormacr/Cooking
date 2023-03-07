$('document').ready(function() {
    // var server_url = 'https://4faf-178-141-127-143.eu.ngrok.io/';

    // var recipes_request = new XMLHttpRequest();

    // recipes_request.open('GET', server_url + 'recipes/', true);

    // recipes_request.send();

    // console.log(recipes_request.responseText);

    // if (recipes_request.status = 200) {
    //     
    // }

    response = [{"recipe_id":1,"recipe_desc":{"name":"dssd","photo":"/photo/recipe/1_recipe_photo.jpg","servings_cout":1,"cook_time":"00:00:01","rating":0,"recommend":null,"author":1}}]

    var recipe_cards_container = $('#recipe-cards');

    var recipe_cards = [];

    response.forEach(recipe => {
        recipe_cards.push(
            {
                name: recipe['recipe_desc']['name'],
                time: recipe['recipe_desc']['cook_time'],
                img_src: recipe['recipe_desc']['photo']
            }
        )
    });

    recipe_cards_container.loadTemplate('templates/recipe_card_tpl.html', recipe_cards);
});