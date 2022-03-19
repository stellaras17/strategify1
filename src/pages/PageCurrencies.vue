<template>
  <q-page>
      <q-list
        v-for="(currency, key) in currencies"
        :key="key"
        class="q-ma-lg"
        bordered
        seperated>
        <q-item
        class="q-mb-md flex-center"
        >
            <q-item-section avatar>
            <q-avatar>
                <img :src="getIcon(key)"/>
            </q-avatar>
            </q-item-section>
            <div class="col">
                <q-item-section class="text-h6"> {{key}} : {{currency}}</q-item-section>
            </div>
        </q-item>
            
      </q-list>
  </q-page>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'

export default {
    data () {
        return {

        }
    },
    computed: {
        ...mapGetters('currencies', ['currencies'])
    },
    methods: {
        getIcon(ticker){
            switch(ticker) {
                case 'BTC':
                    return require("../assets/logos/btc.png")
                case 'BNB':
                    return require('../assets/logos/bnb.png')
                case 'ETH':
                    return require('../assets/logos/eth.png')
                case 'ZIL':
                    return require('../assets/logos/zil.png')
            }
        }
        }
    }

</script>

<style>

</style>