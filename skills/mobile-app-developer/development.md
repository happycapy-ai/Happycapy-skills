# Development & Testing Guide

Use this document when working on the **before-publish** phase: project setup, dependencies, asset preparation, local testing, and fixing build-time errors. For ship-to-store workflows, see `publishing.md`.

## 1. Project Scaffolding

### From scratch

```bash
npx create-expo-app@latest my-app -t blank
cd my-app
git init
```

### From existing repo

```bash
git clone <repo>
cd <repo>
npm install --legacy-peer-deps   # see Peer Deps section below
```

### Verify Expo SDK version

```bash
npx expo --version
cat package.json | grep '"expo"'
```

**Always check `https://docs.expo.dev/versions/latest/` for the current SDK version and its compatible React Native / React versions before adding new packages.** Mismatches between SDK and dependency versions cause most build failures.

## 2. Project Structure (Recommended)

```
my-app/
├── app.json                          # Expo config (single source of truth)
├── eas.json                          # EAS Build/Submit profiles
├── .npmrc                            # legacy-peer-deps=true
├── .gitignore                        # MUST include *.p8, *-service-account.json, .env
├── package.json                      # Pin volatile peers exactly
├── package-lock.json                 # Keep in sync with package.json
├── App.js                            # Entry point
├── assets/
│   ├── icon.png                      # 1024×1024 RGB no alpha
│   ├── splash-icon.png               # 1024×1024 RGBA OK
│   ├── android-icon-foreground.png   # 512×512 RGBA, 66% safe area
│   ├── android-icon-background.png   # 512×512
│   ├── android-icon-monochrome.png   # 512×512 (Android 13+ themed icons)
│   └── favicon.png                   # 48×48 (web only, optional)
├── src/
│   ├── api.js                        # API client (use env vars, not hardcoded keys)
│   ├── constants.js                  # Read from `expo-constants` / EAS env
│   └── screens/
└── tests/                            # Optional: jest, detox, maestro
```

## 3. `app.json` Template

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "splash": {
      "image": "./assets/splash-icon.png",
      "resizeMode": "contain",
      "backgroundColor": "#FFFFFF"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.example.myapp",
      "buildNumber": "1",
      "infoPlist": {
        "ITSAppUsesNonExemptEncryption": false
      }
    },
    "android": {
      "package": "com.example.myapp",
      "versionCode": 1,
      "adaptiveIcon": {
        "foregroundImage": "./assets/android-icon-foreground.png",
        "backgroundImage": "./assets/android-icon-background.png",
        "monochromeImage": "./assets/android-icon-monochrome.png"
      }
    },
    "web": { "favicon": "./assets/favicon.png" },
    "extra": {
      "eas": { "projectId": "<EAS_PROJECT_UUID>" }
    },
    "owner": "<expo_username>"
  }
}
```

Notes:
- `ITSAppUsesNonExemptEncryption: false` skips Apple's encryption export prompt.
- Android `versionCode` is auto-incremented by EAS when `eas.json` has `autoIncrement: true`.
- If `eas.json` sets `appVersionSource: "remote"`, the local `buildNumber` / `versionCode` values are ignored at build time — EAS owns them.

## 4. Dependency Management

### `.npmrc` (project root)

```
legacy-peer-deps=true
```

Required for React 19 era — EAS runs `npm ci --include=dev` which is strict.

### Pin volatile peer deps

Some packages publish patch versions independently (e.g. `react-dom`, `scheduler`). If the user's project uses caret ranges (`^19.1.0`) and a new patch ships, the lock file diverges from `package.json`. Pin them exact:

```json
{
  "dependencies": {
    "react": "19.1.0",
    "react-dom": "19.1.0",
    "react-native": "0.81.5"
  }
}
```

### When `package.json` and `package-lock.json` go out of sync

Symptom (in EAS log):
```
npm error `npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json are in sync.
npm error Invalid: lock file's react-dom@19.2.6 does not satisfy react-dom@19.1.0
```

