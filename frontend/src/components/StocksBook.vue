<template>
  <div class="stocks-book">
    <div class="stocks-container">
      <div class="stocks-header">
        <img class="stocks-logo" :src="require('./../assets/logo.png')" />
        <h2 class="stocks-title">StocksBook</h2>
      </div>
      <div class="stocks-searchbox">
        <span class="p-input-icon-left stocks-inputbox">
          <i class="pi pi-search stocks-searchicon" />
          <InputText
            ref="stocks_input"
            type="text"
            class="stocks-input"
            v-model="searchValue"
            @keyup="handleSearch"
          />
        </span>
      </div>
      <div class="stock-tablebox">
        <StocksTable v-if="!searchValueNotFound" :stocks="stocks" />
        <h3 class="stock-notfound" v-else>Stock Not Found!</h3>
      </div>
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
      searchValue: "",
      searchValueNotFound: false,
    };
  },
  mounted() {
    this.$refs.stocks_input.$el.focus();
  },
  methods: {
    handleSearch() {
      if (this.searchValue === "") {
        this.stocks = [];
        this.searchValueNotFound = false;
      } else {
        axios
          .get(`/stocks/search/${this.searchValue}`)
          .then((res) => (this.stocks = res.data))
          .then(
            (data) => (this.searchValueNotFound = !Object.keys(data).length)
          );
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.stocks-book {
  padding: 2rem;
  display: flex;
  justify-content: center;
  min-height: 100vh;
}
.stocks-container {
  width: 100%;
  display: flex;
  padding-top: 5rem;
  align-items: center;
  flex-direction: column;
  background-color: #eeeeee;
}
.stocks-header {
  display: flex;
  justify-content: space-evenly;
  align-items: flex-end;
  padding-bottom: 3rem;
  width: 30rem;
}
.stocks-title {
  font-family: Open Sans, sans-serif;
  font-size: 3.5rem;
  font-weight: 300;
}
.stocks-logo {
  height: 4rem;
}
.stocks-searchbox {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  padding-bottom: 3rem;
  width: 40rem;
}
.stocks-inputbox {
  display: flex;
  align-items: center;
  width: 100%;
}
.stocks-searchicon {
  padding-left: 0.5rem;
}
.stocks-input {
  width: 100%;
  padding-left: 3rem !important;
  border-radius: 2.5rem;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}
.stocks-input:focus {
  border-color: #c1c1c1 !important;
  box-shadow: none !important;
}
.stocks-input:hover {
  border-color: #c1c1c1 !important;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 10px 10px !important;
}
.stock-tablebox {
  width: 90%;
  padding-top: 2.5rem;
  padding-bottom: 2.5rem;
}
.stock-notfound {
  font-family: Open Sans, sans-serif;
  text-align: center;
  font-size: 2rem;
  font-weight: 300;
}
@media only screen and (min-width: 481px) and (max-width: 769px) {
  .stocks-book {
    padding: 1.5rem;
  }
  .stocks-header {
    justify-content: center;
  }
  .stocks-logo {
    height: 3rem;
    margin-right: 0.35rem;
  }
  .stocks-title {
    font-size: 2.75rem;
    margin-left: 0.35rem;
  }
  .stocks-searchbox {
    width: 90%;
  }
  .stock-notfound {
    font-size: 1.5rem;
  }
  .stock-tablebox {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
  }
}

@media only screen and (max-width: 480px) {
  .stocks-book {
    padding: 1rem;
  }
  .stocks-header {
    justify-content: center;
  }
  .stocks-logo {
    height: 2.5rem;
    margin-right: 0.35rem;
  }
  .stocks-title {
    font-size: 2.25rem;
    margin-left: 0.35rem;
  }
  .stocks-searchbox {
    width: 90%;
  }
  .stock-notfound {
    font-size: 1.5rem;
  }
  .stock-tablebox {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }
}
</style>
