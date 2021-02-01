function actualizar(){
    document.getElementById("FormularioActualizar").action="/Actualizar";
} 

function eliminar(){
    document.getElementById("FormularioActualizar").action="/Actualizar/Eliminar";
} 

function publicar() {
    document.getElementById("FormularioActualizar").action = "/crearBlog";
} 

function cambiarContrasena() {
    document.getElementById("FormularioActualizar").action = "/cambiarContrasena";
} 
