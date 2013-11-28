/**
 * Created by cristian on 14/10/13.
 */

DialogYesNo = function(){
  $(document.body).append('<div id="dialog" title="Basic dialog"></div>');
  this.show = function(msg, title, fYes, fNo, risky){
      $( "#dialog" ).attr("title", title);
      $( "#dialog" ).html(msg);
      var btns = null;
      var onClose = null;
      if (fYes == null)
        fYes = function(){}
      if (fNo != null){
          var btnYes = {
              id: 'btnYes',
              text: 'Sí',
              click: function () {
                      fYes();
                      $(this).remove();
                  }
          }
          var btnNo = {
              id: 'btnNo',
              text: 'No',
              click: function () {
                      fNo();
                      $(this).remove();
                  }
          }
          if (risky == true)
              btns = [btnNo, btnYes];
          else
              btns = [btnYes, btnNo];
          onClose = fNo;
      }else{
          btns = [{
              id: 'btnOk',
              text: 'Aceptar',
              click: function () {
                      fYes();
                      $(this).remove();
                  }
          }]
          onClose = fYes;
      }
      if (onClose == null)
          onClose = function(){};
      $( "#dialog" ).dialog({
          autoOpen: true,
          modal: true,
          buttons: btns,
          close: onClose
      });
  }
}

function Paginador(event){
    this.url = "";
    this.idLista = "";
    this.event = event;
    this.pageCount = 0;
    this.isSearch = "";

    /* Método que asignara la url y posteriormente llamará al clic para el Paginador de Administradores*/
    this.evt = function(tipo, doctor){
        if (tipo == '1'){
            this.pageCount = parseInt($("#AdminCount").val());
            this.isSearch = $("#AdminSearch").val();
            this.url = "/administrator/ListaDeAdmins/?page=";
            this.idLista = "#ListaAdministradores";
        }else if (tipo == '2'){
            this.pageCount = parseInt($("#DoctorCount").val());
            this.isSearch = $("#DoctorSearch").val();
            this.url = "/administrator/ListaDeDoctores/?page=";
            this.idLista = "#ListaDoctores";
        }else if (tipo == '3'){
            if (doctor == null){
                this.pageCount = parseInt($("#PatientCount").val());
                this.isSearch = $("#PatientSearch").val();
                this.idLista = "#ListaPatient";
                this.url = '/doctor/ListaGralPacientes/?page='
            }else{
                this.pageCount = parseInt($("#MyPatientCount").val());
                this.isSearch = $("#MyPatientSearch").val();
                this.idLista = "#ListaMyPatient";
                this.url = '/doctor/ListaDePacientes/?page='
            }
        }
        this.getOnClic();
    };

    /* Método que manejara el clic del usuario*/
    this.getOnClic = function(){
        // En caso de que este deshabilitado
        if($(this.event).hasClass("disabled")) return;
        // Comprobamos si es un botón con letra
        var page;
        if($.isNumeric($(this.event).text()))
            page = parseInt($(this.event).text());
        else{
            var btnS;
            $(this.event).siblings().each(function(){
                if($(this).hasClass("page-container")){
                    btnS = $(this);
                    return false;
                }
            });
            if($(this.event).text().indexOf("First") >= 0)
                this.event = $(btnS).children().first();
            else if($(this.event).text().indexOf("Last") >= 0){
                this.event = $(btnS).children().last();
            }
            else{
                var event = this.event;
                $(btnS).children().each(function(){
                    if($(this).hasClass("current")) {
                        if($(event).text().indexOf("Prev") >= 0)
                            event = $(this).prev();
                        else if($(event).text().indexOf("Next") >= 0)
                            event = $(this).next();
                    }
                });
                this.event = event;
            }
            page = parseInt($(this.event).text());
    }
    // Mandamos llamar el GET de la lista correspondiente
    this.getList(page);
    };

    this.getList = function(page){
        // Para usarlo en las funciones anidadas.
        var event = this.event;
        // Obtenemos la cantidad de botones que hay en el paginador.
        var pageCount = this.pageCount + 1;
        var idLista = this.idLista;
        $.get(this.url + page.toString() + "&nombre=" + this.isSearch, function(data){
            $(idLista).replaceWith(data);
            $(event).addClass("current");
            $(event).siblings().each(function(){
                if($(this).hasClass("current")){
                    $(this).removeClass("current");
                }
            });
        });
        // A continuación habilitamos o deshabilitamos los botones segun sea necesario.
        $(this.event).parent().siblings().each(function(){
            if(page == 1){
                if($(this).hasClass("first") || $(this).hasClass("previous"))
                    $(this).addClass("disabled");
                else
                    $(this).removeClass("disabled");
            }else if(page == pageCount){
                if($(this).hasClass("next") || $(this).hasClass("last"))
                    $(this).addClass("disabled");
                else
                    $(this).removeClass("disabled");
            }else if($(this).hasClass("disabled"))
                $(this).removeClass("disabled");
        });
    }
}

