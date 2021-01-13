var enviar = document.getElementById('button-Send');

enviar.addEventListener("click", function(){
    var opinion = document.getElementById("op").value;
    var texto = {"mensaje" : opinion}
    alert("Gracias por tus comentarios");
    $.ajax({
        url: '/textcognitive',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(texto),
        success: function(texto) {
            console.log(texto);
        }
     });
});