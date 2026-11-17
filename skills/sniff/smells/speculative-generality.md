# Speculative Generality (YAGNI)

Build what was asked. Nothing for the imagined next requirement.

Cut:
- Options, flags, and config knobs with one call site passing the default.
- Abstract base classes, interfaces, and registries with one implementation.
- Generic type parameters used at one concrete type.
- `try/catch` that logs and rethrows unchanged.
- Defensive checks for states the type system or caller already rules out.
- Exports nothing imports.
- A new function, type, or file with one user.
- A new field, option, parameter, or flag that nothing reads. Check the repo, not only the change.
- A check, default, or fallback for a case nothing shown produces.

Before cutting a piece with one user, apply the deletion test from
`codebase-design`: imagine it deleted. If the complexity vanishes, it was a
pass-through, so cut it. If the complexity reappears across its callers, it
earns its keep.

If you genuinely think something extra is needed, say it in one line and let
the user decide. Don't build it preemptively.
