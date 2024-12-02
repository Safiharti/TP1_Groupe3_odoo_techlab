def amount_to_text(amount, lang='fr'):
    from num2words import num2words
    return num2words(amount, lang=lang)
