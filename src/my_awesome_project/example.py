"""Example module for testing pre-commit hooks."""


def greet(name: str) -> str:
    """Return a greeting message.

    Args:
        name: The name to greet

    Returns:
        A greeting message
    """
    return f"Hello, {name}!"


def process_items(items: list[str]) -> str | None:
    """Process a list of items.

    Args:
        items: List of items to process

    Returns:
        Processed result or None if empty
    """
    if not items:
        return None
    return ", ".join(items)


if __name__ == "__main__":
    print(greet("World"))
    print(process_items(["apple", "banana", "cherry"]))
