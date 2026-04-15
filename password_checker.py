import re

COMMON_WEAK_PASSWORDS = {
    "123456",
    "password",
    "123456789",
    "12345678",
    "12345",
    "qwerty",
    "abc123",
    "letmein",
    "welcome",
    "admin",
}

SPECIAL_CHAR_REGEX = re.compile(r"[!@#$%^&*()_+\-=[\]{};:'\\\"|,.<>/?`~]")


def evaluate_password_strength(password: str) -> tuple[str, list[str]]:
    """Evaluate a password and return a strength label plus suggestions."""
    password = password.strip()
    suggestions: list[str] = []

    if not password:
        return "Weak", ["Enter a password to evaluate."]

    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = bool(SPECIAL_CHAR_REGEX.search(password))
    is_common = password.lower() in COMMON_WEAK_PASSWORDS

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if has_lower and has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1
    if not is_common:
        score += 1

    if is_common or score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    if is_common:
        suggestions.append("Avoid very common passwords like 'password' or '123456'.")
    if length < 8:
        suggestions.append("Use at least 8 characters.")
    elif length < 12:
        suggestions.append("Longer passwords (12+ characters) are stronger.")
    if not has_lower or not has_upper:
        suggestions.append("Mix lowercase and uppercase letters.")
    if not has_digit:
        suggestions.append("Include digits (0-9).")
    if not has_special:
        suggestions.append("Add symbols like !, @, #, $, %, or &.")
    if has_lower and has_upper and has_digit and has_special and length >= 12 and not is_common:
        suggestions.append("Great job! Your password is strong. Keep it unique and private.")

    if not suggestions:
        suggestions.append("Your password is already strong. Avoid reusing it on other sites.")

    return strength, suggestions


def format_evaluation(password: str) -> str:
    strength, suggestions = evaluate_password_strength(password)
    lines = [f"Password strength: {strength}", "Suggestions:"]
    for suggestion in suggestions:
        lines.append(f"- {suggestion}")
    return "\n".join(lines)


def main() -> None:
    print("Password Strength Checker")
    print("Enter a password to evaluate. Press Enter to quit.")

    while True:
        try:
            password = input("Password: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if password == "":
            print("No password entered. Exiting.")
            break

        print()
        print(format_evaluation(password))
        print()


if __name__ == "__main__":
    main()
