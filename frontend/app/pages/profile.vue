<script setup lang="ts">
import * as z from "zod";
import type { SelectItem } from "@nuxt/ui";
import type { ProfileOut } from "~/types/api_response";

const toast = useToast();

const {
  data: profileData,
  refresh,
  status,
} = useAuthenticatedApi<ProfileOut>("/profiles");

const isLoading = computed(() => status.value === "pending");
const profile = computed(() => profileData.value ?? null);

const targetSemesterOptions: SelectItem[] = [
  { label: "Summer 2026", value: "summer_2026" },
  { label: "Winter 2026", value: "winter_2026" },
];

const editSchema = z.object({
  name: z.string().min(1, "First name is required"),
  family_name: z.string().min(1, "Family name is required"),
  gpa: z.number().min(0).max(4, "GPA must be between 0 and 4"),
  target_term: z.string().min(1, "Target term is required"),
});

const isEditing = ref(false);
const isSaving = ref(false);

const editState = reactive({
  name: "",
  family_name: "",
  gpa: 0 as number,
  target_term: "",
});

function startEditing() {
  if (!profile.value) return;
  editState.name = profile.value.name;
  editState.family_name = profile.value.family_name;
  editState.gpa = profile.value.gpa;
  editState.target_term = profile.value.target_term;
  isEditing.value = true;
}

function cancelEditing() {
  isEditing.value = false;
}

async function saveProfile() {
  isSaving.value = true;
  const { error } = await useAuthenticatedApi("/profiles", {
    method: "PATCH",
    body: { ...editState },
  });
  isSaving.value = false;
  if (error.value) {
    toast.add({
      title: "Failed to update profile",
      color: "error",
    });
    return;
  }
  await refresh();
  isEditing.value = false;
  toast.add({ title: "Profile updated", color: "success" });
}

const targetTermLabel = computed(() => {
  const opt = targetSemesterOptions.find(
    (o) => o.value === profile.value?.target_term,
  );
  return (
    (opt?.label as string | undefined) ?? profile.value?.target_term ?? "—"
  );
});
</script>

<template>
  <div>
    <UPageHeader title="Profile" />

    <USkeleton v-if="isLoading" class="mt-4 min-h-64 min-w-full" />

    <UCard v-else-if="profile" class="mt-4 max-w-full">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <UAvatar
              :alt="`${profile.name} ${profile.family_name}`"
              size="lg"
            />
            <div>
              <p class="font-semibold text-highlighted">
                {{ profile.name }} {{ profile.family_name }}
              </p>
              <p class="text-sm text-muted">{{ profile.email }}</p>
            </div>
          </div>
          <UButton
            v-if="!isEditing"
            label="Edit"
            icon="i-lucide-pencil"
            color="neutral"
            variant="outline"
            size="sm"
            @click="startEditing"
          />
        </div>
      </template>

      <template v-if="!isEditing">
        <dl class="grid grid-cols-2 gap-4">
          <div>
            <dt class="text-xs text-muted uppercase tracking-wide">
              First Name
            </dt>
            <dd class="mt-1 text-sm text-highlighted font-medium">
              {{ profile.name }}
            </dd>
          </div>
          <div>
            <dt class="text-xs text-muted uppercase tracking-wide">
              Family Name
            </dt>
            <dd class="mt-1 text-sm text-highlighted font-medium">
              {{ profile.family_name }}
            </dd>
          </div>
          <div>
            <dt class="text-xs text-muted uppercase tracking-wide">GPA</dt>
            <dd class="mt-1 text-sm text-highlighted font-medium">
              {{ profile.gpa.toFixed(2) }}
            </dd>
          </div>
          <div>
            <dt class="text-xs text-muted uppercase tracking-wide">
              Target Term
            </dt>
            <dd class="mt-1 text-sm text-highlighted font-medium">
              {{ targetTermLabel }}
            </dd>
          </div>
        </dl>
      </template>

      <template v-else>
        <UForm
          :schema="editSchema"
          :state="editState"
          class="space-y-4"
          @submit="saveProfile"
        >
          <div class="grid grid-cols-2 gap-4">
            <UFormField label="First Name" name="name" required>
              <UInput v-model="editState.name" class="w-full" />
            </UFormField>
            <UFormField label="Family Name" name="family_name" required>
              <UInput v-model="editState.family_name" class="w-full" />
            </UFormField>
          </div>
          <UFormField label="GPA" name="gpa" required>
            <UInput
              v-model.number="editState.gpa"
              type="number"
              :min="0"
              :max="4"
              :step="0.1"
              class="w-full"
            />
          </UFormField>
          <UFormField label="Target Term" name="target_term" required>
            <USelect
              v-model="editState.target_term"
              :items="targetSemesterOptions"
              class="w-full"
            />
          </UFormField>

          <div class="flex items-center justify-end gap-2 pt-2">
            <UButton
              label="Cancel"
              color="neutral"
              variant="ghost"
              :disabled="isSaving"
              @click="cancelEditing"
            />
            <UButton
              type="submit"
              label="Save"
              icon="i-lucide-check"
              :loading="isSaving"
            />
          </div>
        </UForm>
      </template>
    </UCard>
  </div>
</template>