function Busqueda (){

    this.id = ''
    this.idSearch = ''
    this.url = ''
    this.idPag = ''
    this.idLst = ''

    this.set = function(event, tipo, doctor){
        if (tipo == '1'){
            this.id = "BusqAdmin";
            this.idSearch = '#AdminSearch';
            this.url = '/administrator/adminPaginator/';
            this.idPag = '#admPag';
            this.idLst = '#ListaAdministradores';
            this.idBtn1 = '#btnAdm1'
        }else if (tipo == '2'){
            this.id = "BusqDoctor";
            this.idSearch = '#DoctorSearch';
            this.url = '/administrator/doctorPaginator/';
            this.idPag = '#docPag';
            this.idLst = '#ListaDoctores';
            this.idBtn1 = '#btnDoc1'
        }else if(tipo == '3'){
            if (doctor == null){
                this.id = "BusqPatient";
                this.idSearch = '#PatientSearch';
                this.url = '/doctor/patientPaginator/';
                this.idPag = '#paPag';
                this.idLst = '#ListaPatient';
                this.idBtn1 = '#btnPa1'
            }else{
                this.id = "BusqMyPatient";
                this.idSearch = '#MyPatientSearch';
                this.url = '/doctor/myPatientPaginator/';
                this.idPag = '#mypaPag';
                this.idLst = '#ListaMyPatient';
                this.idBtn1 = '#btnMyPa1'
            }
        }
        this.buscar(event);
    }

    this.buscar = function(event){
        if($(event).attr("id") == this.id){
            var idPag = this.idPag;
            var idLst = this.idLst;
            var txtBusq = $(event).val();
            if (txtBusq.length == 0){
                $(this.idSearch).val("");
                $(this.idBtn1).trigger("click");
                $.get(this.url, function(data){
                    $(idPag).replaceWith(data);
                });
                return;
            }
            $(this.idSearch).val(txtBusq);
            $.get(this.url + "?nombre=" + txtBusq, function(data){
                $(idPag).remove();
                $(idLst).replaceWith(data);
            });
        }
    }
}

var loadPage = function(data){
    var init = data.indexOf("<body"), fin = data.indexOf("</body>");
    for (; data[init] != '>'; init++);
    $("body").html(data.substring(init + 1, fin));
}

var validatePassword = function(){
    var txt = $("#id_password").val();
    var pattern1 = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{6,25}$/;
    if(pattern1.test(txt))
        return true;
    else{
        var out = "El password ";
        pattern1 =  /(?=.*\d)/;
        if (pattern1.test(txt)){
            pattern1 = /(?=.*[A-Z])/;
            if (pattern1.test(txt)){
                pattern1 = /(?=.*[a-z])/;
                if (pattern1.test(txt)){
                    if (txt.length < 6 || txt > 25)
                        out += 'debe contener al menos 6 carácteres'
                }
                else
                    out += 'debe tener al menos una minúscula';
            }
            else
                out += 'debe tener al menos una mayúscula';
        }
        else
            out += 'debe tener al menos un número';
        new DialogYesNo().show(out, "Error");
        return false;
    }
};