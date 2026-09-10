"""Password Strength Checker - local-only CLI utility."""

import getpass
import math
import re


def check_password(password: str) -> dict:
    """Return a strength score and feedback without storing the password."""
    if not password:
        return {"score": 0, "level": "Very Weak", "feedback": ["Password cannot be empty."]}

    score = 0
    feedback = []
    length = len(password)

    if length >= 8:
        score += 2
    else:
        feedback.append("Use at least 8 characters.")
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    checks = [
        (r"[a-z]", "Add lowercase letters."),
        (r"[A-Z]", "Add uppercase letters."),
        (r"\d", "Add numbers."),
        (r"[^A-Za-z0-9]", "Add special characters."),
    ]
    for pattern, message in checks:
        if re.search(pattern, password):
            score += 1
        else:
            feedback.append(message)

    if re.search(r"(.)\1\1", password):
        score -= 1
        feedback.append("Avoid repeated characters such as 'aaa' or '111'.")
    if re.search(r"1234|abcd|qwerty|password", password.lower()):
        score -= 2
        feedback.append("Avoid common patterns and dictionary-like passwords.")

    score = max(0, min(8, score))
    if score <= 2:
        level = "Very Weak"
    elif score <= 4:
        level = "Weak"
    elif score <= 6:
        level = "Good"
    else:
        level = "Strong"

    if not feedback and score >= 6:
        feedback.append("Great! This password has a strong mix of length and character types.")

    return {"score": score, "level": level, "feedback": feedback}


def main() -> None:
    print("🔐 Password Strength Checker")
    print("Your password is checked locally and is never stored.\n")
    password = getpass.getpass("Enter password: ")
    result = check_password(password)
    print(f"\nStrength: {result['level']} ({result['score']}/8)")
    print("Suggestions:")
    for item in result["feedback"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()
