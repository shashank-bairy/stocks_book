<template>
  <StocksBook />
</template>

<script>
import StocksBook from "./components/StocksBook.vue";

export default {
  name: "App",
  components: {
    StocksBook,
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
}

html,
body {
  background-color: white;
  color: #555;
  font-family: Open Sans, sans-serif;
  font-size: 16px;
  text-rendering: optimizeLegibility;
  overflow-x: hidden;
}
</style>
