# Security Checklist for Public GitHub Repository

## ✅ Pre-Commit Security Checklist

Before pushing to GitHub, verify:

### 1. **Environment Variables**
- [ ] `.env` file is in `.gitignore`
- [ ] `.env` file is NOT committed to git
- [ ] `.env.example` contains NO real credentials
- [ ] All sensitive values use placeholder text (e.g., `your-api-key-here`)

### 2. **Credentials & Secrets**
- [ ] No API keys in code files
- [ ] No passwords in code files
- [ ] No connection strings in code files
- [ ] No access tokens in code files
- [ ] All secrets loaded from environment variables

### 3. **Personal Data**
- [ ] `activities_data.json` is in `.gitignore` (contains your personal activities)
- [ ] No personal email addresses in code
- [ ] No personal phone numbers in code
- [ ] No internal Microsoft information exposed

### 4. **Configuration Files**
- [ ] `config.py` loads from environment variables
- [ ] No hardcoded credentials in `config.py`
- [ ] Docker files use environment variable substitution

### 5. **Git History**
- [ ] Run: `git log --all --full-history --` to check if `.env` was ever committed
- [ ] If `.env` was committed, you MUST rotate your API keys immediately

## 🚨 If You Accidentally Committed Secrets

### Immediate Actions:

1. **Rotate ALL credentials immediately:**
   ```bash
   # Go to Azure Portal and regenerate your API keys
   # Update your .env file with new keys
   ```

2. **Remove from git history:**
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push (if already pushed):**
   ```bash
   git push origin --force --all
   ```

4. **Contact GitHub Support** to purge cached versions

## ✅ Current Status

### Files Protected (in .gitignore):
- ✅ `.env` - Contains your real Azure credentials
- ✅ `activities_data.json` - Contains your personal activity data
- ✅ `.venv/` - Python virtual environment
- ✅ `__pycache__/` - Python cache files
- ✅ `*.pyc` - Compiled Python files

### Safe to Commit:
- ✅ `.env.example` - Template with NO real credentials
- ✅ `.gitignore` - Specifies what to ignore
- ✅ All `.py` files - Use environment variables
- ✅ `README.md`, `DOCKER.md`, etc. - Documentation
- ✅ `requirements.txt` - Dependencies
- ✅ `docker-compose.yml` - Uses ${ENV_VAR} syntax
- ✅ All files in `static/`, `routes/`, `tests/`

## 📋 Verification Commands

Run these before your first push:

```bash
# 1. Verify .env is ignored
git status | grep .env
# Should return nothing (means it's ignored)

# 2. Check what will be committed
git add .
git status

# 3. Search for potential secrets in staged files
git diff --cached | grep -i "key\|password\|secret\|token"

# 4. Verify .gitignore is working
git check-ignore .env
# Should output: .env (means it's ignored)
```

## 🔐 Best Practices

### DO:
- ✅ Use `.env` for local development
- ✅ Use environment variables in production
- ✅ Use GitHub Secrets for CI/CD
- ✅ Use Azure Key Vault for production secrets OR Managed Identities
- ✅ Commit `.env.example` with placeholder values
- ✅ Document required environment variables in README
- ✅ Rotate API keys regularly (every 90 days)

### DON'T:
- ❌ Commit `.env` file
- ❌ Hard-code credentials in any file
- ❌ Share API keys in Slack/email/issues
- ❌ Use production credentials in development
- ❌ Commit `activities_data.json` (personal data)
- ❌ Include credentials in comments
- ❌ Paste credentials in pull request descriptions

## 🔍 Files to Review

Before committing, review these files for accidental secrets:

1. `config.py` - Should ONLY use `os.environ.get()`
2. `ai_service.py` - Should import from config module
3. `docker-compose.yml` - Should use `${VAR}` syntax
4. `.env.example` - Should have placeholder text only

## ✅ Ready to Push Checklist

- [ ] Run `git status` and verify `.env` is NOT listed
- [ ] Run `git diff --cached` and scan for secrets
- [ ] Verify `.env.example` has NO real values
- [ ] Verify `activities_data.json` is ignored
- [ ] All configuration uses environment variables
- [ ] Documentation is updated
- [ ] Tests pass: `pytest tests/`
