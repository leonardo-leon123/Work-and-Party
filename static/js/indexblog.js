const intro = introJs();
intro.setOptions({
    steps: [
        {
            intro: '¡Bienvenido al Blog! Aqui podrás encontrar comentarios de nuestros eventos y también podrás conversar con Sura.'
        },
        {
            element: '#disqus_thread',
            intro: 'Aquí puedes leer los comentarios o poner un comentario de nuestro servicio.'
        },
        {
            intro: 'Puedes conversar con Sura por si tuviste algun problema con nuestro servicio, puede que te lleves una gran sorpresa.'
        },
        {
            element: '#move-chat',
            intro: 'Da Click Aquí'
        }
    ]
})
intro.start();
let cerrar = document.querySelectorAll(".close")[0];
let abrir = document.querySelectorAll(".cta")[0];
let modal = document.querySelectorAll(".modal")[0];
let modalC = document.querySelectorAll(".modal-container")[0];

abrir.addEventListener("click", function (e) {
    e.preventDefault();
    modalC.style.opacity = "1";
    modalC.style.visibility = "visible";
    modal.classList.toggle("modal-close")
});

cerrar.addEventListener("click", function () {
    modal.classList.toggle("modal-close")
    setTimeout(function () {
        modalC.style.opacity = "0";
        modalC.style.visibility = "hidden";
    }, 600)
});
window.addEventListener("click", function (e) {
    if (e.target == modalC) {
        modal.classList.toggle("modal-close")
        setTimeout(function () {
            modalC.style.opacity = "0";
            modalC.style.visibility = "hidden";
        }, 600)
    }
});

box1 = document.querySelector(".box1");
icon_bg1 = document.querySelector(".box1 .check");
icon_check1 = document.querySelector(".box1 .fa-check");

box2 = document.querySelector(".box2");
icon_bg2 = document.querySelector(".box2 .check");
icon_check2 = document.querySelector(".box2 .fa-check");

box3 = document.querySelector(".box3");
icon_bg3 = document.querySelector(".box3 .check");
icon_check3 = document.querySelector(".box3 .fa-check");

box4 = document.querySelector(".box4");
icon_bg4 = document.querySelector(".box4 .check");
icon_check4 = document.querySelector(".box4 .fa-check");
value_box = 0;

document.querySelector(".box1").addEventListener("click",function(){
    value_box = "3";
    box1.classList.toggle("box-selected");
    icon_bg1.classList.toggle("check-selected");
    icon_check1.classList.toggle("icon-check");

    box2.classList.remove("box-selected");
    icon_bg2.classList.remove("check-selected");
    icon_check2.classList.remove("icon-check");

    box3.classList.remove("box-selected");
    icon_bg3.classList.remove("check-selected");
    icon_check3.classList.remove("icon-check"); 
    
    box4.classList.remove("box-selected");
    icon_bg4.classList.remove("check-selected");
    icon_check4.classList.remove("icon-check"); 
});
document.querySelector(".box2").addEventListener("click",function(){
    value_box = "4";
    box2.classList.toggle("box-selected");
    icon_bg2.classList.toggle("check-selected");
    icon_check2.classList.toggle("icon-check");
    
    box1.classList.remove("box-selected");
    icon_bg1.classList.remove("check-selected");
    icon_check1.classList.remove("icon-check");

    box3.classList.remove("box-selected");
    icon_bg3.classList.remove("check-s elected");
    icon_check3.classList.remove("icon-check"); 
    
    box4.classList.remove("box-selected");
    icon_bg4.classList.remove("check-selected");
    icon_check4.classList.remove("icon-check"); 
});
document.querySelector(".box3").addEventListener("click",function(){
    value_box = "5";
    box3.classList.toggle("box-selected");
    icon_bg3.classList.toggle("check-selected");
    icon_check3.classList.toggle("icon-check"); 

    box2.classList.remove("box-selected");
    icon_bg2.classList.remove("check-selected");
    icon_check2.classList.remove("icon-check");

    box1.classList.remove("box-selected");
    icon_bg1.classList.remove("check-selected");
    icon_check1.classList.remove("icon-check"); 
    
    box4.classList.remove("box-selected");
    icon_bg4.classList.remove("check-selected");
    icon_check4.classList.remove("icon-check"); 
});
document.querySelector(".box4").addEventListener("click",function(){
    value_box = "6";
    box4.classList.toggle("box-selected");
    icon_bg4.classList.toggle("check-selected");
    icon_check4.classList.toggle("icon-check");

    box2.classList.remove("box-selected");
    icon_bg2.classList.remove("check-selected");
    icon_check2.classList.remove("icon-check");

    box3.classList.remove("box-selected");
    icon_bg3.classList.remove("check-selected");
    icon_check3.classList.remove("icon-check");  
    box1.classList.remove("box-selected");
    icon_bg1.classList.remove("check-selected");
    icon_check1.classList.remove("icon-check"); 
});

