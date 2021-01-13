/* Medallas */
$(document).ready(function obtenermedallas(){
    obtener = "dame los puntos"
    let data = {
        "obtener": 'dame los puntos',
      };  
    $.ajax({
        url: '/obtenerpuntos',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(data),
        success: function(data){
            if (data['alerta']==='Si'){
                puntos = data['puntos']
                //puntos = 1000               
                $('#show-puntos').html(puntos)
                //hierro
                if (puntos >= 10 && puntos <= 30)
                {
                    $("#hierro").prop("checked", true);
                    
                }
                //bronce
                if (puntos >= 30 && puntos <= 50)
                {
                    $("#bronce").prop("checked", true);
                    
                }
                //plata
                if (puntos >= 50 && puntos <= 100)
                {
                    $("#plata").prop("checked", true);
                    
                }
                //oro
                if (puntos >= 100 && puntos <= 200)
                {
                    $("#oro").prop("checked", true);
                    
                }
                //platino
                if (puntos >= 200 && puntos <= 300)
                {
                    $("#platino").prop("checked", true);
                    
                }
                //diamante
                if (puntos >= 300 && puntos <= 400)
                {
                    $("#diamante").prop("checked", true);
                    
                }
                //maestro
                if (puntos >= 400 && puntos <= 500)
                {
                    $("#maestro").prop("checked", true);
                    
                }
                //gran maestro
                if (puntos >= 500 && puntos <= 1000)
                {
                    $("#gran-maestro").prop("checked", true);
                    
                }
                //retador
                if (puntos >= 1000 && puntos <= 20000)
                {
                    $("#retador").prop("checked", true);
                    
                }
            } else {
                console.log("Error en el ajax")
            }
        }
    })
})



/* Onboarding */
const intro = introJs();
intro.setOptions({
    steps: [
        {
            intro: '¡Hola que tal! Esto es una guía sobre la página.'
        },
        {
            element: '#step-one',
            intro: 'En esta opción podrás visualizar a todos los clientes que estan en proceso de contratación.'
        },
        {
            element:'#step-two',
            intro: 'Aquí podrás escoger que deseas consultar  y que tipo de evento quieres visualizar'
        },
        {
            element: '#step-three',
            intro: 'De igual forma podrás escoger entre "Encuestas y Contratos" según lo que necesites realizar'
        },
        {
            element: '#step-four',
            intro:'Aquí podrás visualizar la cantidad de puntos que llevas acumulados ¡Vamos por más!'
        },
        {
            element: '#step-five',
            intro:'Aquí tenemos un catálogo de medallas donde podrás ver cual es la tuya.'
        },
        {
            intro:'Dale click en "Preventa", nos vemos allá.'
        }
        

        
    ]
})
intro.start();


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

