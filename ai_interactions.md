# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->


**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->
I read through the documentation and also verified that the tests were still working
---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
I asked the model to "add professional-grade docstrings to every function in logic_utils.py"
I also asked it to "review my code for PEP 8 style compliance"
```

**Linting output before:**

```
Findings
1. Line too long — E501 (the main issue)
Your code logic is clean; nearly all violations are the long # FIX: comments and section headers.

app.py

app.py:3 (145 chars) and app.py:74 (190 chars) — the # FIX: comments
app.py:4 (88 chars) — the four-name import
logic_utils.py

logic_utils.py:80 (151) and logic_utils.py:113 (100) — # FIX: comments
tests/test_game_logic.py

L34, L53, L67, L80 (80–94 chars) — section-header comments
conftest.py

L1 (84 chars)
The fix is to wrap these. For the import:


from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)
For the long comments, split across multiple # lines.

2. Import grouping — E402-adjacent
app.py:1-4: PEP 8 wants three import groups separated by blank lines — standard library, third-party, then local:

import random

import streamlit as st

from logic_utils import (...)
Right now random (stdlib) and streamlit (third-party) are in one block, and the # FIX: comment sits between the import statements.

3. Comment style consistency
app.py:48 uses # Fix: while everywhere else is # FIX:. Minor, but worth making uniform.

Bonus (not PEP 8, but I spotted it)
app.py:102-106 — both branches of the if/else assign the identical value, so the conditional and the commented-out # secret = str(...) line are dead code. This looks like a leftover from the high/low glitch we already fixed in check_guess. It can collapse to just:


secret = st.session_state.secret
This is a logic cleanup, not a style rule — flagging it separately so you can decide.
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->
It suggested that the comments I wrote (the # FIX ones) were too long, so I shortened them. It also told me to group my imports in a more organised way, and suggested I made the spaces between # and my comments consistent. I applied all these changes.
Earlier on though, it suggested I changed the names of some of the existing tests, but I rejected those changes because it suggested ones that were a bit longer and I did not see the point in doing that.
---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
