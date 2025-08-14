# Build and Deploy (Quick)
1. Upload and extract package into your cloned repo on VPS.
2. Run: sudo ./scripts/setup_env.sh
3. Optional: replace branding assets in branding/
4. Commit and push to dev branch:
   git checkout -b dev
   git add .
   git commit -m "Add XXOS dev package v2 (beta)"
   git push origin dev
5. Build ISO: sudo ./scripts/build_iso.sh
6. Test in QEMU/VM.
