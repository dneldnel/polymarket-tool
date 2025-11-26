# Flask Web API Specification

## ADDED Requirements

### Requirement: Flask REST API Backend
**User Story:** As a developer, I need a Flask-based REST API that provides the same market data functionality as the current CLI tool, so that web applications can consume Polymarket data programmatically.

**The system SHALL** provide a Flask-based REST API that mirrors all CLI functionality through HTTP endpoints.

#### Scenario: Basic Market Data API
**Given** the Flask application is running
**When** a client makes a GET request to `/api/v1/markets`
**Then** the API returns a JSON response containing:
- Market list with pagination metadata
- Success status indicator
- Response timestamp
- Error handling for API failures

**When** the request includes query parameters like `limit=20&category=politics&active_only=true`
**Then** the API filters the response accordingly and returns only matching markets

#### Scenario: API Response Format Consistency
**Given** any API endpoint is called successfully
**When** the response is returned
**Then** it follows the standard format:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**And** error responses follow the format:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error description"
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Requirement: Market Data Endpoints
**User Story:** As a frontend developer, I need comprehensive API endpoints for accessing market data with filtering and pagination, so that I can build responsive user interfaces.

**The system SHALL** provide comprehensive REST endpoints for market data access with full filtering, pagination, and search capabilities.

#### Scenario: Market Listing with Pagination
**Given** the system has market data available
**When** a GET request is made to `/api/v1/markets?page=1&limit=50`
**Then** the response includes:
- Array of market objects for the requested page
- Pagination metadata (current page, total pages, total count)
- Sorting options by price, volume, or liquidity

#### Scenario: Market Filtering
**Given** markets exist across different categories
**When** filtering parameters are provided (`category=politics`, `active_only=true`)
**Then** the API returns only markets matching the specified criteria
**And** includes counts of filtered vs total markets

#### Scenario: Single Market Details
**Given** a valid market ID exists
**When** a GET request is made to `/api/v1/markets/{market_id}`
**Then** the API returns detailed information for that specific market
**Including** price history, token details, and trading statistics

#### Scenario: Market Categories
**Given** markets are categorized by type
**When** a GET request is made to `/api/v1/markets/categories`
**Then** the API returns a list of all available categories with market counts

### Requirement: API Configuration and Health
**User Story:** As a system administrator, I need configuration management and health check endpoints, so that I can monitor and maintain the web application.

**The system SHALL** provide configuration management and health monitoring endpoints for system administration.

#### Scenario: Configuration Management
**Given** the system has configurable parameters
**When** a GET request is made to `/api/v1/config`
**Then** the API returns current configuration values (excluding sensitive data)

**When** a PUT request is made to `/api/v1/config` with valid parameters
**Then** the configuration is updated and the new values are returned

#### Scenario: Health Monitoring
**Given** the Flask application is running
**When** a GET request is made to `/api/v1/health`
**Then** the API returns status information:
- Application status (healthy/unhealthy)
- External API connectivity status
- Response time metrics
- Last successful data fetch timestamp

### Requirement: CORS and API Security
**User Story:** As a frontend developer, I need proper CORS configuration and security measures, so that the web application can securely communicate with the API.

**The system SHALL** implement proper CORS configuration and security measures for safe API communication.

#### Scenario: Cross-Origin Requests
**Given** the frontend is served from a different origin than the API
**When** the frontend makes AJAX requests to the API
**Then** the API includes appropriate CORS headers
**And** preflight OPTIONS requests are handled correctly

#### Scenario: Rate Limiting
**Given** the API is publicly accessible
**When** a client makes too many requests within a time window
**Then** the API responds with HTTP 429 status
**And** includes rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining)

## MODIFIED Requirements

### Requirement: Market Data Fetching Logic
**Modification:** Refactor existing `PolymarketMarketFetcher` class to support web API usage while maintaining CLI functionality.

**The system SHALL** refactor the market data fetching logic to support both CLI and web interfaces with shared functionality.

#### Scenario: Shared Data Access Layer
**Given** both CLI and web applications need to access market data
**When** the `PolymarketMarketFetcher` is instantiated
**Then** it can be configured for either CLI or web usage
**And** maintains the same error handling and retry logic for both interfaces

#### Scenario: Web-Specific Data Processing
**Given** market data is requested via API
**When** processing the response
**Then** the data is formatted for JSON serialization
**And** includes web-specific metadata (pagination info, response timing)

### Requirement: Configuration Management
**Modification:** Extend current configuration system to support web application settings.

**The system SHALL** extend the configuration system to support both CLI and web-specific settings.

#### Scenario: Web Configuration Extensions
**Given** the application runs in web mode
**When** loading configuration
**Then** it includes web-specific settings:
- Flask application configuration
- CORS allowed origins
- Rate limiting parameters
- API endpoint versions

#### Scenario: Environment-Based Configuration
**Given** the application can run in different environments
**When** starting the web server
**Then** configuration adapts based on FLASK_ENV or NODE_ENV
**And** appropriate debug/production settings are applied

## REMOVED Requirements

### Requirement: CLI-Only Output Formats
**Removal:** Remove dependency on CLI-specific output formatting (tabulate tables) from core data fetching logic.

#### Scenario: Separated Presentation Logic
**Given** the application serves both CLI and web interfaces
**When** formatting market data for output
**Then** CLI formatting is handled by dedicated CLI functions
**And** web formatting is handled by API response serialization
**And** core data processing remains format-agnostic

### Requirement: Command-Line Argument Validation
**Removal:** Move CLI-specific argument validation out of core business logic.

#### Scenario: Interface-Specific Validation
**Given** different interfaces have different validation requirements
**When** validating input parameters
**Then** CLI validation handles command-line arguments
**And** API validation handles HTTP query parameters
**And** shared validation rules are centralized in utility functions