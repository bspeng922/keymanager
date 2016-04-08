$(document).ready(function () {
    $('.sidebar-menu').children("li").each(function () {
        if (String(window.location).indexOf($(this).children("a").attr("href")) >= 0)
            $(this).addClass('active');
    });
});
