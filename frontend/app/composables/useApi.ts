export const useAuthenticatedApi = createUseFetch({
  baseURL: useRuntimeConfig().public.apiBase,
  onRequest: ({ options }) => {
    const { token } = useAuth();
    options.headers.set("Authorization", `${token.value}`);
  },
});

export const useApi = createUseFetch({
  baseURL: useRuntimeConfig().public.apiBase,
});
