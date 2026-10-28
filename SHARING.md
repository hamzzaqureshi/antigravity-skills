# How to Share the Antigravity Skills Suite

This guide explains how to share your 19 modular skills with friends, teammates, and the developer community.

---

## Method 1: Send the Ready-Made ZIP (Fastest)

If your friends just want a file to download via **Discord, WhatsApp, Telegram, Slack, or Google Drive**:

1. A clean, self-contained ZIP archive is generated in your `dist/` folder:
   - **File:** `dist/antigravity-skills.zip` (~14 MB)
2. Send this file to your friend.
3. **Instructions for your friend:**
   - Unzip the file anywhere.
   - Open terminal in the unzipped folder and run:
     ```bash
     # Linux / macOS:
     ./install.sh

     # Windows (Command Prompt / PowerShell):
     python install.py
     ```
   - The interactive prompt lets them choose:
     - `1) Antigravity Global` (`~/.gemini/config/skills`) — skills become available in all their projects.
     - `2) Current Project Workspace` (`./.agents/skills`) — skills are scoped to that project.
     - `3) Claude Code Global` (`~/.claude/skills`) — for friends using Claude Code CLI.

> **Tip:** You can re-generate fresh ZIP archives anytime by running:
> ```bash
> python3 package.py
> ```

---

## Method 2: Publish to GitHub (Best for Collaboration & Updates)

Publishing to GitHub gives you a permanent repository where friends can star, fork, clone, and receive updates via `git pull`.

Since GitHub CLI (`gh`) is already logged into your account (`hamzzaqureshi`), you can publish with these 4 commands:

```bash
cd ~/Documents/skills

# 1. Initialize git repository
git init -b main

# 2. Stage all skill files and scripts
git add .

# 3. Create initial commit
git commit -m "feat: initial commit of modular Antigravity skills suite"

# 4. Create public repo on GitHub and push in one shot
gh repo create antigravity-skills --public --source=. --remote=origin --push
```

### How Friends Install from Your GitHub Repo:
```bash
git clone https://github.com/hamzzaqureshi/antigravity-skills.git
cd antigravity-skills
./install.sh
```

### How Friends Add Skills to Their Existing Projects (Git Submodule):
```bash
# In their project directory:
git submodule add https://github.com/hamzzaqureshi/antigravity-skills.git .agents/skills
```

---

## Method 3: One-Liner Web Installer (Zero-Clone)

Once pushed to GitHub, friends don't even need to clone the repository! They can install with a single curl command:

```bash
curl -fsSL https://raw.githubusercontent.com/hamzzaqureshi/antigravity-skills/main/install.sh | bash
```

To install directly to their global configuration without prompts:
```bash
curl -fsSL https://raw.githubusercontent.com/hamzzaqureshi/antigravity-skills/main/install.sh | bash -s -- --global
```

Or install specific skills:
```bash
curl -fsSL https://raw.githubusercontent.com/hamzzaqureshi/antigravity-skills/main/install.sh | bash -s -- --skills court,threeui,ui-ux-max --global
```

---

## Method 4: As an Antigravity Plugin

Antigravity natively supports modular **Plugins** (`plugins/<plugin-name>/plugin.json`).

When you run `python3 package.py`, it automatically generates:
`dist/antigravity-skills-pack/`

Friends can drop this folder directly into their Antigravity plugins directory:
- **Global:** `~/.gemini/config/plugins/antigravity-skills-pack/`
- **Project:** `<project-root>/.agents/plugins/antigravity-skills-pack/`

Antigravity will automatically ingest and namespace all 9 skills on launch!

---

## Cross-Agent Compatibility

| AI Assistant / IDE | How Friends Use These Skills |
| :--- | :--- |
| **Google Antigravity IDE** | Run `./install.sh --global` (installs to `~/.gemini/config/skills/`) |
| **Claude Code (CLI)** | Run `./install.sh --claude` (installs to `~/.claude/skills/` using standard `SKILL.md`) |
| **Cursor / Windsurf** | Run `./install.sh --project <dir>` to put markdown prompts in `.agents/skills/` |
| **Project Repositories** | Run `./install.sh --project <repo-path>` to commit `.agents/skills/` to team git |

---

## Testing Everything Before Sharing

To verify that all 9 skills, scripts, and validators are running at 100% pass rate:
```bash
python3 -B test_all.py
```
*(Runs all 145 checks concurrently in under 1 second)*
