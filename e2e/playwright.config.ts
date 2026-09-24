import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  use: { baseURL: "http://localhost:8080" },
  webServer: {
    command: "docker compose up --build",
    url: "http://localhost:8080/api/health",
    reuseExistingServer: !process.env.CI,
  },
});
