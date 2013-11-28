/**
 * Created by cristian on 27/10/13.
 */

var RegistrarAdmin = function(){
    if (!validatePassword())
        return;
    $.post("/administrator/RegisterAdmin", $("#register").serialize(), function(data){
        if (data == 'True'){
            //alert('Administrador registrado con éxito');
            new DialogYesNo().show('Administrador registrado con éxito', 'Éxito', function(){
                window.location = "/administrator/";
            });
        }else if(data.indexOf("Error") >= 0){
            new DialogYesNo().show(data, "Error");
        }else{
            new DialogYesNo().show("Los campos contienen errores, Favor de verificar", "Error", function(){
                loadPage(data);
            });
        }
    });
}

var RegistrarDoctor = function(){
    $.post(".", $("#register").serialize(), function(data){
        if (data === "True"){
            new DialogYesNo().show('Éxito al registrar al doctor\n¿Desea registrar un nuevo doctor?', 'Atención',
            function(){
                $(":text").each(function(){
                    $(this).val("");
                });
                $(":password").each(function(){
                    $(this).val("");
                });
                $(":checkbox").each(function(){
                    $(this).removeAttr('checked');
                });
                $("input[type='date']").each(function(){
                    $(this).val("");
                });
                $(".errorlist").each(function(){
                   $(this).remove();
                });
            },
            function(){
                window.location = "/administrator/";
            });
        }else if(data.indexOf("Error") >= 0){
            new DialogYesNo().show(data, "Error");
        }else{
            new DialogYesNo().show("Los campos contienen errores, Favor de verificar", "Error", loadPage(data));
        }
    });
}