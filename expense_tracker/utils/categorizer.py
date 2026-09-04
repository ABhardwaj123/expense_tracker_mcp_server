CATEGORY_KEYWORDS = {
    "Food": ["dinner", "lunch", "breakfast", "restaurant", "grocery", "food", "coffee"],
    "Transport": ["uber", "taxi", "cab", "fuel", "petrol", "bus", "train", "flight"],
    "Bills": ["electricity", "rent", "wifi", "internet", "water"],
    "Entertainment": ["netflix", "movie", "spotify", "game", "concert"],
    "Shopping": ["amazon", "clothes", "shoes", "mall"],
    "Health": ["doctor", "medicine", "pharmacy", "hospital", "gym"],
}



def guess_category(note):

    if not note:
        return "Other"

    words = [word.lower() for word in note.split()]

    best_category = "Other"
    best_count = 0

    for category , keywords in CATEGORY_KEYWORDS.items():

        count = sum(1 for keyword in keywords if keyword in words)

        if count > best_count:
            best_count = count
            best_category = category

    return best_category
