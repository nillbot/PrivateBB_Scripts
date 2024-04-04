## Portscanner

Install using script __(root required)__

```
curl https://raw.githubusercontent.com/nillbot/PrivateBB_Scripts/main/portscanner.py > /usr/local/bin/portscanner.py && \
ln -s /usr/local/bin/portscanner.py /usr/local/bin/portscan && \
chmod +x /usr/local/bin/portscan
```

then type `portscan` anywhere in the terminal to access

```
$ portscan -h
usage: portscan [-h] [-s] [-p] [-i] [-o] [-th] [-t]

Check ports for a list of hostnames or a single host

options:
  -h, --help           show this help message and exit
  -s , --host          Single host to scan
  -p , --port          Port number to check
  -i , --input_file    Path to the file containing the list of hosts to scan
  -o , --output_file   Path to the output file to export hosts with the port being open
  -th , --threads      Maximum number of threads to use while checking a list of hosts (Default: 10)
  -t , --timeout       Timeout for dismissing host if it doesn't respond (Default: 3)
```
## Subdomain finder

Install using script __(root required)__

```
curl https://raw.githubusercontent.com/nillbot/PrivateBB_Scripts/main/subscanner.sh > /usr/local/bin/subscanner.sh && \
ln -s /usr/local/bin/subscanner.sh /usr/local/bin/subscan && \
chmod +x /usr/local/bin/subscan
```

then type `subscan` anywhere in the terminal to access
```
$ subscan

Usage: /usr/local/bin/subscan <target_domain> [output_directory]

Examples:
  subscan example.com
  subscan example.com example_folder

If output_directory is not provided, it defaults to the target_domain name
```

You can also scan a list of domains using the following command

```
while IFS= read -r domain; do subscan $domain subscan_$domain; done < domains.txt
```

Or Run with parallel processing (threading)

```
< domains.txt xargs -n 1 -P 5 -I {} sh -c 'subscan {} subscan_{}'
```

`-P` defines the amount of max threads to use `5` in this case
