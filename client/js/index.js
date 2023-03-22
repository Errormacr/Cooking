const server_url = 'http://localhost:8000/';

var params = new Map();
params.set('offset', 0);
params.set('name_sort', 0);
params.set('score_sort', 0);
params.set('time_sort', 0);

async function fetch_recipes (params, append) {
    let query = server_url + 'recipes/get/?limit=6';

    for (const [param, value] of params) {
        query += '&' + param + '=' + value;
    }

    const response = await fetch(query, {
        method: 'POST',
        credentials: 'include'
    });
    console.log(response);
    const recipes = await response.json();

    console.log(recipes);

    const recipe_cards_container = $('#recipe-cards');

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
        append: append
    });

    if (recipes.length < 6) {
        $('#more_btn').hide();
    }
}

async function fetch_tags() {
    let query = server_url + 'tag';

    const response = await fetch(query, {
        method: 'GET',
        credentials: 'include'
    });
    console.log(response);
    const tags = await response.json();

    console.log(tags);

    const tags_container = $('#tags_container');

    let tags_data = [];

    tags.forEach(tag => {
        tags_data.push(
            {
                tag: '#' + tag['name'],
                href: 'search.html?tag=' + tag['id']
            }
        )
    });

    tags_container.loadTemplate('templates/main/tag_tpl.html', tags_data, {
        append: true
    });
}

function on_more_btn_click () {
    fetch_recipes(params, true);
    params.set('offset', params.get('offset') + 6);
}

async function fetch_filters () {
    let query = server_url + 'recipesmin_max';

    const response = await fetch(query, {
        method: 'GET',
        credentials: 'include'
    });
    console.log(response);
    const limits = await response.json();

    console.log(limits);

    $('#kKal_filter').ionRangeSlider({
        type: "double",
        min: limits['min kkal'],
        max: limits['max kkal'],
        postfix: ' кКал',
        step: 0.01,
        onStart: function (data) {
            params.set('ot_kkal', data.min);
            params.set('do_kkal', data.max);
        },
        onFinish: function (data) {
            params.set('ot_kkal', data.from);
            params.set('do_kkal', data.to);
            reload_recipes();
        }
    });

    $('#belki_filter').ionRangeSlider({
        type: "double",
        min: limits['min belki'],
        max: limits['max belki'],
        postfix: ' г',
        step: 0.01,
        onStart: function (data) {
            params.set('ot_belki', data.min);
            params.set('do_belki', data.max);
        },
        onFinish: function (data) {
            params.set('ot_belki', data.from);
            params.set('do_belki', data.to);
            reload_recipes();
        }
    });

    $('#zhiry_filter').ionRangeSlider({
        type: "double",
        min: limits['min zhyri'],
        max: limits['max zhyri'],
        postfix: ' г',
        step: 0.01,
        onStart: function (data) {
            params.set('ot_zhiry', data.min);
            params.set('do_zhiry', data.max);
        },
        onFinish: function (data) {
            params.set('ot_zhiry', data.from);
            params.set('do_zhiry', data.to);
            reload_recipes();
        }
    });

    $('#uglevody_filter').ionRangeSlider({
        type: "double",
        min: limits['min uglevody'],
        max: limits['max uglevody'],
        postfix: ' г',
        step: 0.01,
        onStart: function (data) {
            params.set('ot_uglevody', data.min);
            params.set('do_uglevody', data.max);
        },
        onFinish: function (data) {
            params.set('ot_uglevody', data.from);
            params.set('do_uglevody', data.to);
            reload_recipes();
        }
    });

    $('#time_filter').ionRangeSlider({
        type: "double",
        min: limits['min time'] / 60,
        max: limits['max time'] / 60,
        postfix: ' мин',
        onStart: function (data) {
            params.set('more_cook_time', (data.min - 1) * 60);
            params.set('less_cook_time', (data.max + 1) * 60);
        },
        onFinish: function (data) {
            params.set('more_cook_time', (data.from - 1) * 60);
            params.set('less_cook_time', (data.to + 1) * 60);
            reload_recipes();
        }
    });

    $('#rating_filter').ionRangeSlider({
        type: "double",
        min: limits['min rating'],
        max: limits['max rating'],
        onStart: function (data) {
            params.set('ot_raiting', data.min);
            params.set('do_raiting', data.max);
        },
        onFinish: function (data) {
            params.set('ot_raiting', data.from);
            params.set('do_raiting', data.to);
            reload_recipes();
        }
    });
}

function reload_recipes() {
    $('#more_btn').show();
    params.set("offset", 0);
    fetch_recipes(params, false);
    params.set("offset", 6);
}

function close_menus() {
    $('.menu-block > div').each(function(index, element) {
        $(element).css('display', 'none');
    })
}

var conditions = [' ↓', '  ', ' ↑']

$('document').ready(function() {
    fetch_filters();
    fetch_tags();
    
    $('#more_btn').click();

    $('#filter_btn').click(function(event) {
        event.preventDefault();

        if ($('.filter-menu').css('display') == 'none') {
            close_menus();
            $('.filter-menu').css('display', 'block');
            $('.filter-menu').animate({opacity: 1}, 300);
        } else {
            $('.filter-menu').animate({opacity: 0}, 300, function() {
                $('.filter-menu').css('display', 'none');
            });
        }
    })
    
    $('#sort_btn').click(function(event) {
        event.preventDefault();

        if ($('.sort-menu').css('display') == 'none') {
            close_menus();
            $('.sort-menu').css('display', 'block');
            $('.sort-menu').animate({opacity: 1}, 300);
        } else {
            $('.sort-menu').animate({opacity: 0}, 300, function() {
                $('.sort-menu').css('display', 'none');
            });
        }
    })


    $('#sortings > li').click(function() {
        sorting = $(this).attr('id');

        let value = params.get(sorting);

        if (value == 1)  {
            value = -1;
        } else {
            value += 1;
        }

        params.set('name_sort', 0);
        params.set('score_sort', 0);
        params.set('time_sort', 0);
        
        $('#sortings > li').each(function(index, element) {
            $(element).html($(element).html().slice(0, -1) + conditions[1]);
        })

        params.set(sorting, value);

        $(this).html($(this).html().slice(0, -1) + conditions[value + 1]);

        reload_recipes();

        console.log(params.get(sorting));
    })
});
