<template>
  <DataTable
    ref="st"
    :value="stocks"
    v-if="stocks.length"
    showGridlines
    stripedRows
    :paginator="true"
    :rows="10"
    paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    :rowsPerPageOptions="[10, 20, 50]"
    responsiveLayout="scroll"
    class="stocks-table"
  >
    <template #header>
      <div style="text-align: left">
        <Button
          icon="pi pi-external-link"
          label="Export"
          @click="exportCSV($event)"
        />
      </div>
    </template>
    <Column field="code" header="Code"></Column>
    <Column field="name" header="Name"></Column>
    <Column field="open" header="Open" style="text-align: right">
      <template #body="slotProps">
        {{ formatCurrency(slotProps.data.open) }}
      </template>
    </Column>
    <Column field="high" header="High" style="text-align: right">
      <template #body="slotProps">
        {{ formatCurrency(slotProps.data.high) }}
      </template>
    </Column>
    <Column field="low" header="Low" style="text-align: right">
      <template #body="slotProps">
        {{ formatCurrency(slotProps.data.low) }}
      </template>
    </Column>
    <Column field="close" header="Close" style="text-align: right">
      <template #body="slotProps">
        {{ formatCurrency(slotProps.data.close) }}
      </template>
    </Column>
    <template #paginatorLeft> </template>
    <template #paginatorRight> </template>
  </DataTable>
</template>
<script>
export default {
  name: "StocksTable",
  props: {
    stocks: {
      type: Array,
      required: true,
    },
  },
  methods: {
    formatCurrency(value) {
      return `₹${value.toFixed(2)}`;
    },
    exportCSV() {
      this.$refs.st.exportCSV();
    },
  },
};
</script>

<style scoped>
.stocks-table {
  width: 100%;
  padding: 2.5rem;
}
</style>
