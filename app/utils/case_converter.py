
def camel_case_to_snake_case(input_str : str) -> str:
    chars = []
    for c_idx, char in enumerate(input_str):
        if char.isupper() and c_idx > 0:
            if (c_idx != (len(input_str) - 3)) and (input_str[c_idx - 1:c_idx + 2] == input_str[c_idx - 1:c_idx + 2].upper()):
                pass
            else:
                chars.append('_')

        chars.append(char.lower())    
    return "".join(chars)

