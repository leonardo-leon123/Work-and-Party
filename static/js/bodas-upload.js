// $(document).ready(function(){
//     (async() => {
//         const {value: email} = await
//         Swal.fire({
//             title: 'Confirma tu correo',
//             input: 'email',
//             inputLabel: 'Escribe tu email con el que reservaste',
//             inputPlaceholder: 'Escribe aqui tu email',
//         })
//         if(email){
//             let data = {
//                 "Correo": email
//             }
//             console.log(data)
//             $.ajax({​​
//                 url: '/confrim',
//                 method: 'POST',
//                 headers: {​​
//                     'Content-Type':'application/json'
//                 }​​,
//                 dataType: 'json',
//                 data: JSON.stringify(data),
//                 success: function(data){​​
//                     if(data['alerta'] === 'Si'){​​
//                         Swal.fire({​​
//                             icon: 'success',
//                             title: 'Enviado',
//                             text: 'El correo fue enviado con éxito'
//                         }​​);
//                         var id = data['id']
//                     }​​ else {​​
//                         Swal.fire({​​
//                             icon: 'error',
//                             title: 'Oops...',
//                             text: 'Hubo un error al enviar el correo ; Inténtelo de nuevo'
//                         }​​);
//                     }​​
//                 }​​
//             }​​)
//         }
//     })()
// })
// $(document).ready(function(){
//     async function ValidarCorreo() {
//         const {value: email} = await
//         Swal.fire({
//             title: 'Confirma tu correo',
//             input: 'email',
//             inputLabel: 'Escribe tu email con el que reservaste',
//             inputPlaceholder: 'Escribe aqui tu email',
//         })
//         if(email)
//         {
//             let data = {
//                 "Correo": email
//             }
//             console.log(data)
//         }
//     }
// })


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
function readURL2(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah2')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
function readURL3(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah3')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}