import { describe, it, expect, vi, beforeEach } from "vitest";
import { mountSuspended, mockNuxtImport } from "@nuxt/test-utils/runtime";
import LoginPage from "~/pages/login.vue";

const { signInMock, addToastMock } = vi.hoisted(() => ({
  signInMock: vi.fn(),
  addToastMock: vi.fn(),
}));

mockNuxtImport("useAuth", () => () => ({ signIn: signInMock }));
mockNuxtImport("useToast", () => () => ({ add: addToastMock }));

describe("Login Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders email and password fields", async () => {
    const component = await mountSuspended(LoginPage);

    expect(component.find('[type="email"]').exists()).toBe(true);
    expect(component.find('[type="password"]').exists()).toBe(true);
  });

  it("renders a submit button", async () => {
    const component = await mountSuspended(LoginPage);

    const buttons = component.findAll("button");
    expect(buttons.length).toBeGreaterThan(0);
  });

  it("renders the sign up link", async () => {
    const component = await mountSuspended(LoginPage);

    const link = component.find('a[href="/signup"]');
    expect(link.exists()).toBe(true);
    expect(link.text()).toContain("Sign up here");
  });

  it("calls signIn with email, password and callbackUrl on submit", async () => {
    signInMock.mockResolvedValue(undefined);
    const component = await mountSuspended(LoginPage);

    await (component.vm as any).onSubmit({
      data: { email: "user@example.com", password: "secret123" },
    });

    expect(signInMock).toHaveBeenCalledWith(
      { email: "user@example.com", password: "secret123" },
      { callbackUrl: "/" },
    );
  });

  it("shows error toast when signIn throws", async () => {
    signInMock.mockRejectedValue(new Error("Network error"));
    const component = await mountSuspended(LoginPage);

    await (component.vm as any).onSubmit({
      data: { email: "user@example.com", password: "wrong" },
    });

    expect(addToastMock).toHaveBeenCalledWith(
      expect.objectContaining({ title: "Something went wrong" }),
    );
  });
});
