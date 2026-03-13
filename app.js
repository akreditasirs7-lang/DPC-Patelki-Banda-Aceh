const form = document.getElementById("formPendaftaran")

const preview = document.getElementById("previewFoto")

const fotoInput = document.getElementById("foto")

fotoInput.addEventListener("change",function(){

const file = this.files[0]

if(file){

preview.src = URL.createObjectURL(file)

preview.classList.remove("hidden")

}

})

form.addEventListener("submit",async function(e){

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

if(!data.nama || !data.email){

alert("Nama dan Email wajib diisi")

return

}

console.log("DATA PENDAFTARAN",data)

alert("Data berhasil dikirim")

// nanti ini bisa kirim ke backend API

/*
await fetch("API_URL",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify(data)
})
*/

})
