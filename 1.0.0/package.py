
name = "k_mysql"
version = "1.0.0"
authors = ["Felix Benicourt"]

requires = ["python-3.10", "mysql_connector_python"]

def commands():
    env.PYTHONPATH.append(this.root)
    env.PYTHONPATH.append("{root}/k_mysql")
    env.PATH.append(this.root)
    env.PATH.append("{root}/k_mysql")