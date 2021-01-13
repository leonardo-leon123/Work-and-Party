document.getElementById("btn_eventoBoda").addEventListener("click", function(evento){
    evento.preventDefault();
    Swal.fire({
        icon: 'question',
        title: '¿Qué quieres ver?',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: `Contratos`,
        denyButtonText: `Encuestas`,
        confirmButtonColor: '#FFAE00',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#F05656',
        denyButtonColor: '#FFAE00'
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            location.href = "/contratosBoda";
        } else if (result.isDenied) {
            location.href = "/eventosBoda";
        }
    })
});
document.getElementById("btn_eventoTec").addEventListener("click", function(evento){
    evento.preventDefault();
    Swal.fire({
        icon: 'question',
        title: '¿Qué quieres ver?',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: `Contratos`,
        denyButtonText: `Encuestas`,
        confirmButtonColor: '#FFAE00',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#F05656',
        denyButtonColor: '#FFAE00'
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            location.href = "/contratosTec";
        } else if (result.isDenied) {
            location.href = "/eventosTec";
        }
    })
});
document.getElementById("btn_eventoXv").addEventListener("click", function(evento){
    evento.preventDefault();
    Swal.fire({
        icon: 'question',
        title: '¿Qué quieres ver?',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: `Contratos`,
        denyButtonText: `Encuestas`,
        confirmButtonColor: '#FFAE00',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#F05656',
        denyButtonColor: '#FFAE00'
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            location.href = "/contratosXV";
        } else if (result.isDenied) {
            location.href = "/eventosXv";
        }
    })
});
document.getElementById("btn_eventoOtro").addEventListener("click", function(evento){
    evento.preventDefault();
    Swal.fire({
        icon: 'question',
        title: '¿Qué quieres ver?',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: `Contratos`,
        denyButtonText: `Encuestas`,
        confirmButtonColor: '#FFAE00',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#F05656',
        denyButtonColor: '#FFAE00'
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            location.href = "/contratosOtros";
        } else if (result.isDenied) {
            location.href = "/eventosOtro";
        }
    })
});

function redireccionar(url){
    console.log(url);
    window.locationf= url;
}setTimeout ("redireccionar()", 5000);