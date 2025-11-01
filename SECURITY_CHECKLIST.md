# 🔒 Security Checklist Before Git Commit

This checklist helps ensure no sensitive information is accidentally committed to your repository.

## ✅ Pre-Commit Security Verification

### 1. Environment & Configuration Files
- [ ] No `.env` files with real API keys or passwords
- [ ] No `config.ini` or `settings.py` with hardcoded secrets
- [ ] No AWS credentials files (`.aws/`, `aws-credentials`)
- [ ] No database connection strings with passwords
- [ ] No `.env.local`, `.env.production` files

### 2. API Keys & Secrets
- [ ] No files containing `api-key`, `api_key`, `apikey`
- [ ] No `secrets.json`, `secrets.yaml`, `secrets.txt`
- [ ] No `*.key`, `*.pem`, `*.p12`, `*.pfx` files
- [ ] No password files (`*password*`, `*.pwd`)
- [ ] No private SSH keys (`id_rsa*`, `id_dsa*`)

### 3. Python & Virtual Environments
- [ ] `.venv/` directory is excluded (✓ Already in .gitignore)
- [ ] `__pycache__/` directories are excluded (✓ Already in .gitignore)
- [ ] `requirements.txt` contains only public package names
- [ ] No `.ipynb` files with output containing sensitive data

### 4. Database & Data Files
- [ ] No `*.db`, `*.sqlite`, `*.sqlite3` files with real data
- [ ] No `data.csv`, `data.json` with production data
- [ ] No `database.sql` with real credentials
- [ ] Data files in `.gitignore` if they contain sensitive info

### 5. Logs & Debug Files
- [ ] No `*.log` files with error messages containing secrets
- [ ] No `debug.log`, `error.log`, `access.log` files
- [ ] No stack traces with environment variables

### 6. IDE & Editor Files
- [ ] `.vscode/` directory is excluded (✓ Already in .gitignore)
- [ ] No `.idea/` files (JetBrains IDEs)
- [ ] No `.DS_Store` files (✓ Already in .gitignore)

## 🛠️ Commands to Run Before Commit

```bash
# Check for common sensitive file patterns
find . -name "*.env*" -o -name "*secret*" -o -name "*password*" -o -name "*.key" -o -name "*.pem"

# Check for API keys in text files
grep -r "api[_-]key\|apikey\|secret\|password" . --include="*.txt" --include="*.py" --include="*.js" --include="*.json"

# Check for database URLs
grep -r "postgres://\|mysql://\|mongodb://\|redis://" . --include="*.py" --include="*.js" --include="*.json"

# Check for AWS credentials patterns
grep -r "AWS_ACCESS_KEY_ID\|AWS_SECRET_ACCESS_KEY" . --include="*.py" --include="*.js" --include="*.env*"

# Show files that would be added to git
git status --porcelain

# Check what git is about to commit
git diff --cached
```

## 🚨 Red Flags to Watch For

1. **Hardcoded credentials in code:**
   ```python
   # BAD - Never commit these
   API_KEY = "sk-1234567890abcdef..."
   DATABASE_URL = "postgresql://user:password@localhost/db"
   ```

2. **Environment files with real values:**
   ```bash
   # BAD - If these contain real secrets
   echo "API_KEY=real_key_here" > .env
   ```

3. **Configuration files with passwords:**
   ```ini
   # BAD
   [database]
   password = my_real_password
   ```

## ✅ Best Practices

1. **Use environment variables for secrets:**
   ```python
   import os
   API_KEY = os.getenv('API_KEY')  # Set in .env file (not committed)
   ```

2. **Use `.env.example` for templates:**
   ```bash
   # This file CAN be committed
   API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```

3. **Use secrets management for production:**
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager
   - HashiCorp Vault

4. **Regular security scans:**
   ```bash
   # Install and run security scanner
   pip install bandit
   bandit -r . -f json -o security-report.json
   ```

## 📋 Current Workspace Status

✅ **Secured in .gitignore:**
- `.venv/` - Python virtual environment
- `__pycache__/` - Python cache files
- `*.pyc` - Compiled Python files
- `.vscode/` - VS Code settings
- `.DS_Store` - macOS system files

⚠️ **Currently in workspace (check if sensitive):**
- `uv.lock` - Package lock file (usually safe to commit)
- `pyproject.toml` - Project configuration (usually safe)
- `requirements.txt` - Dependencies list (usually safe)

## 🔍 Next Steps

1. Run the security check commands above
2. Remove any sensitive files found
3. Use `git rm --cached <file>` to unstage files already added
4. Make sure `.env` files are never created with real secrets
5. Set up pre-commit hooks to automatically check for secrets

## 📞 If You Find a Secret

If you accidentally commit a secret:

1. **Immediately rotate the secret** (change API keys, passwords, etc.)
2. Remove the secret from the file
3. Use `git rm --cached <file>` to unstage
4. Make a new commit removing the secret
5. Contact your security team if this was a production system

---

**Remember: It's easier to prevent commits than to clean up git history later!**