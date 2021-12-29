<template>
  <h1>いままで読んだ本</h1>

  <h2>推移</h2>
  <div class="wrapper">
    <LineChart :chartData="lineData" />
  </div>

  <h2>内訳</h2>
  <PieChart :chartData="pieData" />

  <h2>List groupby</h2>
  <table>
    <thead>
      <tr>
        <th>author</th>
        <th>page</th>
        <th>count</th>
      </tr>
    </thead>
    <tbody>
      <div v-for="item in groupByYearAll" :key="item.id">
        <tr>
          <td>
            {{ item.year }}
          </td>
          <td>
            {{ item.page }}
          </td>
          <td>
            {{ item.count }}
          </td>
        </tr>
      </div>
    </tbody>
  </table>

  <!-- <h2>List</h2>
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
  </table> -->
</template>

<script lang="ts">
import { API } from "aws-amplify";
import { listBooks } from "../graphql/queries";

import { Chart, ChartData, registerables } from "chart.js";
import { defineComponent, ref } from "vue";
import { PieChart, LineChart } from "vue-chart-3";
Chart.register(...registerables);

export default defineComponent({
  name: "Test",
  components: {
    PieChart,
    LineChart,
  },
  setup() {
    const books = ref([]);
    const groupByYearAll = ref();
    const groupByYearHearder = ref([]);
    const groupByYearCount = ref([]);
    const lineData = ref();

    const load = async () => {
      console.log("hogehoge");

      // AppSync 経由でデータ取得
      const booksapi = await API.graphql({
        query: listBooks,
        variables: {
          limit: 1000,
        },
      });

      // Amplify コードが型推論できずにエラーになるので包んであげているけどやりたいことは books.value への代入
      ((booksapi: any) => {
        books.value = booksapi.data.listBooks.items;
      })(booksapi);
      // };

      // 日付の折れ線グラフを表示するために、年で集計する
      // const groupByYear = () => {
      const groupBy = books.value.reduce((result: any, current: any) => {
        const element = result.find(
          (value: any) => value.year === current.readDate.slice(0, 4)
        );

        if (element) {
          element.count++;
          element.page += current.page;
        } else {
          result.push({
            year: current.readDate.slice(0, 4),
            count: 1,
            page: current.page,
          });
        }

        return result;
      }, []); //初期値は[]

      groupBy.sort((a: any, b: any) => a.year - b.year);
      groupByYearHearder.value = groupBy.map((el: any) => el.year);
      groupByYearCount.value = groupBy.map((el: any) => el.count);

      groupByYearAll.value = groupBy;

      console.log("fugafugaaa");

      lineData.value = {
        labels: groupByYearHearder.value,
        datasets: [
          {
            label: "冊数",
            data: groupByYearCount.value,
            fill: true,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
          },
        ],
      };
    };

    load();
    // groupByYear();
    console.log("setup");
    console.log(groupByYearHearder.value);
    console.log(groupByYearCount.value);

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
    return { pieData, lineData, books, groupByYearAll };
  },
});
</script>

<style scoped>
.wrapper {
  /* display: flex; */
  /* width: 300px; */
}
</style>
