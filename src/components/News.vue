<template>
  <div class="bg-grey-2">
    <q-item-label
          header
          class="text-primary"
        >
          News
        </q-item-label>
        <q-list v-for="(article,title) in news" :key="title" >
        <q-card style="max-width: 300px;" class="q-mb-lg q-ml-xs cursor-pointer" @click="goToUrl(article.url)"  >
        <img :src="article.urlToImage">

        <q-card-section>
            <div class="text-h6">{{article.title}}</div>
        </q-card-section>

        
        </q-card >
        </q-list>
  </div>
</template>

<script>
import { openURL } from 'quasar'
export default {
    data() {
        return {
            news: []
        }
    },
    methods: {
        fetchNews(){
            var news = new Array
            fetch('https://newsapi.org/v2/everything?q=Bitcoin&from=2021-12-19&sortBy=publishedAt&apiKey=80489bc6cf9d4a489e5cc3aa0daf8f05')
            .then(a=>a.json())
            .then(response => response.articles.forEach(element => {
                news.push(element)
            }))
            this.news=news
            console.log(this.news);
        },
        goToUrl(url) {
            openURL(url)
        }
    },
    mounted() {
        this.fetchNews()
    }
}
</script>

<style>

</style>