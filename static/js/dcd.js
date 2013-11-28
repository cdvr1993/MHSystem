/**
 * Created by cristian on 14/10/13.
 */
$(document).ready(function(){
    var generarLlave = function(){
        var MAX = 1;
        var MIN = 0;
        var key128 = "";
        var key256 = "";
        for(var i = 0; i < 128; i++) key128 += Math.floor(Math.random() * (MAX - MIN + 1)) + MIN;
        for(var i = 0; i < 256; i++) key256 += Math.floor(Math.random() * (MAX - MIN + 1)) + MIN;
        var encrypted = "" + CryptoJS.AES.encrypt(key256, key128);
        alert(key256);
        $.post("./SaveKey/",
                {
                    key : key128,
                    enc : encrypted
                },
                function(){
                    var name = "Cristian David Velázquez Ramírez"
                    var encrypted = "" + CryptoJS.AES.encrypt(name, key256);
                    var tildes = []
                    for(var i = 0; i < name.length; i++ ){
                        if(name.charCodeAt(i) >= 128)
                            tildes.push(name[i])
                    }
                    tildes = tildes.toString();
                    $.post("./DecodeData/",
                        {
                            Name : encrypted,
                            Til : tildes
                        },
                        function(data){
                            alert(data);
                        }
                    );
                });
        return key256;
    };

    $("#btn").click(function(){
        generarLlave();
    });
});