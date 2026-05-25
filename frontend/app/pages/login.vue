<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent, AuthFormField } from "@nuxt/ui";

definePageMeta({
  layout: false,
});

const toast = useToast();
const { signIn } = useAuth();

const fields: AuthFormField[] = [
  {
    name: "email",
    type: "email",
    label: "Email",
    placeholder: "Enter your email",
    required: true,
  },
  {
    name: "password",
    label: "Password",
    type: "password",
    placeholder: "Enter your password",
    required: true,
  },
];

const schema = z.object({
  email: z.email("Invalid email"),
  password: z.string("Password is required"),
});

type Schema = z.output<typeof schema>;

function onSubmit(payload: FormSubmitEvent<Schema>) {
  signIn(
    {
      email: payload.data.email,
      password: payload.data.password,
    },
    { callbackUrl: "/" },
  ).catch(() => toast.add({ title: "Something went wrong" }));
}
</script>

<template>
  <div class="min-h-full min-w-full flex items-center justify-center">
    <UPageCard class="max-w-fit">
      <UAuthForm
        class="max-w-fit"
        :schema="schema"
        title="Login"
        description="Enter your credentials to access your account."
        icon="i-lucide-user"
        :fields="fields"
        @submit="onSubmit"
      />
      <USeparator> </USeparator>
      <span class="text-sm text-muted text-center"
        >Don't have an account?
        <ULink class="text-primary" to="/signup">Sign up here</ULink></span
      >
    </UPageCard>
  </div>
</template>
