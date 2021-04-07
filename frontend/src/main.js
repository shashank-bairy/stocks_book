import { createApp } from "vue";
import App from "./App.vue";

import PrimeVue from "primevue/config";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import InputText from "primevue/inputtext";

import "primevue/resources/themes/saga-blue/theme.css"; //theme
import "primevue/resources/primevue.min.css"; //core css
import "primeicons/primeicons.css"; //icons

const app = createApp(App);
app.use(PrimeVue);

app.component("DataTable", DataTable);
app.component("Column", Column);
app.component("Button", Button);
app.component("InputText", InputText);

app.mount("#app");
