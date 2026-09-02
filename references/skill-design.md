# Safe skill customization

Prefer this companion skill over replacing upstream files.

When behavior differs, compare the installed schema and official documentation first. A missing action can indicate a different product generation, not a broken installation.

If the user authorizes a managed override, record its version, preserve a rollback copy outside the repository, make the smallest supported change, and test a synthetic positive and negative case. Do not silently overwrite bundled skills or turn a local ordering workaround into a universal rule.
