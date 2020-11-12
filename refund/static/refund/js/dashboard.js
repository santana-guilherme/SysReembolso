const OVERALL_CHART_COLOR = 'white'

$(document).ready(() => {
    const refunds_by_user = $('#refunds_by_user')
    $.ajax({
        url: refunds_by_user.data('url'),
        success: (data) => {
           barChart(data, refunds_by_user, "Finished refunds by user")
        }
    })

    const solicitations_by_date = $('#solicitations_price_by_month')
    $.ajax({
        url:  solicitations_by_date.data('url'),
        success: (data) => {
            barChart(data, solicitations_by_date, "Gastos com solicitatção por mês")
        }
    })

    const solicitations_overview = $('#solicitations_overview')
    $.ajax({
        url:  solicitations_overview.data('url'),
        success: (data) => {
            doughnutChart(data, solicitations_overview, "Solicitations Overview")
        }
    })

    const solicitations_by_month = $('#solicitations_by_month')
    $.ajax({
        url:  solicitations_by_month.data('url'),
        success: (data) => {
            lineChart(data, solicitations_by_month, "Nº of solicitations by month")
        }
    })
})

function barChart(data, el, title) {
    var ctx  = el[0].getContext('2d');
    new Chart(ctx,{
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Refund price',
                data: data.data,
                backgroundColor: data.colors.map(color => {
                    return color+'78'
                }),
                borderColor: data.colors,
                borderWidth:3
            }]
        },
        options: {
            responsive: true,
            legend:{ position: 'top', labels: { fontColor: OVERALL_CHART_COLOR} },
            title: {
                display: true,
                text: title,
                fontColor: OVERALL_CHART_COLOR
            },
            scales: {
                yAxes: [{ 
                    ticks: { beginAtZero: true, fontColor:OVERALL_CHART_COLOR },
                    scaleLabel:{display: true, labelString:'R$', fontColor: OVERALL_CHART_COLOR},
                    gridLines: {color: OVERALL_CHART_COLOR}
                }],
                xAxes: [{
                    gridLines: { display: false },
                    ticks: {
                        minor: { fontColor:OVERALL_CHART_COLOR }
                    }
                }]
            },
        }
    })
}

function doughnutChart(data, el, title) {
    var ctx  = el[0].getContext('2d');
    new Chart(ctx,{
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Solicitations',
                data: data.data,
            }]
        },
        options: {
            responsive: true,
            legend:{ position: 'bottom', labels: { fontColor: OVERALL_CHART_COLOR} },
            title: {
                display: true,
                text: title,
                fontColor: OVERALL_CHART_COLOR
            },
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Paired12'
                }
            }
        }
    })
}

function lineChart(data, el, title) {
    var ctx  = el[0].getContext('2d');
    new Chart(ctx,{
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Solicitations',
                data: data.data,
                borderColor: data.colors,
                backgroundColor: data.colors[0]+'78',
                borderWidth:3
            }]
        },
        options: {
            responsive: true,
            legend:{ position: 'top', labels: { fontColor: OVERALL_CHART_COLOR} },
            title: {
                display: true,
                text: title,
                fontColor: OVERALL_CHART_COLOR
            },
            scales: {
                yAxes:[{
                    ticks: { fontColor: OVERALL_CHART_COLOR },
                    gridLines: { color: OVERALL_CHART_COLOR }
                }],
                xAxes: [{
                    ticks: { minor: { fontColor:OVERALL_CHART_COLOR } },
                    gridLines: { color: OVERALL_CHART_COLOR }
                }]
            }
        }
    })
}