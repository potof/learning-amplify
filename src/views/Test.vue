<template>
  <div class="home">
    <h2>This is Test Page</h2>

    <input type="text" v-model="title" placeholder="title">
    <input type="text" v-model="readDate" placeholder="read date">
    <input type="text" v-model="page" placeholder="page">
    <button v-on:click="createBook">Create Book</button>
    <div v-for="item in books" :key="item.id">
      <h3>{{ item.title }}</h3>
      <p>{{ item.readDate }}</p>
      <p>{{ item.page }}</p>
    </div>
  </div>
</template>


<script>
import { API } from 'aws-amplify';
import { createBook } from '../graphql/mutations';
import { listBooks } from '../graphql/queries';

export default {
  name: 'Test',
  data() {
    return {
      title: '',
      readDate: '',
      page: '',
      books: []
    }
  },
  created(){ 
    this.getBooks();
  },
  methods: {
    async createBook() {
      const { title, readDate, page } = this;
      if (!title || !readDate || !page) return;
      const book = { title, readDate, page };
      this.book = [...this.books, book];
      await API.graphql({
        query: createBook,
        variables: {input: book},
      });
      this.title = '';
      this.readDate = '';
      this.page = '';
    },
    async getBooks() {
      const books = await API.graphql({
        query: listBooks
      });
      console.log('aaa')
      console.log(books)
      this.books = books.data.listBooks.items;
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
p {
  color: #42b983;
}
</style>
