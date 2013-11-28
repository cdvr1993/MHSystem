/**
 * Created by cristian on 10/11/13.
 */

var Upload = function(){
    $("#id_id").val($("#idPte").val());
    $('#upload').submit();
    $("#upload").trigger("reset");
}

var SearchPatient = function(event){
    var url="/doctor/searchPatient/";
    var id="BusqPte";
    var idSearch="#PteSearch";
    if($(event).attr("id") == id){
        var txt= $(event).val();
        if (txt.length == 0){
            $(idSearch).val("");
            $.get(url,function(data){
                var init = data.indexOf("<div class"), fin = data.indexOf("</div>");
                for (; data[init] != '>'; init++);
                 $("select").html(data.substring(init + 1, fin));
            });
            return;
        }
    $(idSearch).val(txt);
    $.get(url+"?nombre="+txt,function(data){
        var init = data.indexOf("<div class"), fin = data.indexOf("</div>");
        for (; data[init] != '>'; init++);
        $("select").html(data.substring(init + 1, fin));
        $("#opciones").trigger("change");
    });
    }
}

var selectItem = function(event){
    if($(event).attr("id")=="opciones"){
        var valor = $(event).val();
        $.post("/doctor/searchPatient/",{'ID':valor},function(data){
            $("#idPte").val(valor)
            var init = data.indexOf("<table"), fin = data.indexOf("</table>");
            for (; data[init] != '>'; init++);
            $("table").html(data.substring(init + 1, fin));
        });
    }
}

var searchMedicine = function(event){
    var idBusq=$(event).attr('id')
    var num = idBusq.substring(7,idBusq.length)
        var txt = $(event).val()
        if(txt.length==0)
            $('#MedSearch'+num).val("")
        else
            $('#MedSearch'+num).val(txt)
    $.get("/doctor/medicamentos/?search="+txt+"&idmed=&num="+num,function(data){

        var init = data.indexOf("<select id=\"SelectMedicine"+num), fin = data.indexOf("</select>",init);
        for (; data[init] != '>'; init++);
        $("#SelectMedicine"+num).html(data.substring(init + 1, fin));
        init = data.indexOf("<select id=\"SelectDescription"+num)
        fin = data.indexOf("</select>",init);
        for (; data[init] != '>'; init++);
        $("#SelectDescription"+num).html(data.substring(init + 1, fin));
        $('#SelectMedicine'+num).trigger("change");
    });

}

var selectMedicine = function(event){
    var idSel=$(event).attr('id')
    var num = idSel.substring(14,idSel.length)
        var valor = $(event).val();
        var search = $('#MedSearch'+num).val()
        $.get("/doctor/medicamentos/?search="+search+"&idmed="+valor+"&num="+num,function(data){
            $('#idNomMed'+num).val(valor)
            var init = data.indexOf("<select id=\"SelectDescription"+num), fin = data.indexOf("</select>",init);
            for (; data[init] != '>'; init++);
            $("#SelectDescription"+num).html(data.substring(init + 1, fin));
            $('#SelectDescription'+num).trigger("change");
        });
}

var selectDescription = function(event){
    var idSel=$(event).attr('id')
    var num = idSel.substring(17,idSel.length)
        var desc = $(event).val();
        var nom = $('#idNomMed'+num).val()
        $.post("/doctor/medicamentos/",{'IDNom':nom,'IDDes':desc,'num':num},function(data){
            $('#idMed'+num).val(desc);
            var init = data.indexOf("<table id=\"InformacionMed"+num), fin = data.indexOf("</table>",init);
            for (; data[init] != '>'; init++);
            $("#InformacionMed"+num).html(data.substring(init + 1, fin));
        });
}

var agregarPrescripcion = function(){
    var diag = $('#idDiagnostico').val()
    var paciente=$("#idPaciente").val()
    if(paciente=="")
        new DialogYesNo().show("No hay paciente seleccionado", "Error");
    else{
        window.location ="/doctor/prescripcion?pte="+paciente+"&idd="+diag
        $('#add_med').trigger("click");
    }
}

