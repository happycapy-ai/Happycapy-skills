# Publishing & Submission Guide

Use this document for the **after-development** phase: configuring `eas.json`, running EAS Build + Submit, getting builds onto TestFlight / Play Internal Testing, and shipping to the public stores. For project setup, deps, asset prep, and local testing, see `development.md`.

## 0. Pre-Flight (Read First)

Before invoking any submit command:

- [ ] All items in `development.md` § 9 "Pre-Publish Checklist" are checked
- [ ] User has provided all credentials (see § 1 below)
- [ ] You're using a **clean** `eas-cli` (in `/tmp/eas-install/` if project's local install is broken)
- [ ] EAS project is initialized: `eas init` or `eas init --id <existing-uuid>`

## 1. Required Credentials

### iOS / TestFlight / App Store

| Item | Format | Where to get |
|---|---|---|
| ASC API Key (`.p8`) | File | https://appstoreconnect.apple.com/access/integrations/api → "+" |
| Issuer ID | UUID | Same page, top of API Keys table |
| Key ID | 10-char alphanumeric | Created with the .p8 |
| Apple Team ID | 10-char alphanumeric | https://developer.apple.com/account → Membership |
| ASC App ID | Numeric | App Store Connect → My Apps → app → App Info → "Apple ID" |
| Bundle Identifier | Reverse-DNS | Pre-registered in Certificates, Identifiers & Profiles |

The ASC API Key role: **App Manager** is enough for `eas submit`; **Admin** is required if you want EAS to also create distribution certificates and provisioning profiles.

### Android / Play Internal / Play Store

| Item | Format | Where to get |
|---|---|---|
| Service Account JSON | File | Play Console → Setup → API access → Create service account → download JSON |
| Package name | Reverse-DNS | Must match what's in app.json `android.package` |
| Existing Play Console app | — | Created manually in Play Console (free) |
| **First AAB uploaded manually** | — | Google requires the first build to be uploaded via the web UI before API automation works |

### Expo

| Item | Format | Where to get |
|---|---|---|
| `EXPO_TOKEN` | String | https://expo.dev/accounts/<user>/settings/access-tokens |

## 2. `eas.json` — Full Submit Profile

```json
{
  "cli": {
    "version": ">= 12.0.0",
    "appVersionSource": "remote"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "ios": { "simulator": true },
      "android": { "buildType": "apk" }
    },
    "production": {
      "autoIncrement": true,
      "ios": { "image": "latest" },
      "android": { "image": "latest" }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "ascAppId": "<NUMERIC_APP_ID>",
        "appleTeamId": "<TEAM_ID>",
        "ascApiKeyPath": "./AuthKey_XXXXXXXXXX.p8",
        "ascApiKeyId": "XXXXXXXXXX",
        "ascApiKeyIssuerId": "<ISSUER_UUID>"
      },
      "android": {
        "serviceAccountKeyPath": "./play-service-account.json",
        "track": "internal",
        "releaseStatus": "draft"
      }
    }
  }
}
```

`track` options for Android: `internal` (closed test), `alpha`, `beta`, `production`.
`releaseStatus`: `draft` (you finalize in Play Console) or `completed` (auto-publish to that track).

## 3. First-Time Credentials Setup (One-Off)

EAS needs to create a Distribution Certificate and Provisioning Profile on Apple's side. The first time, this requires interactive yes-prompts. Use `expect` from a non-TTY sandbox:

```bash
cat > /tmp/eas-credentials.exp <<'EOF'
#!/usr/bin/expect -f
set timeout 180
spawn /tmp/eas-install/node_modules/.bin/eas credentials --platform ios
expect "Generate a new Apple Distribution Certificate?" { send "y\r" }
expect "Generate a new Apple Provisioning Profile?" { send "y\r" }
expect eof
EOF
chmod +x /tmp/eas-credentials.exp
EXPO_TOKEN=<token> /tmp/eas-credentials.exp
```

After this runs once, `--non-interactive` works forever (until certs expire ~1 year later).

For Android, EAS auto-creates a keystore the first time you run a production build. Download a backup with `eas credentials` after first build.

