#!/usr/bin/env bash
# ==============================================================================
# Google Antigravity Skills Suite - Universal Shell Installer
# Works with: Antigravity IDE, Claude Code, and agent-compatible workspaces.
# ==============================================================================

set -e

# ANSI Color codes
if [ -t 1 ]; then
  BOLD="\033[1m"
  GREEN="\033[0;32m"
  CYAN="\033[0;36m"
  YELLOW="\033[1;33m"
  RED="\033[0;31m"
  DIM="\033[2m"
  RESET="\033[0m"
else
  BOLD=""
  GREEN=""
  CYAN=""
  YELLOW=""
  RED=""
  DIM=""
  RESET=""
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# All 21 Production Skills in Suite
ALL_SKILLS=(
  "court"
  "secure-audit"
  "anti-vcode"
  "impeccable"
  "steal"
  "taste"
  "designs"
  "ui-ux-max"
  "threeui"
  "rev-engineer"
  "logo-design"
  "writing-readme"
  "arena"
  "ponytail"
  "last30days"
  "scrapling"
  "humanizer"
  "diagram-design"
  "socratic"
  "rigor"
  "sanzo-wada-colors"
)

# Bundles
BUNDLE_DESIGN=(
  "anti-vcode"
  "designs"
  "ui-ux-max"
  "threeui"
  "taste"
  "sanzo-wada-colors"
  "diagram-design"
  "logo-design"
  "impeccable"
)

BUNDLE_ENGINEERING=(
  "rigor"
  "secure-audit"
  "socratic"
  "court"
  "rev-engineer"
  "scrapling"
  "ponytail"
  "arena"
)

BUNDLE_PROSE=(
  "writing-readme"
  "humanizer"
  "steal"
  "last30days"
)

# State variables
MODE=""
CUSTOM_PATH=""
SELECTED_SKILLS=()
RUN_TESTS=false
DRY_RUN=false
INSTALL_ALL_FLAG=false
BUNDLE_NAME=""

show_help() {
  cat << EOF
${BOLD}Google Antigravity Skills Suite - Installer${RESET}

${BOLD}USAGE:${RESET}
    ./install.sh [OPTIONS]

${BOLD}DESTINATION OPTIONS:${RESET}
    -g, --global           Install globally for Antigravity IDE (~/.gemini/config/skills) [Default]
    -p, --project [DIR]    Install locally into project repository (.agents/skills)
    -c, --claude           Install globally for Claude Code (~/.claude/skills)
    --claude-project [DIR] Install locally for Claude Code project (.claude/skills)
    --custom DIR           Install into custom target directory

${BOLD}SKILL SELECTION OPTIONS:${RESET}
    -a, --all              Install all 21 skills without prompting
    -b, --bundle NAME      Install curated bundle: 'design' (9), 'engineering' (8), or 'prose' (4)
    -s, --skills LIST      Comma-separated list of skills to install
    -l, --list             List available skills and bundles
    -t, --test             Run test suite after installation
    -d, --dry-run          Simulate installation without copying files
    -h, --help             Show this help message

${BOLD}EXAMPLES:${RESET}
    ./install.sh --all --global          # Instant 10-second install of all 21 skills
    ./install.sh --bundle design -g      # Install 9 design skills globally
    ./install.sh --bundle engineering -p # Install 8 engineering skills into local repo
    ./install.sh --skills court,taste -g # Install specific skills
    ./install.sh                         # Launch guided 2-step interactive installer
EOF
  exit 0
}

