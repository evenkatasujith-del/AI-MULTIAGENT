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