$(document).ready(() => {
    const $user_charts = $('#user_charts')
    $.ajax({
        url: $user_charts.data('url'),
        success: (data) => {
            var ctx  = $user_charts[0].getContext('2d');
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
                            scheme: 'brewer.SetOne3'
                        }
                    }
                }
            })
        }
    })
})

