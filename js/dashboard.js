const table = document.getElementById("dataTable")

let database = JSON.parse(localStorage.getItem("pendaftar")) || []

function tampilkanData(){

table.innerHTML = ""

database.forEach((data,index)=>{

table.innerHTML += `

<tr class="border-b">

<td class="p-3">${data.nama}</td>

<td class="p-3">${data.str}</td>

<td class="p-3">${data.kta}</td>

<td class="p-3">${data.tempatKerja}</td>

<td class="p-3">${data.gaji}</td>

<td class="p-3">${data.phone}</td>

<td class="p-3">${data.email}</td>

<td class="p-3">

<button onclick="hapus(${index})" class="bg-red-500 text-white px-3 py-1 rounded">

Hapus

</button>

</td>

</tr>

`

})

}

function hapus(index){

database.splice(index,1)

localStorage.setItem("pendaftar",JSON.stringify(database))

tampilkanData()

}

tampilkanData()
