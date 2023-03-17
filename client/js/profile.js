function on_prof_data_click() {
    $('.menu').css('background', 'linear-gradient(to right, #61b030 33%, #d9d9d9 33%)');
    $('#profile_data').css('color', '#fff');
    $('#favourite_recipes').css('color', '');
    $('#users_recipes').css('color', '');

    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/profile_data_tpl.html');
}

function on_fav_recipes_click() {
    $('.menu').css('background', 'linear-gradient(to right, #d9d9d9 33%, #61b030 33% 66%, #d9d9d9 66%)');
    $('#profile_data').css('color', '');
    $('#favourite_recipes').css('color', '#fff');
    $('#users_recipes').css('color', '');
    
    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/fav_recipe_card_tpl.html');
}

function on_users_recipes_click() {
    $('.menu').css('background', 'linear-gradient(to right, #d9d9d9 66%, #61b030 66%)');
    $('#profile_data').css('color', '');
    $('#favourite_recipes').css('color', '');
    $('#users_recipes').css('color', '#fff');

    profile_content_container = $('#profile_content_container');
    profile_content_container.loadTemplate('templates/profile/users_recipe_card_tpl.html');
}

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}

$('document').ready(function() {
    tab = $.urlParam('tab')
    if (tab == 1) {
        $('#profile_data').click();
    } else if (tab == 2) {
        $('#favourite_recipes').click();
    }
});