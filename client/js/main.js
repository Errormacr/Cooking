$('document').ready(function() {
    var header_container = $('header');
    header_container.loadTemplate("templates/main/header_tpl.html", {});

    var footer_container = $('footer');
    footer_container.loadTemplate("templates/main/footer_tpl.html", {});
});