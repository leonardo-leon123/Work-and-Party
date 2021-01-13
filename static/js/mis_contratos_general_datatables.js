$(document).ready(function () {
  $('.contrato').hide()
  $('.verificado').hide()
  var table = $('#mis_contratos').DataTable({
    //para cambiar el lenguaje a español
    "language": {
      "lengthMenu": "Mostrar _MENU_ registros",
      "zeroRecords": "No se encontraron resultados",
      "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
      "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
      "infoFiltered": "(filtrado de un total de _MAX_ registros)",
      "sSearch": "Buscar:",
      "oPaginate": {
        "sFirst": "Primero",
        "sLast": "Último",
        "sNext": "Siguiente",
        "sPrevious": "Anterior"
      },
      "sProcessing": "Procesando...",
    }
  });
  $(document).on("click", ".BtnVer", function () {
    $('.contrato').hide()
    table
      .row($(this).parents('tr'))
      .remove()
      .draw();
    $('.contrato').hide()
    $(".elige-contrato").hide()
    $('.verificado').fadeIn()
    fila = $(this).closest("tr");
            ID = fila.find('td:eq(0)').text();
            let data = {
              "ID" : ID,
            };
            $.ajax({
              url: '/contratoVerficar',
              method: 'POST',
              headers: {
                  'Content-Type':'application/json'
              },
              dataType: 'json',
              data: JSON.stringify(data),
              success: function(data){
                  if (data['alerta']==='Si'){
                      console.log("Confirmado")
                      points()
                  } else {
                      console.log("Error en el ajax")
                  }
              }
          })
  });




  window.onscroll = function () {
    BarraDeProgreso()
  };

  function BarraDeProgreso() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("barraDeProgreso").style.width = scrolled + "%";
  }

  var fila;
  $(document).on("click", ".BtnPreview", function () {
    $('.verificado').hide()
    $(".elige-contrato").hide()
    $(".contrato").show()
    $('.centeredOverlay').show();
    $(".titulo-contrato").hide()
    fila = $(this).closest("tr");
    ID = fila.find('td:eq(0)').text();
    console.log(ID)
    let data = {
      "ID": ID,
    };
    $.ajax({
      url: '/contratosBoda',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      data: JSON.stringify(data),
      success: function (data) {
        if (data['alerta'] === 'Si') {
          console.log("Si me llego :D")
          var nombre = data['nombre']
          var curp1 = data['curp1']
          var domicilio = data['domicilio']
          var date = data['date']
          var location = data['location']
          var filename = data['filename']
          var filename3 = data['filename3']
          var correo = data['correo']
          var evento = data['evento']
          console.log(nombre, curp1, domicilio, date, location, filename, filename3, correo, evento)
          $(".nombre").html(nombre);
          $(".curp1").html(curp1);
          $(".domicilio").html(domicilio);
          $(".date").html(date);
          $(".location").html(location);
          $(".filename").html(filename);
          $(".filename3").html(filename3);
          $(".correo").html(correo);
          $(".evento").html(evento);
          $(".titular").html(nombre);

          document.getElementById("ine-1").src = `http://127.0.0.1:5000/static/upload/img/${filename}`;
          document.getElementById("domicilio").src = `http://127.0.0.1:5000/static/upload/img/${filename3}`;
          $('.centeredOverlay').hide();
          $(".titulo-contrato").show();
        }

      }
    })
  })
})

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