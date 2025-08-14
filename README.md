# XXOS Final Dev Package (v2, Beta) - for dev branch

This package contains the DEV package to bootstrap XXOS development on your Ubuntu 24.10 VPS.
It includes build scripts, branding, first-boot installer GUI, web console skeleton, and a local AI assistant stub.
Relay prototype is omitted (will be added later).

Target branch: dev

IMPORTANT: I cannot push to GitHub for you. Run the git commands on your VPS.
Do NOT paste secrets or PATs in chat. Revoke any exposed PATs immediately.

Contents (key):
- scripts/{setup_env.sh, build_iso.sh, push_to_github.sh}
- livebuild/ (config for live-build)
- installer/xxos-installer-gui.py (GTK installer GUI)
- agent/xxos-agent/ (local assistant stub - FastAPI)
- branding/ (placeholders to replace)
- docs/ (build & deploy instructions)

This is a BETA release. Many features are stubs and should be tested in VMs before production use.
© 2025 Zeeshan Saeed Paracha • XXOS (Beta)