list_skills() {
  echo -e "${BOLD}Available Skills in Suite (21 total):${RESET}"
  echo -e "────────────────────────────────────────────────────────────────────────"
  echo -e "  1.  ${CYAN}court${RESET}              - Adversarial idea & architecture trials"
  echo -e "  2.  ${CYAN}secure-audit${RESET}       - Coverage-led vulnerability hunting & AST validators"
  echo -e "  3.  ${CYAN}anti-vcode${RESET}         - 40-point anti-slop code scanner & Swiss design"
  echo -e "  4.  ${CYAN}impeccable${RESET}         - 24-command design framework & offline detector"
  echo -e "  5.  ${CYAN}steal${RESET}              - Austin Kleon creative operating system"
  echo -e "  6.  ${CYAN}taste${RESET}              - Leonxlnx v2 anti-slop frontend dials & preflight"
  echo -e "  7.  ${CYAN}designs${RESET}            - Curated 67 design themes & token registry"
  echo -e "  8.  ${CYAN}ui-ux-max${RESET}          - BM25 design intelligence (79 styles, 192 palettes)"
  echo -e "  9.  ${CYAN}threeui${RESET}            - 104 production 3D & WebGL Three.js components"
  echo -e "  10. ${CYAN}rev-engineer${RESET}       - REA: Decompilation, Electron/JS & binary reconstruction"
  echo -e "  11. ${CYAN}logo-design${RESET}        - Disciplined SVG brand identity & 1,400+ reference library"
  echo -e "  12. ${CYAN}writing-readme${RESET}     - The Art of Writing Excellent GitHub READMEs (50-point rubric)"
  echo -e "  13. ${CYAN}arena${RESET}              - 100 sub-agents tournament bracket to eliminate bad answers"
  echo -e "  14. ${CYAN}ponytail${RESET}           - The lazy senior dev: minimal diffs & shortcut debt tracking"
  echo -e "  15. ${CYAN}last30days${RESET}         - Real-time temporal intelligence (Reddit, X, YouTube, HN, Polymarket)"
  echo -e "  16. ${CYAN}scrapling${RESET}          - Adaptive web scraping, stealth browsing & Cloudflare bypass"
  echo -e "  17. ${CYAN}humanizer${RESET}          - Wikipedia-backed 26-pattern anti-AI-writing polish & prose humanizer"
  echo -e "  18. ${CYAN}diagram-design${RESET}     - Editorial HTML+SVG diagrams (45 types, no shadows, Antigravity IDE helper)"
  echo -e "  19. ${CYAN}socratic${RESET}           - Senior engineering self-interrogation (15 domains, 10 decision packs)"
  echo -e "  20. ${CYAN}rigor${RESET}              - Empirical engineering discipline (grounding, task ledger, review)"
  echo -e "  21. ${CYAN}sanzo-wada-colors${RESET}  - Sanzo Wada 1930s color dictionary (348 palettes, WCAG contrast & tokens)"
  echo -e "\n${BOLD}Curated Bundles:${RESET}"
  echo -e "  • ${GREEN}design${RESET}      (9 skills): anti-vcode, designs, ui-ux-max, threeui, taste, sanzo-wada-colors, diagram-design, logo-design, impeccable"
  echo -e "  • ${GREEN}engineering${RESET} (8 skills): rigor, secure-audit, socratic, court, rev-engineer, scrapling, ponytail, arena"
  echo -e "  • ${GREEN}prose${RESET}       (4 skills): writing-readme, humanizer, steal, last30days"
  echo -e "────────────────────────────────────────────────────────────────────────"
  exit 0
}

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -g|--global)
      MODE="global"
      shift
      ;;
    -p|--project)
      MODE="project"
      if [[ -n "$2" && "$2" != -* ]]; then
        CUSTOM_PATH="$2"
        shift
      fi
      shift
      ;;
    -c|--claude)
      MODE="claude"
      shift
      ;;
    --claude-project)
      MODE="claude-project"
      if [[ -n "$2" && "$2" != -* ]]; then
        CUSTOM_PATH="$2"
        shift
      fi
      shift
      ;;
    --custom)
      MODE="custom"
      CUSTOM_PATH="$2"
      shift 2
      ;;
    -a|--all)
      INSTALL_ALL_FLAG=true
      shift
      ;;
    -b|--bundle)
      BUNDLE_NAME="$2"
      shift 2
      ;;
    -s|--skills)
      IFS=',' read -r -a CLI_SKILLS <<< "$2"
      SELECTED_SKILLS=("${CLI_SKILLS[@]}")
      shift 2
      ;;
    -l|--list)
      list_skills
      ;;
    -t|--test)
      RUN_TESTS=true
      shift
      ;;
    -d|--dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      show_help
      ;;
    *)
      echo -e "${RED}Unknown option: $1${RESET}"
      show_help
      ;;
  esac
done

# Resolve bundles if specified via flag
if [ -n "$BUNDLE_NAME" ]; then
  case "$BUNDLE_NAME" in
    design)
      SELECTED_SKILLS=("${BUNDLE_DESIGN[@]}")
      ;;
    engineering)
      SELECTED_SKILLS=("${BUNDLE_ENGINEERING[@]}")
      ;;
    prose)
      SELECTED_SKILLS=("${BUNDLE_PROSE[@]}")
      ;;
    *)
      echo -e "${RED}Error: Unknown bundle '$BUNDLE_NAME'. Choose from: design, engineering, prose${RESET}"
      exit 1
      ;;
  esac
elif [ "$INSTALL_ALL_FLAG" = true ]; then
  SELECTED_SKILLS=("${ALL_SKILLS[@]}")
fi

