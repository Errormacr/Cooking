$('document').ready(function() {
    var header_container = $('header');
    header_container.loadTemplate("templates/header_tpl.html", {});

    var footer_container = $('footer');
    footer_container.loadTemplate("templates/footer_tpl.html", {});
});