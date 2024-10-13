import re
import math
import sys


def parse_polynomial(equation):
    """
    Parses a polynomial equation string and returns
    a dictionary of coefficients keyed by their power.

    Args:
        equation (str): The polynomial equation as a string
            (e.g., "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0").

    Returns:
        dict: A dictionary where keys are powers (int)
        and values are the summed coefficients (float).
    """
    # Remove all spaces from the equation for easier processing
    equation = equation.replace(" ", "")

    # Split the equation into left and right sides at the equals sign '='
    left_side, right_side = equation.split('=')

    # Move all terms to the left side by subtracting the right side terms
    # This avoids dealing with parentheses and keeps the equation linear
    equation = left_side + "-" + right_side

    # Replace any double negatives '--' with '+'
    equation = equation.replace('--', '+')

    # Parse terms using regex to match optional sign, coefficient,
    # optional '*', 'X^', and power
    regex_pattern = r'([+-]?)(\d*\.?\d+)?\*?X\^(\d+)'
    terms = re.findall(regex_pattern, equation)

    # Initialize a dictionary to hold coefficients, keyed by power
    coefs = {}
    for term in terms:
        sign_str, coef_str, power_str = term

        # If coefficient is missing (e.g., '+X^2'), it's implied to be '1'
        if coef_str == '':
            coef_str = '1'

        # If sign is missing, it's implied to be '+'
        sign = sign_str if sign_str else '+'

        # Combine sign and coefficient string, then convert to float
        coef = float(sign + coef_str)

        # Convert power string to integer
        power = int(power_str)

        # Sum the coefficients for like terms (same power)
        coefs[power] = coefs.get(power, 0) + coef

    return coefs


def format_coefficient(coef):
    """
    Formats a coefficient by converting it to an integer if it is equivalent
    to an integer, otherwise leaves it as a float.

    Args:
        coef (float): The coefficient to format.

    Returns:
        str: The formatted coefficient as a string.
    """
    if coef == int(coef):
        # If coefficient is a whole number, convert to integer string
        return str(int(coef))
    else:
        # If coefficient is a decimal, keep it as a float string
        return str(coef)


def reduced_form(coefs):
    """
    Creates the reduced form string of the polynomial from the coefficients
    dictionary.

    Args:
        coefs (dict): A dictionary where keys are powers and values are
            coefficients.

    Returns:
        str: The reduced form of the polynomial as a string
            (e.g., "4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0").
    """
    terms = []

    # Iterate over powers in ascending order to match expected output format
    for power in sorted(coefs.keys()):
        coef = coefs[power]

        # Skip terms with zero coefficient
        if coef == 0:
            continue

        # Determine the sign of the term based on the coefficient
        sign = "+" if coef > 0 else '-'

        # Format the coefficient (remove unnecessary decimal points)
        coef_str = format_coefficient(abs(coef))

        # Format the term string (e.g., "+ 4 * X^1")
        term = f"{sign} {coef_str} * X^{power}"

        # Add the term to the list of terms
        terms.append(term)

    # Join the terms into a single string, fix signs, and append '= 0'
    reduced = " ".join(terms).replace("+ -", "- ")\
        .lstrip("+ ").strip() + " = 0"
    return reduced


def solve_polynomial(coefs, degree):
    """
    Solves the polynomial equation based on its degree.

    Args:
        coefs (dict): A dictionary where keys are powers and values are
            coefficients.
        degree (int): The degree of the polynomial (highest power with non-zero
            coefficient).

    Returns:
        str: The solution(s) of the polynomial or an appropriate message if it
            cannot be solved.
    """
    if degree > 2:
        return (
            "The polynomial degree is strictly greater than 2, "
            "I can't solve."
        )
    elif degree == 2:
        return solve_quadratic(coefs)
    elif degree == 1:
        return solve_linear(coefs)
    elif degree == 0:
        # Constant equation ("5 = 0")
        if coefs.get(0, 0) == 0:
            return "Infinite solutions, since 0 = 0."
        else:
            return "No solution, the equation is inconsistent."
    else:
        # If the degree is negative or undefined, assume infinite solutions
        return "Infinite solutions, since 0 = 0."


def solve_linear(coefs):
    """
    Solves a linear equation of the form a * X^1 + b * X^0 = 0.

    Args:
        coefs (dict): A dictionary where keys are powers and values are
            coefficients.

    Returns:
        str: The solution of the linear equation or an appropriate message.
    """
    # Retrieve coefficients for X^1 and X^0 (default to 0 if not present)
    a = coefs.get(1, 0)
    b = coefs.get(0, 0)

    if a == 0:
        if b == 0:
            return "Infinite solutions, since 0 = 0."
        else:
            return "No solution, the equation is inconsistent."
    else:
        # Calculate the solution X = -b / a
        solution = -b / a
        return f"The solution is:\n{solution:.6f}"


def solve_quadratic(coefs):
    """
    Solves a quadratic equation of the form a * X^2 + b * X^1 + c * X^0 = 0
    using the quadratic formula.

    Args:
        coefs (dict): A dictionary where keys are powers and values are
            coefficients.

    Returns:
        str: The solutions of the quadratic equation or an appropriate message.
    """
    # Retrieve coefficients for X^2, X^1, and X^0 (default to 0 if not present)
    a = coefs.get(2, 0)
    b = coefs.get(1, 0)
    c = coefs.get(0, 0)

    # Calculate the discriminant: D = b^2 - 4ac
    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        # Two real and distinct solutions
        sqrt_discriminant = math.sqrt(discriminant)
        solution1 = (-b + sqrt_discriminant) / (2 * a)
        solution2 = (-b - sqrt_discriminant) / (2 * a)
        return (
            "Discriminant is strictly positive, the two solutions are:\n"
            f"{solution1:.6f}\n{solution2:.6f}"
        )
    elif discriminant == 0:
        # One real solution (double root)
        solution = -b / (2 * a)
        return f"Discriminant is zero, the solution is:\n{solution:.6f}"
    else:
        # Discriminant is negative; no real solutions
        return "Discriminant is strictly negative, no real solution."


def main():
    """
    The main function to execute the polynomial solver.
    It reads the equation from command-line arguments, parses it,
    reduces it, determines its degree, solves it, and prints the results.
    """
    # Check if the equation is provided as a command-line argument
    if len(sys.argv) < 2:
        print('Usage: python computorv1.py "equation"')
        sys.exit(1)

    # Read the equation from command-line arguments
    equation = sys.argv[1]

    # Parse the polynomial to get the coefficients
    coefs = parse_polynomial(equation)

    # Generate the reduced form of the polynomial
    reduced = reduced_form(coefs)
    print(f"Reduced form: {reduced}")

    # Determine the degree of the polynomial (highest power with a non-zero
    # coefficient)
    if coefs:
        degree = max(coefs.keys())
    else:
        degree = 0

    print(f"Polynomial degree: {degree}")

    # Solve the polynomial based on its degree and print the solution
    solution = solve_polynomial(coefs, degree)
    print(solution)


if __name__ == "__main__":
    main()
