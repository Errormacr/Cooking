const server_url = 'https://31bb-178-141-127-143.eu.ngrok.io/';

var offset = 0;

async function fetch_recipes (offset) {
    const response = await fetch(server_url + 'recipes/?limit=6&offset=' + offset, {
        credentials: "include"
    });
    console.log(response);
    const recipes = await response.json();

    console.log(recipes);

    var recipe_cards_container = $('#recipe-cards');

    var recipe_cards = [];

    recipes.forEach(recipe => {
        var time = Number(recipe['recipe_desc']['cook_time']);
        var hours = Math.floor(time / 3600);
        var minutes = time % 3600 / 60;
        
        time = (hours != 0 ? hours + ' ч' : "") + " " + (minutes != 0 ? minutes + ' мин' : "");

        var img_src = server_url + 'recipes/photo/' + recipe['recipe_id'];

        recipe_cards.push(
            {
                name: recipe['recipe_desc']['name'],
                time: time,
                img_src: img_src
            }
        )
    });

    recipe_cards_container.loadTemplate('templates/recipe_card_tpl.html', recipe_cards, {
        append: true
    });
}

function on_more_btn_click () {
    fetch_recipes(offset);
    offset += 6;
}

$('document').ready(function() {
    $('#more_btn').click();
});