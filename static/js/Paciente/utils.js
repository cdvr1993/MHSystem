/**
 * Created by cristian on 17/11/13.
 */

var DownloadFile = function(event){
    id = $(event).prev().val();
    window.open("./getFile/?file=" + id.toString());
}

var searchAnalisisByDate = function(){
    var init = $("#id_init").val(), final = $("#id_final").val();
    $.post("./search/", $("#searchForm").serialize(), function(data){
        if (data != 'Error') $("#ListaDeArchivos").replaceWith(data);
    });
}

var DiagnosticoByDate = function(){
    var init = $("#id_init").val(), final = $("#id_final").val();
    if (init == '' && final == ''){
        $("#tblDiagnosticos").remove();
        return;
    }
    $.get("./Filter/?init=" + init + "&final=" + final, function(data){
        var pos = $("#tblDiagnosticos")[0];
        if (data.indexOf("<html>") >= 0)
            loadPage(data);
        else if(data.indexOf("<td>") < 0)
            pos.remove();
        else{
            if (pos == null)
                $("#content-body").append(data);
            else{
                pos.replaceWith(data);
            }
        }
    });
}

var verPrescripcion = function(){
    var idp = $('#idPrescripcion').val()
    var idd = $('#idDiagnostico').val()
    window.location = "/patient/vistaPrescripcion/?idp="+idp+"&idd="+idd
}

var regresarDiagnostico = function(){
    var idd = $('#idDiagnostico').val()
    window.location = "/patient/vistaDiagnostico/?idd="+idd
}