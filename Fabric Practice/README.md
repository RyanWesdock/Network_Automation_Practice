Simple practice script using the fabric, invoke, and paramiko libraries to update firewalls on remote (Linux) hosts.
It works by loading host information from a csv file, setting up an SSH connection to each host, upadting a UFW firewall rule, and then closing the connection.
I tested this by running an SSH server on a Ubuntu Server VM through VirtualBox.

I wanted to emphasize error handling and security, so the script handles errors related to user input (files, sudo password). Rather than hardcoding any values,
the program reads an SSH key for the connection, prompts the user for the sudo password,and requires a separate file for hostnames, usernames, and SSH keys. 
It also informs the user if a host cannot be found or if the connection times out.
