const server_url = sessionStorage.getItem('server_url');

let current_step = 0;

async function fetch_step(index) {
    const query = server_url + 'recipes/' + $.urlParam('id') + '/steps';
    const response = await fetch(query, {
        credentials: 'include'
    });

    const steps = await response.json();
    console.log(steps);

    const total_steps = steps.length;

    const step = steps[index];
    console.log(step);

    $('#step_num_container').loadTemplate('templates/recipe/step_num_tpl.html', {
        step_num: index + 1
    });

    // выяснение типа медиа - изображение или видео
    // const media_query = server_url + 'recipes/' + step['step_ID'] + '_media/'
    // const media_response = await fetch(media_query, {
    //     credentials: 'include'
    // });
    // console.log(media_response);

    // const media = await media_response.blob();
    // console.log(media);

    $('#step_description_container').loadTemplate('templates/recipe/step_description_tpl.html', {
        description: step['description']
    });

    if (step['timer']) {
        const time = step['timer'];        
        const hours = Math.floor(time / 3600);
        const minutes = Math.floor(time % 3600 / 60);
        const seconds = time % 3600 % 60;

        base_hours = (String(hours).length == 1 ? '0' + hours : hours);
        base_minutes = (String(minutes).length == 1 ? '0' + minutes : minutes);
        base_seconds = (String(seconds).length == 1 ? '0' + seconds : seconds);

        $('#timer_container').loadTemplate('templates/recipe/timer_tpl.html', {
            hours: (String(hours).length == 1 ? '0' + hours : hours),
            minutes: (String(minutes).length == 1 ? '0' + minutes : minutes),
            seconds: (String(seconds).length == 1 ? '0' + seconds : seconds)
        });
    } else {
        $('#timer_container').html('')
    };

    if (index == 0) {
        $('#buttons_container').loadTemplate('templates/recipe/step_first_buttons_tpl.html');
    } else if (index == total_steps - 1) {
        $('#buttons_container').loadTemplate('templates/recipe/step_last_buttons_tpl.html');
    } else {
        $('#buttons_container').loadTemplate('templates/recipe/step_buttons_tpl.html');
    };

}

async function fetch_recipe() {
    // запрос информации о рецепте
    const recipes_query = server_url + 'recipes/' + $.urlParam('id');
    const recipes_response = await fetch(recipes_query, {
        credentials: 'include'
    });
    console.log(recipes_response);

    if (!recipes_response.ok) {
        sessionStorage.setItem('cant_find', true);
        $(location).attr('href', 'index.html');
    }

    const recipe_info = await recipes_response.json();
    const recipe = recipe_info[0];
    console.log(recipe);


    const recipe_desc = recipe['recipe_desc']

    // загрузка шаблона названия рецепта
    $('#name_container').loadTemplate('templates/recipe/name_tpl.html', {
        name: recipe_desc['name']
    });

    // загрузка шаблона изображения рецепта
    $('#img_container').loadTemplate('templates/recipe/img_tpl.html', {
        img_src: server_url + 'recipes/photo/' + recipe['recipe_id']
    }, {
        append: true
    });

    // загрузка шаблонов ккал, бжу рецепта
    let categories = new Map();
    categories.set('kkal', 'Калории');
    categories.set('belky', 'Белки');
    categories.set('zhyri', 'Жиры');
    categories.set('uglevody', 'Углеводы');

    let info_data = [];

    for (const [category, category_name] of categories) {
        info_data.push({
            category: category_name,
            value: recipe[category].toFixed(2) + (category_name == 'Калории' ? ' кКал' : ' грамм')
        });
    }
    
    $('#info_container').loadTemplate('templates/recipe/info_block_tpl.html', info_data);

    // загрузка шаблона времени приготовления рецепта
    let time = Number(recipe_desc['cook_time']);
    const hours = Math.floor(time / 3600);
    const minutes = time % 3600 / 60;
        
    time = (hours != 0 ? hours + ' ч' : "") + " " + (minutes != 0 ? minutes + ' мин' : "");

    $('#time_container').loadTemplate('templates/recipe/time_tpl.html', {
        time: time
    }, {
        append: true
    });

    // загрузка шаблона кол-ва порций рецепта
    $('#servings_container').loadTemplate('templates/recipe/servings_tpl.html', {
        count: recipe_desc['servings_cout']
    });

    // запись стандартного кол-ва порций для дальнейших расчетов
    standard_servings = recipe_desc['servings_cout'];

    // загрузка шаблонов ингредиентов рецепта
    let ingredients_data = [];

    recipe['ingredients'].forEach(ingredient => {
        ingredients_data.push({
            name: ingredient[1],
            quantity: ingredient[3],
            unit: ingredient[2]
        });

        // запись стандартного количества для дальнейших расчетов
        standard_quantity.push(ingredient[3])
    });

    $('#ingredients_container').loadTemplate('templates/recipe/ingredient_tpl.html', ingredients_data);

    // запрос шагов рецепта
    const steps_query = server_url + 'recipes/' + $.urlParam('id') + '/steps'
    const steps_response = await fetch(steps_query, {
        credentials: 'include'
    });
    console.log(steps_response);

    const steps = await steps_response.json();
    console.log(steps);

    // загрузка шаблонов шагов рецепта
    let i = 1;
    let steps_data = [];
    steps.forEach(step => {
        steps_data.push({
            step: i + '. ' + step['description']
        })
        i++;
    });

    $('#steps_container').loadTemplate('templates/recipe/step_tpl.html', steps_data);

    // загрузка шаблона рекомендаций рецепта
    if (recipe_desc['recommend']) {
        $('#recommendations_container').loadTemplate('templates/recipe/recommendations_tpl.html', {
            recommendations: recipe_desc['recommend']
        });
    }
    
    // запрос тегов рецепта
    const tags_query = server_url + 'tag/?recipe_id=' + $.urlParam('id');
    const tags_response = await fetch(tags_query, {
        credentials: 'include'
    });
    console.log(tags_response);

    const tags = await tags_response.json();
    console.log(tags);

    // загрузка шаблонов тегов рецепта
    let tags_data = [];

    tags.forEach(tag => {
        tags_data.push({
            tag: '#' + tag['name'],
            href: 'search.html?tag=' + tag['tag_id']
        })
    })

    $('#tags_container').loadTemplate('templates/main/tag_tpl.html', tags_data);
};

