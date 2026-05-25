<script setup lang="ts">
import * as z from "zod";
import { type SelectItem } from "@nuxt/ui";
import type { StepperItem } from "@nuxt/ui";

definePageMeta({
  layout: false,
});
const toast = useToast();

const stepper: Ref<number> = ref(0);
const stepperItems: Ref<StepperItem[]> = ref([
  {
    value: 0,
    title: "Get to know you better",
    icon: "tdesign:personal-information",
    slot: "know-better" as const,
  },
  {
    value: 1,
    title: "Account Information",
    icon: "solar:login-3-line-duotone",
    slot: "account-information" as const,
  },
]);

const targetSemesterOptions: SelectItem[] = [
  {
    label: "Summer 2026",
    value: "summer_2026",
  },
  {
    label: "Winter 2026",
    value: "winter_2026",
  },
];

const knowBetterSchema = z.object({
  name: z.string("First name is required"),
  family_name: z.string("Family name is required"),
  gpa: z.number("GPA is required").lte(4).gte(0),
  target_term: z.string("Target term is required"),
});
type KnowBetterSchemaType = z.output<typeof knowBetterSchema>;
const knowBetterState = reactive<Partial<KnowBetterSchemaType>>({
  name: undefined,
  family_name: undefined,
  gpa: 0,
  target_term: undefined,
});

async function onKnowBetterSubmit() {
  stepper.value = 1;
}

const accountInformationSchema = z.object({
  email: z.email("Email is required"),
  password: z.string("Password is required"),
});
type AccountInformationSchemaType = z.output<typeof accountInformationSchema>;
const accountInformationState = reactive<Partial<AccountInformationSchemaType>>(
  {
    email: undefined,
    password: undefined,
  },
);

const isLoading: Ref<boolean> = ref(false);
async function onAccountInformationSubmit() {
  isLoading.value = true;
  const { error } = await useApi("/profiles", {
    method: "POST",
    body: { ...knowBetterState, ...accountInformationState },
  });
  isLoading.value = false;

  if (error.value) {
    toast.add({
      title: error.value.data?.message ?? "Sign up failed",
      color: "error",
    });
    return;
  }

  toast.add({
    title: "Account created!",
    description: "You can now log in.",
    color: "success",
  });
  await navigateTo("/login");
}
</script>
<template>
  <UContainer
    class="min-h-full min-w-full flex flex-col justify-center items-center"
  >
    <UPageCard class="max-w_fit">
      <UStepper disabled :items="stepperItems" v-model="stepper">
        <template #know-better>
          <UForm
            :schema="knowBetterSchema"
            :state="knowBetterState"
            class="space-y-4 w-full"
            @submit="onKnowBetterSubmit"
          >
            <UFormField label="First Name" name="first_name" required>
              <UInput
                v-model="knowBetterState.name"
                aria-label="First Name"
                class="min-w-full"
              ></UInput>
            </UFormField>
            <UFormField label="Family Name" name="family_name" required>
              <UInput
                v-model="knowBetterState.family_name"
                aria-label="Family Name"
                class="min-w-full"
              ></UInput>
            </UFormField>
            <UFormField label="GPA" name="gpa" required>
              <UInput
                v-model.number="knowBetterState.gpa"
                type="number"
                :min="0"
                :max="4"
                :step="0.1"
                aria-label="GPA"
                class="min-w-full"
              ></UInput>
            </UFormField>
            <UFormField label="Target Term" name="target_term" required>
              <USelect
                v-model="knowBetterState.target_term"
                :items="targetSemesterOptions"
                aria-label="Target Term"
                class="min-w-full"
              ></USelect>
            </UFormField>
            <UButton type="submit" class="min-w-full text-center justify-center"
              >Next</UButton
            >
          </UForm>
        </template>
        <template #account-information>
          <UForm
            :state="accountInformationState"
            :schema="accountInformationSchema"
            @submit="onAccountInformationSubmit"
            class="space-y-4 w-full"
          >
            <UFormField label="Email" name="email" required>
              <UInput
                v-model="accountInformationState.email"
                type="email"
                aria-label="Email"
                class="min-w-full"
              ></UInput>
            </UFormField>
            <UFormField label="Password" name="password" required>
              <UInput
                v-model="accountInformationState.password"
                type="password"
                aria-label="Password"
                class="min-w-full"
              ></UInput>
            </UFormField>
            <div class="w-full flex items-center justify-between gap-x-4">
              <UButton
                color="neutral"
                variant="subtle"
                @click="() => (stepper = 0)"
                class="w-full justify-center"
                :loading="isLoading"
                >Go Back</UButton
              >
              <UButton
                type="submit"
                class="w-full justify-center"
                :loading="isLoading"
                >Sign up</UButton
              >
            </div>
          </UForm>
        </template>
      </UStepper>
      <USeparator></USeparator>
      <span class="text-sm text-muted text-center"
        >Already have an account?
        <ULink to="/login" class="text-primary">Login here</ULink></span
      >
    </UPageCard>
  </UContainer>
</template>
