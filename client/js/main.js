sessionStorage.setItem('server_url', 'http://localhost:8000/');

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}

function search_btn_click() {
    if ($('.searchbar').val()) {
        let href = 'search.html?query=';
        href += $('.searchbar').val();
        $(location).attr('href', href);
    }
};

$.fn.popup = function() {
    this.css('position', 'absolute').fadeIn();
    this.css('top', ($(window).height() - this.height()) / 2 + $(window).scrollTop() - $('header').height() + 'px');
    $('.modal-back').fadeIn();
    $('body').css('overflow', 'hidden');
}

function on_profile_btn_click() {
    if (sessionStorage.getItem('user_id')) {
        const href = "profile.html?tab=1";
        $(location).attr('href', href);
    } else {
        $('#sign_in_modal').popup();
    }
}

function on_fav_btn_click() {
    if (sessionStorage.getItem('user_id')) {
        const href = "profile.html?tab=2";
        $(location).attr('href', href);
    } else {
        $('#sign_in_modal').popup();
    }
}

function on_add_recipe_btn_click() {
    if (sessionStorage.getItem('user_id')) {
        const href = "new_recipe.html";
        $(location).attr('href', href);
    } else {
        $('#sign_in_modal').popup();
    }
}

function on_sign_up_click() {
    $('.auth-modal').fadeOut();
    $('#sign_up_modal').popup();
}

function on_sign_in_click() {
    $('.auth-modal').fadeOut();
    $('#sign_in_modal').popup();
}

$('document').ready(function() { 
    var header_container = $('header');
    header_container.loadTemplate("templates/main/header_tpl.html", {});

    var footer_container = $('footer');
    footer_container.loadTemplate("templates/main/footer_tpl.html", {});

    $('#modals_container').loadTemplate('templates/main/sign_in_modal_tpl.html', null, {
        append: true
    });

    $('#modals_container').loadTemplate('templates/main/sign_up_modal_tpl.html', null, {
        append: true
    });

    $('.modal-back').click(function(){
        $('.auth-modal').fadeOut();
        $('.modal-back').fadeOut();
        $('body').css('overflow', 'auto');
    });
});