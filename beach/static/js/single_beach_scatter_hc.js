function drawScatterChart(results_by_date) {

    var culture = []
    var dna = []

    for (var i = 0; i < results_by_date['dna'].length; i++) {
        result = results_by_date['dna'][i];
        dna.push({x: new Date(result[0]), y:result[1]});
    }
    for (var i = 0; i < results_by_date['culture'].length; i++) {
        result = results_by_date['culture'][i];
        culture.push({x: new Date(result[0]), y: result[1]})
    }

    Highcharts.chart('scatterChart', {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'Sampled Bacteria count'
        },
        subtitle: {
            text: 'from City of Chicago'
        },
        xAxis: {
            tickInterval: (24 * 3600 * 1000), // the number of milliseconds in a day
            allowDecimals: false,
            title: {
                text: 'Date',
                scalable: false
            },
            type: 'datetime',
            minRange: 14 * 24 * 3600000,
            labels: {
                formatter: function() {
                    return Highcharts.dateFormat('%d-%b-%y', (this.value));
                }
            }
        },
        yAxis: {
            title: {
                text: 'Bacteria Count'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: '{point.x}, {point.y} cfu'
                }
            }
        },
        series: [{
            name: 'DNA',
            color: 'rgba(223, 83, 83, .5)',
            data: dna,

        }, {
            name: 'Culture',
            color: 'rgba(119, 152, 191, .5)',
            data: culture
        }]
    });
}