Fix:
```bash
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
git add package-lock.json
```

## 5. Asset Preparation

### Sizes & format requirements

| Asset | Size | Format | Alpha | Notes |
|---|---|---|---|---|
| iOS app icon | 1024×1024 | PNG sRGB | **NO alpha** | Apple rejects alpha |
| Splash | 1024×1024 | PNG | OK | Subject centered |
| Android adaptive foreground | 512×512 | PNG | OK | Content within central 66% safe area |
| Android adaptive background | 512×512 | PNG / solid color | OK | Often solid brand color |
| Android monochrome (themed icons) | 512×512 | PNG (white-on-transparent) | required | Android 13+ |
| Play Store icon (listing) | 512×512 | PNG 32-bit | OK | Different from in-app icon |
| Play Store feature graphic | 1024×500 | PNG / JPG | no transparency | Required for Play Store listing |
| Phone screenshots (Play / App Store) | 1080×1920 (9:16) | PNG / JPG | OK | At least 2, max 8 |
| Favicon (web) | 48×48 | PNG | OK | Optional |

### ImageMagick recipes

```bash
# iOS app icon (no alpha, white background flatten)
convert src.png -resize 1024x1024 -background white -alpha remove -alpha off \
  -colorspace sRGB -type TrueColor PNG24:assets/icon.png

# Splash (alpha OK)
convert src.png -resize 1024x1024 \
  -colorspace sRGB -type TrueColorAlpha PNG32:assets/splash-icon.png

# Android adaptive foreground (centered with safe-area padding)
convert src.png -resize 432x432 -background none -gravity center -extent 512x512 \
  -colorspace sRGB -type TrueColorAlpha PNG32:assets/android-icon-foreground.png

# Android monochrome (white on transparent silhouette)
convert src.png -resize 432x432 -background none -gravity center -extent 512x512 \
  -alpha extract -threshold 50% -negate \
  -colorspace sRGB PNG32:assets/android-icon-monochrome.png

# Play Store feature graphic (1024×500 with brand color background)
convert src.png -resize 400x400 -background "#FFFFFF" -gravity center -extent 1024x500 \
  -colorspace sRGB -type TrueColor PNG24:store-assets/feature-graphic.png

# Web favicon
convert src.png -resize 48x48 PNG32:assets/favicon.png
```

## 6. Environment Variables & Secrets

### Local development

Use a `.env` file (gitignored) loaded via `expo-constants` or `react-native-dotenv`:

```bash
# .env  (do NOT commit)
API_BASE_URL=https://staging.example.com
```

### Build-time secrets via EAS Environment Variables

DO NOT hardcode API keys, gateway tokens, or any secret in `constants.js`. Use EAS env vars:

```bash
# Create a per-environment secret (encrypted, never visible after creation)
eas env:create --name AI_GATEWAY_API_KEY --value <secret> \
  --environment production --visibility secret

# Plain text (not encrypted, but managed centrally)
eas env:create --name API_BASE_URL --value https://prod.example.com \
  --environment production --visibility plaintext

# List
eas env:list --environment production

# Pull into local .env for local dev
eas env:pull --environment development
```

In code, read via `process.env.AI_GATEWAY_API_KEY` (with `expo-env` setup) or `expo-constants` extras.

### Where to store the API/service account keys

| File | Where it lives | Where it's used | Gitignore? |
|---|---|---|---|
| `AuthKey_*.p8` (ASC API Key) | Project root | EAS Submit reads it locally | YES |
| `*-service-account.json` (Play) | Project root | EAS Submit reads it locally | YES |
| `EXPO_TOKEN` | shell env | EAS CLI auth | YES (env only) |

## 7. Local Development & Testing

### Run on Expo Go (fast iteration)

```bash
npx expo start
# scan QR with Expo Go app on phone
# or press i (iOS sim) / a (Android emulator) / w (web)
```

