# EnercoOS Default Zsh Environment
autoload -Uz compinit promptinit
compinit
promptinit

# Prompt style
PROMPT='%F{cyan}⚡ enerco%f:%F{blue}%~%f$ '

# Useful aliases
alias ls='ls --color=auto'
alias ll='ls -la'
alias grep='grep --color=auto'
alias mterp='chromium --app=https://mterp.internal --ozone-platform=wayland'
alias install-os='calamares'
alias lockdown='sudo /usr/local/bin/enerco-lockdown'

# Welcome message
if [[ -o interactive ]]; then
    fastfetch 2>/dev/null || cat /etc/issue
fi