# Interactive mode if target mode or skills selection is missing
if [ -z "$MODE" ] || [ ${#SELECTED_SKILLS[@]} -eq 0 ]; then
  if [ -t 0 ]; then
    echo -e "${BOLD}${CYAN}========================================================================${RESET}"
    echo -e "${BOLD}       Google Antigravity Skills Suite — Guided Interactive Setup       ${RESET}"
    echo -e "${BOLD}${CYAN}========================================================================${RESET}\n"

    # Step 1: Destination
    if [ -z "$MODE" ]; then
      echo -e "${BOLD}Step 1: Choose destination:${RESET}\n"
      echo -e "  ${BOLD}1)${RESET} Antigravity Global        ${DIM}(~/.gemini/config/skills) [Recommended - Universal]${RESET}"
      echo -e "  ${BOLD}2)${RESET} Current Project Workspace ${DIM}(./.agents/skills)        [Project-scoped]${RESET}"
      echo -e "  ${BOLD}3)${RESET} Claude Code Global        ${DIM}(~/.claude/skills)        [Claude CLI]${RESET}"
      echo -e "  ${BOLD}4)${RESET} Claude Code Project       ${DIM}(./.claude/skills)${RESET}"
      echo -e "  ${BOLD}5)${RESET} Custom Directory\n"
      read -rp "Select destination [1-5] (default: 1): " choice_dest
      choice_dest="${choice_dest:-1}"
      case "$choice_dest" in
        1) MODE="global" ;;
        2) MODE="project" ;;
        3) MODE="claude" ;;
        4) MODE="claude-project" ;;
        5)
          MODE="custom"
          read -rp "Enter target directory path: " CUSTOM_PATH
          ;;
        *)
          echo -e "${YELLOW}Defaulting to Antigravity Global.${RESET}"
          MODE="global"
          ;;
      esac
    fi

    # Step 2: Skill Scope
    if [ ${#SELECTED_SKILLS[@]} -eq 0 ]; then
      echo -e "\n${BOLD}Step 2: Choose skills to install:${RESET}\n"
      echo -e "  ${BOLD}1)${RESET} ${GREEN}Install All 21 Skills${RESET}           ${DIM}[Recommended - Complete Suite]${RESET}"
      echo -e "  ${BOLD}2)${RESET} Frontend & Design Bundle       ${DIM}(9 skills: anti-vcode, designs, ui-ux-max, threeui...)${RESET}"
      echo -e "  ${BOLD}3)${RESET} Engineering & Security Bundle  ${DIM}(8 skills: rigor, secure-audit, socratic, court...)${RESET}"
      echo -e "  ${BOLD}4)${RESET} Writing & Research Bundle      ${DIM}(4 skills: writing-readme, humanizer, steal, last30days)${RESET}"
      echo -e "  ${BOLD}5)${RESET} Custom Pick                    ${DIM}(Select by comma-separated numbers, e.g. 1, 8, 20)${RESET}\n"
      read -rp "Select skills [1-5] (default: 1): " choice_scope
      choice_scope="${choice_scope:-1}"
      case "$choice_scope" in
        1)
          SELECTED_SKILLS=("${ALL_SKILLS[@]}")
          ;;
        2)
          SELECTED_SKILLS=("${BUNDLE_DESIGN[@]}")
          ;;
        3)
          SELECTED_SKILLS=("${BUNDLE_ENGINEERING[@]}")
          ;;
        4)
          SELECTED_SKILLS=("${BUNDLE_PROSE[@]}")
          ;;
        5)
          echo -e "\nAvailable skills:"
          for i in "${!ALL_SKILLS[@]}"; do
            printf "  %2d) %s\n" "$((i + 1))" "${ALL_SKILLS[$i]}"
          done
          read -rp $'\nEnter numbers or skill names separated by commas: ' raw_picks
          SELECTED_SKILLS=()
          IFS=',' read -r -a tokens <<< "$raw_picks"
          for tok in "${tokens[@]}"; do
            tok=$(echo "$tok" | xargs)
            if [[ "$tok" =~ ^[0-9]+$ ]]; then
              idx=$((tok - 1))
              if [ $idx -ge 0 ] && [ $idx -lt ${#ALL_SKILLS[@]} ]; then
                SELECTED_SKILLS+=("${ALL_SKILLS[$idx]}")
              fi
            elif [ -n "$tok" ]; then
              for s in "${ALL_SKILLS[@]}"; do
                if [ "$s" = "$tok" ]; then
                  SELECTED_SKILLS+=("$tok")
                  break
                fi
              done
            fi
          done
          if [ ${#SELECTED_SKILLS[@]} -eq 0 ]; then
            echo -e "${YELLOW}No valid skills selected. Defaulting to all 21 skills.${RESET}"
            SELECTED_SKILLS=("${ALL_SKILLS[@]}")
          fi
          ;;
        *)
          SELECTED_SKILLS=("${ALL_SKILLS[@]}")
          ;;
      esac
    fi
  else
    # Non-interactive shell defaults
    [ -z "$MODE" ] && MODE="global"
    [ ${#SELECTED_SKILLS[@]} -eq 0 ] && SELECTED_SKILLS=("${ALL_SKILLS[@]}")
  fi
fi

# Resolve destination directory
TARGET_DIR=""
case "$MODE" in
  global)
    TARGET_DIR="$HOME/.gemini/config/skills"
    ;;
  project)
    BASE_DIR="${CUSTOM_PATH:-.}"
    TARGET_DIR="$BASE_DIR/.agents/skills"
    ;;
  claude)
    TARGET_DIR="$HOME/.claude/skills"
    ;;
  claude-project)
    BASE_DIR="${CUSTOM_PATH:-.}"
    TARGET_DIR="$BASE_DIR/.claude/skills"
    ;;
  custom)
    if [ -z "$CUSTOM_PATH" ]; then
      echo -e "${RED}Error: Custom directory path must be provided.${RESET}"
      exit 1
    fi
    TARGET_DIR="$CUSTOM_PATH"
    ;;
