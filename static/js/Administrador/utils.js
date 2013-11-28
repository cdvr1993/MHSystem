/**
 * Created by cristian on 30/10/13.
 */
var EditUser = function(event, tipo, doctor){
    var idUser = $(event).siblings().first().val();
    if (tipo != 3)
        window.location = "/administrator/EditUser/?id=" + idUser + "&tipo=" + tipo;
    else{
        if (doctor == null)
            window.location = "/doctor/EditUser/?id=" + idUser + "&tipo=" + tipo;
        else
            window.location = "/doctor/EditUser/?id=" + idUser + "&tipo=" + tipo + "&doctor=True"
    }
}

var UpdateChanges = function(){
    $.post(".", $("#register").serialize(), function(data){
        if (data.indexOf('True') >= 0){
            new DialogYesNo().show('Usuario actualizado con éxito', "Éxito", function(){
                if(data.indexOf('Admin') >= 0)
                    window.location = "/administrator/ListaDeUsuarios/";
                else
                    window.location = "/doctor/";
            });
        }else
            new DialogYesNo().show('No se pudo actualizar', "Error", loadPage(data));
    });
}

var BorrarUsuario = function(event, tipo, doctor){
    var idUser = $(event).siblings().first().val();
    var name = $(event).parent().siblings().first().html()
    var doctor = false;
    new DialogYesNo().show('¿Seguro que desea borrar a ' + name + '?', '¡Atención!',
    function(){
        var url = ''
        if (tipo != 3)
            url = '/administrator/DeleteUser/';
        else{
            url = '/doctor/DeleteUser/';
            if (doctor != false)
                doctor = 'True';
        }
        $.post(url, {'ID': idUser, 'Tipo': tipo, 'Doctor' : doctor}, function(data){
            new DialogYesNo().show(data, "Éxito", function(){
                window.location.href = '.';
            })
        });
    },
    function(){/* Do Nothing */}, true)
}