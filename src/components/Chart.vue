<template>
  <div id="chart" />
</template>

<script>
import { createChart } from 'lightweight-charts';
export default {
    data() {
        return {
            
        }
    },
    methods: {
        createChart() {
            /* let chartProperties = {
                width:1500,
                height:600
            }
            let chart = createChart(document.getElementById('chart', chartProperties))
            let candleseries= chart.addCandlestickSeries() */

            fetch('https://api.binance.com/api/v3/kline?symbol=BNBBTC&interval=5m&limit=1000')
            .then(res => res.json(), console.log(res))
            .then(data => {
                let cdata = data.map(data => {
                    return {time:data[0]/1000,open:parseFloat(data[1]),high:parseFloat(data[2]),low:parseFloat(data[3]),close:parseFloat(data[4])}
                })
                console.log(cdata);
            })
            .catch(err => console.log(err))
        }
    },
    mounted() {
        this.createChart()
    }
 }

</script>

<style>

</style>