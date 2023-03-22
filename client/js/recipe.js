const server_url = localStorage.getItem('server_url');

async function fetch_recipe() {
    // запрос информации о рецепте
    const recipes_query = server_url + 'recipes/' + $.urlParam('id');
    const recipes_response = await fetch(recipes_query, {
        credentials: 'include'
    });
    console.log(recipes_response);

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
    categories.set('zhiry', 'Жиры');
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
            name: ingredient[0],
            quantity: ingredient[2],
            unit: ingredient[1]
        });

        // запись стандартного количества для дальнейших расчетов
        standard_quantity.push(ingredient[2])
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

let standard_servings = 0;
let standard_quantity = [];

$('document').ready(function() {
    fetch_recipe();
    
    // обработка нажатий изменения кол-ва порций
    $('#servings > p.sign').click(function() {
        let servings = $('.servings').html();
        const sign = $(this).html();

        if (sign == '+') {
            if (servings < 99) {
                servings++;
            }
        } else if (sign == '-') {
            if (servings > 1) {
                servings--;
            }
        }

        $('.servings').html(servings);
        
        $('span[name*="quantity"]').each(function(index, element) {
            let quantity = $(element).html();

            const part = Math.round(standard_quantity[index] / standard_servings);
            if (sign == '+') {
                quantity = Number(quantity) + part;
            } else if (sign == '-') {
                quantity = Number(quantity) - part;
            }

            $(element).html(Math.round(quantity));
        })
    })
});