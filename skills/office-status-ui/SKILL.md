---
name: office-status-ui
description: Visualize AI assistant working status with a 3D-style virtual office. A cute capybara character moves between different areas based on current task. Use when the user says /office, start office, office status, AI status visualization, capybara office, or wants to see AI working status in real-time.
tools: Bash, Read, Write
---

# Office Status UI

Launch a 3D-style virtual office to visualize AI assistant working status in real-time. A cute capybara character moves between different functional areas based on the current task.

## When to Use

- User says `/office`, `start office`, or `launch office`
- User wants to visualize AI working status
- User asks for `office status` or `AI status`
- User wants a fun status monitoring interface
- User mentions `capybara office` or `capy office`

## Features

- **3D Rendered Office Background** - Beautiful isometric office with 5 functional areas
- **30+ Work States** - Fine-grained status mapping to different areas
- **Smooth Walking Animation** - 3-second transition with walking effect
- **Real-time Statistics** - Track time spent in each area (persisted to localStorage)
- **Demo Mode** - One-click demonstration of all states
- **Humorous Bubble Text** - Fun inner monologues for each state

## Area Mapping

| Area | States |
|------|--------|
| Lounge (Sofa) | idle, waiting, ready, error, stuck |
| Library | thinking, analyzing, planning, researching, reading, learning, searching, confused |
| Desk | writing, coding, editing, debugging, refactoring |
| Server Room | executing, running, processing, building, testing, deploying |
| Meeting Room | meeting, discussing, reviewing, collaborating, responding, explaining, presenting, chatting, answering |

## Quick Start

### Step 1: Clone and Start Server

```bash
# Clone the repository
git clone https://github.com/AchengBusiness/happycapy-office-ui.git
cd happycapy-office-ui

# Install dependency
pip install flask

# Start backend server
cd backend
python app.py > /tmp/capy_office.log 2>&1 &
sleep 3

# Verify server is running
curl -s localhost:18791/health
```

### Step 2: Export Port (for HappyCapy environment)

```bash
/app/export-port.sh 18791
```

### Step 3: Return Preview URL

Tell the user the preview URL and explain the status mapping.

## Real-time Status Update

Use the update script to change capybara's status:

```bash
# Usage: ./update_status.sh <state> <detail> [progress] [ttl]

# Examples
./update_status.sh reading "Reading code..." 20 30
./update_status.sh writing "Writing feature..." 50 60
./update_status.sh responding "Replying to user..." 0 30
./update_status.sh executing "Running tests..." 80 120
./update_status.sh idle "Done" 100 30
```

Parameters:
- `state`: State name (see mapping table above)
- `detail`: Status description text
- `progress`: Progress percentage (0-100)
- `ttl`: Timeout in seconds, auto-returns to idle after timeout

## Example Response

```
Office UI is now running!

Preview: https://18791-xxx-preview.happycapy.ai

Capybara Status Areas:
- Reading/Searching -> Library
- Writing/Coding -> Desk
- Executing/Testing -> Server Room
- Responding/Meeting -> Meeting Room
- Idle/Resting -> Lounge

Click the "Demo Mode" button to see the complete workflow demonstration!
```

## Shutdown Office

```bash
lsof -ti:18791 | xargs kill -9 2>/dev/null
echo "Office closed"
```

## Repository

**GitHub:** https://github.com/AchengBusiness/happycapy-office-ui

**Author:** AchengBusiness

**License:** MIT