async function add_to_fav() {
    const query = server_url + 'users/favourite?recipe_id=' + $.urlParam('id');

    const response = await fetch(query, {
        method: 'POST',
        credentials: 'include'
    });
    console.log(response);
};

// функции для таймера
let timer;
let base_hours, base_minutes, base_seconds;

function on_play_btn_click() {
    if (!timer) {
        timer = setInterval(function() {
            let seconds = Number($('#seconds').html());
            let minutes = Number($('#minutes').html());
            let hours = Number($('#hours').html());
    
            let time_left = hours * 3600 + minutes * 60 + seconds;
            if (!time_left) {
                clearInterval(timer);
                timer = null;
            } else {
                time_left--;
    
                hours = Math.floor(time_left / 3600);
                minutes = Math.floor(time_left % 3600 / 60);
                seconds = time_left % 3600 % 60;
    
                $('#hours').html((String(hours).length == 1 ? '0' + hours : hours));
                $('#minutes').html((String(minutes).length == 1 ? '0' + minutes : minutes));
                $('#seconds').html((String(seconds).length == 1 ? '0' + seconds : seconds));
            }
        }, 1000);
    }
}

function on_pause_btn_click() {
    clearInterval(timer);
    timer = null;
}

function on_restart_btn_click() {
    clearInterval(timer);
    timer = null;
    $('#hours').html(base_hours);
    $('#minutes').html(base_minutes);
    $('#seconds').html(base_seconds);
}

// функции для навигации по шагам
function on_step_by_step_btn_click() {
    $('#step_section').show();
    $('#recipe_section').hide();

    fetch_step(current_step);
};

function on_to_recipe_btn_click() {
    $('#recipe_section').show();
    $('#step_section').hide();
    
    current_step = 0;
};

function on_next_btn_click() {
    current_step++;
    fetch_step(current_step);
};

function on_back_btn_click() {
    current_step--;
    fetch_step(current_step);
};

// инициализация переменных для расчета кол-ва ингредиентов
let standard_servings = 0;
let standard_quantity = [];

$('document').ready(function() {
    $('#step_section').hide();
    fetch_recipe();

    // обработка нажатий изменения кол-ва порций
    $('#servings > p.sign').click(function() {
        let servings = $('.servings').html();
        const sign = $(this).html();

        let changed = false;
        if (sign == '+') {
            if (servings < 99) {
                servings++;
                changed = true;
            }
        } else if (sign == '-') {
            if (servings > 1) {
                servings--;
                changed = true;
            }
        }

        if (changed) {
            $('.servings').html(servings);
        
            $('span[name*="quantity"]').each(function(index, element) {
                let quantity = $(element).html();

                const part = Number(standard_quantity[index] / standard_servings).toFixed(2);
                if (sign == '+') {
                    quantity = Number(quantity) + Number(part);
                } else if (sign == '-') {
                    quantity = Number(quantity) - Number(part);
                }

                quantity = quantity.toFixed(2);
                if (String(quantity).endsWith('.00')) {
                    $(element).html(Math.round(quantity));
                } else {
                    $(element).html(quantity);
                }
            })
        }  
    })
});