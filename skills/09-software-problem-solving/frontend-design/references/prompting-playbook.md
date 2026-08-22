# Prompting Playbook

## Master Prompt Template

```text
You are a Design Systems Engineer + Senior Frontend UI Developer.

[TECH STACK]
- Framework: {{FRAMEWORK}}
- Styling: {{STYLING}}
- Components: {{UI_LIB}}
- Theme: CSS variables or project-native theming

[DESIGN SYSTEM RULES]
1. Layout uses a shared spacing system
2. Typography hierarchy is explicit
3. Colors come from semantic tokens only
4. Shapes and shadows use shared scales
5. Motion is restrained and meaningful
6. Accessibility is mandatory
7. If multi-step, produce a journey map, user flow, or wireflow first
8. If reusable, deliver guideline docs
9. Scan for anti-patterns before final output
10. Before layout, produce a task model, state model, information architecture table, and visibility plan
11. Avoid dashboard/card farm/stacked sections layout unless the task truly is multi-monitoring
12. Keep reference and exception content off the main stage by default

[AESTHETIC DIRECTION]
Style: {{STYLE}}
Key differentiator: {{UNIQUE_FEATURE}}
Target audience: {{AUDIENCE}}

[INTERACTION STATES]
Default, Hover, Active, Focus, Disabled, Loading, Empty, Error

[OUTPUT REQUIREMENTS]
1. Design tokens
2. Component implementations
3. Journey/user-flow artifact when applicable
4. Task model + state model + information architecture table + visibility plan when the screen is a workflow/workbench
5. Page layouts with all states
6. Token-only styling
7. Minimal useful comments
8. Guideline docs when reusable
9. Audit command
```

## Token Generation Prompt

Use when the token system does not exist yet.

Ask for:
- semantic color slots in light/dark mode
- typography scale
- spacing scale
- radius scale
- shadow scale
- motion tokens
- CSS variables, Tailwind integration, and TypeScript types

Do not ask for component code in the same step unless the task is trivial.

## Component Implementation Prompt

Use when tokens already exist and the task is to implement a component.

Require:
- props for variants, sizes, and composition
- default/hover/focus/active/disabled/loading/error states
- accessibility and keyboard support
- responsive behavior
- token-only styling
- usage examples

## Page Development Prompt

Use when components and tokens already exist and the task is to assemble a page.

Require:
- responsive layout
- loading/empty/error states
- explicit primary task hierarchy
- task model split into primary / secondary / low-frequency / rare goals
- state model with entry conditions, must-show content, hidden content, and primary CTA
- information architecture table before layout
- information-role labels for major blocks
- progressive disclosure rules for reference / exception content
- multi-step visibility when applicable
- Gestalt-informed grouping and reading path

## Anti-Stacked Workflow Prompt

Use when the requested screen is a workflow, workbench, reviewer, editor, diff tool, setup flow, or any page that easily collapses into card farm UI.

```text
This is not a dashboard or admin panel. It is a single-primary-task workflow screen.

Before generating any UI code, output:
1. primary task sentence
2. task model: primary / secondary / low-frequency / rare goals
3. state model: entry condition, must-show content, hidden content, primary CTA, exit condition
4. information-role classification for every major block
5. information architecture table
6. visibility plan
7. list of blocks that should be hidden by default and why

Constraints:
- avoid dashboard/card farm/stacked sections layout
- do not give every feature its own card
- first viewport max 2-3 visual groups
- only one primary CTA in the first viewport
- reference content must be on-demand
- exception-handling appears only in matching states
- right rail must not persist unless it directly changes the current decision
- merge or defer sections before adding new panels

After generating the first layout, switch roles and review it as a UX critic:
- remove first-viewport clutter
- merge duplicated feedback panels
- inline helper text instead of large explanation cards
- convert low-frequency content into accordion/drawer/modal/tab where appropriate
```

## Content Audit Prompt

Use when the requested screen contains many requirements and you need the model to decide what belongs in the first viewport before writing any JSX.

```text
Before generating layout, classify every requested block into:
- must-see-now
- next-step-only
- error-only
- on-demand-reference
- keep-off-first-viewport

For every block that is not must-see-now, output:
- hidden_now_because
- reveal_trigger
- container (inline / accordion / drawer / modal / tab / separate step)

If the first viewport still has more than 3 major groups after this pass, convert the flow into tabs / wizard / step navigation instead of adding more cards.
```

## Structured Metadata Prompt

Use when the screen has many conditional blocks and natural language alone is not stable enough.

Ask the model to first emit a JSON-like schema with:
- `id`
- `role`
- `priority`
- `visibility`
- `stage`
- `container`

Then render the page from that schema instead of from an unstructured feature list.

## Review Prompt

Use for self-audit or review.

Check:
- token compliance
- type hierarchy
- spacing/layout consistency
- interactive states
- accessibility
- responsive behavior
- maintainability
- creative differentiation
- flow visibility
- task-first information architecture
- progressive disclosure discipline
- guideline delivery
- anti-pattern scan

## Quick-Start Example

Use a structured brief such as:

```text
Build a team dashboard for a project management app.

Stack: React + TypeScript + Tailwind CSS + shadcn/ui
Style: Minimal Premium SaaS
Audience: product managers and software teams

Components:
- header with search and user menu
- team members grid
- invite modal
- empty state
- loading skeleton

Output:
- design tokens
- component implementations
- dashboard page
- all states
- accessibility notes
```

Rule: do not compress token design, flow design, component design, and final review into one vague prompt if the task is non-trivial.
