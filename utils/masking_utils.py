def mask_string(input_string, mask_status):
   

    # Check input parameter
    if not isinstance(input_string, str):
        raise TypeError("Input parameter must be a string")
    if mask_status=="masked":
    # Check if input string is a number with blanks in between
        if all(c.isdigit() or c == ' ' for c in input_string):
            # Mask all digits except last 4 digits
            masked_string = ''.join(['x' if c.isdigit() and i < len(input_string) - 4 else c for i, c in enumerate(input_string)])
        elif '@' in input_string:
            # Mask email addresses
            username, domain = input_string.split('@')
            
            # Mask username before @ symbol
            if len(username) <= 4:
                masked_username = username[0] + 'x'*(len(username)-1)
            elif len(username) <= 7:
                masked_username = username[0:2] + 'x'*(len(username)-4) + username[-2:]
            else:
                masked_username = username[:2] + 'x'*(len(username)-4) + username[-2:]

            # Mask domain after @ symbol
            if '.' in domain:
                domain_name, extension = domain.split('.')
                if len(domain_name) <= 4:
                    masked_domain_name = domain_name[0] + 'x'*(len(domain_name)-1)
                elif len(domain_name) <= 7:
                    masked_domain_name = domain_name[0:2] + 'x'*(len(domain_name)-4) + domain_name[-2:]
                else:
                    masked_domain_name = domain_name[:2] + 'x'*(len(domain_name)-4) + domain_name[-2:]

                masked_extension = extension[0] + 'x'*(len(extension)-1)
                masked_domain = masked_domain_name + '.' + masked_extension
            else:
                masked_domain = 'x'*len(domain)

            masked_string = masked_username + '@' + masked_domain
        else:
            # Split the input string into words
            words = input_string.split()

            # Mask each word in the input string
            masked_words = []
            for word in words:
                # Determine number of characters to mask
                num_chars_to_mask = max(0, len(word) - 4)

                # Mask characters with 'x', but show first and last 2 characters if word has more than 4 characters
                if word.isalpha() and len(word) <= 4:
                    masked_word = word[0] + 'x'*(len(word)-1)
                elif len(word) <= 7:
                    masked_word = word[0] + 'x'*(len(word)-2) + word[-1]
                else:
                    masked_word = word[:2] + 'x'*(len(word)-4) + word[-2:]

                masked_words.append(masked_word)

            # Join the masked words back into a string, preserving spaces between words
            masked_string = ' '.join(masked_words)

        
    elif mask_status=='redacted':
      masked_string='x'*5
    elif mask_status=='normal':
      masked_string=input_string
    return masked_string 
      

mask_string('rajesham','redacted')