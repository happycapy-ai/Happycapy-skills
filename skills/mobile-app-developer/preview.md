# Expo Web Preview

Generate a web-based preview page for Expo/React Native apps, featuring a phone-frame web preview (left) and an Expo Go QR code for real-device testing (right).

## Overview

This approach uses **Expo Web (react-native-web)** to render the app in the browser. The preview page consists of:

1. **Left side**: Phone frame (iPhone-style) with the app rendered via iframe (static Expo web export)
2. **Right side**: QR code card for scanning with Expo Go on a real device

## Step-by-Step Process

### 1. Ensure Dependencies

The project must have react-native-web support (included by default in Expo). Verify:

```bash
cd <project-dir>
npm install --legacy-peer-deps
```

Critical: `react` and `react-dom` versions MUST match exactly. Mismatch causes blank page (React error #527).

```bash
# Check versions
node -e "const p=require('./package.json'); console.log('react:', p.dependencies.react, 'react-dom:', p.dependencies['react-dom'])"

# Fix if mismatched
npm install react-dom@<exact-react-version> --legacy-peer-deps
```

### 2. Build Static Web Export

```bash
rm -rf dist
npx expo export --platform web
```

This creates a `dist/` folder with the static web bundle.

**Common errors:**
- `ConfigError: dist/package.json does not exist` - Delete `dist/` first, then retry
- Module resolution errors - Check that `.npmrc` contains `legacy-peer-deps=true`

### 3. Serve the Static Export

```bash
npx serve dist -l 8081 -s &
```

Verify:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/
# Should return 200
```

Export the port:
```bash
/app/export-port.sh 8081
# Returns: https://8081-trickle-XXXXX-preview.happycapy.ai
```

### 4. Start Expo Dev Server (for Expo Go QR)

```bash
CI=1 npx expo start --port 8082 > /tmp/expo-dev.log 2>&1 &
sleep 5
```

Export the port:
```bash
/app/export-port.sh 8082
# Returns: https://8082-trickle-XXXXX-preview.happycapy.ai
```

### 5. Generate QR Code SVG

Use the `qrcode` npm module to generate an inline SVG (avoids CDN dependency issues):

```bash
npm install qrcode --prefix ./tmp 2>/dev/null

node -e "
const QRCode = require('./tmp/node_modules/qrcode');
const url = 'exp://8082-trickle-XXXXX-preview.happycapy.ai';  // Use actual exported URL
QRCode.toString(url, {type:'svg', margin:2, width:220}, (err, svg) => {
  if(err) { console.error(err); process.exit(1); }
  process.stdout.write(svg);
});
" > /tmp/qr.svg
```

**Important**: Always embed the QR code as inline SVG in the HTML. Do NOT rely on CDN-loaded JavaScript libraries (like `https://cdn.jsdelivr.net/npm/qrcode@...`) as they may fail to load in sandboxed environments.

### 6. Create Preview HTML Page

Write to `outputs/<app-name>.html` with this structure:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{App Name} Preview</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
}
.header { text-align: center; margin-bottom: 40px; }
.header h1 { font-size: 36px; font-weight: 800; color: #fff; margin-bottom: 8px; }
.header p { font-size: 16px; color: rgba(255,255,255,0.8); }
.container {
  display: flex; gap: 60px; align-items: center;
  flex-wrap: wrap; justify-content: center;
}
.phone-section { text-align: center; }
.phone-section .label { font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 20px; }
.phone-frame {
  width: 375px; height: 750px; background: #000;
  border-radius: 50px; padding: 12px;
  box-shadow: 0 25px 60px rgba(0,0,0,0.4); position: relative;
}
.phone-frame::before {
  content: ''; position: absolute; top: 12px; left: 50%;
  transform: translateX(-50%); width: 150px; height: 28px;
  background: #000; border-radius: 0 0 16px 16px; z-index: 10;
}
.phone-screen {
  width: 100%; height: 100%; border-radius: 40px;
  overflow: hidden; background: #fff;
}
.phone-screen iframe { width: 100%; height: 100%; border: none; }
.qr-section { text-align: center; }
.qr-card {
  background: #fff; border-radius: 20px; padding: 40px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.2); max-width: 340px;
}
.qr-card .badge {
  display: inline-block; background: #e8f5e9; color: #2e7d32;
  font-size: 13px; font-weight: 600; padding: 4px 12px;
  border-radius: 12px; margin-bottom: 16px;
}
.qr-card h2 { font-size: 22px; font-weight: 700; color: #1a1a1a; margin-bottom: 8px; }
.qr-card .desc { font-size: 14px; color: #666; margin-bottom: 24px; line-height: 1.5; }
.qr-code { width: 220px; height: 220px; margin: 0 auto 20px; }
.expo-url {
  background: #f5f5f5; border-radius: 8px; padding: 10px 14px;
  font-size: 12px; color: #555; word-break: break-all; font-family: monospace;
}
</style>
</head>
<body>
<div class="header">
  <h1>{App Name} Preview</h1>
  <p>Left: Web preview | Right: Scan QR for real device testing</p>
</div>
<div class="container">
  <div class="phone-section">
    <div class="label">Web Preview</div>
    <div class="phone-frame">
      <div class="phone-screen">
        <iframe src="{WEB_PREVIEW_URL}" allow="fullscreen"></iframe>
      </div>
    </div>
  </div>
  <div class="qr-section">
    <div class="qr-card">
      <span class="badge">Real Device Testing</span>
      <h2>Scan with Expo Go</h2>
      <p class="desc">Open Expo Go on iPhone / Android, then scan the QR code below.</p>
      <div class="qr-code">
        {INLINE_SVG_QR_CODE}
      </div>
      <div class="expo-url">{EXPO_URL}</div>
    </div>
  </div>
</div>
</body>
</html>
```

Replace placeholders:
- `{App Name}` - The app display name
- `{WEB_PREVIEW_URL}` - The exported port 8081 URL (e.g., `https://8081-trickle-XXXXX-preview.happycapy.ai`)
- `{EXPO_URL}` - The Expo Go URL (e.g., `exp://8082-trickle-XXXXX-preview.happycapy.ai`)
- `{INLINE_SVG_QR_CODE}` - The SVG content from step 5

### 7. Output as Static File

```
<attachments>
<file type="static">outputs/<app-name>.html</file>
</attachments>
```

## Port Allocation

| Port | Purpose |
|------|---------|
| 8081 | Static web export (npx serve) |
| 8082 | Expo dev server (for Expo Go) |

If ports are occupied, kill existing processes first or use alternative ports (8083, 8084, etc.).

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Blank page | react/react-dom version mismatch | `npm install react-dom@<react-version> --legacy-peer-deps` |
| QR code not showing | CDN script blocked | Use inline SVG (never rely on external JS for QR) |
| "Port XXXX in use" | Previous process still running | `pkill -f "serve.*dist"` or `lsof -i :<port>` then kill |
| Expo Go can't connect | Port not exported | Run `/app/export-port.sh <port>` |
| Raw JSON on web preview | Missing `--web` flag or wrong port | Ensure static export is served, not Metro |
| Missing SafeAreaProvider | Navigation crash on web | Wrap app root with `<SafeAreaProvider>` |
| Navigation targets wrong | Screen names mismatch | Ensure `navigate()` calls match exact tab names |

## Expo Go SDK Version

**Default to Expo SDK 54** for Expo Go compatibility. Expo Go only supports specific SDK versions. When scaffolding a new project:

```bash
npx create-expo-app@latest <app-name> --template blank -- --sdk-version 54
```

Or in `app.json`:
```json
{
  "expo": {
    "sdkVersion": "54.0.0"
  }
}
```

If using a newer SDK (e.g., 56), Expo Go may not support it — users would need a development build instead.

## Key Principles

1. **Always use Expo Web (react-native-web)** - Never fall back to pure HTML/CSS recreations
2. **Inline SVG for QR** - External CDN libraries are unreliable in sandboxed environments
3. **Version matching** - react and react-dom MUST be the same version
4. **Static export preferred** - `npx expo export --platform web` produces a reliable static bundle
5. **Two servers** - Static serve for web preview (iframe), Expo dev server for Expo Go (QR code)
6. **Expo Go SDK 54** - Default to SDK 54 for Expo Go real-device testing compatibility
