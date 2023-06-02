<script setup>
defineProps({
  items: {
    type: Array,
    required: false,
    default: () => [],
  },
  fields: {
    type: Array,
    default: () => [{ key: "", label: "", formatter: () => {} }],
  },
});

/**Key field accessor for the header field*/
function fieldKey(field, indx) {
  return typeof field === "object" && "key" in field ? field.key : indx;
}

/**Value field accessor for header field */
function fieldText(field) {
  return typeof field === "object" && "label" in field
    ? field.label
    : typeof field == "string"
    ? field
    : "";
}
</script>

<template>
  <div class="flex w-full">
    <div class="flex w-full align-middle inline-block min-w-full">
      <div class="flex flex-col w-full">
        <table
          v-bind="$attrs"
          class="w-full divide-y divide-gray-100 table-auto text-sm"
          data-attribute="status-table"
          v-if="items.length !== 0"
        >
          <thead>
            <tr>
              <th
                v-for="(field, fieldIndex) in fields"
                :key="fieldKey(field, fieldIndex)"
                class="px-2 py-4 bg-gray-50 content-center select-none"
              >
                <div
                  class="flex justify-center font-medium text-gray-600 text-sm"
                >
                  <div class="py-2" :data-testid="`header-div-${fieldIndex}`">
                    {{ fieldText(field) }}
                  </div>
                </div>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <template v-for="(row, rowIndex) in items">
              <tr v-if="row" :key="rowIndex">
                <template v-for="(field, fieldIndex) in fields">
                  <td
                    v-if="field"
                    :id="field.key"
                    :key="`custom-${rowIndex}-${fieldIndex}`"
                    :classes="'border-2 border-gray-100 px-2 my-2'"
                  >
                    <p
                      :name="`cell(${field.key})`"
                      v-bind="row"
                      class="text-black text-center"
                    >
                      {{ row[field.key] }}
                    </p>
                  </td>
                </template>
              </tr>
            </template>
          </tbody>
        </table>
        <div v-else>
          <div
            class="flex text-md h-20 items-center bg-white text-black whitespace-nowrap w-full text-center justify-center"
            data-testid="empty-text"
          >
            No data to show
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
