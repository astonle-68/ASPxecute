import os
from src.cli import parse_args
from src.misc import banner, generate_random_word
from src.aspexecutor import ASPxecute

def main():
    banner()
    args = parse_args()

    shellcode = os.path.abspath(args.shellcode)
    classname = args.classname
    namespace = args.namespace
    extension = args.extension

    # Generate Class Name and NameSpace if it is none
    if (not classname):
        classname = generate_random_word()

    if (not namespace):
        namespace = generate_random_word()

    print("[+] Using shellcode file: ", shellcode)
    print("[+] Using class name:     ", classname)
    print("[+] Using namespace:      ", namespace)
    print("[+] Using extension:      ", extension)
    print()

    # Generate stuff
    aspexecute = ASPxecute(shellcode, namespace, classname, extension)
    aspexecute.validate()
    aspexecute.template()
    aspexecute.generate_payload()


if __name__ == "__main__":
    main()
