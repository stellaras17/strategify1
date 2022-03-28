<template>
    <div v-if="settings.showChart" style="width:100%" class="flex column flex-center">
        <p class="text-center q-mt-xl text-h3"> Daily chart of {{settings.tickerForChart}} </p>
        <div class="chart"  id="chart"></div>
    </div>
</template>

<script>
import {createChart, CrosshairMode, LightweightCharts} from 'lightweight-charts'
import {mapGetters} from 'vuex'

export default {
    data() {
        return {

        }
    },
    computed: {
        ...mapGetters('settings', ['settings']),
    },
    methods: {
        async getData () {
            const resp = await fetch("https://api.binance.com/api/v3/klines?symbol="+this.settings.tickerForChart+"&interval=1d&limit=1000");
            const data = await resp.json();
            let klinedata = data.map((d) => ({
                time: d[0]/1000,
                open: d[1] *1,
                high: d[2] *1,
                low: d[3] *1,
                close: d[4] *1,

            }))
            return klinedata;
            },
        async renderChart() {
            const chartProperties = {
                timeScale: {
                timeVisible: true,
                secondsVisible: true,
                },
                pane: 0,
            };
            const domElement = document.getElementById('chart');
            const chart = createChart(domElement, chartProperties);
            const candleseries = chart.addCandlestickSeries();
            const klinedata = await this.getData();
            candleseries.setData(klinedata);

            let ws = new WebSocket('wss://stream.binance.com:9443/ws/'+this.settings.tickerForChart.toLowerCase()+'@kline_1d')
            ws.onmessage = (event) => {
                let data = JSON.parse(event.data)
                let date = new Date(data.E)
                let year = date.getFullYear();
                let month = date.getMonth()+1;
                let day = date.getDate()+1;
                let formattedTime = year + '-' + month + '-' + day;
                candleseries.update({ time: formattedTime , open: data.k.o, high: data.k.h, low: data.k.l, close: data.k.c });
            }
        }
    },
    mounted() {
        this.renderChart()
    }
}
</script>

<style scoped>
.chart {
    margin: 0 auto;
    margin-top: 2vh;
    width: 70vw;
    height: 50vh;
}


</style>