# Qt MCP Plugin Testing

## 🤖 AI-First Testing

**Let your AI assistant handle testing!** Simply ask:

```
Test the Qt MCP Plugin and verify it's working correctly
```

```
Run comprehensive tests to ensure both HTTP and TCP MCP protocols work
```

```
Debug any test failures and fix the plugin
```

## Quick Test Commands

```bash
# Run all tests (recommended)
python test_suite.py

# Verbose output for debugging
python test_suite.py --verbose

# Test specific protocols
python test_suite.py --http-only    # HTTP MCP only
python test_suite.py --tcp-only     # TCP MCP only

# Retry logic for unstable environments
python test_suite.py --iterative
```

## What Gets Tested

✅ **Server Connectivity** - Port 3001 accessibility  
✅ **TCP MCP Protocol** - Initialize, tools list, JSON-RPC validation  
✅ **HTTP MCP Protocol** - Server info, POST requests, CORS support  
✅ **Protocol Detection** - Automatic HTTP vs TCP detection  
✅ **Plugin Version** - Version verification and identification  

## Expected Results

```
Results: 10/10 tests passed
✓ All tests passed! MCP server is working correctly with both HTTP and TCP protocols.
```

## AI-Driven Testing Workflow

1. **Build & Install** - Ask AI to build and install the plugin
2. **Run Tests** - Ask AI to run the test suite
3. **Fix Issues** - If tests fail, ask AI to debug and fix
4. **Verify** - Ask AI to re-run tests until all pass

## Common Issues (Let AI Fix)

**Connection failures?** AI can check Qt Creator is running and plugin is loaded

**HTTP test failures?** AI can verify network settings and HTTP parser

**Platform issues?** AI can handle Windows PowerShell, macOS paths, Linux dependencies

## Integration

Tests run automatically during the build process via `build.py` - no manual intervention needed when using AI-assisted development.

**Need help?** Ask your AI assistant - testing is fully automated and designed for AI-assisted debugging.
