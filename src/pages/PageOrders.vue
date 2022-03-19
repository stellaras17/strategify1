<template>
  <q-page>
      <q-list
        v-for="(order, key) in orders"
        :key="key"
        padding
        seperated>
        <q-item
        class="q-mb-md"
        >
            <q-item-section avatar>
            <q-avatar :color="order.type=='BUY' ? 'positive' : order.type=='ERROR' ? 'yellow' : 'negative'" text-color="white" icon="" />
            </q-item-section>
            <div class="col">
                <q-item-section class="text-h6"> {{order.amount}}  {{order.ticker}}</q-item-section>
                <div class="row">
                    <q-item-section class="text-subtitle1">Order placed by strategy:  {{order.strat}}</q-item-section>
                    <q-item-section class="text-subtitle2 text-right text-grey-6"> {{order.time}}</q-item-section>
                </div>
            </div>
        </q-item>
            <q-separator/>
      </q-list>
      <q-btn @click="newOrder()" >Add </q-btn>
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
        ...mapGetters('orders', ['orders'])
    },
    methods: {
        ...mapActions('orders', ['addOrder']),
        newOrder(){
            let payload = {
                type:"BUY",
                strat: "ZIL RSI",
                amount:10000,
                ticker: "ZILUSDT",
                time: Date.now(),
            }
            this.addOrder(payload)
        }
    }
}
</script>

<style>

</style>