<template>
  <h1>いままで読んだ本</h1>

  <div class="container">
    <div class="row">
      <div class="col">
        <p class="h2">{{ days }} <small class="text-muted">days</small></p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <p class="h2">{{ bookCount }} <small class="text-muted">冊</small></p>
      </div>
      <div class="col">
        <p class="h2">
          {{ pageCount }} <small class="text-muted">ページ</small>
        </p>
      </div>
    </div>

    <div class="row">
      <div class="col">
        <p class="h2">
          {{ bookCountYear }} <small class="text-muted">冊／年</small>
        </p>
      </div>
      <div class="col">
        <p class="h2">
          {{ pageCountYear }} <small class="text-muted">ページ／年</small>
        </p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <LineChart :chartData="lineDataSum" />
      </div>
      <div class="col">
        <LineChart :chartData="lineData" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { API } from "aws-amplify";
import { listBooks } from "../graphql/queries";

import { Chart, registerables } from "chart.js";
import { defineComponent, ref } from "vue";
import { LineChart } from "vue-chart-3";
Chart.register(...registerables);

export default defineComponent({
  name: "Test",
  components: {
    LineChart,
  },
  setup() {
    const books = ref();
    const lineData = ref();
    const lineDataSum = ref();

    const days = ref();
    const bookCount = ref();
    const bookCountYear = ref();
    const pageCount = ref();
    const pageCountYear = ref();

    const load = async () => {
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
      books.value.sort((a: any, b: any) => (a.readDate < b.readDate ? -1 : 1));
      // 日付の折れ線グラフを表示するために、年で集計する
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

      let groupByYearHearder: string[] = [];
      let groupByYearCount: string[] = [];
      let groupByYearSum: number[] = [];
      let sumCount = 0;
      groupBy.forEach((element: any) => {
        groupByYearHearder.push(element.year);
        groupByYearCount.push(element.count);

        sumCount += parseInt(element.count);
        groupByYearSum.push(sumCount);
      });

      // 年ごとの冊数グラフ
      lineData.value = {
        labels: groupByYearHearder,
        datasets: [
          {
            label: "年ごと",
            data: groupByYearCount,
            fill: true,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
          },
        ],
      };

      // 累計の冊数グラフ
      lineDataSum.value = {
        labels: groupByYearHearder,
        datasets: [
          {
            label: "累積",
            data: groupByYearSum,
            fill: true,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
          },
        ],
      };

      let yearNum = groupBy.length;
      days.value = (function () {
        let from: number = new Date(books.value[0].readDate).getTime();
        let to: number = new Date(
          books.value[books.value.length - 1].readDate
        ).getTime();
        return (to - from) / 86400000;
      })();
      bookCount.value = books.value.length;
      bookCountYear.value = books.value.length / yearNum;
      pageCount.value = books.value.reduce(
        (sum: number, element: any) => sum + element.page,
        0
      );
      pageCountYear.value = pageCount.value / yearNum;
    };

    load();

    return {
      lineData,
      lineDataSum,
      books,
      days,
      bookCount,
      bookCountYear,
      pageCount,
      pageCountYear,
    };
  },
});
</script>

<style scoped>
small {
  font-size: 18px;
}
</style>
