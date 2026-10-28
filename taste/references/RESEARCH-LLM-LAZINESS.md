# Empirical Research: LLM Output Truncation & Code Laziness

> A synthesis of the root causes of LLM code truncation, brevity bias, and field-tested architectural remediations from Leonxlnx research.

---

## 1. Root Causes of LLM Output Truncation

1. **RLHF & Compute Economics**:
   - Production models (Claude, GPT, Gemini) are fine-tuned with Reinforcement Learning from Human Feedback (RLHF) where human raters prefer concise conversational answers.
   - Inference cost optimizations create an implicit penalty on token count, driving systematic brevity bias.

2. **Training Data Bias**:
   - Millions of StackOverflow answers and tutorial blogs in training sets use placeholder patterns (`// TODO`, `/* rest of implementation */`, `...`).
   - The model learns that emitting placeholders is standard idiomatic behavior for complex files.

3. **Context Asymmetry**:
   - Model input context windows (128k to 1M+ tokens) are drastically larger than output token generation caps (usually 4k to 8k tokens per generation turn).
   - When generating an entire multi-component landing page in one pass, the model approaches the output cap and abruptly starts summarizing or dropping closing tags.

---

## 2. Field-Tested Remediation Techniques

1. **Syntax Binding & File Segmentation**:
   - Break large frontends into isolated leaf components: `Hero.tsx`, `FeatureGrid.tsx`, `Pricing.tsx`, `Footer.tsx`.
   - Never request a 1,500-line monolithic file in a single prompt.

2. **Output Enforcement Directives**:
   - Explicitly instruct the model: *"You are an exhaustive code generator. Never use placeholders, ellipsis comments (`...`), or truncated blocks. Output every line required for the file to compile cleanly."*

3. **Dial Calibration**:
   - Restrain visual density when generating large prototypes to prevent token exhaustion.
   - Use strict Pre-Flight checks to catch truncated or incomplete blocks before deployment.
