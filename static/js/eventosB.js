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
document.querySelector('.star-steps').addEventListener("click", function(){
    intro.start();
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
        orderCellsTop: true,
        fixedHeader: true,
        responsive: true
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