## 4. The Golden One-Shot Command (iOS)

```bash
cd <project-dir>

export EXPO_TOKEN=<expo_pat>
export EXPO_ASC_API_KEY_PATH=$(pwd)/AuthKey_XXXXXXXXXX.p8
export EXPO_ASC_KEY_ID=XXXXXXXXXX
export EXPO_ASC_ISSUER_ID=<issuer-uuid>
export EXPO_APPLE_TEAM_ID=<team-id>
export EXPO_APPLE_TEAM_TYPE=COMPANY_OR_ORGANIZATION   # or INDIVIDUAL

# Run via the clean install if project's eas-cli is broken:
/tmp/eas-install/node_modules/.bin/eas build \
  --platform ios \
  --profile production \
  --non-interactive \
  --auto-submit
```

What happens:
1. Auto-increments `buildNumber` (~5 sec)
2. Uploads project tarball to EAS (~30 sec)
3. EAS builds in cloud (~10–15 min)
4. EAS submits IPA to App Store Connect (~1–3 min)
5. Apple processes the build (~5–15 min) — you'll get an email
6. Build appears on TestFlight: `https://appstoreconnect.apple.com/apps/<asc-app-id>/testflight/ios`

## 5. The Golden One-Shot Command (Android)

```bash
cd <project-dir>

export EXPO_TOKEN=<expo_pat>

/tmp/eas-install/node_modules/.bin/eas build \
  --platform android \
  --profile production \
  --non-interactive \
  --auto-submit
```

After completion: `https://play.google.com/console/u/0/developers/<dev-id>/app/<app-id>/tracks/internal-testing`

**Reminder**: First AAB MUST be uploaded manually via Play Console UI. After that, this command works.

## 6. Combined iOS + Android in One Run

```bash
/tmp/eas-install/node_modules/.bin/eas build \
  --platform all \
  --profile production \
  --non-interactive \
  --auto-submit
```

EAS runs both builds in parallel.

## 7. Common Submit Failures

| Symptom | Root Cause | Fix |
|---|---|---|
| "Distribution Certificate is not validated for non-interactive builds" | First-time setup needs interactive yes-prompts | Run the `expect` script in § 3 once, then `--non-interactive` works |
| App rejected on Apple's automatic check: "icon contains alpha" | iOS app icons must NOT have alpha | `convert in.png -resize 1024x1024 -background white -alpha remove -alpha off -colorspace sRGB -type TrueColor PNG24:icon.png` |
| Apple 2FA prompt blocking submit | Default `eas submit` uses Apple ID auth | Use ASC API Key (set in `eas.json` under `submit.production.ios.ascApiKey*`) — never falls back to 2FA |
| Build fails at INSTALL_DEPENDENCIES, no obvious reason | Need actual log content | `eas build:view <build-id> --json` → grep for `xcodeBuildLogsUrl` and `buildArtifactsUrls` GCS URLs → `curl -L` them |
| "Cannot get Expo config from an Expo project" warning during fingerprint | Non-fatal; expo config loader spawn issue | Ignore — build still succeeds |
| Build succeeds but TestFlight doesn't show new build | Apple processing delay | Wait 5–15 min, refresh App Store Connect TestFlight page |
| Android submit fails: "APK has not been published yet" | First AAB not yet manually uploaded | Upload one AAB through Play Console UI, then retry |
| Android submit fails: "The package name … is not registered" | `app.json` `android.package` doesn't match what's in Play Console | Make them identical |
| Android submit fails: "ServiceAccount … doesn't have access" | Service account not granted permission on the app | Play Console → API access → grant **App permissions** for this specific app |
| Android: "Version code N has already been used" | Two builds collided on the same versionCode | Set `autoIncrement: true` in eas.json production profile |

## 8. Diagnosing a Failed Build (How to Get Real Logs)

```bash
# Get JSON describing the build, including signed log URLs
eas build:view <build-id> --json > /tmp/build.json

# Extract the GCS-signed log URLs
grep -oE 'https://storage\.googleapis\.com/[^"]+' /tmp/build.json

# Fetch them
curl -sL "<url>" | head -200
```

