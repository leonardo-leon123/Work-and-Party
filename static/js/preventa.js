

$(document).ready(function() {
    $('#example').DataTable({
        "language": {
                "lengthMenu": "Mostrar _MENU_ registros",
                "zeroRecords": "No se encontraron resultados",
                "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                "Empty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                "infoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sSearch": "Buscar:",
                "oPaginate": {
                    "sFirst": "Primero",
                    "sLast":"Último",
                    "sNext":"Siguiente",
                    "sPrevious": "Anterior"
			     },
			     "sProcessing":"Procesando...",
        }
    });
    const intro = introJs();
intro.setOptions({
    steps: [
        {
            intro: 'Llegaste a la Sección de Preventa'
        },
        {
            element: '#step-one',
            intro: 'En esta opción podrás visualizar a todos los clientes que estan en proceso de contratación.'
        },
        {
            element: '#contadores',
            intro:'Aquí tenemos el total de clientes y el estatus en el que se encuentran.'
        }
        

        
    ]
})
intro.start();
    var table = $('#example').DataTable();
    $(document).on('click', '.btnDetalle',function(){
        fila = $(this).closest("tr");
        correo = fila.find('td:eq(2)').text();
        let datos = {
            "Correo": correo
        }
        $("#table tbody tr").remove(); 
        let timerInterval
        Swal.fire({
            title: 'Espera un momento estamos consultando los datos',
            html: 'Faltan <b></b> segundos.',
            timer: 1500,
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                timerInterval = setInterval(() => {
                    Swal.getContent().querySelector('b')
                      .textContent = (Swal.getTimerLeft() / 1000)
                        .toFixed(0)
                }, 100)
            },
            willClose: () => {
                clearInterval(timerInterval)
            }
        });
        $.ajax({
            url: '/tracking',
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            dataType: 'json',
            data: JSON.stringify(datos),
            success:function(datos) {
                var tracking = "<b>TRACKING DE CORREOS</b><br>"+
                "<b>Correo del cliente: </b> Me encantaria tener un evento tecnologico con ustedes<br>"+
                "<b>Tu respuesta:</b> Claro que si aqui te mandamos la informacion";
                if(datos['alerta'] === 'Si'){
                    var de = datos['de'];
                    var body = datos['body'];
                    var f = datos['fecha'];
                    td = [];
                    var cont = 0;
                    de.forEach(element => {
                        fecha_splitted = f[cont].split(" ")
                        var fecha = fecha_splitted[1] + "/" + fecha_splitted[2] + "/" + fecha_splitted[3]
                        $("#table tbody").append("<tr><td>"+ de[cont] +"</td><td>"+ body[cont] +"</td><td>"+ fecha +"</td></tr>");
                        console.log(cont);
                        cont += 1;
                    });
                } else {
                    Swal.fire({
                        icon: "warning",
                        title: "No hay ninguna respuesta de este cliente",
                    })
                }
            }
        });
    });
    var fila;
    $(document).on("click",".btnPlantilla", function(){
        fila = $(this).closest("tr");
        correo = fila.find('td:eq(2)').text();
        evento = fila.find('td:eq(5)').text();
        nombre = fila.find('td:eq(0)').text();
        fecha = fila.find('td:eq(3)').text();
        estatus = fila.find('td:eq(4)').text().trim();
        switch(evento){
            case "Boda":
                if(estatus === 'Rojo'){
                    var inputValue = " 'El mejor tipo de amor es el que despierta el alma y nos hace aspirar a más' \n Hola" + nombre + ", estamos muy felices de ayudarlos a volver su sueño realidad.\n Sabemos que quieres hacer una boda en la fecha de " + fecha + ". Si tiene dudas favor de ir a la pagina y Sura el bot te ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if(estatus === 'Amarillo'){
                    var inputValue = "“Sólo el amor puede ayudar a vivir” - Oscar Wilde\n Hola de nuevo " + nombre + ". \n Tenemos esta fecha registrada para el día más importante de sus vidas " + fecha + "\n ¿Quieres seguir el proceso?\n Si tiene dudas favor de ir a la pagina y Sura el bot te ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if(estatus === 'Verde'){
                    var inputValue =  "“(…) Aprenderé historias para contarte, inventaré nuevas palabras para decirte en todas que te quiero como a nadie” - Frida Kahlo“(…) Aprenderé historias para contarte, inventaré nuevas palabras para decirte en todas que te quiero como a nadie” - Frida Kahlo\n Que bueno que confiaron en nosotros para el festejo de su amor, dale click aqui para crear tu contrato: http://127.0.0.1:5000/crea_tu_contrato_bodas \n Atentamente: \n El Equipo de WORK & PARTY";
                }
                (async () => {
                    const { value: text } = await Swal.fire({
                    title: 'Enviar un Correo a:',
                    input: 'textarea',
                    inputLabel: correo,
                    inputValue: inputValue,
                    showCancelButton: true,
                    width: "25%",
                    inputValidator: (value) => {
                        if (!value) {
                        return 'Debes escribir algo.'
                        }
                    }
                    })
                    if(text) {
                        let data = {
                            "Correo" : correo,
                            "Cuerpo" : text,
                            "Asunto" : "Información para el evento de tipo: " + evento,
                            "Tipo": evento
                        };
                        Swal.fire({
                            title: 'Espera un momento estamos enviando el correo',
                            html: 'Faltan <b></b> segundos.',
                            timer: 8000,
                            timerProgressBar: true,
                            didOpen: () => {
                                Swal.showLoading()
                                timerInterval = setInterval(() => {
                                    Swal.getContent().querySelector('b')
                                      .textContent = (Swal.getTimerLeft() / 1000)
                                        .toFixed(0)
                                }, 100)
                            },
                            willClose: () => {
                                clearInterval(timerInterval)
                            }
                        });
                        $.ajax({
                            url: '/eprev',
                            method: 'POST',
                            headers: {
                                'Content-Type':'application/json'
                            },
                            dataType: 'json',
                            data: JSON.stringify(data),
                            success: function(data){
                                if(data['alerta'] === 'Si'){
                                    Swal.fire({
                                        title:'Ajax points'
                                    })
                                    points();
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Oops...',
                                        text: 'Hubo un error al enviar el correo ; Inténtelo de nuevo'
                                    });
                                } 
                            }
                        })
                    }
                })()
                break;
            case "Eventos_Tec":
                if (estatus === 'Rojo'){
                    var inputValue = "'La tecnología no es nada. Lo importante es que tengas fe en la gente, que sean básicamente buenas e inteligentes, y si les das herramientas, harán cosas maravillosas con ellas'. Steve Jobs.\n Hola" + nombre + ", estamos muy felices de ayudarle con su evento lleno de ideas e innovación.\n Sabemos que quieres llevar a cabo tu evento tecnológico en la fecha de " + fecha + ". Si tiene dudas favor de ir a la pagina y Sura el bot la ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if (estatus === 'Amarillo'){
                    var inputValue = "'La tecnología se alimenta a si misma. La tecnología hace posible más tecnología'.-Alvin Toffler.\n Tenemos esta fecha registrada para tu evento tan esperado: " + fecha + "\n ¿Quieres seguir el proceso?\n Si tiene dudas favor de ir a la pagina y Sura el bot la ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if (estatus === 'Verde'){
                    var inputValue ="“El gran motor del cambio: la tecnología”.-Alvin Toffler.\n Agradecdemos la confianza puesta en nosotros para llevar a cabo este día lleno de innvación y diversión, dale click aqui para crear tu contrato http://127.0.0.1:5000/crea_tu_contrato \n Atentamente: \n El Equipo de WORK & PARTY";
                }
                (async () => {
                    const { value: text } = await Swal.fire({
                    title: 'Enviar un Correo a:',
                    input: 'textarea',
                    inputLabel: correo,
                    inputValue: inputValue,
                    showCancelButton: true,
                    width: "25%",
                    inputValidator: (value) => {
                        if (!value) {
                        return 'Debes escribir algo.'
                        }
                    }
                    })
                    if(text) {
                        let data = {
                            "Correo" : correo,
                            "Cuerpo" : text,
                            "Asunto" : "Información para el evento de tipo: " + evento,
                            "Tipo": evento
                        };
                        Swal.fire({
                            title: 'Espera un momento estamos enviando el correo',
                            html: 'Faltan <b></b> segundos.',
                            timer: 8000,
                            timerProgressBar: true,
                            didOpen: () => {
                                Swal.showLoading()
                                timerInterval = setInterval(() => {
                                    Swal.getContent().querySelector('b')
                                      .textContent = (Swal.getTimerLeft() / 1000)
                                        .toFixed(0)
                                }, 100)
                            },
                            willClose: () => {
                                clearInterval(timerInterval)
                            }
                        });
                        $.ajax({
                            url: '/eprev',
                            method: 'POST',
                            headers: {
                                'Content-Type':'application/json'
                            },
                            dataType: 'json',
                            data: JSON.stringify(data),
                            success: function(data){
                                if(data['alerta'] === 'Si'){
                                    Swal.fire({
                                        icon: 'success',
                                        title: 'Enviado',
                                        text: 'El correo fue enviado con éxito'
            
                                    });
                                    points();
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Oops...',
                                        text: 'Hubo un error al enviar el correo ; Inténtelo de nuevo'
                                    });
                                } 
                            }
                        })
                    }
                })()
                break;
            case "Otros":
                if (estatus === 'Rojo'){
                    var inputValue = "Hola" + nombre + ", estamos muy felices de ayudarle con su evento tan especial.\n Sabemos que quieres llevar a cabo tu evento tecnológico en la fecha de " + fecha + ". Si tiene dudas favor de ir a la pagina y Sura el bot la ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if (estatus === 'Amarillo'){
                    var inputValue = "Tenemos esta fecha registrada para tu evento tan esperado: " + fecha + "\n ¿Quieres seguir el proceso?\n Si tiene dudas favor de ir a la pagina y Sura el bot la ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if (estatus === 'Verde'){
                    var inputValue =  "Agradecedemos la confianza puesta en nosotros para llevar a cabo este día lleno de diversión, dale click aqui para crear tu contrato http://127.0.0.1:5000/crea_tu_contrato \n Atentamente: \n El Equipo de WORK & PARTY";
                }
                (async () => {
                    const { value: text } = await Swal.fire({
                    title: 'Enviar un Correo a:',
                    input: 'textarea',
                    inputLabel: correo,
                    inputValue: inputValue,
                    showCancelButton: true,
                    width: "25%",
                    inputValidator: (value) => {
                        if (!value) {
                        return 'Debes escribir algo.'
                        }
                    }
                    })
                    if(text) {
                        let data = {
                            "Correo" : correo,
                            "Cuerpo" : text,
                            "Asunto" : "Información para el evento de tipo: " + evento,
                            "Tipo": evento
                        };
                        Swal.fire({
                            title: 'Espera un momento estamos enviando el correo',
                            html: 'Faltan <b></b> segundos.',
                            timer: 8000,
                            timerProgressBar: true,
                            didOpen: () => {
                                Swal.showLoading()
                                timerInterval = setInterval(() => {
                                    Swal.getContent().querySelector('b')
                                      .textContent = (Swal.getTimerLeft() / 1000)
                                        .toFixed(0)
                                }, 100)
                            },
                            willClose: () => {
                                clearInterval(timerInterval)
                            }
                        });
                        $.ajax({
                            url: '/eprev',
                            method: 'POST',
                            headers: {
                                'Content-Type':'application/json'
                            },
                            dataType: 'json',
                            data: JSON.stringify(data),
                            success: function(data){
                                if(data['alerta'] === 'Si'){
                                    Swal.fire({
                                        icon: 'success',
                                        title: 'Enviado',
                                        text: 'El correo fue enviado con éxito'
                                    });
                                    points();
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Oops...',
                                        text: 'Hubo un error al enviar el correo ; Inténtelo de nuevo'
                                    });
                                } 
                            }
                        })
                    }
                })()
                break;
            case "XV's":
                if (estatus === 'Rojo'){
                    var inputValue = " 'Celebrar una fiesta tan importante debe ser inolvidable' \n Hola" + nombre + ", estamos muy felices de ayudarlos a volver su sueño realidad.\n Sabemos que quieres celebrar unos XV años en la fecha de " + fecha + ". Si tiene dudas favor de ir a la pagina y Sura el bot te ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if (estatus === 'Amarillo'){
                    var inputValue = "Tenemos esta fecha registrada para tu evento tan esperado: " + fecha + "\n ¿Quieres seguir el proceso?\n Si tiene dudas favor de ir a la pagina y Sura el bot la ayudará .\n Atentamente: \n El Equipo de WORK & PARTY";
                }
                if (estatus === 'Verde'){
                    var inputValue = "Agradecdemos la confianza puesta en nosotros para llevar a cabo este día lleno de diversión, dale click aqui para crear tu contrato http://127.0.0.1:5000/crea_tu_contrato \n Atentamente: \n El Equipo de WORK & PARTY";
                }
                (async () => {
                    const inputValue = "";
                    const { value: text } = await Swal.fire({
                    title: 'Enviar un Correo a:',
                    input: 'textarea',
                    inputLabel: correo,
                    inputValue: inputValue,
                    showCancelButton: true,
                    width: "25%",
                    height: "25%",
                    inputValidator: (value) => {
                        if (!value) {
                        return 'Debes escribir algo'
                        }
                    }
                    })
                    if(text) {
                        let data = {
                            "Correo" : correo,
                            "Cuerpo" : text,
                            "Asunto" : "Información para el evento de tipo: " + evento,
                            "Tipo": evento
                        };
                        Swal.fire({
                            title: 'Espera un momento estamos enviando el correo',
                            html: 'Faltan <b></b> segundos.',
                            timer: 8000,
                            timerProgressBar: true,
                            didOpen: () => {
                                Swal.showLoading()
                                timerInterval = setInterval(() => {
                                    Swal.getContent().querySelector('b')
                                      .textContent = (Swal.getTimerLeft() / 1000)
                                        .toFixed(0)
                                }, 100)
                            },
                            willClose: () => {
                                clearInterval(timerInterval)
                            }
                        });
                        $.ajax({
                            url: '/eprev',
                            method: 'POST',
                            headers: {
                                'Content-Type':'application/json'
                            },
                            dataType: 'json',
                            data: JSON.stringify(data),
                            success: function(data){
                                if(data['alerta'] === 'Si'){
                                    Swal.fire({
                                        icon: 'success',
                                        title: 'Enviado',
                                        text: 'El correo fue enviado con éxito'
                                    });
                                    points();
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Oops...',
                                        text: 'Hubo un error al enviar el correo Inténtelo de nuevo'
                                    });
                                }
                            }
                        })
                    }
                })()
                break;
        }
    });
});

function points(){
    let v = {"Variable": "variable"}
    $.ajax({
        url:'/points',
        method:'POST',
        headers : {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data:JSON.stringify (v),
        success:function (v){
            if (v['alerta'] === 'Si'){
                Swal.fire({
                    icon: 'success',
                    title: 'Enviado',
                    text: '¡Enhorabuena! Haz ganado 5 puntos ¡Felicidades!'
                }); 
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Error'
                })
            }
        }
    });
}

