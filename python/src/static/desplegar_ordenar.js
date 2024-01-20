document.getElementById("botonOrdenar").addEventListener("click", function() {
    var contenedorOrdenar = document.getElementById("contenedorOrdenar");
    
    contenedorOrdenar.style.display = (contenedorOrdenar.style.display === "none") ? "block" : "none";

    if (contenedorOrdenar.style.display === "block") {
        contenedorOrdenar.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});