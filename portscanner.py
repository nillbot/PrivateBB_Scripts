#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import queue
import socket
import threading

def check_port(hostname, port=21, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((hostname, port))
        sock.close()
        print(f"\U0001F3F3\U0000FE0F Port \33[36m{port}\33[0m is \33[32mopen\33[0m on \33[33m{hostname}\33[0m")
        return True

    except socket.error:
        print(f"\U0001F6A9 Port \033[36m{port}\33[0m is \33[31mclosed\33[0m on \33[33m{hostname}\33[0m")
        return False

def check_port_for_hosts(input_file, output_file, port, max_threads=10, timeout=3):

    host_queue = queue.Queue()

    with open(input_file, 'r') as f:
        for hostname in f:
            hostname = hostname.strip() 
            if hostname:
                host_queue.put(hostname)

    threads = []

    def port_checker():
        while True:
            hostname = host_queue.get()
            if hostname is None:
                break
            if check_port(hostname, port, timeout):
                if output_file:
                    with open(output_file, "a") as f:
                        f.write(hostname + "\n")

            host_queue.task_done()

    for _ in range(max_threads):
        thread = threading.Thread(target=port_checker)
        thread.start()
        threads.append(thread)

    host_queue.join()

    for _ in range(max_threads):
        host_queue.put(None)

    for thread in threads:
        thread.join()

def scan_single_host(hostname, port, timeout):
    check_port(hostname, port, timeout)

def main(args):
    print()
    if args.input_file and args.host:
        print("Error: Unsupported arguments -i, --input_file and -s, --host. Run -h or --help for more info")
        return
    
    elif not args.input_file and not args.host:
        print("Error: You must specify a host or a file contaning hosts to scan")
        print()
        print("Examples:")
        print("  portscan -s 127.0.0.1 -p 22")
        print("  portscan -i hosts.txt -p 22 -o host_open_ssh.txt")
        print("  portscan -i hosts.txt -p 22 -o host_open_ssh.txt --timeout 5 --threads 20")
        return
    elif args.output_file and args.host:
        print("Error: Outputting to a file is only supported while checking a list of hosts. Run -h or --help for more info.")
        return
    elif args.host and not args.port:
        print("Error: You must specify a port to check")
        return
    elif args.input_file and not args.port:
        print("Error: You must specify a port to check")
        return

    if args.host and args.port:
        scan_single_host(args.host, args.port, args.timeout)
    else:
        check_port_for_hosts(args.input_file, args.output_file, args.port, args.threads, args.timeout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check ports for a list of hostnames or a single host")
    parser.add_argument("-s", "--host", type=str, metavar="", help="Single host to scan")
    parser.add_argument("-p", "--port", type=int, metavar="", help="Port number to check")
    parser.add_argument("-i", "--input_file", metavar="", type=str, help="Path to the file containing the list of hosts to scan")
    parser.add_argument("-o", "--output_file", type=str, metavar="", help="Path to the output file to export hosts with the port being open")
    parser.add_argument("-th", "--threads", type=int, default=10, metavar="", help="Maximum number of threads to use while checking a list of hosts (Default: 10)")
    parser.add_argument("-t", "--timeout", type=int, default=3, metavar="", help="Timeout for dismissing host if it doesn't respond (Default: 3)")
    args = parser.parse_args()
    main(args)
