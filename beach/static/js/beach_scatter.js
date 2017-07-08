function drawScatter(scatterPlot) {

    var readings = []
    var predictions = []

    for (var i = 0; i < scatterPlot.readings.length; i++) {
        readings.push([Date.parse(scatterPlot.readings[i][0]), scatterPlot.readings[i][1]])
    }

    var series = [{
            name: 'Readings',
            color: 'rgba(223, 83, 83, .5)',
            data: readings

    }]

    var title = 'E-Coli Samples (2017)';

    for (var i = 0; i < scatterPlot.predictions.length; i++) {
        predictions.push([Date.parse(scatterPlot.predictions[i][0]), scatterPlot.predictions[i][1]])
    }

    if (predictions.length > 0) {
        series.push(
            {
                name: 'Predictions',
                color: 'rgba(119, 152, 191, .5)',
                data: predictions
            }
        )
        title = 'E-Coli levels -- Samples vs Predictions (2017)';
    }

    Highcharts.chart('scatterPlotDiv', {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: title
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
                text: 'E-Coli level (cfu)'
            },
            plotLines: [{
                value: 1000,
                color: 'red',
                dashStyle: 'shortdash',
                width: 2,
                label: {
                    text: 'Elevated E-Coli Level'
                }
            }], 
        },
        legend: {
            align: 'right',
            verticalAlign: 'top',
            floating: true,
            x: 0,
            y: 0
        },
        tooltip: {
            formatter: function() {
                    return  '<b>' + this.series.name.slice(0,-1) +'</b><br/>' +
                        Highcharts.dateFormat('%b-%e',
                                              new Date(this.x))
                    + '<br>' + this.y + ' cfu';
            }
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
                        headerFormat: '<b>{series.name}</b><br>'
                }
            }
        },
        series: series
    });
}

