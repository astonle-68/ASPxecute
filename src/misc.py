import re
import subprocess
import random
import os 
import hashlib
import hmac
import struct

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

def run_cmd(command)-> tuple[str|bytes, str|bytes, int]:
    """
        Run a command and returns the stdout, stderr, retcode
        obtained as a result of running the provided command
    """
    retcode = 0
    stdout = None
    stderr = None
    with subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE) as proc:
        stdout, stderr = proc.communicate()
        retcode = proc.returncode

    return stdout.decode('utf-8'), stderr.decode('utf-8'), retcode

def run_cmd_check_file(cmd: str, file: str):
    """Check if a file is created after running a cmd, if not, throw an exception"""
    stdout, stderr, retcode = run_cmd(cmd)
    
    # Verify launcher has been added 
    if not os.path.exists(file):
        print(f"[-] Failed to add Launcher.exe: `{cmd}` returned the following:")
        print(f"[-] Stdout:\n{stdout}")
        print(f"[-] Stderr:\n{stderr}")
        print(f"[-] Retcode:\n{retcode}")
        raise Exception(f"Command `{cmd}` failed to produce `{file}`")
    
def get_api_hash(value: str, key: int):
    """
    Generate an HMAC-MD5 hash of the supplied string using an Int64 as the key. 
    This is useful for unique hash based API lookups.
    
    Args:
        value (str): String to hash.
        key (int): 64-bit integer to initialize the keyed hash object 
                  (e.g. 0xabc or 0x1122334455667788).
    
    Returns:
        str: The computed MD5 hash value as uppercase hex string.
    """
    # Convert string to lowercase and encode as UTF-8
    data = value.lower().encode('utf-8')
    
    # Convert 64-bit integer to bytes (little-endian, matching C# BitConverter)
    key_bytes = struct.pack('<q', key)
    
    # Create HMAC-MD5 hash
    hash_obj = hmac.new(key_bytes, data, hashlib.md5)
    
    # Get the hash bytes and convert to uppercase hex string without separators
    return hash_obj.hexdigest().upper()