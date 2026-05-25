<script setup lang="ts">
import type { NavigationMenuItem, SidebarProps, DropdownMenuItem } from "@nuxt/ui";

defineProps<Pick<SidebarProps, "variant" | "collapsible" | "side">>();

const open = ref(true);
const { data, signOut } = useAuth();

const items: NavigationMenuItem[] = [
  {
    label: "Home",
    icon: "i-lucide-house",
    to: "/",
  },
  {
    label: "Applications",
    icon: "majesticons:applications-add",
    to: "/applications",
  },
  {
    label: "Programs",
    icon: "mdi:code-equal",
    to: "/programs",
  },
];

const profileMenuItems: DropdownMenuItem[][] = [
  [
    {
      label: "Profile",
      icon: "i-lucide-user",
      to: "/profile",
    },
  ],
  [
    {
      label: "Logout",
      icon: "i-lucide-log-out",
      onSelect: () => signOut({ callbackUrl: "/login" }),
    },
  ],
];

const displayName = computed(
  () => (data.value as any)?.user?.name ?? (data.value as any)?.user?.email ?? "Account"
);
</script>

<template>
  <div
    class="flex flex-1"
    :class="[
      variant === 'inset' && 'bg-neutral-50 dark:bg-neutral-950',
      side === 'right' && 'flex-row-reverse',
    ]"
  >
    <USidebar
      v-model:open="open"
      :variant="variant"
      :collapsible="collapsible"
      :side="side"
      :ui="{
        container: 'h-full',
      }"
    >
      <div class="flex flex-col h-full">
        <UNavigationMenu :items="items" orientation="vertical" class="flex-1" />
        <div class="p-2 border-t border-default">
          <UDropdownMenu :items="profileMenuItems" :ui="{ content: 'w-48' }">
            <UButton
              variant="ghost"
              color="neutral"
              class="w-full justify-start gap-2"
            >
              <UAvatar :alt="displayName" size="xs" />
              <span class="truncate text-sm">{{ displayName }}</span>
              <UIcon name="i-lucide-chevrons-up-down" class="ml-auto shrink-0 size-4" />
            </UButton>
          </UDropdownMenu>
        </div>
      </div>
    </USidebar>

    <div class="flex-1 flex flex-col overflow-hidden">
      <div
        class="h-16 shrink-0 flex items-center px-4"
        :class="[
          variant !== 'floating' && 'border-b border-default',
          side === 'right' && 'justify-end',
        ]"
      >
        <UButton
          :icon="
            side === 'left' ? 'i-lucide-panel-left' : 'i-lucide-panel-right'
          "
          color="neutral"
          variant="ghost"
          aria-label="Toggle sidebar"
          @click="open = !open"
        />
      </div>

      <div class="flex-1 p-4">
        <slot></slot>
      </div>
    </div>
  </div>
</template>
