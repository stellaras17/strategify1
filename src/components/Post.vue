<template>

    <div class="col">
        <div style="margin-top:0 !important" class="row">
          <div class="q-ml-xs" style="margin-top:0">
            <img style="max-height: 30px; border-radius:14px" src="https://cdn.quasar.dev/img/boy-avatar.png">
          </div>
          <p  class="q-ml-sm" style="margin-top:0; font-size:18px; font-weight:400">{{post.username}}</p>
        </div>
        <div class="col">
            <div style="margin-left: 1rem" class="row">
                <p style="font-weight:600">{{post.strat.name}}</p>
            </div>
            <div style="margin-left: 1rem" class="row">
                <p class="q-mr-xl">Ticker: {{post.strat.ticker}}</p>
                
                <p>Timeframe: {{post.strat.timeframe}}</p>
            </div>
            <div class="row" style="width:100%">
                <div class="col bg-info q-ma-sm">
                    <q-item-section class="bg-green-5 ">
                        <q-item-label class="text-center text-weight-bolder" >BUY @</q-item-label>
                    </q-item-section>

                    <q-item-section >
                        
                        <q-item >
                        <q-item-section>
                            <q-item-label>Indicator: {{ post.strat.buyConditions.indicator }}</q-item-label>
                        </q-item-section>

                        <q-item-section>
                            <q-item-label> {{ post.strat.buyConditions.targetValue }}</q-item-label>
                        </q-item-section>

                        </q-item>
                        
                    </q-item-section>
                    </div>
                    

                    <div class="col bg-info q-ma-sm">
                    <q-item-section class="bg-red-5 ">
                        <q-item-label class="text-center text-weight-bolder" >SELL @</q-item-label>
                    </q-item-section>

                    <q-item-section >
                            <q-item >
                            <q-item-section>
                                <q-item-label>Indicator: {{ post.strat.sellConditions.indicator }}</q-item-label>
                            </q-item-section>

                            <q-item-section>
                                <q-item-label> {{ post.strat.sellConditions.targetValue }} </q-item-label>
                            </q-item-section>

                            </q-item>
                        </q-item-section>
                    </div>
            </div>
            <div class="row q-ml-sm">
                <q-btn @click="dbLikePost(id)" flat :label="post.likes" round :color="userHasLiked ? 'red' : 'primary'" icon="favorite" /> 
            </div>
        </div>
    </div>

</template>

<script>
import { mapActions } from 'vuex'
import { firebaseDb, firebaseAuth } from 'src/boot/firebase'

export default {
    data() {
        return {
           userHasLiked: false
        }
    },
    props: ['post', 'id'],
    methods: {
        ...mapActions('hub', ['dbLikePost']),
        getColors(id) {
            var peopleLiked
            let user = firebaseAuth.currentUser.uid
            let peopleRef = firebaseDb.ref('hub/' + id + '/peopleLiked')
            peopleRef.on('value', function(snapshot) {
                peopleLiked = snapshot.val()
            });
            if(peopleLiked == null){
                this.userHasLiked = false
            }
            else {
                if(peopleLiked.includes(user)){
                    this.userHasLiked = true
                }
                else {
                    this.userHasLiked = false
                }
            }
        },
        dbLikePost(id) {
            var peopleLiked, likes
            let user = firebaseAuth.currentUser.uid
            let peopleRef = firebaseDb.ref('hub/' + id + '/peopleLiked')
            let likesRef = firebaseDb.ref('hub/' + id + '/likes')
            peopleRef.on('value', function(snapshot) {
                peopleLiked = snapshot.val()
            });
            likesRef.on('value', function(snapshot) {
                likes = snapshot.val()
            });
            if(peopleLiked == null){
                let updated = likes+1
                likesRef.set(updated)
                let updatedPeople = [user]
                peopleRef.set(updatedPeople)
                this.userHasLiked = true
            }
            else {
                if(peopleLiked.includes(user)){
                    let updated = likes-1
                    likesRef.set(updated)
                    let updatedPeople = peopleLiked.filter(item => item !== user)
                    peopleRef.set(updatedPeople)
                    this.userHasLiked = false
                    }
                else {
                    let updated = likes+1
                    likesRef.set(updated)
                    let updatedPeople = peopleLiked
                    updatedPeople.push(user)
                    peopleRef.set(updatedPeople)
                    this.userHasLiked = true
                    }
                }
            }
        },
    components: {

    },
    mounted() {
        this.getColors(this.id)
    }
}
</script>

<style>

</style>