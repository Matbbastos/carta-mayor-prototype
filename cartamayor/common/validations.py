def is_valid_card_value(value: str) -> bool:
    if value in [
            "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "J", "Q", "K", "A"]:
        return True
    return False