$(window).scroll(function(){
    var wintop = $(window).scrollTop(), 
    docheight = $(document).height(),
    winheight = $(window).height();
    var result = winheight
    var scroll = (wintop / (docheight - winheight))*100;
    $('.scroll-line').css('width', (scroll+'%'));
});

document.getElementById("icon-menu").addEventListener("click",function(){
    document.getElementById("move-content").classList.toggle('move-container-all');
    document.getElementById("show-menu").classList.toggle('show-lateral');
});

document.getElementById("MChat").addEventListener("click",function(){
    document.getElementById("move-chat").classList.toggle('mostrar-chat');
});

var Form1 = document.getElementById("Form1");
var Form2 = document.getElementById("Form2");
var Form3 = document.getElementById("Form3");

var Next1 = document.getElementById("Next1");
var Next2 = document.getElementById("Next2");
var Back1 = document.getElementById("Back1");
var Back2 = document.getElementById("Back2");
var Fin = document.getElementById("Fin");

Next1.addEventListener("click", function(){
    Form1.style.left = "-1000px";
    Form2.style.left = "40px";
});
Back1.addEventListener("click", function(){
    Form1.style.left = "40px";
    Form2.style.left = "1000px";
});
Next3.addEventListener("click", function(){
    Form2.style.left = "-1000px";
    Form3.style.left = "40px";
});
Back2.addEventListener("click", function(){
    Form2.style.left = "40px";
    Form3.style.left = "1000px";
});

Fin.addEventListener("click",function(){
    nombre = document.getElementById('name').value;
    apellido = document.getElementById('apellido').value;
    fecha = document.getElementById('fecha').value;
    correo = document.getElementById('correo').value;
    asunto = document.getElementById('asunto').value;
    let datos = {
        "nombre" : nombre,
        "apellido" : apellido,
        "fecha" : fecha,
        "correo" : correo,
        "asunto" : asunto,
        "evento" : value_box
    };
    let timerInterval
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
    console.log(datos);
    $.ajax({
        url: '/blog',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(datos),
        success: function(datos) {
            if(datos['alerta'] ===  'Si'){
                Swal.fire({
                    icon: 'success',
                    title: 'Perfecto',
                    text: 'En un lapso de 3 días hábiles le llegará un correo'
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

    modal.classList.toggle("modal-close");
    setTimeout(function () {
        modalC.style.opacity = "0";
        modalC.style.visibility = "hidden";
    }, 600);

    Form2.style.left = "1000px";
    Form3.style.left = "1000px";
    Form1.style.left = "40px";
    
    box1.classList.remove("box-selected");
    icon_bg1.classList.remove("check-selected");
    icon_check1.classList.remove("icon-check"); 
    
    box2.classList.remove("box-selected");
    icon_bg2.classList.remove("check-selected");
    icon_check2.classList.remove("icon-check");

    box3.classList.remove("box-selected");
    icon_bg3.classList.remove("check-selected");
    icon_check3.classList.remove("icon-check"); 
    
    box4.classList.remove("box-selected");
    icon_bg4.classList.remove("check-selected");
    icon_check4.classList.remove("icon-check"); 
    
    document.getElementById("name").value = ""; 
    document.getElementById("apellido").value = ""; 
    document.getElementById("fecha").value = ""; 
    document.getElementById("correo").value = "";
    document.getElementById("asunto").value = "";
});