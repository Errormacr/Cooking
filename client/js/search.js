const server_url = sessionStorage.getItem('server_url');

let params = new Map();
params.set('offset', 0);

async function fetch_title(type) {
    let search_type, value;
    if (type == 'tag') {
        let tag_query = server_url + 'tag/' + $.urlParam('tag');
        let tag_response = await fetch(tag_query, {
            credentials: 'include'
        });
        let tag = await tag_response.json();

        search_type = 'тегу';
        value = tag['name'].trim();
    } else if (type == 'query') {
        search_type = 'запросу';
        value = decodeURI($.urlParam('query'));
    };

    console.log(search_type);
    console.log(value);

    $('#search_title_container').loadTemplate('templates/search/search_title_tpl.html', {
        search_type: search_type,
        query: value
    });
}

async function fetch_recipes(type) {
    let query = server_url + 'recipes/get/?limit=6';
    let fetch_params = {
        method: 'POST',
        credentials: 'include',
    };

    if (type == 'tag') {
        const body = {
            tag: [
                $.urlParam('tag')
            ],
        };

        const headers = {
            "Content-Type": "application/json",
        };

        fetch_params.body = JSON.stringify(body);
        fetch_params.headers = headers;
    } else if (type == 'query') {
        params.set('name', $.urlParam('query'));
    };

    for (const [param, value] of params) {
        query += '&' + param + '=' + value;
    };
    
    const response = await fetch(query, fetch_params);
    console.log(response);

    const recipes = await response.json();
    console.log(recipes);
    
    const recipe_cards_container = $('#recipe_cards');

    let recipe_cards = [];

    if (recipes['detail']) {
        $('#more_btn').hide();
    }

    recipes.forEach(recipe => {
        let time = Number(recipe['cook_time']);
        const hours = Math.floor(time / 3600);
        const minutes = time % 3600 / 60;
        
        time = (hours != 0 ? hours + ' ч' : "") + " " + (minutes != 0 ? minutes + ' мин' : "");

        const img_src = server_url + 'recipes/photo/' + recipe['recipe_id'];

        recipe_cards.push(
            {
                name: recipe['name'],
                time: time,
                img_src: img_src,
                href: 'recipe.html?id=' + recipe['recipe_id']
            }
        )
    });

    recipe_cards_container.loadTemplate('templates/main/recipe_card_tpl.html', recipe_cards, {
        append: true
    });

    if (recipes.length < 6) {
        $('#more_btn').hide();
    }
}

let type;

function on_more_btn_click () {

    fetch_recipes(type);
    params.set('offset', params.get('offset') + 6);
}

$('document').ready(function() {
    if ($.urlParam('tag')) {
        type = 'tag';
    } else if ($.urlParam('query')) {
        type = 'query';
    };

    fetch_title(type);

    $('#more_btn').click();
});