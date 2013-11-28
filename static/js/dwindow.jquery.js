/**
 * @description Create a window to load some content inside, can open content 
 * with ajax or direct html.
 * 
 * @author Marino Esteban
 * 
 * @param {string} top the initial position of the windows from main 
 * window's top.
 * 
 * @param {string} left the initial position of the windows from main
 * window's top.
 * 
 * @param {string} content An html address or direct html string.
 * 
 * @param {string} contentType Specify if the content to load is from an ajax 
 * request or html.
 */
(function($) {

    $.fn.dwindow = function(o) {
        var html = "<div class='dwindow-main'>\
                                <div class='dwindow-title'>\
                                <p></p>\
                                <div class='dwindow-close'>\
                                <img src='/img/close-button.gif'/></div>\
                                </div>\
                                <div class='dwindow-container'></div>\
                                </div>";

        var defaults = {
            title: null,
            top: "10px",
            left: "10px",
            width: null,
            height: null,
            content: null,
            contentType: null //HMTL, Ajax
        };
        $(this).click(function(event) {
            $("body").append(html);
            $.extend(defaults, o);
            $(".dwindow-main").css("zindex", "1000");
            $(".dwindow-main").width(defaults.width);
            $(".dwindow-main").height(defaults.height);
            $(".dwindow-main").draggable();
            $(".dwindow-main .dwindow-title p").text(defaults.title);
            
            $(".dwindow-main .dwindow-close").click(function(ev) {
                $(ev.currentTarget).parent().parent().remove();
            });
            var currentWindow = $("body").last();
            //Cargar contenido
            if (defaults.contentType === "ajax") {
                currentWindow.find(".dwindow-container")
                        .load(defaults.content);
            } else {
                currentWindow.find(".dwindow-container")
                        .html(defaults.content);
            }

        });

    };

})(jQuery);