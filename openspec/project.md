# Project Context

## Purpose
This Python-based Polymarket data fetching tool retrieves prediction market data from the Polymarket CLOB API. The tool enables users to:
- List all available prediction markets with detailed information
- Filter markets by category (politics, sports, crypto, etc.)
- Export market data for analysis
- Monitor active vs inactive markets
- Access real-time pricing and liquidity data

## Tech Stack
- **Python 3.7+** - Core programming language
- **py-clob-client (>=0.28.0)** - Official Polymarket CLOB API client
- **python-dotenv (>=1.0.0)** - Environment variable management
- **requests (>=2.28.0)** - HTTP request handling
- **tabulate (>=0.9.0)** - Table formatting for CLI output
- **pandas (>=1.5.0)** - Data manipulation and analysis
- **rich (>=13.0.0)** - Rich text formatting and display

## Project Conventions

### Code Style
- **PEP 8 compliance** - Python standard style guide
- **Type hints** - Used for function parameters and return values
- **Docstrings** - Comprehensive function documentation in Chinese/English
- **Naming conventions**:
  - Variables: snake_case (e.g., `market_id`, `current_price`)
  - Functions: snake_case with descriptive names (e.g., `extract_market_info`)
  - Classes: PascalCase (e.g., `PolymarketMarketFetcher`)
  - Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_LIMIT`, `MAX_RETRIES`)

### Architecture Patterns
- **Single responsibility** - Separate modules for distinct functionality
  - `main.py` - CLI interface and argument parsing
  - `polymarket_markets.py` - Core market data fetching logic
  - `config.py` - Configuration management
- **Error handling** - Comprehensive try-catch blocks with graceful fallbacks
- **Data processing pipeline** - Fetch → Extract → Format → Display/Export
- **Configuration-driven** - Environment variables with CLI parameter overrides

### Testing Strategy
- **Debug scripts** - Specialized debugging utilities in root directory:
  - `debug_api.py` - API connection testing
  - `debug_edge_cases.py` - Edge case handling validation
  - `debug_extract_info.py` - Data extraction verification
  - `debug_full_api.py` - Full API response analysis
  - `debug_price_issue.py` - Price data problem diagnosis
- **Manual testing** - CLI parameter combinations and edge cases
- **Example validation** - `examples/basic_usage.py` for workflow verification

### Git Workflow
- **Main branch development** - Currently using `main` branch for all development
- **Commit style** - Descriptive commit messages with context
- **No formal branching** - Single-developer workflow with direct main commits
- **Version control** - Standard gitignore for Python projects

## Domain Context

### Polymarket Platform
- **Prediction markets** - Platforms for trading outcomes of future events
- **CLOB API** - Central Limit Order Book API for market data access
- **Market types** - Political elections, sports outcomes, cryptocurrency prices, cultural events
- **Key concepts**:
  - **Price** - Probability representation (0.0 to 1.0, displayed as dollars)
  - **Volume** - 24-hour trading volume in USD
  - **Liquidity** - Available liquidity for trading
  - **Active markets** - Currently tradable markets
  - **Settlement** - Market resolution and payout process

### Data Structure
- **Market ID** - Unique identifier for each market
- **Condition ID** - Oracle condition identifier
- **Token IDs** - Outcome token identifiers
- **Price fields** - Current price, best bid, best ask
- **Metadata** - Description, categories, end dates, active status

## Important Constraints

### Technical Constraints
- **Rate limiting** - Respect API rate limits (configurable via `MAX_RETRIES`)
- **Network reliability** - Handle connection timeouts and API unavailability
- **Data validation** - Robust parsing of potentially incomplete API responses
- **Memory efficiency** - Process large market lists without excessive memory usage

### Business Constraints
- **Educational use** - Tool designed for research and analysis purposes
- **No trading functionality** - Read-only data access, no order placement
- **Compliance** - Respect Polymarket's terms of service
- **Risk disclaimer** - Include investment risk warnings

### Regulatory Constraints
- **No financial advice** - Clear disclaimer about educational purpose only
- **Data privacy** - No collection of personal user information
- **API compliance** - Adherence to Polymarket API usage policies

## External Dependencies

### Critical Dependencies
- **Polymarket CLOB API** (`https://clob.polymarket.com`)
  - Primary data source for market information
  - Requires internet connectivity
  - May have rate limits and availability constraints

### Infrastructure Requirements
- **Python 3.7+ runtime** - Minimum Python version compatibility
- **Virtual environment** - Isolated dependency management (venv recommended)
- **Configuration files** - `.env` file for environment variables

### Optional Integrations
- **JSON export** - File system write permissions for data export
- **Logging** - Configurable log levels and output destinations
- **Custom API endpoints** - Configurable CLOB API URL for testing/alternative environments
