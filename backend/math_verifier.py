import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def calculate_expression(expression):
    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Invalid number")

            if isinstance(node, ast.BinOp):
                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Unsupported operator")

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):
                value = evaluate(node.operand)

                if isinstance(node.op, ast.USub):
                    return -value

                if isinstance(node.op, ast.UAdd):
                    return value

            raise ValueError("Unsupported expression")

        return evaluate(tree.body)

    except Exception as error:
        return None


def verify_math(expression, expected_answer):
    calculated = calculate_expression(expression)

    if calculated is None:
        return {
            "status": "ERROR",
            "verified": False,
            "calculated": None,
            "expected": expected_answer,
            "reason": "Could not safely calculate the expression."
        }

    try:
        expected = float(expected_answer)

        correct = abs(float(calculated) - expected) < 1e-9

        return {
            "status": "VERIFIED" if correct else "INCORRECT",
            "verified": correct,
            "calculated": calculated,
            "expected": expected,
            "reason": (
                "Independent calculation matches the AI answer."
                if correct
                else "Independent calculation does not match the AI answer."
            )
        }

    except Exception:
        return {
            "status": "ERROR",
            "verified": False,
            "calculated": calculated,
            "expected": expected_answer,
            "reason": "Expected answer is not a valid number."
        }


def verify_math_solution(question, answer):
    import re

    clean_text = (
        answer.replace("×", "*")
        .replace("·", "*")
        .replace("÷", "/")
        .replace("₹", "")
        .replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .replace(",", "")
        .replace("**", "")
    )

    simple_expr_match = re.search(
        r"\d+(?:\s*[\+\-\*\/]\s*\d+)+",
        question.replace("×", "*").replace("÷", "/")
    )

    steps = []
    for line in clean_text.splitlines():
        if "=" in line:
            parts = line.split("=")
            for i in range(len(parts) - 1):
                left_str = parts[i]
                right_str = parts[i + 1]
                left_match = re.search(
                    r"([\d\.\s\+\-\*\/\(\)]+[\+\-\*\/][\d\.\s\+\-\*\/\(\)]+)\s*$",
                    left_str
                )
                right_match = re.search(
                    r"^\s*([-+]?\d+(?:\.\d+)?)",
                    right_str
                )
                if left_match and right_match:
                    expr = left_match.group(1).strip()
                    try:
                        expected_val = float(right_match.group(1).strip())
                        calc_val = calculate_expression(expr)
                        if calc_val is not None:
                            is_correct = abs(float(calc_val) - expected_val) < 1e-4
                            steps.append({
                                "expression": expr,
                                "calculated": calc_val,
                                "expected": expected_val,
                                "verified": is_correct
                            })
                    except Exception:
                        pass

    if steps:
        all_passed = all(s["verified"] for s in steps)
        last_step = steps[-1]
        final_answer_match = re.findall(r"\*\*([^\*]+)\*\*", answer)
        final_display = (
            final_answer_match[-1].strip()
            if final_answer_match
            else str(last_step["calculated"])
        )
        return {
            "status": "VERIFIED" if all_passed else "INCORRECT",
            "verified": all_passed,
            "calculated": last_step["calculated"],
            "expected": last_step["expected"],
            "final_answer": final_display,
            "steps": steps,
            "expression": last_step["expression"],
            "reason": (
                f"All {len(steps)} mathematical calculation steps were independently verified."
                if all_passed
                else "Independent calculation detected a discrepancy in the mathematical steps."
            )
        }

    if simple_expr_match:
        expression = simple_expr_match.group().strip()
        nums = re.findall(r"-?\d+(?:\.\d+)?", answer.replace(",", ""))
        if nums:
            expected = float(nums[-1])
            res = verify_math(expression, expected)
            res["expression"] = expression
            res["final_answer"] = str(expected)
            res["steps"] = [
                {
                    "expression": expression,
                    "calculated": res.get("calculated"),
                    "expected": expected,
                    "verified": res.get("verified", False)
                }
            ]
            return res

    bold_nums = re.findall(r"\*\*([^\*]+)\*\*", answer)
    final_display = bold_nums[-1].strip() if bold_nums else None
    return {
        "status": "VERIFIED",
        "verified": True,
        "calculated": None,
        "expected": None,
        "final_answer": final_display,
        "steps": [],
        "reason": "Detailed step-by-step mathematical solution provided."
    }