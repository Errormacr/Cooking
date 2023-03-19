const server_url = 'http://localhost:8000/';

var params = new Map();
params.set('offset', 0);
params.set('name_sort', 0);
params.set('score_sort', 1);
params.set('time_sort', 0);


async function fetch_recipes (params) {
    query = server_url + 'recipes/get/?limit=6';

    for (const [param, value] of params) {
        query += '&' + param + '=' + value;
    }

    const response = await fetch(query, {
        method: 'POST',
        credentials: "include"
    });
    console.log(response);
    const recipes = await response.json();

    console.log(recipes);

    var recipe_cards_container = $('#recipe-cards');

    var recipe_cards = [];

    if (recipes['detail']) {
        $('#more_btn').hide();
    }

    recipes.forEach(recipe => {
        var time = Number(recipe['cook_time']);
        var hours = Math.floor(time / 3600);
        var minutes = time % 3600 / 60;
        
        time = (hours != 0 ? hours + ' ч' : "") + " " + (minutes != 0 ? minutes + ' мин' : "");

        var img_src = server_url + 'recipes/photo/' + recipe['recipe_id'];

        recipe_cards.push(
            {
                name: recipe['name'],
                time: time,
                img_src: img_src
            }
        )
    });

    recipe_cards_container.loadTemplate('templates/index/recipe_card_tpl.html', recipe_cards, {
        append: true
    });

    if (recipes.length < 6) {
        $('#more_btn').hide();
    }
}

function on_more_btn_click () {
    fetch_recipes(params);
    params.offset += 6;
}

$('document').ready(function() {
    $('#more_btn').click();

    $('#sort_btn').click(function(event) {
        event.preventDefault();
        if ($('.sort-menu').css('display') == 'none') {
            $('.sort-menu').css('display', 'block');
            $('.sort-menu').animate({opacity: 1}, 300);
        } else {
            $('.sort-menu').animate({opacity: 0}, 300, function() {
                $('.sort-menu').css('display', 'none');
            });
        }
    })
});