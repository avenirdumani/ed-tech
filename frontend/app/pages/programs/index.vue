<script setup lang="ts">
import { computed, ref, type ComputedRef, h } from "vue";
import { refDebounced } from "@vueuse/core";
import type { TableColumn, TableRow } from "@nuxt/ui";
import type {
  BaseCursorResponse,
  BaseProgramResponse,
} from "~/types/api_response";

const UBadge = resolveComponent("UBadge");

const search = ref("");
const debouncedSearch = refDebounced(search, 400);
const degreeTypeOptions = [
  { label: "MBA", value: "mba" },
  { label: "MS", value: "ms" },
  { label: "PHD", value: "phd" },
];
const limitOptions = [
  { label: "10 / page", value: 10 },
  { label: "25 / page", value: 25 },
  { label: "50 / page", value: 50 },
];

const selectedDegreeType = ref<string>();
const limit = ref(limitOptions[0]);
const cursor = ref("");

const queryData: ComputedRef<Record<string, any>> = computed(() => {
  let base: Record<string, any> = { limit: limit.value.value };
  if (cursor.value) base.cursor = cursor.value;
  if (debouncedSearch.value.trim().length > 0) base.name = debouncedSearch.value;
  if (selectedDegreeType.value) base.degree_type = selectedDegreeType.value;
  return base;
});

const { data, status } = useAuthenticatedApi<
  BaseCursorResponse<BaseProgramResponse>
>("/programs", { query: queryData });

const isLoading: ComputedRef<boolean> = computed(() => status.value === "pending");
const tableData: ComputedRef<BaseProgramResponse[]> = computed(() => data.value?.items || []);
const hasNext: ComputedRef<boolean> = computed(() => !!data.value?.next_cursor);
const hasPrev: ComputedRef<boolean> = computed(() => !!data.value?.previous_cursor);

function goNext() {
  if (!data.value?.next_cursor) return;
  cursor.value = data.value.next_cursor;
}

function goPrev() {
  if (!data.value?.previous_cursor) return;
  cursor.value = data.value.previous_cursor;
}

function onLimitChange() {
  cursor.value = "";
}

const columns: ComputedRef<TableColumn<BaseProgramResponse>[]> = computed(() => [
  {
    accessorKey: "id",
    header: "Title",
    cell: ({ row }) => row.original.name,
  },
  {
    accessorKey: "degree_type",
    header: "Degree Type",
    cell: ({ row }) => {
      const degreeType: string = row.getValue("degree_type");
      return h(UBadge, { color: "neutral", variant: "soft" }, () => degreeType.toUpperCase());
    },
  },
  {
    accessorKey: "application_deadline",
    header: "Application Deadline",
    cell: ({ row }) => {
      const deadline: string = row.getValue("application_deadline");
      return h(UBadge, { color: "info", variant: "subtle" }, () => deadline);
    },
  },
]);

const onRowSelect = (_: Event, row: TableRow<BaseProgramResponse>) => {
  return navigateTo({ path: `/programs/${row.original.id}` });
};
</script>
<template>
  <div>
    <UPageHeader title="Programs"></UPageHeader>
    <USkeleton v-if="isLoading" class="min-h-full min-w-full" />
    <UCard v-else class="min-h-full min-w-full flex flex-col flex-1">
      <template #header>
        <div class="flex items-center gap-3">
          <UInput
            v-model.trim="search"
            placeholder="Search programs..."
            icon="i-lucide-search"
            class="flex-1"
          />
          <USelectMenu
            v-model="selectedDegreeType"
            :items="degreeTypeOptions"
            value-key="value"
            placeholder="Degree type"
            class="w-48"
            clear
          />
        </div>
      </template>
      <UTable
        class="flex-1 w-full h-96"
        :loading="isLoading"
        :data="tableData"
        :columns="columns"
        @select="onRowSelect"
      />
      <template #footer>
        <div class="flex items-center justify-between">
          <USelectMenu
            v-model="limit"
            :items="limitOptions"
            class="w-32"
            @update:model-value="onLimitChange"
          />
          <div class="flex items-center gap-2">
            <UButton
              icon="i-lucide-chevron-left"
              color="neutral"
              variant="outline"
              :disabled="!hasPrev"
              @click="goPrev"
            />
            <UButton
              icon="i-lucide-chevron-right"
              color="neutral"
              variant="outline"
              :disabled="!hasNext"
              @click="goNext"
            />
          </div>
        </div>
      </template>
    </UCard>
  </div>
</template>
