# Goplaces Skill

Modern Google Places API (New) CLI for querying place information with human-friendly output or JSON format for scripting.

## Overview

The goplaces skill provides a command-line interface to the Google Places API (New), enabling text searches, place details, resolution, and reviews. It supports both human-readable output and JSON format for automation.

## Features

- **Text Search**: Search for places by keywords with filters
- **Place Details**: Get detailed information about specific places
- **Place Resolution**: Resolve location names to place IDs
- **Reviews**: Fetch reviews for places
- **Flexible Output**: Human-friendly by default, JSON for scripts
- **Advanced Filters**: Open now, minimum rating, radius, and more

## Installation

### Homebrew (macOS/Linux)

```bash
brew install steipete/tap/goplaces
```

## Configuration

Set your Google Places API key as an environment variable:

```bash
export GOOGLE_PLACES_API_KEY="your_api_key_here"
```

Optional configuration:
- `GOOGLE_PLACES_BASE_URL`: For testing or proxying requests

## Usage Examples

### Search for Places

```bash
# Basic search
goplaces search "coffee"

# Search with filters
goplaces search "coffee" --open-now --min-rating 4 --limit 5

# Search with location bias
goplaces search "pizza" --lat 40.8 --lng -73.9 --radius-m 3000

# Pagination
goplaces search "pizza" --page-token "NEXT_PAGE_TOKEN"
```

### Resolve Locations

```bash
# Resolve a location name to place IDs
goplaces resolve "Soho, London" --limit 5
```

### Get Place Details

```bash
# Get details for a place
goplaces details <place_id>

# Include reviews
goplaces details <place_id> --reviews
```

### JSON Output for Scripts

```bash
# Output in JSON format for parsing
goplaces search "sushi" --json
```

## Command Options

### Common Flags

- `--open-now`: Filter for currently open places
- `--min-rating <number>`: Minimum rating (0-5)
- `--limit <number>`: Maximum number of results
- `--lat <latitude>`: Latitude for location bias
- `--lng <longitude>`: Longitude for location bias
- `--radius-m <meters>`: Search radius in meters
- `--type <type>`: Filter by place type (only first value sent to API)
- `--json`: Output in JSON format
- `--no-color`: Disable ANSI color codes
- `--reviews`: Include reviews in place details

### Price Levels

Price levels range from 0 to 4:
- 0: Free
- 1: Inexpensive
- 2: Moderate
- 3: Expensive
- 4: Very expensive

## Environment Variables

- `GOOGLE_PLACES_API_KEY` (required): Your Google Places API key
- `GOOGLE_PLACES_BASE_URL` (optional): Custom base URL for API requests
- `NO_COLOR`: Set to disable color output

## Notes

- The `--type` filter only sends the first value to the API (API limitation)
- Use `--no-color` or set `NO_COLOR` environment variable to disable ANSI colors
- Price levels follow Google's standard 0-4 scale

## Requirements

- Google Places API key with Places API (New) enabled
- goplaces CLI installed via Homebrew

## Links

- **GitHub Repository**: https://github.com/steipete/goplaces
- **Original Skill Source**: https://github.com/openclaw/skills/tree/main/skills/steipete/goplaces

## License

This skill is provided by steipete. Please refer to the original repository for license information.
