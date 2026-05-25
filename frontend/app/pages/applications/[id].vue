<script setup lang="ts">
import { computed, h, ref, watch } from "vue";
import type { ComputedRef } from "vue";
import type { TableColumn } from "@nuxt/ui";
import type {
  DetailedApplicationResponse,
  TimelineResponse,
  ReadinessResponse,
} from "~/types/api_response";

type ChecklistItem = DetailedApplicationResponse["checklist_items"][number];

const UBadge = resolveComponent("UBadge");
const UIcon = resolveComponent("UIcon");
const USelect = resolveComponent("USelect");

const route = useRoute();
const applicationId = route.params.id;

const { data, status, refresh } =
  useAuthenticatedApi<DetailedApplicationResponse>(
    `/applications/${applicationId}`,
  );

const {
  data: timelineData,
  status: timelineStatus,
  execute: executeTimeline,
} = useAuthenticatedApi<TimelineResponse[]>(
  `/applications/${applicationId}/timeline`,
  { immediate: false },
);

const {
  data: readinessData,
  status: readinessStatus,
  execute: executeReadiness,
} = useAuthenticatedApi<ReadinessResponse>(
  `/applications/${applicationId}/readiness`,
  { immediate: false },
);

const isLoading: ComputedRef<boolean> = computed(
  () => status.value === "pending",
);

const application: ComputedRef<DetailedApplicationResponse | null> = computed(
  () => data.value ?? null,
);

const activeTab = ref("checklist");

const statusOptions = [
  { label: "Not Started", value: "not_started" },
  { label: "In Progress", value: "in_progress" },
  { label: "Completed", value: "complete" },
];

const updatingIds = ref<string[]>([]);

const refreshAll = () => {
  refresh();
  if (timelineData.value) executeTimeline();
  if (readinessData.value) executeReadiness();
};

const updateChecklistStatus = async (itemId: string, newStatus: string) => {
  updatingIds.value = [...updatingIds.value, itemId];
  await useAuthenticatedApi(
    `/applications/${applicationId}/checklist/${itemId}`,
    { method: "PATCH", body: { status: newStatus } },
  );
  updatingIds.value = updatingIds.value.filter((id) => id !== itemId);
  refreshAll();
};

watch(activeTab, (tab) => {
  if (
    tab === "timeline" &&
    !timelineData.value &&
    timelineStatus.value !== "pending"
  ) {
    executeTimeline();
  }
  if (
    tab === "readiness" &&
    !readinessData.value &&
    readinessStatus.value !== "pending"
  ) {
    executeReadiness();
  }
});

const toLocalDate = (iso: string) =>
  new Date(iso).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });

const statusColor = (s: string): string => {
  const map: Record<string, string> = {
    complete: "success",
    in_progress: "info",
    pending: "warning",
    overdue: "error",
    not_started: "neutral",
  };
  return map[s] ?? "neutral";
};

const completedCount: ComputedRef<number> = computed(
  () =>
    application.value?.checklist_items.filter((i) => i.status === "complete")
      .length ?? 0,
);

const totalCount: ComputedRef<number> = computed(
  () => application.value?.checklist_items.length ?? 0,
);

const tabItems = [
  {
    label: "Checklist",
    value: "checklist",
    slot: "checklist",
    icon: "i-lucide-list-checks",
  },
  {
    label: "Timeline",
    value: "timeline",
    slot: "timeline",
    icon: "i-lucide-clock",
  },
  {
    label: "Readiness",
    value: "readiness",
    slot: "readiness",
    icon: "i-lucide-target",
  },
];

