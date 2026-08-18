# STRICT SECURITY & PRE-GIT-PUSH SANITIZATION RULE

## CRITICAL MANDATE:
BEFORE making ANY `git commit`, `git push`, or uploading ANY file to GitHub or public repositories, the AI assistant MUST perform a 100% thorough security audit for secrets, API tokens, passwords, private keys, and personal identifiers.

## RULES & AUDIT PROCEDURES:

1. **AUTOMATIC PRE-COMMIT SECRET INSPECTION**:
   - Always run a pattern audit searching for:
     - `TELEGRAM_BOT_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`, `GITHUB_PAT`, `API_KEY`, `SECRET`, `PASSWORD`, `PRIVATE_KEY`
     - Telegram Chat IDs (e.g. `ALLOWED_CHAT_IDS`, `6649449367`, or personal user IDs)
     - Private IP addresses, private credentials, or SSH private keys (`id_rsa`, `id_ed25519`)
     - Live `.env` files containing actual active tokens.

2. **MANDATORY SANITIZATION**:
   - If ANY sensitive key or token is detected in code, documentation, scripts, or examples, the AI MUST IMMEDIATELY SANITIZE it into a safe placeholder before staging or committing (e.g., `TELEGRAM_BOT_TOKEN="your_bot_token_here"`).
   - NEVER commit raw `.env` files containing live secrets. Ensure `.env` is listed in `.gitignore`.

3. **ABSOLUTE PROHIBITION**:
   - DO NOT upload any risk data, confidential tokens, or personal identifiers under any circumstances.
   - If uncertain whether a string is a secret, treat it as a secret and sanitize it first.
