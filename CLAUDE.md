<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based Polymarket data fetching tool that retrieves prediction market data from the Polymarket CLOB API. The tool provides functionality to list markets, filter by categories, and export data for analysis.

## Core Architecture

### Main Components

- **main.py** - CLI entry point with argument parsing and market filtering logic
- **polymarket_markets.py** - Core market data fetching class using py-clob-client
- **config.py** - Configuration management with environment variable support
- **examples/** - Usage examples and code patterns

### Data Flow

1. **Initialization**: `PolymarketMarketFetcher` initializes CLOB client connection
2. **Data Retrieval**: Fetches market data via `client.get_markets()` or `client.get_simplified_markets()`
3. **Data Processing**: `extract_market_info()` parses raw API responses into structured format
4. **Display**: `display_markets_table()` formats data using tabulate library
5. **Export**: Optional JSON export functionality

### API Integration

The tool integrates with Polymarket's CLOB API through the `py-clob-client` library. Key API calls:
- `get_markets()` - Full market data with all fields
- `get_simplified_markets()` - Basic market information

## Development Commands

### Running the Application

```bash
# Basic usage - show first 50 markets
python main.py

# Show specific number of markets
python main.py --limit 20

# Show all markets
python main.py --all

# Filter by category
python main.py --category politics

# Show only active markets
python main.py --active-only

# Export data to JSON
python main.py --export-json

# Verbose logging
python main.py --verbose

# Show configuration
python main.py --show-config
```

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment (copy .env.example to .env)
cp .env.example .env

# Run examples
python examples/basic_usage.py
```

### Debugging Tools

The project includes several debugging scripts:
- `debug_api.py` - API connection debugging
- `debug_edge_cases.py` - Edge case handling
- `debug_extract_info.py` - Data extraction debugging
- `debug_price_issue.py` - Price data issue debugging
- `debug_full_api.py` - Full API response debugging

## Configuration

### Environment Variables (.env)

```bash
CLOB_API_URL=https://clob.polymarket.com
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
MAX_RETRIES=3
DEFAULT_LIMIT=50

# Optional authentication (not needed for public market data)
# PRIVATE_KEY=your_private_key_here
# CLOB_API_KEY=your_api_key_here
# CLOB_SECRET=your_secret_here
# CLOB_PASS_PHRASE=your_passphrase_here
```

### Configuration Management

The `config.py` module provides centralized configuration handling:
- Environment variable loading via python-dotenv
- Validation for required configuration
- Sensitive data masking in display output

## Key Dependencies

- **py-clob-client** (>=0.28.0) - Polymarket CLOB API client
- **requests** (>=2.28.0) - HTTP requests
- **python-dotenv** (>=1.0.0) - Environment variable management
- **tabulate** (>=0.9.0) - Table formatting
- **pandas** (>=1.5.0) - Data manipulation
- **rich** (>=13.0.0) - Rich text formatting

## Testing

No formal test suite is currently implemented. Testing is done through:
- Debug scripts in the root directory
- Example usage in `examples/basic_usage.py`
- Manual CLI testing with various parameters

## Code Patterns

### Error Handling

The code implements comprehensive error handling:
- Try-catch blocks around all API calls
- Graceful fallbacks for missing data
- Detailed logging for debugging
- Validation of configuration parameters

### Data Processing

- **Market Categories**: Inferred from text keywords in titles/descriptions
- **Price Handling**: Robust parsing with None checking and type conversion
- **Date Formatting**: ISO datetime parsing with fallback formatting
- **Status Determination**: Active/closed states derived from multiple boolean fields

### CLI Interface

Uses argparse with comprehensive help text and examples. Supports:
- Limiting results
- Category filtering
- Active market filtering
- JSON export
- Verbose logging
- Configuration display

## Common Tasks

When working with this codebase:

1. **Adding new filters**: Extend the filter functions in `main.py`
2. **Modifying output**: Update `display_markets_table()` method
3. **Adding API endpoints**: Extend `PolymarketMarketFetcher` class
4. **Configuration changes**: Modify `config.py` and update `.env.example`
5. **Debugging API issues**: Use the existing debug scripts as templates