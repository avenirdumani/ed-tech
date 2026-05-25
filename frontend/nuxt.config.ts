// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@sidebase/nuxt-auth", "@nuxt/ui"],
  css: ["~/assets/css/main.css"],
  runtimeConfig: {
    public: {
      apiBase: process.env.BASE_API_URL,
    },
  },
  auth: {
    baseURL: process.env.BASE_API_URL,
    provider: {
      type: "local",
      endpoints: {
        signIn: { path: "/login", method: "post" },
        signOut: false,
        getSession: { path: "/profiles", method: "get" },
      },
      token: {
        signInResponseTokenPointer: "/access_token",
        type: "Bearer",
      },
      session: {
        dataType: {
          id: "string",
          name: "string",
          family_name: "string",
          email: "string",
          gpa: "number",
          target_term: "string",
        },
      },
    },
  },
});
