/* Onboarding */
const intro = introJs();
intro.setOptions({
    steps: [
        {
            intro: 'Esta es la página de eventos. Aquí podrás ver las encuestas realizadas de los eventos de nuestra empresa.'
        },
        {
            element: '#step-one',
            intro: 'Aquí podrás ver los eventos por nombre y filtrar las imagenes.'
        },
        {
            element: '#first-table',
            intro: 'En esta tabla podrás ver los correos y podrás filtrar por nombre también.'
        },
        {
            element: '#enviar',
            intro: 'Cada vez que envíes un correo a una persona que tenga una mala calificación (<2.5) podrás ganarte puntos si el cliente acepta reservar de nuevo.'
        },
        {
            element: '#detalle',
            intro: 'Si quieres saber las preguntas y las respuestas de cada cliente, puedes darle click aquí y abrirá una nueva ventana con dichos datos.'
        },
        {
            element: '#step-two',
            intro: 'Aquí podrás ver las fotos de los eventos seleccionados previamente.'
        },
        {
            intro: 'Si le das click en el botón de más podrás agregar nuevas imagenes dependiendo del evento que eliges en "Encuestas".'
        },
        {
            element: '#agregar',
            intro: 'Aquí'
        },
        {
            intro: 'Si quieres puedes subir una imagen y probar los filtros; después de eso deslogeate y ganarás tus primeros puntos para empezar con el pie derecho; ¡Mucha Suerte!'
        }
    ]
})
/*intro.start();*/
document.querySelector('.star-steps').addEventListener("click", function(){
    intro.start();
});

var fila;
$(document).on("click",".btnCorreo", function(){
    fila = $(this).closest("tr");
    correo = fila.find('td:eq(2)').text();
    evento = fila.find('td:eq(1)').text().split(" ");
    cal = fila.find('td:eq(3)').text().split(" ");
    console.log(correo)
    console.log(cal)
    let data = {
        "Correo": correo,
        "Cal": cal[1]
    }
    let timerInterval
    Swal.fire({
    title: 'Espera un momento se esta enviando el correo',
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
    }).then((result) => {
    /* Read more about handling dismissals below */
    if (result.dismiss === Swal.DismissReason.timer) {
        console.log('I was closed by the timer')
    }
    })
    $.ajax({
        url: '/enviar',
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
    });
});
$(document).on("click",".btnDetalle", function(){
    fila = $(this).closest("tr");
    id = fila.find("td:eq(0)").text();
    correo = fila.find("td:eq(2)").text();
    console.log(correo);
    let datos = {
        "Id": id
    }
    console.log(datos);
    let timerInterval
    Swal.fire({
    title: 'Espera un momento estamos consultando los datos',
    html: 'Faltan <b></b> segundos.',
    timer: 4000,
    timerProgressBar: true,
    didOpen: () => {
        Swal.showLoading()
        timerInterval = setInterval(() => {
        const content = Swal.getContent()
        if (content) {
            const b = content.querySelector('b')
            if (b) {
            b.textContent = Swal.getTimerLeft()
            }
        }
        }, 100)
    },
    willClose: () => {
        clearInterval(timerInterval)
    }
    }).then((result) => {
    /* Read more about handling dismissals below */
    if (result.dismiss === Swal.DismissReason.timer) {
        console.log('I was closed by the timer')
    }
    })
    $.ajax({
        url: 'detalles',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(datos),
        success: function(datos) {
            if(datos['alerta'] ===  'Si'){
                Swal.fire({
                    title: "Detalles",
                    html: 'Aqui puedes ver los detalles de la encuesta de: ' + correo +
                '<table><tr><th>¿El evento fue lo que esperaba?</th> <th>Califique el evento</th> <th>¿Asistiría de nuevo a uno de nuestros eventos?</th> <th>¿Nos recomendaría con amigos y/o familiares?</th> <th>Comentanos que te pareció el evento</th> </tr> <tr><td>'+ datos["p1"] +'</td><td>'+ datos["p2"] +'</td><td>'+ datos["p3"] +'</td><td>'+ datos["p4"] +'</td> <td>'+ datos["p5"] +'</td></tr></table>',
                    width: "70%"
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Hubo un error, inténtelo de nuevo'
                });
            }
        }
    });
});

