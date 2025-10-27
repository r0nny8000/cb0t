Code Style
==========

DocStrings and Comments
-----------------------
- If a function or method has no docstring, please generate a docstring whitin only one line and less than 160 characters.
- Do not document parameters.
- Do not genereate an Args and Returns section.
- Do not modify existing documentation. If there is documentation already present, leave it as is.
- Some special methods like __init__ do not require a docstring.

String Formating
----------------
- Use f-strings for string formatting. Avoid using the format() method or the % operator.
- Example: `f"Hello, {name}!"` instead of `"Hello, {}".format(name)` or `"Hello, %s" % name`.

Follow PEP 8 guidelines automatically
-------------------------------------
- Clear separation of concerns
- Maintainable and testable code structure

Tech Stack
----------------
- Python 3.12
- Azure Functions
- pytest for testing
- Kranken for HTTP requests

Security
----------------
- Never log sensitive data (API keys, passwords)
- Validate all user inputs
- Use environment variables for secrets

Error Handling
----------------
- Use specific exceptions, not bare except
- Log errors with context
