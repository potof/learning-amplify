<template>
  <h1>いままで読んだ本</h1>

  <h2>推移</h2>
  <div class="wrapper">
    <LineChart :chartData="lineData" />
  </div>

  <h2>内訳</h2>
  <PieChart :chartData="pieData" />

  <h2>List</h2>
  <table>
    <thead>
      <tr>
        <th>Title</th>
        <th>date</th>
        <th>page</th>
      </tr>
    </thead>
    <tbody>
      <div v-for="item in books" :key="item.id">
        <tr>
          <td>
            {{ item.title }}
          </td>
          <td>
            {{ item.readDate }}
          </td>
          <td>
            {{ item.page }}
          </td>
        </tr>
      </div>
    </tbody>
  </table>
</template>

<script lang="ts">
import { API } from "aws-amplify";
import { listBooks } from "../graphql/queries";

import { Chart, ChartData, registerables } from "chart.js";
import { defineComponent } from "vue";
import { PieChart, LineChart } from "vue-chart-3";
Chart.register(...registerables);

export default defineComponent({
  name: "Test",
  data() {
    return {
      title: "",
      readDate: "",
      page: "",
      books: [],
    };
  },
  components: {
    PieChart,
    LineChart,
  },
  created() {
    this.getBooks();
  },
  setup() {
    const lineData: ChartData<"line"> = {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
      datasets: [
        {
          label: "My First Dataset",
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: true,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    };

    const pieData: ChartData<"pie"> = {
      labels: ["Red", "Blue", "Yellow"],
      datasets: [
        {
          label: "My First Dataset",
          data: [300, 50, 100],
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)",
          ],
          hoverOffset: 4,
        },
      ],
    };
    return { pieData, lineData };
  },

  methods: {
    async getBooks() {
      const books = await API.graphql({
        query: listBooks,
        variables: {
          limit: 1000,
        },
      });
      console.log("aaa");
      console.log(books);
      ((books: any) => {
        this.books = books.data.listBooks.items;
      })(books);
    },
  },
});
</script>

<style scoped>
.wrapper {
  /* display: flex; */
  /* width: 300px; */
}
</style>