const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const optionsList = document.querySelectorAll(".option");
const searchBox = document.querySelector(".search-box input");

selected.addEventListener("click", () =>{
    optionsContainer.classList.toggle("active");
    searchBox.value = "";
    filterList("");
    if (optionsContainer.classList.contains("active")){
        searchBox.focus();
    }
});

optionsList.forEach(o => {
    o.addEventListener("click", () => {
        selected.innerHTML = o.querySelector("label").innerHTML;
        optionsContainer.classList.remove("active");
    });
});

searchBox.addEventListener("keyup", function(e){
    filterList(e.target.value);
});
const filterList = searchTerm => {
    searchTerm = searchTerm.toLowerCase();
    optionsList.forEach(option => {
        let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
        if(label.indexOf(searchTerm) != -1){
            option.style.display = "block";
        } else {
            option.style.display = "none";
        }
    })
}

const grid = new Muuri('.grid', {
    layout:{
        rounding:false
    }
});

$(document).ready(function(){
    var table = $('#first-table').DataTable({
        "language": {
            "lengthMenu": "Mostrar _MENU_ registros",
            "zeroRecords": "No se encontraron resultados",
            "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
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
    grid.refreshItems().layout();
    document.getElementById('grid').classList.add('imagenes-cargadas');
    const enlaces = document.querySelectorAll('#categorias a');
    enlaces.forEach((elemento) => {
        elemento.addEventListener('click', (evento) => {
            evento.preventDefault();
            const categoria = evento.target.innerHTML;
            console.log(categoria);
            if(categoria == 'Todos'){
                grid.filter('[data-categoria]')
            } else {
                grid.filter(`[data-categoria = "${categoria}"]`)
            }
        });
    });
    
});

const overlay = document.getElementById('overlay');
document.querySelectorAll('.separar .grid .item img').forEach( (elemento) => {
    elemento.addEventListener("click", () => {
        const ruta = elemento.getAttribute('src');
        const descripcion = elemento.parentNode.parentNode.dataset.descripcion;
        overlay.classList.add('activo');
        document.querySelector('#overlay img').src = ruta;
        document.querySelector('#overlay .descripcion').innerHTML = descripcion;
    });
}); 
document.querySelector('#btn-cerrar-popup').addEventListener("click", () => {
    overlay.classList.remove('activo');
});
overlay.addEventListener("click", (evento) => {
    if (evento.target.id == 'overlay'){
        overlay.classList.remove('activo');
    }
});
/* Modal */
let cerrar = document.querySelectorAll(".close")[0];
let modal = document.querySelectorAll(".modal")[0];
let modalC = document.querySelectorAll(".modal-container")[0];
let abrir = document.getElementById("agregar");

abrir.addEventListener("click", function(){
    modalC.style.opacity = "1";
    modalC.style.visibility = "visible";
    modal.classList.toggle("modal-close");
});

cerrar.addEventListener("click", function(){
    modal.classList.toggle("modal-close");
    setTimeout(function(){
        modalC.style.opacity = "0";
        modalC.style.visibility = "hidden";
    },600);
});
window.addEventListener("click", function(e){
    if(e.target == modalC){
        modal.classList.toggle("modal-close");
        setTimeout(function(){
            modalC.style.opacity = "0";
            modalC.style.visibility = "hidden";
        },600);
    }
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
function pointsButton(){
    let timerInterval

    Swal.fire({
    title: 'Espera un momento estamos consultando los datos',
    html: 'Faltan <b>/b> segundos.',
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
    }).then((result) => {
    /* Read more about handling dismissals below */
    if (result.dismiss === Swal.DismissReason.timer) {
        console.log('I was closed by the timer')
    }
    })
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
