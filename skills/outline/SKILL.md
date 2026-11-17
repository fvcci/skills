---
name: outline
description: Format supplied content as clean nested numbered outlines for category breakdowns, action outlines, or an explicit /outline request. Organize the requested content without inventing plan steps or executing actions.
---

# Outline

Make the requested hierarchy visible, with concise parents and only the necessary detail beneath them. Formatting content does not authorize executing the actions described.

## Build a meaningful hierarchy

Before drafting or emitting any part of an outline, choose imperative or declarative form based on what the user needs, honoring any explicitly requested form. Use imperative form when directing action and declarative form when stating facts or enumerating resources; keep each leaf to one concise statement in the chosen form. Preserve every requested task and technical constraint, add detail only when requested or necessary, and do not invent steps, claims or deliverables.

Preserve the user's category labels and requested layer order, including when categories organize an action plan. For category breakdowns, use short category labels without adding goals, benefits or explanatory claims. For action plans without a specified category structure, parent headings name shared outcomes.

Before writing explanatory text, identify what the reader wants to understand or decide and draft a hierarchy of labels, comparing possible groupings when the problem is complex. For each grouping, check what every modifier in its label claims about every child against the supplied facts; broaden the label or move a child when the label overstates what is known. Keep labels about entities distinct from labels about all their traffic: “apps with cluster-local health checks” leaves job delivery unspecified, whereas “cluster-local health checks and job connections” claims both paths are local. Do not infer an entity’s purpose from a familiar name; label an unknown organizing attribute as unknown. Read the roots as an overview, then test how the reader would locate different requested items or details. If the reader must still scan a long list of entity names inside a category, subdivide that branch into recognizable groups; repeat this check at every depth, not just the roots. Inspect siblings as a coherent subdivision and reorganize any branch that mixes unrelated ideas or hides a requested distinction inside prose before filling the skeleton.

Preserve explicitly requested layers; otherwise, choose categories that let the reader recognize a branch, skip it, or descend into progressively deeper detail. In an inventory, make requested distinctions labeled branches beneath each entity, with concrete answers below them: category -> app -> public/private traffic -> actual ingress path, not category -> app -> a sentence mentioning exposure. Retain a requested distinction even when it has one answer, but put the actual answer at the final level rather than adding an empty “Details” or “Ingress path” wrapper.

Create only branches with relevant supporting information, unless the user explicitly asks for every present/absent case. Do not fill an example’s possible branches mechanically: a private-only service needs its private path, not a public branch containing “none” or a repetition of the private path. State a material unknown once under the affected entity, and keep information of another kind under its own accurate label.

Before sending, compare the tree against the requested entities and constraints: keep every named entity findable and retain qualifiers such as “only,” “except,” and “unknown” at their original scope. Attach a condition, uncertainty, or restriction to the item it qualifies, rather than making a disconnected scope section or placing a shared constraint under just one entity. Read each leaf with all its ancestors and reject combined claims that the supplied facts do not support.

Use complete sentences or items that grammatically complete a shared lead-in for actions and explanations. Category headings may be bare labels. Move repeated wording to the parent or lead-in; avoid repeating scaffolding such as “Ensure that” on every sibling. Do not replace sentences with telegram-style fragments.

## Make the hierarchy render correctly

Start the numbered roots with the actual divisions of the answer; do not place the entire tree beneath a numbered title or restatement of the question. By default, use native Markdown numbered lists at every level, with each sibling list starting at one. Number phase headings too. Every outline item, including a file-link child, needs a number. Do not add a dotted address inside a native numbered item.

Indent children beneath their actual parent. Separate top-level groups and immediate child groups with blank lines; keep deeper siblings adjacent. Use bold sparingly for the words carrying the point. Honor requested emphasis conventions without inventing new markers.

If Felix requests full addresses, use explicit text labels at every level, including the top level; do not use native list markers anywhere. Keep indentation consistent across branches, with `&emsp;` repeated once per depth and two trailing spaces for line breaks:

```markdown
**1.** Parent.  
&emsp;**1.1.** Child.  
**2.** Another parent.  
&emsp;**2.1.** Another child.
```

When revising an outline, preserve unaffected wording and structure. Reorganizing does not justify dropping requested content or adding new content.
