from sqlalchemy.ext.hybrid import hybrid_property
from inventory import db

class Networkscope(db.Model):
    cidr = db.Column(db.String(50),primary_key=True)
    description = db.Column(db.String(2500), nullable=True)
    hosts = db.relationship('Linux_inventory',backref='hosts_cidr')

    def __repr__(self):
        return '%r' % (self.cidr)

class Linux_inventory(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    IPAddress = db.Column(db.String(50),nullable=False,unique=True)
    hostname = db.Column(db.String(100),nullable=False)
    operating_system = db.Column(db.String(500),nullable=True)
    uptime = db.Column(db.String(1500), nullable=True)
    application = db.Column(db.String(250), nullable=True)
    enviorment = db.Column(db.String(50),nullable=True)
    last_status_check = db.Column(db.String(50),nullable=False)
    last_time_checked = db.Column(db.DATETIME)
    networkscope_cidr = db.Column(db.String(50),db.ForeignKey('networkscope.cidr'))


    @hybrid_property
    def total_passed(self):
        total = [ x for x in Linux_inventory.query.all() if x.last_status_check == "Passed" ]
        return total

    @hybrid_property
    def total_failed(self):
        total = [ x for x in Linux_inventory.query.all() if x.last_status_check == "Failed" ]
        return total

    def __repr__(self):
        return '%r' % (self.hostname)
