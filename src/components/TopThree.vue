<template>
        <div class="row prices-div">
            <q-card class="my-card cursor-pointer" @click="goToURL('BTC')">
                <q-card-section class="text-center text-weight-bold">
                    <q-img
                        src="~assets/logos/btc.png"
                        :ratio="1"
                        width="140px"
                    />
                </q-card-section>
                <q-card-section :class="btcclass" class="text-center text-weight-bold text-size">
                    {{ btcPrice }}$
                </q-card-section>
            </q-card>
            <q-card class="cursor-pointer my-card" @click="goToURL('ETH')">
                <q-card-section class="text-center text-weight-bold">
                    <q-img
                        src="~assets/logos/eth.png"
                        :ratio="1"
                        width="140px"
                    />
                </q-card-section>
                <q-card-section :class="ethclass" class="text-center text-weight-bold text-size" >
                    {{ ethPrice }}$
                </q-card-section>
            </q-card>
            <q-card class="cursor-pointer my-card" @click="goToURL('BNB')">
                <q-card-section class="text-center text-weight-bold">
                    <q-img
                        src="~assets/logos/bnb.png"
                        :ratio="1"
                        width="140px"
                    />
                </q-card-section>
                <q-card-section :class="bnbclass" class="text-center text-weight-bold text-size">
                    {{ bnbPrice }}$
                </q-card-section>
            </q-card>
        </div>
    
</template>

<script>
import { openURL } from 'quasar'

export default {
    data() {
        return {
            btcPrice: 0,
            ethPrice: 0,
            bnbPrice: 0,
            latestPriceBTC: 0,
            latestPriceETH: 0,
            latestPriceBNB: 0,
            btcclass: 'text-black',
            ethclass: 'text-black',
            bnbclass: 'text-black',
        }
    },
    methods: {
        fetchData() {
            let wsBTC = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@trade')
            let wsETH = new WebSocket('wss://stream.binance.com:9443/ws/ethusdt@trade')
            let wsBNB = new WebSocket('wss://stream.binance.com:9443/ws/bnbusdt@trade')
            

            wsBTC.onmessage = (event) => {
                let data = JSON.parse(event.data)
                this.btcPrice = parseFloat(data.p).toFixed(2)
                this.btcclass = this.checkColor(this.btcPrice, this.latestPriceBTC)
                this.latestPriceBTC = this.btcPrice
            }
            wsETH.onmessage = (event) => {
                let data = JSON.parse(event.data)
                this.ethPrice = parseFloat(data.p).toFixed(2)
                this.ethclass = this.checkColor(this.ethPrice, this.latestPriceETH)
                this.latestPriceETH = this.ethPrice
                
            }
            wsBNB.onmessage = (event) => {
                let data = JSON.parse(event.data)
                this.bnbPrice = parseFloat(data.p).toFixed(2)
                this.bnbclass = this.checkColor(this.bnbPrice, this.latestPriceBNB)
                this.latestPriceBNB = this.bnbPrice
                
            }
        },
        checkColor(price, latestPrice) {
            let classstyle = ""

            if(Math.round(latestPrice)==0 || Math.round(latestPrice) === Math.round(price)){
                classstyle='text-black'
            }else {
                if(Math.round(price) > Math.round(latestPrice)) {
                    classstyle='text-green'
                }else {
                    classstyle='text-red'
                }
            }
            return classstyle     
        },
        goToURL(value) {
            switch(value){
                case 'BTC':
                    openURL('https://www.tradingview.com/symbols/BTCUSD/')
                    break
                case 'ETH':
                    openURL('https://www.tradingview.com/symbols/ETHUSD/')
                    break
                case 'BNB':
                    openURL('https://www.tradingview.com/symbols/BNBUSDT/')
                    break
            }
        }
    },
    mounted() {
        this.fetchData()
        }
 }

</script>

<style lang="scss" scoped>
    .prices-div{
        max-width: 800px;
        margin: 0 auto;
    }
    .my-card {
        width: 100%;
        max-width: 230px;
        margin-left:5px
    }
    .text-size {
        font-size: 20px;
    }
    
</style>