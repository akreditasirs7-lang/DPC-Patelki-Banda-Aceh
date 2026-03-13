const form = document.getElementById("formPendaftaran")

const preview = document.getElementById("previewFoto")

const fotoInput = document.getElementById("foto")

// preview foto

fotoInput.addEventListener("change",function(){

const file = this.files[0]

if(file){

preview.src = URL.createObjectURL(file)

preview.classList.remove("hidden")

}

})

// submit form

form.addEventListener("submit",function(e){

e.preventDefault()

const data = {

nama:document.getElementById("nama").value,

str:document.getElementById("str").value,

kta:document.getElementById("kta").value,

tempatKerja:document.getElementById("tempatKerja").value,

gaji:document.getElementById("gaji").value,

phone:document.getElementById("phone").value,

email:document.getElementById("email").value

}

// ambil data lama

let database = JSON.parse(localStorage.getItem("pendaftar")) || []

// tambah data baru

database.push(data)

// simpan

localStorage.setItem("pendaftar",JSON.stringify(database))

alert("Pendaftaran berhasil")

form.reset()

})
