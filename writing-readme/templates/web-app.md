# [Application Name]

> [Engaging elevator pitch: What does this web application do? e.g. "Real-time collaborative markdown editor with live peer-to-peer sync and offline persistence."]

[Live Demo](https://[your-app-domain].com) · [Report Bug](https://github.com/[owner]/[repo]/issues) · [Feature Request](https://github.com/[owner]/[repo]/issues)

<!-- Add hero screenshot or UI demonstration here -->
<!-- ![Application Preview](assets/screenshot.png) -->

---

## Features

- **[Feature 1]:** [User-facing capability and why it matters.]
- **[Feature 2]:** [Interactive real-time or offline feature.]
- **[Feature 3]:** [Accessibility, dark mode, responsive layout.]

---

## Tech Stack

- **Framework:** Next.js 15 (App Router) / React 19 / Vue 3
- **State Management:** Zustand / Pinia
- **Styling:** Tailwind CSS / CSS Modules
- **Backend / Database:** Supabase / PostgreSQL / Prisma
- **Testing:** Playwright (E2E), Vitest (Unit)

---

## Local Development Setup

### 1. Prerequisites
- Node.js `>= 20.x`
- pnpm `>= 9.x`

### 2. Installation
```bash
git clone https://github.com/[owner]/[repo].git
cd [repo]
pnpm install
```

### 3. Environment Variables
Create a local `.env.local` file:
```bash
cp .env.example .env.local
```

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Base API endpoint | `http://localhost:3000/api` |
| `DATABASE_URL` | Local DB connection | `postgresql://postgres:pass@localhost:5432/app` |

### 4. Run Development Server
```bash
pnpm dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Available NPM Scripts

- `pnpm dev` — Start local development server with Turbopack.
- `pnpm build` — Generate optimized production build.
- `pnpm start` — Run production server.
- `pnpm test` — Run unit and component test suites.
- `pnpm test:e2e` — Execute Playwright end-to-end browser tests.
- `pnpm lint` — Run ESLint and TypeScript typecheck.
