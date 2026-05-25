<script setup lang="ts">
import { computed, h } from "vue";
import type { ComputedRef } from "vue";
import type { TableColumn } from "@nuxt/ui";
import type {
  DetailedProgramResponse,
  BaseApplicationResponse,
} from "~/types/api_response";

type Requirement = DetailedProgramResponse["requirements"][number];

const UBadge = resolveComponent("UBadge");
const UIcon = resolveComponent("UIcon");

const route = useRoute();
const { data, status } = useAuthenticatedApi<DetailedProgramResponse>(
  `/programs/${route.params.id}`,
);

const isApplying = ref(false);
const applyError = ref<string | null>(null);

const apply = async () => {
  isApplying.value = true;
  applyError.value = null;
  const { data: newApplication, error } =
    await useAuthenticatedApi<BaseApplicationResponse>("/applications", {
      method: "POST",
      body: { program_id: route.params.id },
    });
  isApplying.value = false;
  if (error.value) {
    applyError.value =
      (error.value as any).data?.detail ??
      "Failed to submit application. Please try again.";
    return;
  }
  navigateTo(`/applications/${newApplication.value!.id}`);
};

const isLoading: ComputedRef<boolean> = computed(
  () => status.value === "pending",
);

const program: ComputedRef<DetailedProgramResponse | null> = computed(
  () => data.value ?? null,
);

const columns: ComputedRef<TableColumn<Requirement>[]> = computed(() => [
  {
    accessorKey: "title",
    header: "Title",
  },
  {
    accessorKey: "type",
    header: "Type",
    cell: ({ row }) => {
      const type: string = row.getValue("type");
      return h(UBadge, { color: "neutral", variant: "soft" }, () => type);
    },
  },
  {
    accessorKey: "description",
    header: "Description",
  },
  {
    accessorKey: "evidence_type",
    header: "Evidence Type",
    cell: ({ row }) => {
      const evidenceType: string = row.getValue("evidence_type");
      return h(
        UBadge,
        { color: "primary", variant: "subtle" },
        () => evidenceType,
      );
    },
  },
  {
    accessorKey: "due_offset_days",
    header: "Due Offset (days)",
    cell: ({ row }) => {
      const days: number = row.getValue("due_offset_days");
      return h(UBadge, { color: "info", variant: "subtle" }, () => `${days}d`);
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
        @click="navigateTo('/programs')"
      />
      <USkeleton v-if="isLoading" class="h-8 w-64" />
      <UPageHeader v-else :title="program?.name ?? ''" class="flex-1" />
    </div>

    <USkeleton v-if="isLoading" class="min-h-96 min-w-full" />

    <template v-else-if="program">
      <div class="flex items-center gap-2 mb-6">
        <UBadge color="neutral" variant="soft" size="lg">
          {{ program.degree_type.toUpperCase() }}
        </UBadge>
        <UBadge
          color="info"
          variant="subtle"
          size="lg"
          icon="i-lucide-calendar"
        >
          Deadline: {{ program.application_deadline }}
        </UBadge>
        <div class="flex-1" />
        <UButton
          label="Apply"
          icon="i-lucide-send"
          :loading="isApplying"
          @click="apply"
        />
      </div>

      <UAlert
        v-if="applyError"
        color="error"
        variant="soft"
        icon="i-lucide-circle-x"
        :description="applyError"
        class="mb-4"
      />

      <UCard class="min-w-full">
        <template #header>
          <p class="text-sm font-semibold text-highlighted">Requirements</p>
          <p class="text-sm text-muted">
            {{ program.requirements.length }} requirement{{
              program.requirements.length !== 1 ? "s" : ""
            }}
          </p>
        </template>
        <UTable
          class="w-full"
          :data="program.requirements"
          :columns="columns"
        />
      </UCard>
    </template>
  </div>
</template>
