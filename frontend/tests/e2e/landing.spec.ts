import { test, expect, type Page } from "@playwright/test";
import content from "../../src/data/landing-content.json";
import config from "../../src/data/app-config.json";

test.describe("Landing page — load", () => {
  test("returns 200 and renders the hero headline", async ({ page, request }) => {
    const head = await request.get("/");
    expect(head.status()).toBe(200);

    await page.goto("/");
    await expect(page.locator("html")).toHaveAttribute("lang", /.+/);
    await expect(
      page.getByRole("heading", { level: 1, name: content.hero.headline })
    ).toBeVisible();
  });
});

test.describe("Navbar", () => {
  test("desktop: logo, category badge, and primary nav links visible", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/");

    const navbar = page.getByRole("navigation").first();
    await expect(navbar.getByRole("link", { name: new RegExp(content.app.name) }).first()).toBeVisible();
    await expect(navbar.getByText(content.app.category, { exact: true })).toBeVisible();

    for (const link of config.navigation.links.slice(0, 4)) {
      await expect(navbar.getByRole("link", { name: link.text, exact: true })).toBeVisible();
    }
  });

  test("desktop: primary CTA in navbar points to /checklists/create", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/");

    const navbar = page.getByRole("navigation").first();
    const cta = navbar.getByRole("link", { name: content.hero.ctaPrimary.text });
    await expect(cta).toBeVisible();
    await expect(cta).toHaveAttribute("href", "/checklists/create");
  });

  test("mobile: hamburger toggles expanded menu", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    const navbar = page.getByRole("navigation").first();
    const toggle = navbar.getByRole("button").first();
    await expect(toggle).toBeVisible();

    // Before opening, expanded links should not be visible.
    const lastLinkText = config.navigation.links[config.navigation.links.length - 1].text;
    await expect(navbar.getByRole("link", { name: lastLinkText, exact: true })).toHaveCount(0);

    await toggle.click();
    await expect(navbar.getByRole("link", { name: lastLinkText, exact: true })).toBeVisible();
  });
});

test.describe("Hero section", () => {
  test("renders headline, subheadline, both CTAs with correct hrefs, and all stats", async ({
    page,
  }) => {
    await page.goto("/");

    await expect(
      page.getByRole("heading", { level: 1, name: content.hero.headline })
    ).toBeVisible();
    await expect(page.getByText(content.hero.subheadline, { exact: false })).toBeVisible();

    const primary = page
      .getByRole("link", { name: content.hero.ctaPrimary.text })
      .filter({ has: page.locator("svg") })
      .first();
    await expect(primary).toBeVisible();
    await expect(primary).toHaveAttribute("href", content.hero.ctaPrimary.href);

    const secondary = page.getByRole("link", { name: content.hero.ctaSecondary.text });
    await expect(secondary.first()).toBeVisible();
    await expect(secondary.first()).toHaveAttribute("href", content.hero.ctaSecondary.href);

    for (const stat of content.hero.stats) {
      await expect(page.getByText(stat.value, { exact: true }).first()).toBeVisible();
      await expect(page.getByText(stat.label, { exact: true }).first()).toBeVisible();
    }
  });
});

test.describe("Features section", () => {
  test("renders all three tier headers", async ({ page }) => {
    await page.goto("/");
    for (const tier of content.featureTiers) {
      await expect(
        page.getByText(`${tier.tier} — ${tier.label}`, { exact: true })
      ).toBeVisible();
    }
  });

  test("renders one card per feature in landing-content.json", async ({ page }) => {
    await page.goto("/");
    const section = page.locator("#features");
    await expect(section).toBeVisible();

    for (const feature of content.features) {
      const card = section.getByRole("link", { name: new RegExp(escapeRegExp(feature.title)) });
      await expect(card.first()).toBeVisible();
      await expect(card.first()).toHaveAttribute("href", feature.href);
    }
  });
});

test.describe("Workflow section", () => {
  test("renders title and all four steps", async ({ page }) => {
    await page.goto("/");
    await expect(
      page.getByRole("heading", { level: 2, name: content.workflow.title })
    ).toBeVisible();
    for (const step of content.workflow.steps) {
      await expect(
        page.getByRole("heading", { level: 3, name: step.title })
      ).toBeVisible();
      await expect(page.getByText(step.description, { exact: false })).toBeVisible();
    }
  });
});

test.describe("Testimonials section", () => {
  test("renders both quotes with author + role", async ({ page }) => {
    await page.goto("/");
    for (const t of content.testimonials) {
      await expect(page.getByText(t.quote, { exact: false })).toBeVisible();
      await expect(page.getByText(t.author, { exact: true })).toBeVisible();
      await expect(page.getByText(t.role, { exact: true })).toBeVisible();
    }
  });
});

test.describe("CTA section", () => {
  test("renders heading and both buttons with correct hrefs", async ({ page }) => {
    await page.goto("/");
    await expect(
      page.getByRole("heading", { name: /Ready to Simplify Your Offboarding\?/i })
    ).toBeVisible();

    const primary = page.getByRole("link", { name: "Start Your First Offboarding" });
    await expect(primary).toBeVisible();
    await expect(primary).toHaveAttribute("href", "/checklists/create");

    const secondary = page.getByRole("link", { name: /Ask the AI Copilot/i });
    await expect(secondary).toBeVisible();
    await expect(secondary).toHaveAttribute("href", "/copilot");
  });
});

test.describe("Footer", () => {
  test("renders all configured links and copyright", async ({ page }) => {
    await page.goto("/");
    const footer = page.getByRole("contentinfo");
    await expect(footer).toBeVisible();
    for (const link of content.footer.links) {
      const l = footer.getByRole("link", { name: link.text, exact: true });
      await expect(l).toBeVisible();
      await expect(l).toHaveAttribute("href", link.href);
    }
    await expect(footer.getByText(content.footer.copyright, { exact: true })).toBeVisible();
  });
});

test.describe("Floating Copilot widget", () => {
  test("toggle opens chat panel with initial greeting", async ({ page }) => {
    await page.goto("/");

    // The floating widget renders a fixed button. Use the icon-only button at the bottom-right.
    const buttons = page.getByRole("button");
    // Click the last button on the page (the floating toggle is appended at the end of the tree).
    const toggle = buttons.last();
    await expect(toggle).toBeVisible();
    await toggle.click();

    await expect(
      page.getByText(/I'm your DClaw Offboard Copilot/i)
    ).toBeVisible();
  });
});

test.describe("Route smoke tests — every linked destination returns 200", () => {
  const routes = Array.from(
    new Set([
      "/",
      ...content.features.map((f) => f.href),
      ...content.footer.links.map((l) => l.href),
      ...config.navigation.links.map((n) => n.href),
      content.hero.ctaPrimary.href,
    ])
  ).filter((href) => href.startsWith("/"));

  for (const route of routes) {
    test(`GET ${route} -> 200`, async ({ request }) => {
      const res = await request.get(route);
      expect(res.status(), `expected ${route} to return 200`).toBe(200);
    });
  }
});

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Avoid unused-import error: keep Page type re-exported for editor jump-to-def.
export type { Page };
