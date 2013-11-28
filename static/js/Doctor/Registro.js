/**
 * Created by ines on 11/11/13.
 */


var RegistrarPaciente = function(){
    $.post(".", $("#register").serialize(), function(data){
        if (data === "True"){
            new DialogYesNo().show('Éxito al registrar al paciente. ¿Desea registrar un nuevo paciente?', 'Atención',
            function(){
                $(":input").each(function(){
	            if($(this).attr("type") != "button")
		            $(this).val("");
                })
            },
            function(){
                window.location = "/doctor/";
            });
        }else if(data.indexOf("Error") >= 0)
            new DialogYesNo(data, "Error");
        else
            new DialogYesNo("Hay errores en los campos, Por favor compruébelos", "Error", loadPage(data));
    });
}