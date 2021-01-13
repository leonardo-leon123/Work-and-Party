function Cargar()
{
    console.log("Hola")
    nombre = document.getElementById('nm1').value;   
    curp1 = document.getElementById('crp1').value;
    adr = document.getElementById('adr').value;    
    date = document.getElementById('dt').value;
    lc = document.getElementById('lc').value;
    fn = document.getElementById('fn').value;    
    fn3 = document.getElementById('fn3').value;
    cr = document.getElementById('cr').value;
    ev = document.getElementById('ev').value;
    console.log(nombre,curp1,adr,date,lc,fn,fn3)
    let data = {
        "Nombre": nombre,
        "curp_conyuge1":curp1,
        "domicilio2":adr,
        "date":date,
        "location":lc,
        "filename":fn,
        "filename3":fn3,
        "correo":cr,
        "evento":ev,
    }
    console.log(data)   
    Swal.fire({
      title: '¿Están tus datos correctos?',
      text: "No podrás editarlo después",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: '¡Están correctos!',
      cancelButtonText: "Cancelar",
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          icon: 'success',
          title: 'Perfecto! Tu contrato esta creado, puedes descargarlo dando click en el botón',
          confirmButtonText: `Descargar PDF`,
        }).then((result) => {
          if (result.isConfirmed) {
              location.href = `/${lc}/${date}/${nombre}/${curp1}/${adr}/${fn}/${fn3}/${cr}/${ev}`;
          }
      })
      $.ajax({
        url: '/confirmacion_general',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(data),
        success: function(data){
            if (data['alerta']==='Si'){
                console.log("Confirmado")
            } else {
                console.log("Error en el ajax")
            }
        }
    })
    }
  })
}
