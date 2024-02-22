$(document).ready(function () {
    $("#table1, #table2").fixMe();
    $(".up").click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 2000);
    });
});
