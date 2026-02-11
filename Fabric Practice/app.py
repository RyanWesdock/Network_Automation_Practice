from fabric import Connection
from invoke import FailingResponder, Failure
import csv
from paramiko.ssh_exception import NoValidConnectionsError
from getpass import getpass

def firewall_update(host_dict):
    """Takes a dictionary of a host IP address, username, and key,
    sets up an SSH connection to the host, and then updates the
    firewall settings for the host. It then closes the connection."""
    p = getpass("\nEnter password: ").rstrip() + '\n' # The newline simulates hitting the enter key
    d = Connection(host=host_dict["Host"],
                   user=host_dict["Username"],
                   connect_kwargs={'key_filename': host_dict["Key"]},
                   connect_timeout=3,
                   )
    sudo_pass = FailingResponder(
        pattern=r'\[sudo\] password',
        response=p,
        sentinel=r'Sorry.*')

    try:
        d.run("sudo ufw deny 21",
              pty=True,
              watchers=[sudo_pass]
              )
    except Failure:
        firewall_update(host_dict) # This enables a more graceful response to an incorrect password.
    d.close()


def host_update():
    """Iterates through a csv file to feed host information
    to the firewall update function."""
    while True:
        f = input("Enter file name: ")
        try:
            with open(f, "r") as c:
                cfile = csv.DictReader(c)
                for host in cfile:
                    try:
                        print(f"\nConnecting to Host at {host["Host"]}")
                        firewall_update(host)
                    except NoValidConnectionsError:
                        print(f"Unable to Connect -- Host at {host["Host"]} not found")
                    except TimeoutError:
                        print(f"Connection timeout to Host at {host["Host"]}")
            break
        except FileNotFoundError:
            print("File Not Found")

