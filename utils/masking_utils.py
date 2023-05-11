import re

def mask_string(input_string):
 
    # Check input parameter
    if not isinstance(input_string, str):
        raise TypeError("Input parameter must be a string")

    # Check if input string is an email
    if re.match(r"[^@]+@[^@]+\.[^@]+", input_string):
        # Mask email address
        username, domain = input_string.split("@")
        num_chars_to_mask = max(0, len(username) - 4)
        if len(username) < 7:
            masked_username = username[0] + "x"*(len(username)-2) + username[-1]
        else:
            masked_username = username[:2] + "x"*(len(username)-4) + username[-2:]
        masked_email = masked_username + "@" + domain
    elif all(c.isdigit() or c == ' ' for c in input_string):
        # Mask all digits except last 4 digits
        masked_email = ''.join(['x' if c.isdigit() and i < len(input_string) - 4 else c for i, c in enumerate(input_string)])
    else:
        # Split the input string into words
        words = input_string.split()

        # Mask each word in the input string
        masked_words = []
        for word in words:
            # Determine number of characters to mask
            if len(word) < 7:
                num_chars_to_mask = max(0, len(word) - 2)
                masked_word = word[0] + "x"*num_chars_to_mask + word[-1]
            else:
                num_chars_to_mask = max(0, len(word) - 4)
                masked_word = word[:2] + "x"*num_chars_to_mask + word[-2:]

            masked_words.append(masked_word)

        # Join the masked words back into a string, preserving spaces between words
        masked_email = ' '.join(masked_words)

    return masked_email
