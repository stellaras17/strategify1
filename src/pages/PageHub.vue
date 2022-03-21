<template>
  <q-page padding>
        <q-list
            style="width:100%"
            class="q-mb-lg"
            v-for="(post, key) in strats"
            :key="key"
            padding
            bordered
            seperated>
            <post
            :post="post"
            :id="key">
            </post>
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
        ...mapGetters('hub', ['strats'])
    },
    methods: {

    },
    components: {
         'post': require('components/Post.vue').default
    }
}
</script>

<style lang="scss">

</style>