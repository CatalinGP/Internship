import re


def validate_cnp_length(func):
    def wrapper(cnp):
        if len(cnp) != 13:
            return "Marime CNP invalida"
        return func(cnp)

    return wrapper


def validate_cnp_format(func):
    def wrapper(cnp):
        if not re.match(r'^\d+$', cnp):
            return "CNP-ul contine caractere non-numerice"

        valid_length = re.match(r'^[1-8]\d{12}$', cnp)
        if not valid_length:
            return "Format CNP invalid"

        return func(cnp)

    return wrapper


def validate_cnp_checksum(func):
    def wrapper(cnp):
        components = [int(x) for x in cnp]
        weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
        total = sum(c * w for c, w in zip(components[:12], weights)) % 11
        expected_checksum = 1 if total == 10 else total
        if components[12] != expected_checksum:
            return "CNP checksum invalid"
        return func(cnp)

    return wrapper


@validate_cnp_length
@validate_cnp_format
@validate_cnp_checksum
def interpret_cnp(cnp):
    sex = "Barbat" if int(cnp[0]) in [1, 3, 5, 7] else "Femeie"
    birth_year = int(cnp[1:3])
    birth_month = int(cnp[3:5])
    birth_day = int(cnp[5:7])
    county_code = int(cnp[7:9])
    unique_sequence = int(cnp[9:12])

    return {
        "Sex": sex,
        "Anul": 1900 + birth_year if birth_year < 99 else 1800 + birth_year,
        "Luna": birth_month,
        "Ziua": birth_day,
        "Cod judet": county_code,
        "Secventa unica": unique_sequence,
        "CNP": cnp
    }


# Test the function with a valid CNP
valid_cnp = "1920823226711"
result = interpret_cnp(valid_cnp)
print(result)

# Test the function with an invalid CNP
invalid_cnp = "1234567890abc"
result = interpret_cnp(invalid_cnp)
print(result)
