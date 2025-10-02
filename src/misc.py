import re
import random

def banner():
    print(r"""
    ___   _____ ____                       __     
   /   | / ___// __ \_  _____  _______  __/ /____ 
  / /| | \__ \/ /_/ / |/_/ _ \/ ___/ / / / __/ _ \
 / ___ |___/ / ____/>  </  __/ /__/ /_/ / /_/  __/
/_/  |_/____/_/   /_/|_|\___/\___/\__,_/\__/\___/ 

 "ASPNet is dead, Long live the ASPNET Compiler"      
                                - @whokilleddb
""")
    
def generate_random_word():
    """Generate a random compound word by combining two words."""
    # List of common English words to combine
    words = [
        "sun", "moon", "star", "fire", "water", "earth", "wind", "light",
        "dark", "blue", "red", "green", "stone", "wood", "silver", "gold",
        "snow", "rain", "thunder", "storm", "cloud", "sky", "bird", "fish",
        "tree", "flower", "mountain", "river", "ocean", "forest", "garden",
        "night", "day", "shadow", "dream", "heart", "soul", "spirit", "mind",
        "dragon", "wolf", "bear", "eagle", "lion", "tiger", "fox", "snake",
        "sword", "shield", "bow", "arrow", "blade", "hammer", "crown", "ring",
        "book", "song", "tale", "magic", "crystal", "frost", "flame", "dust"
    ]
    word1 = random.choice(words)
    word2 = random.choice(words)
    
    # Ensure we don't combine the same word twice
    while word2 == word1:
        word2 = random.choice(words)
    
    return word1 + word2


def is_valid_csharp_classname(name):
    """
    Check if a string is a valid C# class name.
    
    C# class name rules:
    1. Must start with a letter (a-z, A-Z) or underscore (_)
    2. Can contain letters, digits (0-9), and underscores
    3. Cannot be a C# keyword
    4. Cannot be empty or None
    5. Can start with @ to use keywords as identifiers (verbatim identifier)
    
    Args:
        name (str): The string to validate
        
    Returns:
        bool: True if valid, False otherwise

    ^ Yes This is clanker code
    """
    
    # C# keywords that cannot be used as class names
    csharp_keywords = {
        'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch',
        'char', 'checked', 'class', 'const', 'continue', 'decimal', 'default',
        'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit',
        'extern', 'false', 'finally', 'fixed', 'float', 'for', 'foreach',
        'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal',
        'is', 'lock', 'long', 'namespace', 'new', 'null', 'object',
        'operator', 'out', 'override', 'params', 'private', 'protected',
        'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short',
        'sizeof', 'stackalloc', 'static', 'string', 'struct', 'switch',
        'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong',
        'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void',
        'volatile', 'while'
    }
    
    # Check if name is None or empty
    if not name or not isinstance(name, str):
        return False
    
    # Handle verbatim identifier (starts with @)
    if name.startswith('@'):
        # Remove @ and validate the rest
        name = name[1:]
        # Verbatim identifiers can use keywords
        if not name:
            return False
    else:
        # Check if it's a keyword (case-sensitive)
        if name in csharp_keywords:
            return False
    
    # Check if name matches valid C# identifier pattern
    # Must start with letter or underscore, followed by letters, digits, or underscores
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    
    if not re.match(pattern, name):
        return False
    
    return True