#!/usr/bin/env bash
# gbro-collage-broll environment self-check (AI Gateway variant for this environment).
# Exit 0 = all good; exit 1 = at least one item missing (details on stdout).

set -u

resolve_skill_dir() {
  # generate-image/generate-video may live under ~/.claude/skills (installed
  # from the Happycapy-skills catalog) or /opt/claude-skills (pre-baked into
  # some Happycapy sandboxes). Check both, prefer the user-installed one.
  for candidate in "$HOME/.claude/skills/$1" "/opt/claude-skills/$1"; do
    if [ -d "$candidate" ]; then
      printf '%s' "$candidate"
      return 0
    fi
  done
  printf '%s' "$HOME/.claude/skills/$1"
}

GEN_IMAGE_SKILL="$(resolve_skill_dir generate-image)"
GEN_VIDEO_SKILL="$(resolve_skill_dir generate-video)"
FAIL=0

ok()   { printf 'PASS  %s\n' "$1"; }
bad()  { printf 'FAIL  %s\n' "$1"; FAIL=1; }

# 1. AI_GATEWAY_API_KEY (drives both Gate 2 stills and Gate 3 video via the AI Gateway)
if [ -n "${AI_GATEWAY_API_KEY:-}" ]; then
  ok "AI_GATEWAY_API_KEY 已设置"
else
  bad "AI_GATEWAY_API_KEY 未设置（本环境的 AI Gateway 凭证，应已由平台注入；如缺失请联系平台方）"
fi

# 2. ffmpeg / ffprobe
if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
  ok "ffmpeg / ffprobe 可用"
else
  bad "ffmpeg / ffprobe 缺失（Debian/Ubuntu: sudo apt install ffmpeg）"
fi

# 3. Python >= 3.10 (Gate 2 still generation helper)
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
  ok "python3 >= 3.10"
else
  bad "python3 缺失或版本低于 3.10"
fi

# 4. node (Gate 3 video generation via generate-video skill's SDK script)
if command -v node >/dev/null 2>&1; then
  ok "node 可用"
else
  bad "node 缺失（Gate 3 依赖 generate-video skill 的 generate_video_sdk.js）"
fi

# 5. sibling generate-image / generate-video skills present
if [ -f "$GEN_IMAGE_SKILL/scripts/generate_image.py" ]; then
  ok "generate-image skill 可用（Gate 2 静帧兜底方案）"
else
  bad "未找到 $GEN_IMAGE_SKILL（Gate 2 静帧生成需要它，或改用本 skill 自带的 scripts/generate_still_gateway.py）"
fi

if [ -f "$GEN_VIDEO_SKILL/scripts/generate_video_sdk.js" ]; then
  ok "generate-video skill 可用（Gate 3 视频生成）"
else
  bad "未找到 $GEN_VIDEO_SKILL（Gate 3 视频生成依赖它）"
fi

exit $FAIL
