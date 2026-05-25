<script setup lang="ts">
import type { ApplicationPreview } from "~/types/api_response";

const { data, status } = useAuthenticatedApi<ApplicationPreview[]>(
  "/applications/preview",
);

const isLoading = computed(() => status.value === "pending");
const applications = computed(() => data.value ?? []);

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
</script>

<template>
  <div>
    <UPageHeader title="Dashboard" />

    <div
      v-if="isLoading"
      class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mt-6"
    >
      <USkeleton v-for="i in 3" :key="i" class="h-48" />
    </div>

    <div
      v-else-if="!applications.length"
      class="flex flex-col items-center justify-center py-24 gap-3"
    >
      <UIcon name="i-lucide-folder-open" class="w-12 h-12 text-muted" />
      <p class="text-base font-semibold text-highlighted">
        No applications yet
      </p>
      <p class="text-sm text-muted">
        Browse programs to start your first application.
      </p>
      <UButton
        label="Browse Programs"
        icon="i-lucide-search"
        class="mt-2"
        @click="navigateTo('/programs')"
      />
    </div>

    <div
      v-else
      class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mt-6"
    >
      <UCard
        v-for="app in applications"
        :key="app.id"
        class="cursor-pointer transition-shadow hover:shadow-md"
        @click="navigateTo(`/applications/${app.id}`)"
      >
        <template #header>
          <div class="flex items-start justify-between gap-2">
            <p class="text-sm font-semibold text-highlighted leading-snug">
              {{ app.program.name }}
            </p>
            <UBadge color="neutral" variant="soft" size="sm" class="shrink-0">
              {{ app.program.degree_type.toUpperCase() }}
            </UBadge>
          </div>
          <p class="text-xs text-muted mt-1 flex items-center gap-1">
            <UIcon name="i-lucide-calendar" class="w-3 h-3 shrink-0" />
            Deadline: {{ app.program.application_deadline }}
          </p>
        </template>

        <div class="space-y-3">
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <p class="text-xs text-muted">Readiness</p>
              <UBadge
                :color="readinessColor(app.readiness_score)"
                variant="subtle"
                size="sm"
              >
                {{ Math.round(app.readiness_score) }}/100
              </UBadge>
            </div>
            <USlider
              :model-value="app.readiness_score"
              :color="readinessColor(app.readiness_score)"
              :min="0"
              :max="100"
              disabled
            />
          </div>

          <div class="pt-2 border-t border-neutral-100 dark:border-neutral-800">
            <p class="text-xs text-muted mb-1.5">Next Milestone</p>
            <template v-if="app.next_milestone">
              <div class="flex items-center justify-between gap-2">
                <p class="text-xs font-medium text-highlighted truncate">
                  {{ app.next_milestone.title }}
                </p>
                <UBadge
                  :color="milestoneStatusColor(app.next_milestone.status)"
                  variant="subtle"
                  size="sm"
                  class="shrink-0"
                >
                  {{ app.next_milestone.status.replace(/_/g, " ") }}
                </UBadge>
              </div>
              <p class="text-xs text-muted mt-0.5">
                {{ app.next_milestone.date }}
              </p>
            </template>
            <p v-else class="text-xs text-muted">No upcoming milestones</p>
          </div>
        </div>
      </UCard>
    </div>
  </div>
</template>
