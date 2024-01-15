document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById("grafico_barras").getContext("2d");
    var myChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: datos_grafica.meses,
            datasets: [{
                label: "Viajes por Mes",
                data: datos_grafica.viajes_por_mes,
                backgroundColor: "rgba(255, 132, 132, 0.2)",
                borderColor: "rgba(255, 132, 132, 1)",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }
    });
});