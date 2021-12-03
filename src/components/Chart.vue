<template>
  <div>
      <div class="q-ml-md" id="chart"></div>
  </div>
</template>

<script>
import { createChart, CrosshairMode } from 'lightweight-charts'

export default {
    methods: {
        createChart() {
            var candlesticks = new Array
            let data = []

            let burl = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=2"
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
                    /* let timestamp = parseInt(element[0])
                    let date = new Date(timestamp);
                    let year = date.getFullYear()
                    let month = date.getMonth()
                    let day = date.getDate()
                    element[0]=year+'-'+month+'-'+day */
                    element[0]= parseInt(element[0])/1000
                    element[1]=element[1].replace('"', '')
                    element[2]=element[2].replace('"', '')
                    element[3]=element[3].replace('"', '')
                    element[4]=element[4].replace('"', '')
                    data.push({"time":element[0],"open":parseFloat(element[1]),"high":parseFloat(element[2]),"low":parseFloat(element[3]),"close":parseFloat(element[4])})
                    
                })
            }
            request.send()
            
            console.log(data);

            var chart = createChart(document.getElementById('chart'), {
            width: 800,
            height: 300,
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

            candleSeries.setData(data);

            let wsBTC = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@trade')
            wsBTC.onmessage = (event) => {
            let data = JSON.parse(event.data)
            }
        }
    },
    mounted() {
        this.createChart()
    }
}
</script>

<style lang="scss" scoped>
.tv-lightweight-charts {
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px;
        margin-bottom: 20px;
        
    }
</style>