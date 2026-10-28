# [Package / Library Name]

> [Concise value statement: What functionality does this library export? e.g. "Lightweight, zero-dependency resilient retry mechanism with exponential backoff and jitter."]

[![GitHub](https://img.shields.io/badge/GitHub-[owner]%2F[repo]-181717?logo=github)](https://github.com/[owner]/[repo])
[![npm version](https://img.shields.io/npm/v/[pkg].svg)](https://www.npmjs.com/package/[pkg])
[![PyPI version](https://img.shields.io/pypi/v/[pkg].svg)](https://pypi.org/project/[pkg]/)
[![Bundle Size](https://img.shields.io/bundlephobia/minzip/[pkg])](https://bundlephobia.com/package/[pkg])
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Installation

```bash
# npm
npm install [package-name]

# yarn / pnpm
pnpm add [package-name]

# Python (if PyPI package)
pip install [package-name]
```

---

## 30-Second Quickstart

```typescript
import { retryOperation } from '[package-name]';

const result = await retryOperation(
  async () => fetchUserData('user-123'),
  {
    maxRetries: 3,
    backoffMs: 200,
  }
);

console.log(result);
```

---

## API Reference & Cheat Sheet

### `functionName(param, [options])`
Performs [operation description].

#### Parameters
- **`param`** (`string`, *required*): Description of input parameter.
- **`options`** (`Object`, *optional*):
  - **`timeoutMs`** (`number`, default `5000`): Maximum execution budget in ms.
  - **`strict`** (`boolean`, default `false`): Enable strict schema validation.

#### Returns
- `Promise<ResultType>`: Resolves with structured output or rejects with `LibraryError`.

---

## Runtime & Platform Compatibility

| Environment | Supported Versions | Notes |
| :--- | :---: | :--- |
| **Node.js** | `>= 18.0.0` | CommonJS & ESM dual exports |
| **Browsers** | Modern (ES2022+) | Treeshakeable, `< 3kb` gzipped |
| **Deno / Bun** | Fully Supported | Direct URL and `bun add` compatible |

---

## Running Tests

```bash
npm test
npm run test:coverage
```
