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
curl https://raw.githubusercontent.com/nillbot/PrivateBB_Scripts/main/subdomain_finder.sh > /usr/local/bin/subdomain_finder.sh && \
ln -s /usr/local/bin/subdomain_finder.sh /usr/local/bin/subscanner && \
chmod +x /usr/local/bin/subscanner
```

then type `subscanner` anywhere in the terminal to access. Usage:
```
subscanner example.com
```