var guardarPrescripcion = function(){
    var dicc ={}
    var keys=[]
    var flag = true
    $("textarea").each(function(){
           if ($(this).attr('id').indexOf("indicacion")==0){
               var id=$(this).attr('id')
               var index = id.substring(10,id.length)
               var v = $('#idMed'+index).val()
               for (var i in keys){
                   if (keys[i] == v){
                       new DialogYesNo().show("Medicamentos repetidos", "Error");
                       flag = false;
                       break;
                   }
               }
               keys.push(v)
               dicc[v]= $('#'+id).val()
           }
    });
    if(flag == true){
        dicc['IDP'] = $('#idPat').val();
        dicc['IDDiag'] = $('#idDiagnostico').val();
        dicc.obs = $("#observaciones").val();

        $.post(".",dicc,function(data){
            new DialogYesNo().show("Prescripción guardada", "Éxito", function(){
                var init = data.indexOf("\"idPrescripcion"), eq = data.indexOf("=",init), fin = data.indexOf(">",eq);
                var idp=data.substring(eq + 1, fin);
                init = data.indexOf("\"idDiagnostico"); eq = data.indexOf("=",init); fin = data.indexOf(">",eq);
                url="/doctor/vistaPrescripcion/?idp="+idp+"&idd="+data.substring(eq + 1, fin);
                window.location=url;
            });
        });
    }
}

var regresarDiagnostico = function(){
    var idd = $('#idDiagnostico').val()
    window.location = "/doctor/vistaDiagnostico/?idd="+idd
}

var verPrescripcion = function(){
    var idp = $('#idPrescripcion').val()
    var idd = $('#idDiagnostico').val()
    window.location = "/doctor/vistaPrescripcion/?idp="+idp+"&idd="+idd
}

var eliminarPrescripcion = function(){
    var path=location.pathname
    var idp=$('#idPrescripcion').val()
    var idd=$('#idDiagnostico').val()
    if(path.indexOf('vistaPrescripcion')>-1){
         $.get("/doctor/deletePrescripcion/?idp="+idp+"&idd="+idd,function(data){
             if(data=='True'){
                 new DialogYesNo().show("Prescripción eliminada correctamente", "Éxito", function(){
                     window.location = "/doctor/vistaDiagnostico/?idd="+idd;
                 });
             }
             else
                new DialogYesNo().show("Error al eliminar prescripción. Intente nuevamente", "Error");
         });
    }
}

var CrearDiagnostico = function(){
    var idPaciente=$("#idPte").val()
    if(idPaciente!=""){
        $.post(".",{'IDP':idPaciente, 'text':$("#id_text").val()},function(data){
            new DialogYesNo().show("Diagnóstico guardado", "Éxito", function(){
                var init = data.indexOf("\"idDiagnostico"), eq = data.indexOf("=",init), fin = data.indexOf(">",eq);
                window.location = "/doctor/vistaDiagnostico/?idd="+data.substring(eq+1, fin);
            });
        });
    }
}

var agregarMeds = function(){
    var num = $('#meds').val()
    $.get("/doctor/medicamentos/?search=&idmed=&num="+num,function(data){
        nuevo_num = parseInt(num)+1
        $('#meds').val(nuevo_num)
        $("#newPresc").append(data)
    })
}

var quitarMeds = function(event){
    var id = $(event).attr('id')
    var num = id.substring(id.length-1,id.length)
    $('#Medicina'+num).remove()
}

var BusquedaPacienteByDate = function(){
    /* Función que realizara un filtro por nombre de paciente y/o rango de fechas
    *  Si todos los parámetros son vacíos eliminará los resultados actuales */
    var name = $("#id_name").val(), init = $("#id_init").val(), final = $("#id_final").val();
    if (name == '' && init == '' && final == ''){
        $("#historial").remove();
        return;
    }
    $.get("./Filter/?name=" + name + "&init=" + init + "&final=" + final, function(data){
        var pos = $("#historial")[0];
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

var imprimirPrescripcion = function(){
    var idp=$('#idPrescripcion').val()
    var idd=$('#idDiagnostico').val()
    if(idp!=0){
        window.open("/doctor/printPrescripcion/?idp="+idp+"&idd="+idd, "Imprimir","fullscreen=yes")
    }
}

var eliminarDiagnostico = function(id){
    new DialogYesNo().show("¿Seguro que desea eliminar a " + $("#row_" + id).children().first().text() + "?", "Confirmación",
    function(){
        $.get("/doctor/deleteDiagnostico/?idd="+id,function(data){
             if(data=='True'){
                 new DialogYesNo().show("Diagnóstico eliminado correctamente", "Exito", function(){
                    $("#row_" + id).remove()
                 });
             }
             else
                new DialogYesNo().show("Error al eliminar diagnóstico. Intente nuevamente", "Error");
         });
    },
    function(){

    }, true);
}
