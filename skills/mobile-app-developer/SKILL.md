---
name: mobile-app-developer
description: End-to-end mobile app development and publishing using Expo + EAS. Covers project scaffolding, asset preparation, peer-dep / lock-file troubleshooting (development.md), web preview with phone frame and Expo Go QR code (preview.md), AND automated build + submit to TestFlight / App Store (publishing.md), with full automation via Apple ASC API Key (no Mac, no Xcode, no 2FA required). Use when the user wants to build, test, preview, publish, or automate the release pipeline of a React Native / Expo iOS or Android app.
---

# mobile-app-developer

End-to-end playbook for shipping an Expo / React Native app — from scaffolding to TestFlight / Play Store — fully automated from a Linux sandbox.

## When to Trigger

Trigger this skill when the user wants to:

- Scaffold or modify a React Native / Expo project
- Run / test / debug the app locally (Expo Go, dev client, simulator)
- **Generate a web preview page** with phone frame + Expo Go QR code
- Configure EAS Build (cloud build) for iOS or Android
- Publish to **TestFlight** (iOS internal testing) or **Google Play Internal Testing**
- Submit to App Store / Play Store public release
- Set up ASC API Key auth (bypass Apple 2FA)
- Replace icons / splash screens for store compliance
- Diagnose EAS build failures (peer deps, lock files, credentials, fingerprint, etc.)

Do NOT trigger for: pure native iOS/Android (no Expo), Flutter, Cordova/Capacitor, KMP/Compose Multiplatform.

## Skill Layout

This skill is split into focused documents. Read the relevant one(s) on demand — do NOT preload all.

| File | Read when… |
|---|---|
| **`development.md`** | Setting up project, installing deps, configuring `app.json`, preparing icons/splash, running on simulator/device, fixing peer-dep / lock-file errors, managing env vars / secrets |
| **`publishing.md`** | Configuring `eas.json` submit profile, ASC API Key / Play Service Account, running build + submit, diagnosing submit failures, App Store / Play Store metadata checklists |
| **`preview.md`** | Generating a web preview page with phone frame + Expo Go QR code. Uses Expo Web (react-native-web) static export for browser preview and Expo dev server for real-device QR scanning |

If the user's task spans multiple (e.g. "build a new Expo app and ship it to TestFlight"), read `development.md` first, then `publishing.md`.

## Default Tech Stack

| Layer | Choice |
|---|---|
| Framework | Expo (latest stable — check `https://docs.expo.dev/versions/latest/` before scaffolding) |
| Build / Distribution | EAS Build + EAS Submit (Expo cloud) |
| Auth (Apple) | App Store Connect API Key (`.p8`) — bypasses 2FA |
| Auth (Google) | Play Console Service Account JSON |
| Auth (Expo) | Personal Access Token via `EXPO_TOKEN` |

## Hard Preconditions

Before starting **any** build or publish work, confirm with the user:

- Expo account + `EXPO_TOKEN` (https://expo.dev/accounts/<user>/settings/access-tokens)
- For iOS:
  - Apple Developer account (paid, $99/year)
  - ASC API Key: `.p8` file + Issuer ID + Key ID (role ≥ App Manager; ≥ Admin to create certs)
  - Apple Team ID + ASC App ID + Bundle Identifier
- For Android:
  - Google Play Console account ($25 one-time)
  - Service Account JSON key (created in Play Console → API access)
  - Package name + Play Console app already created
  - **First AAB must be uploaded manually to Play Console** before automation works

If anything is missing, **ask the user** before proceeding. Do not guess.

## Sandbox Requirements

The sandbox/CI must have:

```bash
node --version       # >= 18
npm --version        # >= 9
convert -version     # ImageMagick — for icon/splash conversion
expect -v            # for first-time non-interactive credential setup
curl --version       # for fetching build logs
```

Quick check:
```bash
for cmd in node npm convert expect curl; do
  command -v $cmd >/dev/null 2>&1 && echo "[OK] $cmd" || echo "[MISSING] $cmd"
done
```

If anything is missing, install before continuing (`apt-get install imagemagick expect`).

## Architecture Recommendation

| Phase | AI/API key location | Why |
|---|---|---|
| Internal testing (TestFlight / Play Internal) | OK to call AI Gateway directly from client | Speed of iteration; risk is bounded by closed tester pool |
| Public release | **MUST** proxy through your own backend | Embedded keys can be extracted from any IPA/AAB |

## Useful URLs

- Expo SDK matrix: https://docs.expo.dev/versions/latest/
- EAS dashboard: `https://expo.dev/accounts/<owner>/projects/<slug>/builds`
- ASC API Keys: https://appstoreconnect.apple.com/access/integrations/api
- Play Console API access: https://play.google.com/console → Setup → API access
- Expo PAT: https://expo.dev/accounts/<user>/settings/access-tokens

## Notes

- All commands tested on Linux. macOS users get extra options (local Xcode, simctl) which this skill avoids for portability.
- Treat `.p8` files and Service Account JSONs like passwords. Always gitignore (`*.p8`, `*-service-account.json`).
- This skill assumes EAS cloud build. Local builds (`expo prebuild` + native toolchain) are out of scope.
