var ctx = document.getElementById("myChart");
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        datasets: [
        {
            type: 'line',
            yAxisID: 'score',
            // backgroundColor: 'transparent',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            tension: 0,
            fill: "+1"
        },
        {
            type: 'line',
            yAxisID: 'score',
            // backgroundColor: 'transparent',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            borderColor: 'rgba(255, 99, 132, 0.5)',
            pointBackgroundColor: 'rgba(255, 99, 132, 0.5)',
            tension: 0,
            fill: "-1"
        },
        {
            yAxisID: 'submission',
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'transparent'
        },
        ]
    },
    plugins: [ChartDataSource],
    options: {
        scales: {
            yAxes: [
            {
                id: 'submission',
                position: 'right',
                gridLines: {
                    drawOnChartArea: false
                },
                scaleLabel: {
                    display: true,
                    fontColor: 'rgb(54, 162, 235)',
                    labelString: '#Submission'
                },
                ticks: {
                    min: 0,
                }
            },
            {
                id: 'score',
                gridLines: {
                    drawOnChartArea: false
                },
                scaleLabel: {
                    display: true,
                    fontColor: 'rgb(255, 99, 132)',
                    labelString: 'Score'
                }
            }
        ]
        },
        plugins: {
            datasource: {
                url: 'data/statistics.csv'
            }
        }
    }
});