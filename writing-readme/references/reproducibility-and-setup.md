# Reproducibility & Setup Engineering

> "If a developer cannot follow your installation instructions in a clean environment, your project does not work."

---

## The Clean-Install Protocol

Most broken READMEs suffer from the **"It works on my machine"** curse:
- The author has global packages installed that aren't listed in dependencies.
- The author has local environment variables configured in `.bashrc` or `.zshrc`.
- The author has database migrations already run or existing test databases.

### How to Conduct a Clean-Install Test

Always test your instructions in a sterile container or clean virtual machine:

```bash
# 1. Run a sterile disposable container matching target OS
docker run -it --rm ubuntu:24.04 bash

# 2. In the container, follow ONLY the commands in your README
apt-get update && apt-get install -y git curl python3 python3-pip
git clone <your-repo>
cd <your-repo>
<follow installation steps>

# 3. Record every missing command, package, or implicit step.
```

If any command fails, your README is incomplete.

---

## The Prerequisites Checklist

Explicitly declare dependencies before giving installation commands:
1. **Runtime & Language Versions:** Specify supported minimum and maximum versions (e.g. `Python 3.10 - 3.12`, `Node.js >= 20.9.0`).
2. **Build Tools & Compilers:** Mention if C++ compilers (`gcc`, `clang`, `build-essential`), CMake, or Rust are needed to compile native bindings.
3. **Platform Constraints:** Document macOS Apple Silicon (arm64) quirks, Linux glibc/musl requirements, or Windows WSL requirements.
4. **Third-Party Accounts:** Disclose if an account or API key (Stripe, OpenAI, AWS, HuggingFace) is required.

---

## Configuration & Secrets Management

### Rule 1: Never Include Real Secrets
Never commit real API keys, database passwords, or JWT secrets in README examples. Use descriptive dummy values:
- `sk_test_placeholder...`
- `postgres://user:password@localhost:5432/dbname`

### Rule 2: Provide a `.env.example`
In your repository, include a `.env.example` file with documented variable names and sensible defaults. In your README, instruct the user:
```bash
cp .env.example .env
```

### Rule 3: Document Every Variable in a Table
Use a structured markdown table:

| Variable | Description | Default | Required? |
| :--- | :--- | :--- | :---: |
| `DATABASE_URL` | PostgreSQL connection URI | `postgres://localhost:5432/app` | Yes |
| `CACHE_TTL_SEC` | Redis cache retention in seconds | `3600` | No |
| `API_KEY` | Third-party service auth token | *None* | Yes |

---

## Expected Output Verification

Every critical command in your README should show what success looks like:

```bash
$ python main.py --check-health

[INFO] Connected to PostgreSQL at localhost:5432 (latency: 1.2ms)
[INFO] Loaded 4 pipeline models in 0.42s
Server listening on http://127.0.0.1:8080
```

Providing expected output allows the reader to immediately verify they succeeded without guessing whether warnings are benign or fatal.
