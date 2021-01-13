var documentos_generados = 0

//var contador_contratos = document.getElementById("numero_de_contratos").innerHTML; 
 

document.cookie = "username=12"


document.getElementById("submit").addEventListener("click",set_cookie)



function set_cookie()
{
    var set_documento_generado = parseInt(getCookie("badges"))
    set_documento_generado += 1
    document.cookie = `badges = ${set_documento_generado}`
    return console.log(set_documento_generado)
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


