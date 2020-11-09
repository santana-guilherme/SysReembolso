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
                label: 'Refund',
                data: data.data,
            }]
        },
        options: {
            responsive: true,
            legend:{ position: 'top' },
            title: {
                display: true,
                text: title
            },
            scales: {
                yAxes: [{ ticks: { min: 0 } }]
            },
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Paired12'
                }
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
            legend:{ position: 'bottom' },
            title: {
                display: true,
                text: title
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
            }]
        },
        options: {
            responsive: true,
            legend:{ position: 'top' },
            title: {
                display: true,
                text: title
            },
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Paired12'
                }
            }
        }
    })
}