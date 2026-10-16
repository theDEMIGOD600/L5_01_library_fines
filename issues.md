# Lab 5: Static Code Analysis — Known Issues Table

**Module Analyzed:** `library_system.py`  
**Tools Applied:** Bandit, Pylint, Flake8  
**Final Pylint Score:** 10.00 / 10  
**Bandit Vulnerabilities:** 0  
**Flake8 Style Violations:** 0  

---

## Identified Issues & Resolutions

| Issue | Tool | Severity / Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B307: Blacklist Call** | Bandit | Medium / Security | 45 | Use of `eval()` in `fine_from_rule()` allows arbitrary code execution and injection vulnerabilities. | Replaced `eval()` with a safe AST-based arithmetic expression parser (`ast.parse`) using pre-whitelisted operators. |
| **B110 / W0702 / E722** | Bandit / Pylint / Flake8 | Low / Bug | 21 | Bare `except: pass` in `return_book()` silently suppresses all exceptions (including KeyboardInterrupt/system errors). | Replaced bare except with explicit exception tuple `except (KeyError, ValueError): pass` to handle missing keys gracefully. |
| **W0102: Dangerous Default** | Pylint | Medium / Bug | 9 | Mutable default argument `dates=[]` in `add_book_loan()` shares the same list across subsequent calls, leaking state between students. | Changed default parameter to `dates=None` and dynamically initialized a new list `dates = []` inside the function. |
| **R1732 / W1514: Unmanaged Open** | Pylint | Medium / Resource Leak | 34, 40 | File operations (`open()`) in `load_records` and `save_records` did not use context managers or specify UTF-8 encoding. | Refactored file access using `with open(file, mode, encoding='utf-8') as f:` to guarantee proper descriptor closure. |
| **C0103: Invalid Name** | Pylint | Style / Convention | 27 | Function name `renewBook()` violated PEP 8 `snake_case` naming conventions. | Renamed function to `renew_book()`, maintaining a backwards-compatible reference. |
| **C0114 / C0116: Missing Docstrings** | Pylint | Convention / Maintainability | 1, 9, 16, 24, 27, 33, 39, 44, 47, 52 | Missing module and function docstrings explaining purpose, arguments, and return types. | Added comprehensive PEP 257 compliant docstrings to the module and all function definitions. |
| **F401: Unused Import** | Flake8 / Pylint | Low / Style | 2 | Module `os` was imported but never utilized anywhere in the code. | Removed `import os`. |
| **E501: Line Length Exceeded** | Flake8 | Style | 14, 31 | Multiple code lines exceeded the standard PEP 8 limit of 79 characters. | Reformatted multi-argument print calls and strings across multiple lines within 79 characters. |
| **E302 / E305: Blank Lines** | Flake8 | Style | 9, 16, 24, 27, 33, 39, 44, 47, 52, 68 | Insufficient blank lines separating top-level function definitions (expected 2 blank lines). | Added standard 2 blank lines between all top-level functions and classes. |