esac

echo -e "\n${BOLD}Target Directory:${RESET} ${CYAN}$TARGET_DIR${RESET}"
echo -e "${BOLD}Selected Skills:${RESET}  ${#SELECTED_SKILLS[@]} of ${#ALL_SKILLS[@]} (${SELECTED_SKILLS[*]})\n"

if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}[DRY RUN] No files will be modified.${RESET}"
fi

# Create target directory if needed
if [ "$DRY_RUN" = false ]; then
  mkdir -p "$TARGET_DIR"
fi

installed_count=0
for skill in "${SELECTED_SKILLS[@]}"; do
  skill=$(echo "$skill" | xargs) # trim whitespace
  SRC_PATH="$SCRIPT_DIR/$skill"
  DEST_PATH="$TARGET_DIR/$skill"

  if [ ! -d "$SRC_PATH" ]; then
    echo -e "  ${YELLOW}Warning: Skill '$skill' not found in $SCRIPT_DIR. Skipping.${RESET}"
    continue
  fi

  echo -e "  ${GREEN}Installing${RESET} ${BOLD}$skill${RESET}..."

  if [ "$DRY_RUN" = false ]; then
    mkdir -p "$DEST_PATH"
    # Copy files excluding python caches and temp files
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --delete \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='*.pyo' \
        --exclude='.DS_Store' \
        --exclude='node_modules' \
        --exclude='.court' \
        --exclude='.impeccable' \
        --exclude='.rigor' \
        --exclude='.artist' \
        --exclude='dist' \
        "$SRC_PATH/" "$DEST_PATH/"
    else
      # Fallback to cp
      rm -rf "$DEST_PATH"
      mkdir -p "$DEST_PATH"
      cp -rf "$SRC_PATH/." "$DEST_PATH/"
      find "$DEST_PATH" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
      find "$DEST_PATH" -type f -name "*.pyc" -delete 2>/dev/null || true
    fi

    # Make executable scripts runnable
    find "$DEST_PATH/scripts" "$DEST_PATH/bin" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.cjs" -o -name "*.js" \) -exec chmod +x {} + 2>/dev/null || true
  fi

  installed_count=$((installed_count + 1))
done

echo -e "\n${BOLD}${GREEN}Successfully installed $installed_count skill(s) into $TARGET_DIR${RESET}\n"

# Run validation tests if requested
if [ "$RUN_TESTS" = true ]; then
  echo -e "${BOLD}${CYAN}Running verification tests...${RESET}\n"
  if [ -f "$SCRIPT_DIR/test_all.py" ]; then
    python3 -B "$SCRIPT_DIR/test_all.py"
  fi
fi

echo -e "${BOLD}Next Steps:${RESET}"
if [ "$MODE" = "global" ]; then
  echo -e "  • Skills are now globally available in Antigravity IDE across all workspaces."
elif [ "$MODE" = "project" ]; then
  echo -e "  • Commit .agents/skills into your repository to share with collaborators."
elif [ "$MODE" = "claude" ]; then
  echo -e "  • Skills are now accessible to your Claude Code agent sessions."
fi
echo -e "  • Trigger any skill in chat (e.g., ${CYAN}/rigor${RESET}, ${CYAN}/court${RESET}, ${CYAN}/taste${RESET}, ${CYAN}/anti-vcode${RESET})\n"