The URLs are time-limited GCS-signed links — fetch promptly.

## 9. App Store (Apple) Public Submission Checklist

Beyond TestFlight, before the public release goes live:

- [ ] Screenshots: 5 required sizes for iPhone (6.7", 6.5", 5.5"), iPad (12.9" 2nd gen, 12.9" 6th gen) if `supportsTablet: true`
- [ ] App description (≤4000 chars), promotional text (≤170 chars), keywords (≤100 chars total, comma-separated)
- [ ] Support URL, Marketing URL (optional), Privacy Policy URL (REQUIRED)
- [ ] Demo account credentials for Apple's review team (if app has login)
- [ ] Backend proxy for AI calls — no embedded keys in client
- [ ] Crash monitoring configured (Sentry or EAS Insights)
- [ ] Privacy nutrition labels filled in App Store Connect → App Privacy
- [ ] Age rating questionnaire completed
- [ ] Content moderation in place if app has user-generated content (REQUIRED by App Store guideline 1.2)
- [ ] Dedicated icon at 1024×1024 — full-canvas composition (avoid small subject in large white field)
- [ ] App Review Information: contact name, phone, email
- [ ] Version Release: choose "manually" or "automatic after approval"

## 10. Play Store (Google) Public Submission Checklist

Play is stricter than Apple about metadata. Even **Internal Testing** requires most of these:

- [ ] App name (≤30 chars)
- [ ] Short description (≤80 chars)
- [ ] Full description (≤4000 chars)
- [ ] App icon for store listing: 512×512 PNG 32-bit
- [ ] Feature graphic: 1024×500 PNG/JPG (no transparency)
- [ ] Phone screenshots: at least 2, max 8, 16:9 or 9:16
- [ ] App category
- [ ] Contact email + (optional) website + phone
- [ ] **Privacy policy URL (REQUIRED, even for internal testing)**
- [ ] Content rating questionnaire (IARC)
- [ ] Target audience age range
- [ ] **Data safety form** (Google is strict — list every data type collected, sharing, encryption)
- [ ] Government / News / COVID / Financial / Health questionnaires (each has policy implications)
- [ ] Ads declaration (yes/no)
- [ ] Tester list (email addresses or Google Group) for Internal Testing track

## 11. EAS Update (OTA Hot Updates)

After your binary is shipped, JS / asset changes can be pushed without going through App Store / Play review:

```bash
# Set up EAS Update once
eas update:configure
# Now the runtime version is pinned; native changes still require a new build

# Push an update
eas update --branch production --message "Fix typo in welcome screen"

# View update history
eas update:list --branch production

# Rollback
eas update:rollback-to-embedded
```

Constraints:
- Only JS, assets, and config changes — anything that touches native code requires a new EAS Build + store submission
- Updates are scoped per `runtimeVersion` (set in app.json or via `runtimeVersion: { policy: "appVersion" }`)

## 12. Useful Diagnostic Commands

```bash
# Who am I?
eas whoami

# What's the project?
eas project:info

# Recent builds
eas build:list --limit 10

# Detail on a specific build
eas build:view <build-id>

# Get build logs as JSON (includes signed log URLs)
eas build:view <build-id> --json

# Recent submits
eas submit:list --limit 10

# Current credentials state
eas credentials --platform ios
eas credentials --platform android

# Env vars on EAS
eas env:list --environment production
```

## 13. Useful URLs

- EAS dashboard: `https://expo.dev/accounts/<owner>/projects/<slug>/builds`
- Submission detail: `https://expo.dev/accounts/<owner>/projects/<slug>/submissions/<id>`
- TestFlight: `https://appstoreconnect.apple.com/apps/<asc-app-id>/testflight/ios`
- App Store Connect: `https://appstoreconnect.apple.com/apps/<asc-app-id>`
- Play Console: `https://play.google.com/console/u/0/developers/<dev-id>/app/<app-id>`
- Play Internal Testing: `https://play.google.com/console/u/0/developers/<dev-id>/app/<app-id>/tracks/internal-testing`
- Apple Developer Portal: `https://developer.apple.com/account/resources`