const columns: ComputedRef<TableColumn<ChecklistItem>[]> = computed(() => [
  { accessorKey: "requirement_title", header: "Requirement" },
  {
    accessorKey: "requirement_type",
    header: "Type",
    cell: ({ row }) => {
      const type: string = row.getValue("requirement_type");
      return h(UBadge, { color: "neutral", variant: "soft" }, () => type);
    },
  },
  {
    accessorKey: "required",
    header: "Required",
    cell: ({ row }) => {
      const required: boolean = row.getValue("required");
      return h(UIcon, {
        name: required ? "i-lucide-check-circle" : "i-lucide-circle",
        class: required
          ? "text-success-500 w-5 h-5"
          : "text-neutral-400 w-5 h-5",
      });
    },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const item = row.original as ChecklistItem;
      return h(USelect, {
        modelValue: item.status,
        items: statusOptions,
        loading: updatingIds.value.includes(item.id),
        size: "sm",
        class: "w-36",
        "onUpdate:modelValue": (val: string) =>
          updateChecklistStatus(item.id, val),
      });
    },
  },
  { accessorKey: "due_date", header: "Due Date" },
  { accessorKey: "notes", header: "Notes" },
]);
</script>

<template>
  <div>
    <div class="flex items-center gap-2 mb-4">
      <UButton
        icon="i-lucide-arrow-left"
        color="neutral"
        variant="ghost"
        size="sm"
        @click="navigateTo('/applications')"
      />
      <USkeleton v-if="isLoading" class="h-8 w-64" />
      <UPageHeader
        v-else
        :title="application?.program.name ?? ''"
        class="flex-1"
      />
    </div>

    <USkeleton v-if="isLoading" class="min-h-96 min-w-full" />

    <template v-else-if="application">
      <div class="flex flex-wrap items-center gap-2 mb-6">
        <UBadge color="neutral" variant="soft" size="lg">
          {{ application.program.degree_type.toUpperCase() }}
        </UBadge>
        <UBadge
          color="info"
          variant="subtle"
          size="lg"
          icon="i-lucide-calendar"
        >
          Deadline: {{ application.program.application_deadline }}
        </UBadge>
        <UBadge
          color="neutral"
          variant="outline"
          size="lg"
          icon="i-lucide-clock"
        >
          Applied: {{ toLocalDate(application.created_at) }}
        </UBadge>
        <div class="flex-1" />
        <UButton
          label="View Program"
          icon="i-lucide-external-link"
          color="neutral"
          variant="soft"
          size="sm"
          @click="navigateTo(`/programs/${application.program.id}`)"
        />
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <UCard>
          <div class="flex items-center gap-3">
            <UIcon
              name="i-lucide-list-checks"
              class="w-6 h-6 text-primary-500 shrink-0"
            />
            <div>
              <p class="text-2xl font-bold text-highlighted">
                {{ totalCount }}
              </p>
              <p class="text-sm text-muted">Total Requirements</p>
            </div>
          </div>
        </UCard>
        <UCard>
          <div class="flex items-center gap-3">
            <UIcon
              name="i-lucide-check-circle"
              class="w-6 h-6 text-success-500 shrink-0"
            />
            <div>
              <p class="text-2xl font-bold text-highlighted">
                {{ completedCount }}
              </p>
              <p class="text-sm text-muted">Completed</p>
            </div>
          </div>
        </UCard>
        <UCard>
          <div class="flex items-center gap-3">
            <UIcon
              name="i-lucide-circle-dashed"
              class="w-6 h-6 text-warning-500 shrink-0"
            />
            <div>
              <p class="text-2xl font-bold text-highlighted">
                {{ totalCount - completedCount }}
              </p>
              <p class="text-sm text-muted">Remaining</p>
            </div>
          </div>
        </UCard>
      </div>

      <UTabs v-model="activeTab" :items="tabItems">
        <template #checklist>
          <UCard class="mt-4">
            <template #header>
              <p class="text-sm font-semibold text-highlighted">Checklist</p>
              <p class="text-sm text-muted">
                {{ completedCount }} of {{ totalCount }} completed
              </p>
            </template>
            <div class="overflow-x-auto">
              <UTable
                class="w-full"
                :data="application.checklist_items"
                :columns="columns"
              />
            </div>
          </UCard>
        </template>

        <template #timeline>
          <div class="mt-4">
            <USkeleton
              v-if="timelineStatus === 'pending'"
              class="min-h-64 w-full"
            />
            <UCard v-else-if="timelineData?.length">
              <template #header>
                <p class="text-sm font-semibold text-highlighted">Timeline</p>
                <p class="text-sm text-muted">
                  {{ timelineData.length }} event{{
                    timelineData.length !== 1 ? "s" : ""
                  }}
                </p>
              </template>
              <ol
                class="relative border-s border-neutral-200 dark:border-neutral-700 ms-3"
              >
                <li
                  v-for="event in timelineData"
                  :key="event.id"
                  class="mb-8 ms-6 last:mb-0"
                >
                  <span
                    class="absolute -inset-s-3 flex h-6 w-6 items-center justify-center rounded-full ring-4 ring-white dark:ring-neutral-900"
                    :class="
                      event.status === 'completed'
                        ? 'bg-success-100 dark:bg-success-900'
                        : event.status === 'overdue'
                          ? 'bg-error-100 dark:bg-error-900'
                          : 'bg-neutral-100 dark:bg-neutral-800'
                    "
                  >
                    <UIcon
                      :name="
                        event.status === 'completed'
                          ? 'i-lucide-check'
                          : 'i-lucide-clock'
                      "
                      class="h-3 w-3"
                      :class="
                        event.status === 'completed'
                          ? 'text-success-600'
                          : event.status === 'overdue'
                            ? 'text-error-600'
                            : 'text-neutral-500'
                      "
                    />
                  </span>
                  <div class="flex flex-wrap items-center gap-2 mb-1">
                    <p class="text-sm font-semibold text-highlighted">
                      {{ event.title }}
                    </p>
                    <UBadge
                      :color="statusColor(event.status)"
                      variant="subtle"
                      size="sm"
                    >
                      {{ event.status.replace(/_/g, " ") }}
                    </UBadge>
                    <time class="text-xs text-muted sm:ms-auto">{{
                      event.date
                    }}</time>
                  </div>
                  <div class="flex flex-wrap gap-2 mt-1">
                    <UBadge color="neutral" variant="soft" size="sm">
                      {{ event.checklist_item.requirement_type }}
                    </UBadge>
                    <p
                      v-if="event.checklist_item.notes"
                      class="text-sm text-muted"
                    >
                      {{ event.checklist_item.notes }}
                    </p>
                  </div>
                </li>
              </ol>
            </UCard>
            <div
              v-else-if="timelineStatus !== 'pending'"
              class="flex flex-col items-center justify-center py-16 text-muted gap-2"
            >
              <UIcon name="i-lucide-calendar-x" class="w-10 h-10" />
              <p class="text-sm">No timeline events found.</p>
            </div>
          </div>
        </template>

        <template #readiness>
          <div class="mt-4">
            <USkeleton
              v-if="readinessStatus === 'pending'"
              class="min-h-64 w-full"
            />
            <template v-else-if="readinessData">
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                <UCard>
                  <div class="flex items-center gap-4">
                    <div
                      class="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-primary-50 dark:bg-primary-900/20"
                    >
                      <p
                        class="text-xl font-bold text-primary-600 dark:text-primary-400"
                      >
                        {{ Math.round(readinessData.readiness_score) }}
                      </p>
                    </div>
                    <div>
                      <p class="text-sm text-muted">Readiness Score</p>
                      <p class="text-sm font-semibold text-highlighted">/100</p>
                    </div>
                  </div>
                </UCard>
                <UCard>
                  <div class="flex items-center gap-3">
                    <UIcon
                      name="i-lucide-circle-x"
                      class="w-6 h-6 text-error-500 shrink-0"
                    />
                    <div>
                      <p class="text-2xl font-bold text-highlighted">
                        {{ readinessData.missing_requirements.length }}
                      </p>
                      <p class="text-sm text-muted">Missing</p>
                    </div>
                  </div>
                </UCard>
                <UCard>
                  <div class="flex items-center gap-3">
                    <UIcon
                      name="i-lucide-flag"
                      class="w-6 h-6 text-info-500 shrink-0"
                    />
                    <div>
                      <p class="text-2xl font-bold text-highlighted">
                        {{ readinessData.next_milestones.length }}
                      </p>
                      <p class="text-sm text-muted">Upcoming Milestones</p>
                    </div>
                  </div>
                </UCard>
              </div>

              <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <UCard v-if="readinessData.missing_requirements.length">
                  <template #header>
                    <p class="text-sm font-semibold text-highlighted">
                      Missing Requirements
                    </p>
                    <p class="text-sm text-muted">
                      {{ readinessData.missing_requirements.length }}
                      outstanding
                    </p>
                  </template>
                  <ul
                    class="divide-y divide-neutral-100 dark:divide-neutral-800"
                  >
                    <li
                      v-for="req in readinessData.missing_requirements"
                      :key="req.requirement_id"
                      class="flex flex-wrap items-start gap-2 py-3 first:pt-0 last:pb-0"
                    >
                      <UIcon
                        name="i-lucide-alert-circle"
                        class="w-4 h-4 text-error-500 mt-0.5 shrink-0"
                      />
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-highlighted">
                          {{ req.title }}
                        </p>
                        <div class="flex flex-wrap items-center gap-2 mt-1">
                          <UBadge color="neutral" variant="soft" size="sm">{{
                            req.type
                          }}</UBadge>
                          <span class="text-xs text-muted"
                            >Due: {{ req.due_date }}</span
                          >
                        </div>
                      </div>
                    </li>
                  </ul>
                </UCard>

                <UCard v-if="readinessData.next_milestones.length">
                  <template #header>
                    <p class="text-sm font-semibold text-highlighted">
                      Upcoming Milestones
                    </p>
                    <p class="text-sm text-muted">
                      {{ readinessData.next_milestones.length }} ahead
                    </p>
                  </template>
                  <ul
                    class="divide-y divide-neutral-100 dark:divide-neutral-800"
                  >
                    <li
                      v-for="(milestone, i) in readinessData.next_milestones"
                      :key="i"
                      class="flex flex-wrap items-start gap-2 py-3 first:pt-0 last:pb-0"
                    >
                      <UIcon
                        name="i-lucide-flag"
                        class="w-4 h-4 text-info-500 mt-0.5 shrink-0"
                      />
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-highlighted">
                          {{ milestone.title }}
                        </p>
                        <div class="flex flex-wrap items-center gap-2 mt-1">
                          <UBadge
                            :color="statusColor(milestone.status)"
                            variant="subtle"
                            size="sm"
                          >
                            {{ milestone.status.replace(/_/g, " ") }}
                          </UBadge>
                          <span class="text-xs text-muted">{{
                            milestone.date
                          }}</span>
                        </div>
                      </div>
                    </li>
                  </ul>
                </UCard>

                <div
                  v-if="
                    !readinessData.missing_requirements.length &&
                    !readinessData.next_milestones.length
                  "
                  class="col-span-full flex flex-col items-center justify-center py-16 text-muted gap-2"
                >
                  <UIcon name="i-lucide-party-popper" class="w-10 h-10" />
                  <p class="text-sm">
                    All caught up — no missing requirements or upcoming
                    milestones.
                  </p>
                </div>
              </div>
            </template>
            <div
              v-else
              class="flex flex-col items-center justify-center py-16 text-muted gap-2"
            >
              <UIcon name="i-lucide-target" class="w-10 h-10" />
              <p class="text-sm">No readiness data available.</p>
            </div>
          </div>
        </template>
      </UTabs>
    </template>
  </div>
</template>
