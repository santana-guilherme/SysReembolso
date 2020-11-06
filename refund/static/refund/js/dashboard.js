$(document).ready(() => {
    const refunds_by_user = $('#refunds_by_user')
    $.ajax({
        url: refunds_by_user.data('url'),
        success: (data) => {
           barChart(data, refunds_by_user)
        }
    })

    const solicitations_by_date = $('#solicitations_by_month')
    $.ajax({
        url:  solicitations_by_date.data('url'),
        success: (data) => {
            barChart(data, solicitations_by_date)
        }
    })
})

function barChart(data, el) {
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
                text: 'Refunds by user'
            },
            scales: {
                yAxes: [{ ticks: { min: 0 } }]
            },
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Paired12'
                }
            },
            layout: {
                width: 300,
                height: 300
            }
        }
    })
}