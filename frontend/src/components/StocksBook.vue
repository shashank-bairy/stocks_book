<template>
  <div class="stocks-book">
    <div class="stocks-container">
      <div class="stocks-header">
        <h1 class="stocks-title">StocksBook</h1>
        <img class="stocks-logo" :src="require('./../assets/bb.png')" />
      </div>
      <div class="stocks-searchbox">
        <div class="p-inputgroup">
          <InputText type="text" v-model="search_value" />
          <Button
            icon="pi pi-search"
            label="Search"
            class="p-button-primary"
            @click="handleSearch"
          />
        </div>
      </div>
      <StocksTable :stocks="stocks" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import StocksTable from "./StocksTable.vue";

export default {
  name: "StocksBook",
  components: {
    StocksTable,
  },
  data() {
    return {
      stocks: [],
      search_value: "",
    };
  },
  methods: {
    handleSearch() {
      if (this.search_value === "") {
        this.stocks = [];
      } else {
        axios
          .get(`http://localhost:8000/stocks/search/${this.search_value}`)
          .then((res) => (this.stocks = res.data));
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.stocks-book {
  padding: 50px;
  background-color: #29bb89;
  display: flex;
  justify-content: center;
  min-height: 100vh;
}
.stocks-container {
  width: 100%;
  background-color: #f9f9f9;
  display: flex;
  padding-top: 5rem;
  align-items: center;
  flex-direction: column;
}
.stocks-header {
  display: flex;
  justify-content: space-evenly;
  align-items: flex-end;
  padding-bottom: 2rem;
  width: 30rem;
}

.stocks-title {
  font-size: 3.5rem;
}

.stocks-logo {
  height: 5rem;
}
.stocks-searchbox {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
}
.stocks-inputbox {
  display: flex;
  align-items: center;
  width: 50%;
}
.stocks-input {
  width: 100%;
}
</style>
