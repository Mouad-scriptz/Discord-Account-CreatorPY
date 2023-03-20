# I know this can be better
import pkg_resources, os
installed = 0
uninstalled = 0
command = "pip install "
for lib in ['tls-client','requests','colorama','pytz','pyyaml','datetime']:
    try:
        dist = pkg_resources.get_distribution(lib)
        installed += 1
        command = command + lib + " "
    except pkg_resources.DistributionNotFound:
        uninstalled += 1
        command = command + lib + " "
command = command + " --upgrade"
print("(I) Installed libraries:",installed)
print("(I) Libraries to install:",uninstalled)
os.system(command)
print("(S) Installed all needed libraries, run main.py")
input("(E) Press ANY Key to exit.")