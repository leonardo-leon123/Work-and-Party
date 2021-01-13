function Cargar()
{
    console.log("Hola")
    nombre = document.getElementById('nm1').value;   
    nombre2 = document.getElementById('nm2').value;
    curp1 = document.getElementById('crp1').value;    
    curp2 = document.getElementById('crp2').value;
    adr = document.getElementById('adr').value;    
    date = document.getElementById('dt').value;
    lc = document.getElementById('lc').value;
    fn = document.getElementById('fn').value;    
    fn2 = document.getElementById('fn2').value;    
    fn3 = document.getElementById('fn3').value;
    cr = document.getElementById('cr').value;
    ev = document.getElementById('ev').value;
    console.log(nombre,nombre2,curp1,curp2,adr,date,lc,fn,fn2,fn3)
    let data = {
        "Nombre": nombre,
        "Nombre2":nombre2,
        "curp_conyuge1":curp1,
        "curp_conyuge2":curp2,
        "domicilio2":adr,
        "date":date,
        "location":lc,
        "filename":fn,
        "filename2":fn2,
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
            location.href = `/${lc}/${date}/${nombre}/${nombre2}/${curp1}/${curp2}/${adr}/${fn}/${fn2}/${fn3}/${cr}/${ev}`;
        }
    })
      $.ajax({
        url: '/confirmacion',
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