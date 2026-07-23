# Security Policy & Pre-Commit Audit Rule

## AI Agent Security Guideline
This repository strictly enforces zero-leakage security policies:
1. **Pre-Push Inspection**: All code, documentation, and assets must be audited for secret keys, tokens, and personal credentials before any `git push`.
2. **Sanitization Mandate**: Any detected credentials, API keys, or private IDs must be automatically sanitized into placeholder values.
3. **Ignored Sensitive Files**: `.env` and runtime state files are strictly listed in `.gitignore`.
