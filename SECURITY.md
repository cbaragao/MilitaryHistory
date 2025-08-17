# Security Configuration Guide

## ⚠️ CRITICAL: API Keys Were Exposed in Git History

**IMMEDIATE ACTION REQUIRED**: The settings.toml file containing your NARA API key and Data.world token was committed to Git and **IS VISIBLE IN THE PUBLIC REPOSITORY** at https://github.com/cbaragao/MilitaryHistory.git

### 🚨 Compromised Credentials

The following credentials are exposed in commit `b1c66be` and need immediate rotation:

1. **NARA API Key**: `4xAb9IEf1568AYb4eaRUY8f0admbxZIF4QvZYLjT`
2. **Data.world JWT Token**: Contains admin/read/write permissions for user `aragaocb`

### 🔄 Required Actions (DO THIS NOW)

1. **Rotate Data.world Token**:
   - Go to https://data.world/settings/advanced
   - Revoke the current token
   - Generate a new token
   - Update your local `src/config/settings.toml` file

2. **Rotate NARA API Key**:
   - Go to https://catalog.archives.gov/
   - Generate a new API key
   - Update your local `src/config/settings.toml` file

3. **Clean Git History** (if you want to remove the exposure):
   ```bash
   # WARNING: This rewrites history and affects anyone who has cloned the repo
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch src/config/settings.toml' \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (DANGEROUS - only do this if no one else has cloned)
   git push origin --force --all
   ```

## 🔒 Secure Configuration Setup

### Initial Setup

1. **Copy the template**:
   ```bash
   cp src/config/settings.toml.example src/config/settings.toml
   ```

2. **Add your new API credentials**:
   ```toml
   [nara]
   api_key="your_new_nara_api_key"
   
   [datadotworld]
   token="your_new_datadotworld_token"
   ```

3. **Verify the file is gitignored**:
   ```bash
   git status  # settings.toml should NOT appear in untracked files
   ```

### Security Best Practices

- ✅ **Never commit `settings.toml`** - it's now in `.gitignore`
- ✅ **Use `settings.toml.example`** for sharing configuration structure
- ✅ **Rotate keys regularly** - especially after any suspected exposure
- ✅ **Use environment variables** in production environments
- ✅ **Monitor API usage** for unauthorized access patterns

### Environment Variables Alternative

For additional security, you can use environment variables instead of the settings file:

```bash
export NARA_API_KEY="your_key_here"
export DATADOTWORLD_TOKEN="your_token_here"
```

Then update your code to read from environment variables as a fallback.

### What's Protected Now

The updated `.gitignore` now protects:
- `src/config/settings.toml` - Main config file
- `*.toml` - All TOML files (be careful with this)
- `.env*` - Environment variable files

### Monitoring

**Check your accounts for unauthorized usage**:
- Data.world: Monitor dataset uploads/downloads you didn't perform
- NARA: Check API usage quotas and access logs

---

## 📞 If You Need Help

- Data.world support: https://help.data.world/
- NARA API support: https://catalog.archives.gov/help

**Remember**: This exposure happened because configuration files with secrets were committed to Git. Always use templates and `.gitignore` for sensitive configuration.