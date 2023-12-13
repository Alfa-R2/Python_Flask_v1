let editing=false;
let cod=0;
// CREATE
productsForm.addEventListener("submit",async (e)=>{
    e.preventDefault();
    let descripcion=productsForm["txt_desc"].value;
    let categoria=productsForm["txt_cat"].value;
    let precio=productsForm["numb_prec"].value;
    let url='/api/productos';
    let method="POST";
    let procedure="insert_productos";
    if(editing){
        //UPDATE
        url=`/api/productos/${cod}`;
        method="PUT";
        procedure="update_productos"
        editing=false;
    }
    const response=await(await fetch(url,{
        method:method,
        headers:{
            "content-type":"application/json"
        },
        body:JSON.stringify({
            descripcion,
            categoria,
            precio
        })
    })).json();
    alert(response[0][procedure]);
    productsForm.reset();
    read();
})
// READ
const read=async ()=>{
    const response= await ((await fetch("/api/productos")).json());
    productsList.innerHTML="";
    response.forEach(producto => {
        const productItem= document.createElement("li")
        productItem.classList="" //Agregar clases
        productItem.innerHTML= `
        <br>
        <h3>${producto.descripcion}</h3>
        <button class="btnDelete">Eliminar</button>
        <button class="btnUpdate">Actualizar</button> <br>
        <span>${producto.codigo} </span><span>${producto.categoria} </span><span>${producto.precio}</span>
        `
        productsList.append(productItem);
        const btnDelete= productItem.querySelector(".btnDelete")
        btnDelete.onclick=(e)=>{
            if (confirm("¿Desea eliminar este producto?")){
                eliminar(producto.codigo);
            }  
        }
        const btnUpdate= productItem.querySelector(".btnUpdate");
        btnUpdate.onclick=(e)=>{
            edit(producto.codigo);
        }
    });
};
//DELETE
const eliminar= async(id)=>{
    const request= await fetch(`/api/productos/${id}`, {
        method:"DELETE",
        headers:{
            "content-type":"application/json"
        }
    })
    const response= await request.json()
    alert(response[0].delete_productos)
    read();
}
//LOAD
window.addEventListener("DOMContentLoaded",(e)=>{
    read();
})
//EDIT
const edit=async(id)=>{
    const request=await((await fetch(`/api/productos/${id}`)).json())
    productsForm["txt_desc"].value=request.descripcion;
    productsForm["txt_cat"].value=request.categoria;
    productsForm["numb_prec"].value=request.precio;
    cod=id;
    editing=true;

}