### Run on dev client (when using native modules not in Expo Go)

```bash
eas build --profile development --platform ios
# install resulting build on device
npx expo start --dev-client
```

### Smoke test the build profile locally before pushing to EAS

```bash
# Generates a simulator-runnable build — confirms Metro bundle works
eas build --profile preview --platform ios --local
```

### Internal distribution (preview builds for QA)

`eas.json` should include:
```json
{
  "build": {
    "preview": {
      "distribution": "internal",
      "ios": { "simulator": true },
      "android": { "buildType": "apk" }
    }
  }
}
```

Then `eas build --profile preview --platform all` produces a sharable install link without going through TestFlight / Play.

## 8. Common Development Failures

| Symptom | Root Cause | Fix |
|---|---|---|
| `eas: command not found` after `npm install eas-cli` | Project node_modules corrupt; binary not symlinked | Install in `/tmp/eas-install/` (clean dir): `mkdir -p /tmp/eas-install && cd /tmp/eas-install && npm init -y && npm install eas-cli` and use full path |
| `npm ci` fails: ERESOLVE peer dep conflict | React 19 ecosystem version mismatch | Add `.npmrc` with `legacy-peer-deps=true` AND pin volatile deps exactly |
| `npm ci` fails: lock file out of sync | Edited `package.json` without regenerating lock | `rm -rf node_modules package-lock.json && npm install --legacy-peer-deps` |
| Metro bundler stuck / cache stale | Watchman / Metro cache | `npx expo start --clear` or `watchman watch-del-all` |
| "Cannot find module 'expo-constants'" at runtime | Native module not in Expo Go | Use a dev client build instead of Expo Go |
| Asset (image) not found at runtime | Forgot to `require()` it or wrong path case | Use `require('./assets/icon.png')`, ensure case matches filesystem (Linux is case-sensitive) |
| Build fails with "fingerprint" warning but no other error | Non-fatal; expo config loader spawn issue | Ignore — build still succeeds |
| `eas init` says "project already exists" | Old `extra.eas.projectId` in app.json | Either delete the field and re-init, or use `eas init --id <existing-id>` |
| Phone shows "HTTP response error 500: CommandError: Input is required, but 'npx expo' is in non-interactive mode" when scanning QR / opening preview URL | `app.json` has `owner` or `extra.eas.projectId` set, so Expo dev server tries to look up account info from expo.dev. With no `EXPO_TOKEN` set and no TTY (sandbox), the auth prompt fails | Restart with `EXPO_TOKEN=<pat> EXPO_NO_TELEMETRY=1 npx expo start --port 8081 --host lan < /dev/null > /tmp/expo.log 2>&1 &` — `< /dev/null` is required so stdin doesn't trigger interactive prompts |
| Bundle URL in manifest points to wrong public host (stale session) | Proxy hardcodes `PUBLIC_HOST` from a previous session | Make the proxy read `req.headers['x-forwarded-host'] \|\| req.headers.host` instead of a hardcoded value |

## 9. Pre-Publish Checklist

Before handing off to `publishing.md`, confirm:

- [ ] `app.json` has correct `bundleIdentifier` (iOS) and `package` (Android), matching what's in App Store Connect / Play Console
- [ ] `version` in `app.json` is set (`1.0.0` for first release)
- [ ] All required icons exist and pass spec (run `file assets/*.png` to verify dimensions)
- [ ] iOS `icon.png` has NO alpha channel (`file assets/icon.png` should say "8-bit/color RGB", not "RGBA")
- [ ] `eas.json` exists with at minimum a `production` build profile
- [ ] `.gitignore` includes `*.p8`, `*-service-account.json`, `.env`
- [ ] `package-lock.json` is in sync with `package.json` (`npm ci --dry-run` succeeds)
- [ ] Local smoke test passed (`npx expo start` runs without errors)
- [ ] Secrets are in EAS env / Secrets, NOT in source

When all checked, proceed to `publishing.md`.
