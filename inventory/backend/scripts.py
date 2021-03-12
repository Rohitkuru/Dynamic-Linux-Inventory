import netaddr
from scapy.all import *
import time
import threading
import paramiko


linux_host = []
lock = threading.Lock()
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def find_linux_hosts(ip_addr):
    ''' this function will use scapy to send packet to destination host and in case of valid response add that in inventory'''

    ssh_packet = IP(dst=str(ip_addr)) / TCP(dport=[22], flags="S")
    ssh_check_result = sr1(ssh_packet, timeout=1, verbose=False)
    if ssh_check_result:
        if ssh_check_result.getlayer(IP).ttl == 64:
            lock.acquire()
            linux_host.append({})
            linux_host[len(linux_host) - 1]["ip"] = ip_addr
            try:
                try:
                    hostname = socket.gethostbyaddr(ip_addr)
                    linux_host[len(linux_host) - 1]["hostname"] = hostname[0]
                except socket.herror as e:
                    linux_host[len(linux_host) - 1]["last_status"] = "FAILED"
                    linux_host[len(linux_host) - 1]["hostname"] = "UNKNOWN"
                for command in ["uptime", "cat /etc/redhat-release"]:
                    output = execute_command(command, ip_addr)
                    if output:
                        for line in output.readlines():
                            linux_host[len(linux_host) - 1][command] = line.rstrip("\r\n")

                client.close()
            finally:
                lock.release()


def execute_command(command,ip_addr):
    try:
        client.connect(ip_addr, port="22", username="rkurdukar", password="India@1", timeout=2)
        stdin, stdout, stderr = client.exec_command(command, get_pty=True, timeout=300)
        return stdout
    except paramiko.ssh_exception.BadAuthenticationType as e:
        linux_host[len(linux_host) - 1][command]  = "BadAuthenticationType"
        linux_host[len(linux_host) - 1]["last_status"] = "FAILED"
        logging.error(e)
    except paramiko.ssh_exception.AuthenticationException as e:
        linux_host[len(linux_host) - 1][command] = "AuthenticationFailed"
        linux_host[len(linux_host) - 1]["last_status"] = "FAILED"
        logging.error(e)

    except Exception as e:
        return e



def scan(range):

    logging.info("--------- Finding linux host from range {} -----------".format(range))
    try:

        range_obj = netaddr.IPNetwork(range)
        if len(list(range_obj.iter_hosts())) <= 512:
            host_list = range_obj.iter_hosts()
            threads = []
            t1 = time.time()
            for ip_addr in host_list:
                thread = threading.Thread(target=find_linux_hosts, args=[str(ip_addr)])
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
            logging.info("Total linux host found {}".format(len(linux_host)))
            logging.info("Total time taken {}".format(time.time() - t1))
        else:
            return "Too long range provided , please limit range till /23 only "


    except Exception as e:
        logging.error("[ERROR:] Exception occured {}".format(e))
        return e

    logging.info("------------- Scanning for hosts completed --------------- ")

    for each in linux_host:
        if "last_status" not in each:
            each['last_status'] = "PASSED"
        each['last_time_checked'] = datetime.now()

    return linux_host
