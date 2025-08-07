# Azure Functions Modular Architecture Refactoring

## Overview
This document describes the refactoring of the Azure Functions application from a monolithic structure to a modular, maintainable architecture.

## What Was Done

### 1. Created Modular Directory Structure
```
cb0t/
├── function_app.py          # Main entry point
├── routes/
│   ├── __init__.py
│   ├── index.py            # Index route handler
│   ├── ticker.py           # Ticker-related HTTP routes
│   ├── balance.py          # Balance-related HTTP routes
│   └── env.py              # Environment-related HTTP routes
├── services/
│   ├── __init__.py
│   ├── cost_basis.py       # Cost basis calculation logic
│   └── trading.py          # Trading and accumulation logic
├── timers/
│   ├── __init__.py
│   └── accumulate.py       # Timer-triggered functions
└── utils/
    ├── __init__.py
    ├── html_renderer.py     # HTML rendering utilities
    └── kraken_client.py     # Kraken API client configuration
```

### 2. Separated Concerns
- **Routes**: Handle HTTP requests and responses
- **Services**: Contain business logic (cost basis calculation, trading)
- **Timers**: Handle scheduled tasks
- **Utils**: Shared utilities (HTML rendering, API clients)

### 3. Maintained Functionality
- All existing HTTP routes work exactly as before
- Timer-triggered accumulation functions remain functional
- All tests pass without modification
- Code follows existing style guidelines

### 4. Benefits Achieved
- **Easier Testing**: Each module can be tested independently
- **Better Maintainability**: Changes to one function don't affect others
- **Clearer Dependencies**: Import structure shows relationships
- **Scalability**: Easy to add new routes or services
- **Reusable Code**: Services can be shared across multiple routes

### 5. Key Files Created

#### Main Entry Point (`function_app.py`)
- Registers all HTTP routes and timer triggers
- Clean, minimal configuration

#### Routes Module
- `index.py`: Main landing page
- `ticker.py`: Kraken ticker information
- `balance.py`: Account balance with P&L calculation
- `env.py`: Environment information

#### Services Module
- `cost_basis.py`: Calculates cost basis from trade history
- `trading.py`: Handles cryptocurrency accumulation logic

#### Utils Module
- `html_renderer.py`: Jinja2 template rendering
- `kraken_client.py`: Kraken API client setup

#### Timers Module
- `accumulate.py`: Periodic cryptocurrency accumulation

### 6. Migration Verification
- All imports work correctly
- Poetry environment compatibility maintained
- All 8 existing tests pass
- Code follows PEP 8 and project style guidelines

### 7. Folder Rename (Updated)
- Renamed `cb0t/` folder to `assets/` for better semantic naming
- Updated all imports throughout the project:
  - `from cb0t.asset import Asset` → `from assets.asset import Asset`
  - `from cb0t.asset_pairs import ...` → `from assets.asset_pairs import ...`
  - `import cb0t.engine` → `import assets.engine`
- Updated references in notebooks and test files
- All tests continue to pass after the rename

## Next Steps
1. Consider adding integration tests for the new modular structure
2. Add type hints to service functions
3. Consider adding error handling middleware
4. Document API endpoints and service contracts

The refactoring is complete and the application is ready for production use with improved maintainability and testability.
