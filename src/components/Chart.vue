<template>
    <div class="row">
        <q-space />
      <div class="chart" id="chart" />
      <q-space />
    </div>
      

</template>

<script>
import { createChart, CrosshairMode } from 'lightweight-charts'

export default {
    data() {
        return {
            
        }
    },
    methods: {
        createChart(ticker) {
            
            console.log(ticker);
             var chart = createChart(document.getElementById('chart'), {
                width: 1200,
                height: 500,
                    layout: {
                        backgroundColor: '#000000',
                        textColor: 'rgba(255, 255, 255, 0.9)',
                    },
                    grid: {
                        vertLines: {
                            color: 'rgba(197, 203, 206, 0.5)',
                        },
                        horzLines: {
                            color: 'rgba(197, 203, 206, 0.5)',
                        },
                    },
                    crosshair: {
                        mode: CrosshairMode.Normal,
                    },
                    rightPriceScale: {
                        borderColor: 'rgba(197, 203, 206, 0.8)',
                    },
                    timeScale: {
                        borderColor: 'rgba(197, 203, 206, 0.8)',
                    },
                });
            
            var candleSeries = chart.addCandlestickSeries({
                upColor: 'rgba(255, 144, 0, 1)',
                downColor: '#000',
                borderDownColor: 'rgba(255, 144, 0, 1)',
                borderUpColor: 'rgba(255, 144, 0, 1)',
                wickDownColor: 'rgba(255, 144, 0, 1)',
                wickUpColor: 'rgba(255, 144, 0, 1)',
            });

            var candlesticks = new Array
            var data = new Array

            let burl = "https://api.binance.com/api/v3/klines?symbol="+ticker+"&interval=1d&limit=1000"
            let request = new XMLHttpRequest()
            request.open('GET',burl,true)
            request.onload = function() {
                let response = request.response
                response = response.replace('[[', '')
                response = response.replace(']]', '')
                let candles = response.split('],[')
                
                for (let index = 0; index < candles.length; index++) {
                    candlesticks[index] = candles[index].split(',')
                }
                candlesticks.forEach(element => {
                    //element[0]= parseInt(element[0])/1000
                    let date = new Date(parseInt(element[0]))
                    let year = date.getFullYear();
                    let month = date.getMonth() +1;
                    let day = date.getDate();
                    let formattedTime = year + '-' + month + '-' + day;
                    element[1]=element[1].replace('"', '')
                    element[2]=element[2].replace('"', '')
                    element[3]=element[3].replace('"', '')
                    element[4]=element[4].replace('"', '')
                    data.push({time:formattedTime,open:parseFloat(element[1]),high:parseFloat(element[2]),low:parseFloat(element[3]),close:parseFloat(element[4])})                    
                })
            candleSeries.setData(data);
            }
            request.send()
            

            let wsBTC = new WebSocket('wss://stream.binance.com:9443/ws/'+ticker.toLowerCase()+'@kline_1d')
            wsBTC.onmessage = (event) => {
                let data = JSON.parse(event.data)
                
                let date = new Date(data.E)
                let year = date.getFullYear();
                let month = date.getMonth() +1;
                let day = date.getDate();
                let formattedTime = year + '-' + month + '-' + day;
                candleSeries.update({ time: formattedTime , open: data.k.o, high: data.k.h, low: data.k.l, close: data.k.c });
            }
        }
    },
    mounted() {
        this.createChart('BTCUSDT')
    }
}
</script>

<style lang="scss" scoped>
    .chart {
        margin-left: 0 auto;
        margin-right: 0 auto;
        margin-top: 20px;
        margin-bottom: 20px;
        }
    .tv-lightweight-charts {
        margin-left: 0 auto;
        margin-right: 0 auto;
    }
    table {
        margin-left: 0 auto;
        margin-right: 0 auto;
    }
</style>