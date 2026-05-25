<script setup lang="ts">
import { computed, h, ref } from "vue";
import type { ComputedRef } from "vue";
import { type TableRow, type TableColumn } from "@nuxt/ui";
import type { ApplicationPreview, BaseCursorResponse } from "~/types/api_response";

const UBadge = resolveComponent("UBadge");

const limitOptions = [
  { label: "10 / page", value: 10 },
  { label: "25 / page", value: 25 },
  { label: "50 / page", value: 50 },
];

const limit = ref(limitOptions[0]);
const cursor = ref("");

const queryData = computed(() => {
  const base: Record<string, any> = { limit: limit.value.value };
  if (cursor.value) base.cursor = cursor.value;
  return base;
});

const { data, status } = useAuthenticatedApi<BaseCursorResponse<ApplicationPreview>>(
  "/applications",
  { query: queryData },
);

const isLoading: ComputedRef<boolean> = computed(() => status.value === "pending");
const tableData: ComputedRef<ApplicationPreview[]> = computed(() => data.value?.items ?? []);
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

const readinessColor = (score: number): string => {
  if (score >= 80) return "success";
  if (score >= 50) return "warning";
  return "error";
};

const milestoneStatusColor = (s: string): string => {
  const map: Record<string, string> = {
    completed: "success",
    in_progress: "info",
    pending: "warning",
    overdue: "error",
    not_started: "neutral",
  };
  return map[s] ?? "neutral";
};

const toLocalDate = (iso: string) =>
  new Date(iso).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });

const columns: ComputedRef<TableColumn<ApplicationPreview>[]> = computed(() => [
  {
    accessorKey: "program",
    header: "Program",
    cell: ({ row }) => {
      const program = row.getValue("program") as ApplicationPreview["program"];
      return h("div", [
        h("p", { class: "font-medium text-highlighted text-sm" }, program.name),
        h(
          UBadge,
          { color: "neutral", variant: "soft", size: "sm", class: "mt-0.5" },
          () => program.degree_type.toUpperCase(),
        ),
      ]);
    },
  },
  {
    accessorKey: "program",
    id: "deadline",
    header: "Deadline",
    cell: ({ row }) => {
      const program = row.getValue("program") as ApplicationPreview["program"];
      return h(
        "span",
        { class: "text-sm text-muted" },
        program.application_deadline,
      );
    },
  },
  {
    accessorKey: "readiness_score",
    header: "Readiness",
    cell: ({ row }) => {
      const score: number = row.getValue("readiness_score");
      return h(
        UBadge,
        { color: readinessColor(score), variant: "subtle" },
        () => `${Math.round(score)}/100`,
      );
    },
  },
  {
    accessorKey: "next_milestone",
    header: "Next Milestone",
    cell: ({ row }) => {
      const milestone = row.getValue("next_milestone") as
        | ApplicationPreview["next_milestone"]
        | null;
      if (!milestone) {
        return h("span", { class: "text-sm text-muted" }, "—");
      }
      return h("div", [
        h(
          "p",
          { class: "text-sm font-medium text-highlighted" },
          milestone.title,
        ),
        h("div", { class: "flex items-center gap-1.5 mt-0.5" }, [
          h(
            UBadge,
            {
              color: milestoneStatusColor(milestone.status),
              variant: "subtle",
              size: "sm",
            },
            () => milestone.status.replace(/_/g, " "),
          ),
          h("span", { class: "text-xs text-muted" }, milestone.date),
        ]),
      ]);
    },
  },
  {
    accessorKey: "created_at",
    header: "Applied",
    cell: ({ row }) => {
      const date: string = row.getValue("created_at");
      return h("span", { class: "text-sm text-muted" }, toLocalDate(date));
    },
  },
]);

const onRowSelect = (_: Event, row: TableRow<ApplicationPreview>) => {
  return navigateTo({ path: `/applications/${row.original.id}` });
};
</script>

<template>
  <div>
    <UPageHeader title="Applications" />
    <USkeleton v-if="isLoading" class="min-h-full min-w-full" />
    <UCard v-else class="min-h-full min-w-full flex flex-col flex-1 mt-4">
      <div class="overflow-x-auto">
        <UTable
          class="flex-1 w-full"
          :loading="isLoading"
          :data="tableData"
          :columns="columns"
          @select="onRowSelect"
        />
      </div>
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
