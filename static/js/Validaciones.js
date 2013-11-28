/**
 * Created by cristian on 28/10/13.
 */

var MatchesPassword = function(firstStr, secondStr){
    $("#errorPass").remove()
    if ($(firstStr).val().length > 0 && $(firstStr).val() == $(secondStr).val())
        return;
    $(secondStr).after('<div id="errorPass" class="row"><label class="inline" style="width:250px;" onclick="$(this).remove();">No coinciden las contraseñas</label></div>');
}