# Shiftopia – Future-Proof Architecture

This directory structure follows a **monorepo enterprise-grade** design, inspired by Vercel, Linear, and Apple ecosystem.

## Structure
- `apps/` – platform-specific applications (web, mobile, desktop, miniapp)
- `packages/` – shared libraries (core, ui, i18n, wallet, theme, motion, identity, governance, civilization)
- `messages/` – JSON translation files (next-intl ready)
- `public/` – static assets (glyphs, seals, wallpapers, icons)

## Current Status
- All original Shiftopia content (Constitution, Shahnameh, Economy, etc.) is preserved in `packages/civilization/`.
- The current GitHub Pages site (`index.html`) remains the primary interface until the new web app is built.
- This architecture is **additive** – no existing file has been deleted or moved out of the root.

## Next Steps (for future development)
1. Build a Next.js app in `apps/web` using the packages.
2. Implement wallet connection (RainbowKit + Wagmi).
3. Create a design system with Tailwind + shadcn.
4. Add PWA capabilities.
5. Develop mobile and desktop apps (React Native, Tauri).

## Why This Matters
Shiftopia is not a website; it is a **civilization platform**. This architecture ensures it can scale to any platform, language, and identity system without rewrites.
