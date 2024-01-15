document.addEventListener("DOMContentLoaded", function () {
            var ctx = document.getElementById("grafico_lineas").getContext("2d");
            var myChart = new Chart(ctx, {
                type: "line",
                data: datos_grafica_lineas,
                options: {
                    scales: {
                        x: {
                            type: "category",
                            labels: datos_grafica_lineas.labels,
                        },
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        });