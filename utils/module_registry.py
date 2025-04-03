from modules.email_module import EmailModule
from modules.username_module import UsernameModule
from modules.domain_module import DomainModule
from modules.ip_module import IPModule
from modules.phone_module import PhoneModule
from modules.address_module import AddressModule
from modules.realname_module import RealNameModule

def get_modules_for_target(target):
    modules = []
    if target.startswith("email:"):
        mod = EmailModule()
        if mod.enabled:
            modules.append(mod)
        else:
            print("[!] EmailModule disabled (missing config).")
    elif target.startswith("username:"):
        mod = UsernameModule()
        if mod.enabled:
            modules.append(mod)
        else:
            print("[!] UsernameModule disabled (missing config).")
    elif target.startswith("domain:"):
        mod = DomainModule()
        if mod.enabled:
            modules.append(mod)
        else:
            print("[!] DomainModule disabled (missing config).")
    elif target.startswith("ip:"):
        mod = IPModule()
        if mod.enabled:
            modules.append(mod)
        else:
            print("[!] IPModule disabled (missing config).")
    elif target.startswith("phone:"):
        mod = PhoneModule()
        if mod.enabled:
            modules.append(mod)
        else:
            print("[!] PhoneModule disabled (missing config).")
    elif target.startswith("address:"):
        mod = AddressModule()
        if mod.enabled:
            modules.append(mod)
        else:
            print("[!] AddressModule disabled (missing config).")
    elif target.startswith("realname:"):
        mod = RealNameModule()
        if mod.enabled:
            modules.append(mod)
        else:
            print("[!] RealNameModule disabled (missing config).")
    return modules
