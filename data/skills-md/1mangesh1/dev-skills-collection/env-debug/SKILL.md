---
name: env-debug
description: Debug environment issues with PATH, permissions, environment variables, and configuration problems. Use when user asks to "fix PATH", "command not found", "permission denied", "debug environment", "env vars not working", "fix shell config", "debug node/python not found", or any environment troubleshooting tasks.
---

# Environment Debugging

Troubleshoot PATH, permissions, env vars, and configuration issues.

## "Command Not Found"

```bash
# Check if command exists
which node
which python
command -v node
type node

# Check PATH
echo $PATH
echo $PATH | tr ':' '\n'  # One per line

# Find where a binary lives
which -a python       # All matches in PATH
whereis python       # Binary, source, and man pages

# Common fixes
export PATH="/usr/local/bin:$PATH"           # Prepend
export PATH="$HOME/.local/bin:$PATH"         # User binaries
export PATH="$HOME/.cargo/bin:$PATH"         # Rust
export PATH="$HOME/go/bin:$PATH"             # Go
export PATH="$HOME/.nvm/versions/node/v20.0.0/bin:$PATH"  # nvm

# Make permanent - add to shell config:
# ~/.bashrc (bash), ~/.zshrc (zsh), ~/.profile (login shell)
```

## Shell Configuration

```bash
# Which shell am I using?
echo $SHELL
echo $0

# Config file load order:
# bash login:    /etc/profile → ~/.bash_profile → ~/.bashrc
# bash non-login: ~/.bashrc
# zsh login:     ~/.zprofile → ~/.zshrc
# zsh non-login: ~/.zshrc

# Reload config
source ~/.zshrc
source ~/.bashrc

# Check if interactive/login
[[ $- == *i* ]] && echo "Interactive" || echo "Non-interactive"
shopt -q login_shell && echo "Login" || echo "Non-login"  # bash
[[ -o login ]] && echo "Login" || echo "Non-login"        # zsh
```

## Environment Variables

```bash
# View all
env
printenv

# View specific
echo $NODE_ENV
printenv NODE_ENV

# Set for current session
export API_KEY="abc123"
export NODE_ENV=production

# Set for single command
NODE_ENV=test npm test
DATABASE_URL=postgres://localhost/test python manage.py migrate

# Unset
unset API_KEY

# Check if set
[ -z "$API_KEY" ] && echo "NOT SET" || echo "SET: $API_KEY"

# .env file loading
# Node.js: dotenv, or node --env-file=.env app.js (Node 20.6+)
# Python: python-dotenv
# Shell: source .env or export $(cat .env | xargs)
```

## Permission Issues

```bash
# Check file permissions
ls -la /path/to/file

# Permission format: drwxrwxrwx
# d = directory, r = read, w = write, x = execute
# [owner][group][others]

# Make executable
chmod +x script.sh
chmod 755 script.sh    # rwxr-xr-x

# Fix npm global permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH="$HOME/.npm-global/bin:$PATH"

# Fix SSH key permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 644 ~/.ssh/config

# Check who owns a file
ls -la /usr/local/bin/node

# Fix ownership
sudo chown -R $(whoami) /usr/local/lib/node_modules
```

## Port Issues

```bash
# What's using a port?
lsof -i :3000              # macOS/Linux
ss -tlnp | grep 3000       # Linux
netstat -tlnp | grep 3000  # Linux

# Kill process on port
lsof -ti :3000 | xargs kill -9   # macOS/Linux
fuser -k 3000/tcp                 # Linux

# Check if port is available
nc -z localhost 3000 && echo "IN USE" || echo "FREE"
```

## Node.js Issues

```bash
# Multiple Node versions?
which -a node
node --version

# nvm issues
nvm ls                     # List installed versions
nvm use 20                 # Switch version
nvm alias default 20       # Set default
nvm current                # Current version

# npm cache issues
npm cache clean --force
rm -rf node_modules package-lock.json && npm install

# Global packages location
npm root -g
npm list -g --depth=0

# npx not finding package
npx --yes package-name     # Force install
npm exec -- package-name   # Alternative
```

## Python Issues

```bash
# Multiple Python versions?
which -a python
which -a python3
python --version
python3 --version

# Virtual environment active?
echo $VIRTUAL_ENV

# Wrong pip?
which pip
pip --version      # Shows which Python it's linked to
python -m pip --version  # Use specific Python's pip

# Module not found?
python -c "import sys; print('\n'.join(sys.path))"
python -c "import package; print(package.__file__)"

# pyenv issues
pyenv versions
pyenv which python
pyenv shell 3.12.1
```

## DNS / Network Issues

```bash
# DNS resolution
nslookup example.com
dig example.com
host example.com

# Test connectivity
ping -c 3 example.com
curl -v https://example.com

# Check proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY
echo $NO_PROXY

# SSL certificate issues
openssl s_client -connect example.com:443

# Test specific port
nc -zv example.com 443
curl -v telnet://example.com:443
```

## Docker Issues

```bash
# Docker daemon running?
docker info

# Permission denied?
sudo usermod -aG docker $USER
# Then log out and back in

# DNS issues in container
docker run --dns 8.8.8.8 myimage

# Can't connect to container?
docker inspect <container> | grep IPAddress
docker port <container>
```

## Disk Space

```bash
# Check disk usage
df -h

# Find large files/dirs
du -sh *
du -sh * | sort -rh | head -20

# Node.js specific
du -sh node_modules/
npx npkill    # Interactive node_modules cleaner

# Docker specific
docker system df
docker system prune -a --volumes
```

## Quick Diagnostic Script

```bash
#!/bin/bash
echo "=== System ==="
uname -a
echo ""
echo "=== Shell ==="
echo "$SHELL ($0)"
echo ""
echo "=== PATH ==="
echo $PATH | tr ':' '\n'
echo ""
echo "=== Key Tools ==="
for cmd in node npm python python3 pip git docker; do
  printf "%-10s" "$cmd:"
  command -v $cmd 2>/dev/null && $cmd --version 2>/dev/null | head -1 || echo "NOT FOUND"
done
echo ""
echo "=== Env Vars ==="
for var in NODE_ENV VIRTUAL_ENV HOME USER SHELL TERM; do
  printf "%-15s %s\n" "$var:" "${!var:-NOT SET}"
done
```

## Reference

For tool-specific troubleshooting: `references/troubleshooting.md`
