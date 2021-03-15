from inventory.backend.logger import logging
from inventory.models import Linux_inventory,Networkscope
from inventory import db


def add_record(linux_host,range):

    try:
        if not Networkscope.query.filter_by(cidr=range).first():
            cidr_record = Networkscope(cidr=range)
            db.session.add(cidr_record)
            db.session.commit()
            logging.info("Record has been added to database, record is {}".format(cidr_record))
        else:
            logging.info("CIDR {} already exist in database ".format(range))

        for each in linux_host:
            if not Linux_inventory.query.filter_by(IPAddress=each['ip']).first():
                host_record = Linux_inventory(IPAddress=each['ip'], hostname=each['hostname'],
                                    uptime=each['uptime'],
                                    operating_system=each['cat /etc/redhat-release'],
                                    last_time_checked=each['last_time_checked'], last_status_check=each['last_status'],
                                    networkscope_cidr=range)
                db.session.add(host_record)
                db.session.commit()
                logging.info("Record has been added in database , record is {} ".format(host_record))
            else:
               logging.info("Record already  in database .. {} , hence skipping ".format(each['ip']))

    except Exception as e:
        db.session.rollback()
        logging.error(" add_record operation failed , due to exception occured .. {}".format(e))