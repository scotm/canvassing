/**
 * Created by scotm on 02/03/15.
 */
$(".content.active").css('display', 'block');
$(".accordion").on("click", "li", function (event) {
    if ($(this).is('.active')) {
        var self = $(this);
        setTimeout(function () {
            self.addClass('active').find(".content").addClass('active');
        }, 10);
    } else {
        $("li.active").find(".content").slideToggle();
        $(this).find(".content").slideToggle();
    }
});