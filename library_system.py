"""Library Fine and Book Renewal System module.

Tracks student book loans, calculates overdue fines, manages book renewals,
and persists loan records to JSON storage safely.
"""

import ast
import json
import operator
from datetime import datetime

# Module constants and shared state
LOANS = {}
FINE_PER_DAY = 2

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _safe_eval(node, variables):
    """Safely evaluate basic arithmetic expressions from AST nodes.

    Args:
        node: The AST node to evaluate.
        variables: Dictionary mapping variable names to numeric values.

    Returns:
        The evaluated numeric result.

    Raises:
        ValueError: If node contains unsupported operations or variables.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            left_val = _safe_eval(node.left, variables)
            right_val = _safe_eval(node.right, variables)
            return SAFE_OPERATORS[op_type](left_val, right_val)
        raise ValueError(f"Unsupported operator: {op_type}")
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](_safe_eval(node.operand, variables))
        raise ValueError(f"Unsupported unary operator: {op_type}")
    raise ValueError(f"Unsupported AST node: {type(node)}")


def add_book_loan(student_id, book_id, dates=None):
    """Record a book loan for a student.

    Args:
        student_id: Unique identifier for the student.
        book_id: Unique identifier or title of the book.
        dates: Optional list of timestamps tracking loan events.
    """
    if not student_id:
        return
    if dates is None:
        dates = []
    dates.append(str(datetime.now()))
    book_id_str = str(book_id)
    LOANS[student_id] = LOANS.get(student_id, []) + [book_id_str]
    print(
        f"{student_id} borrowed {book_id_str} "
        f"(loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Process return of a borrowed book.

    Args:
        student_id: Unique identifier for the student.
        book_id: Unique identifier of the book being returned.
    """
    try:
        book_id_str = str(book_id)
        LOANS[student_id].remove(book_id_str)
        if len(LOANS[student_id]) == 0:
            del LOANS[student_id]
    except (KeyError, ValueError):
        pass


def calculate_fine(days_overdue):
    """Calculate the fine based on number of days overdue.

    Args:
        days_overdue: Number of days the book is past due.

    Returns:
        Computed monetary fine.
    """
    return max(0, days_overdue) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Renew a borrowed book for a specified number of extra days.

    Args:
        student_id: Unique identifier for the student.
        book_id: Unique identifier of the book.
        extra_days: Additional days requested for loan extension.
    """
    global FINE_PER_DAY  # pylint: disable=global-statement
    if extra_days > 14:
        FINE_PER_DAY += 1
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


# Maintain alias for compatibility
renewBook = renew_book  # pylint: disable=invalid-name


def load_records(file="loans.json"):
    """Load loan records from a JSON file into memory.

    Args:
        file: Path to the JSON records file.
    """
    try:
        with open(file, "r", encoding="utf-8") as f_in:
            data = json.load(f_in)
            LOANS.clear()
            LOANS.update(data)
    except FileNotFoundError:
        LOANS.clear()


def save_records(file="loans.json"):
    """Save active loan records to a JSON file.

    Args:
        file: Path to the destination JSON file.
    """
    with open(file, "w", encoding="utf-8") as f_out:
        json.dump(LOANS, f_out, indent=2)


def fine_from_rule(rule, days):
    """Evaluate a dynamic fine rule safely using AST arithmetic parsing.

    Args:
        rule: String arithmetic expression (e.g., 'days * 2 + 10').
        days: Days overdue variable to inject into formula.

    Returns:
        Integer fine result.
    """
    parsed = ast.parse(rule, mode='eval')
    return int(_safe_eval(parsed.body, {"days": days}))


def print_report():
    """Print a summary report of all active student loans."""
    print("Loan Report")
    for student, book_list in LOANS.items():
        print(student, "->", book_list)


def main():
    """Execute standard demonstration workflow for the library system."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", "4521")
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    print("S102 owes:", calculate_fine(int(days)))
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
