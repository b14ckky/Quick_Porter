import argparse
import os
import socket
import sys
import threading
import subprocess
from colorama import Fore
from termcolor import colored
import random

rainbow = ['red', 'green', 'green', 'blue', 'magenta', 'cyan']
r0 = random.randint(0, 5)
r1 = random.randint(0, 5)
r2 = random.randint(0, 5)
r3 = random.randint(0, 5)
r4 = random.randint(0, 5)

print(colored("\t┌────────────────────────────────────┐", rainbow[r0]))
print(colored("\t│ ╔═╗ ┬ ┬┬┌─┐┬┌─  ╔═╗┌─┐┬─┐┌┬┐┌─┐┬─┐ │", rainbow[r1]))
print(colored("\t│ ║═╬╗│ │││  ├┴┐  ╠═╝│ │├┬┘ │ ├┤ ├┬┘ │", rainbow[r2]))
print(colored("\t│ ╚═╝╚└─┘┴└─┘┴ ┴  ╩  └─┘┴└─ ┴ └─┘┴└─ │", rainbow[r3]))
print(colored("\t└──────────────0xb14cky──────────────┘", rainbow[r4]))

parser = argparse.ArgumentParser(
    description="A Fast Port Scanner Script !!",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=47)
)
parser.add_argument("-d", "--domain", help="Domain Name You Want to Scan", type=str)
parser.add_argument("-p", "--port", help="Any Specific Port", type=int)
parser.add_argument("-sp", "--start_port", help="Starting Port Number", type=int)
parser.add_argument("-ep", "--end_port", help="Ending Port Number", type=int)
# parser.add_argument('--thread', help="Number of Threads", type=int)
# parser.add_argument('--max_thread', help="At Maximum Threads", type=bool)
parser.add_argument("-o", "--output", help="Saving Output In Another File", type=str)
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if args.output:
    ip = socket.gethostbyname(args.domain)
    f = open(f'{args.output}', 'w')
    f.write("\t--------------------------------------\n")
    f.write("\t Victim IP :")
    f.write(ip)
    f.write("\n")
    f.write("\t Victim Domain :")
    f.write(args.domain)
    f.write("\n")
    f.write("\t--------------------------------------\n")
    f.write("\n\tPORT\t\tSTATE\t\tSERVICE\n")


def scan(port):
    s = socket.socket()
    s.settimeout(5)
    result = s.connect_ex((args.domain, port))

    if result == 0:
        mycmd = subprocess.getoutput(f'getent services {port} | cut -d " " -f 1')
        if mycmd != "":
            data = f"\t{port}\t\tOPEN\t\t{mycmd}"
            print(data)
            if args.output:
                f.write(f"\t{port}\t\tOPEN\t\t{mycmd}\n")
    s.close()


ip = socket.gethostbyname(args.domain)
print("\n")
print(Fore.RED, "\t--------------------------------------", Fore.RESET)
print("\t Victim IP :", Fore.RED, ip, Fore.RESET)
print("\t Victim Domain :", Fore.RED, args.domain, Fore.RESET)
print(Fore.RED, "\t--------------------------------------\n", Fore.RESET)
print(Fore.CYAN, "\n\tPORT\t\tSTATE\t\tSERVICE", Fore.RESET)

threads = []

if args.port:
    t = threading.Thread(target=scan, args=(args.port,))
    t.start()


elif args.start_port and args.end_port:
    for i in range(args.start_port, args.end_port + 1):
        t = threading.Thread(target=scan, args=(i,))
        t.start()
        threads.append(t)

    for item in threads:
        item.join()
