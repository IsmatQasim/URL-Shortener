import hashlib

# Base62 alphabet — 62 characters total
# a-z = 26, A-Z = 26, 0-9 = 10
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
BASE = len(ALPHABET)  # 62


def encode_base62(number: int) -> str:
    """
    Koi bhi number lo → Base62 string mein convert karo

    Example:
        encode_base62(12345) → "dnh"

    Kaise kaam karta hai:
        12345 ÷ 62 = 199 remainder 7   → ALPHABET[7]  = 'h'
          199 ÷ 62 = 3   remainder 13  → ALPHABET[13] = 'n'
            3 ÷ 62 = 0   remainder 3   → ALPHABET[3]  = 'd'
        Reverse karo → "dnh"
    """
    if number == 0:
        return ALPHABET[0]

    result = []
    while number > 0:
        remainder = number % BASE       # 62 se divide karo, remainder lo
        result.append(ALPHABET[remainder])  # Us index ka character lo
        number //= BASE                 # Number ko 62 se divide karo (integer)

    return "".join(reversed(result))    # Ulta karo — correct order milega


def url_to_short_id(original_url: str, attempt: int = 0) -> str:
    """
    URL lo → MD5 hash banao → Base62 encode karo → 6 char ID nikalo

    'attempt' parameter collision handling ke liye hai:
        - attempt=0: hash ke pehle 8 digits use karo
        - attempt=1: agley 8 digits use karo (agar collision hua)
        - attempt=2: aur agley 8 digits... aur aise hi

    Yeh real Bitly/TinyURL jaisa approach hai!
    """

    # Step 1: URL ka MD5 hash banao
    # MD5 ek 32-character hex string deta hai
    # Example: "https://google.com" → "8ffdefbdec956b595d257f0aaeefd623"
    url_with_salt = original_url + str(attempt)   # attempt milao taake har baar alag hash mile
    md5_hash = hashlib.md5(url_with_salt.encode()).hexdigest()

    # Step 2: Hash ke pehle 8 characters lo (hex mein)
    # "8ffdefbd" — yeh ek hex number hai
    chunk = md5_hash[attempt * 4: attempt * 4 + 8]

    # Step 3: Hex string ko integer mein convert karo
    # "8ffdefbd" → 2415853501 (decimal number)
    number = int(chunk, 16)

    # Step 4: Number ko Base62 mein encode karo
    # 2415853501 → "3mfHgK" (6 characters)
    short_id = encode_base62(number)

    # Step 5: Exactly 6 characters chahiye
    # Agar zyada hain → pehle 6 lo
    # Agar kam hain → aage '0' lagao (padding)
    return short_id[:6].ljust(6, '0')


def decode_base62(encoded: str) -> int:
    """
    Base62 string → original number wapas

    Example:
        decode_base62("dnh") → 12345

    (URL shortener mein direct use nahi hota,
     lekin samajhne ke liye aur interviews ke liye important hai)
    """
    number = 0
    for char in encoded:
        number = number * BASE + ALPHABET.index(char)
    return number