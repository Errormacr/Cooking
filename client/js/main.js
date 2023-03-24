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

$('document').ready(function() { 
    var header_container = $('header');
    header_container.loadTemplate("templates/main/header_tpl.html", {});

    var footer_container = $('footer');
    footer_container.loadTemplate("templates/main/footer_tpl.html", {});
});