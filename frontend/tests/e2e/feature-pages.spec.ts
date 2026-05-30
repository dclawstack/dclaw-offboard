import { test, expect } from "@playwright/test";
import content from "../../src/data/landing-content.json";

type FeaturePage = {
  path: string;
  heading: string | RegExp;
  // True if the page fetches from the backend on mount.
  // We still expect the shell to render — failed fetch should not blank the page.
  fetchesBackend: boolean;
  // Most feature pages render a "Back to home" link. A few (list/dashboard pages) don't.
  hasBackToHome: boolean;
};

const featureById = (id: string) => {
  const f = content.features.find((x) => x.id === id);
  if (!f) throw new Error(`landing-content.json is missing feature id="${id}"`);
  return f;
};

const PAGES: FeaturePage[] = [
  { path: "/copilot",      heading: featureById("copilot").title,      fetchesBackend: false, hasBackToHome: true },
  { path: "/checklists",   heading: /Offboarding Checklists/i,         fetchesBackend: true,  hasBackToHome: false },
  { path: "/access",       heading: /Access Revocation/i,              fetchesBackend: false, hasBackToHome: true },
  { path: "/risk",         heading: /Risk Assessment.*IP Protection/i, fetchesBackend: true,  hasBackToHome: false },
  { path: "/interviews",   heading: featureById("interviews").title,   fetchesBackend: false, hasBackToHome: true },
  { path: "/knowledge",    heading: featureById("knowledge").title,    fetchesBackend: false, hasBackToHome: true },
  { path: "/integrations", heading: /Integration Hub/i,                fetchesBackend: true,  hasBackToHome: false },
  { path: "/alumni",       heading: featureById("alumni").title,       fetchesBackend: false, hasBackToHome: true },
  { path: "/payroll",      heading: featureById("payroll").title,      fetchesBackend: false, hasBackToHome: true },
  { path: "/compliance",   heading: /Compliance Automation/i,          fetchesBackend: true,  hasBackToHome: false },
  { path: "/dashboard",    heading: /Dashboard/i,                      fetchesBackend: true,  hasBackToHome: false },
  { path: "/assets",       heading: /Asset Recovery/i,                 fetchesBackend: true,  hasBackToHome: false },
  // Coming-soon stubs created earlier this session.
  { path: "/sentiment",    heading: /Sentiment.*Early Warning/i,       fetchesBackend: false, hasBackToHome: true },
  { path: "/teams",        heading: /Team Transition.*Coverage/i,      fetchesBackend: false, hasBackToHome: true },
];

for (const p of PAGES) {
  test.describe(`${p.path}`, () => {
    test("loads and renders heading", async ({ page }) => {
      // Silently absorb fetch failures from API-touching pages — we only care that
      // the shell still renders. The backend isn't required to be up for these tests.
      page.on("pageerror", () => {});

      const res = await page.goto(p.path);
      expect(res?.status(), `expected ${p.path} to return 200`).toBe(200);

      await expect(
        page.getByRole("heading", { level: 1, name: p.heading })
      ).toBeVisible();
    });

    if (p.hasBackToHome) {
      test("Back-to-home link works", async ({ page }) => {
        await page.goto(p.path);
        const back = page.getByRole("link", { name: /Back to home/i });
        await expect(back).toBeVisible();
        await expect(back).toHaveAttribute("href", "/");
        await back.click();
        await page.waitForURL("**/");
        await expect(
          page.getByRole("heading", { level: 1, name: content.hero.headline })
        ).toBeVisible();
      });
    }

    if (p.fetchesBackend) {
      test("shell renders even when backend fetches fail", async ({ page }) => {
        // Force every API call from the page to fail. Page should still render.
        await page.route("**/api/**", (route) => route.abort());
        const res = await page.goto(p.path);
        expect(res?.status()).toBe(200);
        await expect(
          page.getByRole("heading", { level: 1, name: p.heading })
        ).toBeVisible();
      });
    }
  });
}

test.describe("Coming-soon stubs", () => {
  for (const path of ["/sentiment", "/teams"]) {
    test(`${path} shows "Coming soon" badge`, async ({ page }) => {
      await page.goto(path);
      await expect(page.getByText(/Coming soon/i)).toBeVisible();
    });
  }
});

test.describe("Legal/docs stubs", () => {
  test("/privacy renders policy headings", async ({ page }) => {
    await page.goto("/privacy");
    await expect(page.getByRole("heading", { level: 1, name: /Privacy Policy/i })).toBeVisible();
    await expect(page.getByRole("heading", { level: 2, name: /Data We Collect/i })).toBeVisible();
  });

  test("/terms renders terms headings", async ({ page }) => {
    await page.goto("/terms");
    await expect(page.getByRole("heading", { level: 1, name: /Terms of Service/i })).toBeVisible();
    await expect(page.getByRole("heading", { level: 2, name: /Acceptance/i })).toBeVisible();
    const privacyLink = page.getByRole("link", { name: /Privacy Policy/i });
    await expect(privacyLink).toHaveAttribute("href", "/privacy");
  });

  test("/docs renders navigation cards", async ({ page }) => {
    await page.goto("/docs");
    await expect(page.getByRole("heading", { level: 1, name: /Documentation/i })).toBeVisible();
    await expect(page.getByRole("heading", { level: 2, name: /Getting Started/i })).toBeVisible();
    await expect(page.getByRole("heading", { level: 2, name: /API Reference/i })).toBeVisible();
  });
});
