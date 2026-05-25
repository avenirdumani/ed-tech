export default defineNuxtRouteMiddleware((to) => {
  const { status } = useAuth();
  if (
    status.value === "unauthenticated" &&
    !["/signup", "/login"].includes(to.path)
  ) {
    return navigateTo({ path: "/login" });
  }
  if (
    status.value === "authenticated" &&
    ["/signup", "/login"].includes(to.path)
  ) {
    return navigateTo({ path: "/" });
  }
});
