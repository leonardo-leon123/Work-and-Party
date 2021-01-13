/* Onboarding */
const intro = introJs();
intro.setOptions({
    steps: [
        {
            intro: '¡Hola que tal! Esto es una guia sobre la pagina.'
        },
        {
            element: '#step-one',
            intro: 'En esta sección te podemos apoyar con volviendo a poner este tutorial \n o puedes enviar un correo a soporte si no funciona algo.'
        },
        {
            intro: 'Tenemos un top donde se muestran los compañeros que han recuperado a clientes molestos; más adelante te diré como ganarte esos puntos.'
        },
        {
            element: '#leaderboard',
            intro: 'Aqui esta el top 5.'
        },
        {
            intro: 'Ahora pon el puntero del mouse en "Encuestas" y elige una categoria de eventos \n ¡Nos vemos allá!'
        }
    ]
})
document.querySelector('.star-steps').addEventListener("click", function(){
    intro.start();
});

let ubicacionPrincipal = window.pageYOffset;
let cerrar = document.querySelectorAll(".close")[0];
let abrir = document.querySelectorAll(".cta")[0];
let modal = document.querySelectorAll(".modal")[0];
let modalC = document.querySelectorAll(".modal-container")[0];
AOS.init();

window.addEventListener("scroll", function () {
    let actual = this.window.pageYOffset;
    if (ubicacionPrincipal >= actual) {
        this.document.getElementsByTagName("nav")[0].style.top = "0px"
    } else {
        document.getElementsByTagName("nav")[0].style.top = "-100px"
    }
    ubicacionPrincipal = actual;
})
//Menú
let e_header = document.querySelectorAll(".enlaces-header")[0];
let semaforo = true;
document.querySelectorAll(".hamburger")[0].addEventListener("click", function () {
    if (semaforo) {
        document.querySelectorAll(".hamburger")[0].style.color = "#fff";
        semaforo = false
    } else {
        document.querySelectorAll(".hamburger")[0].style.color = "#000";
        semaforo = true
    }
    e_header.classList.toggle("menu2")
})

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
    }, 900)
});

window.addEventListener("click", function (e) {
    console.log(e.target)
    if (e.target == modalC) {
        modal.classList.toggle("modal-close")
        setTimeout(function () {
            modalC.style.opacity = "0";
            modalC.style.visibility = "hidden";
        }, 600)
    }
});
