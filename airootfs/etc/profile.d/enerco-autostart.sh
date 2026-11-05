# EnercoOS TTY1 Graphical Autostart
if [[ -z "${DISPLAY:-}" ]] && [[ -z "${WAYLAND_DISPLAY:-}" ]] && [[ "$(tty)" == "/dev/tty1" ]]; then
    if [[ ! -f "${HOME}/.config/hypr/hyprland.lua" ]] && [[ -d "/etc/skel" ]]; then
        cp -rT /etc/skel "${HOME}" 2>/dev/null || true
        chown -R 1000:1000 "${HOME}" 2>/dev/null || true
    fi
    exec /usr/local/bin/enerco-session
fi
