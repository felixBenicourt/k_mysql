
# table_definitions.py


TABLES = {
    "project": {
        "id": "INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY",
        "name": "VARCHAR(255) NOT NULL"
    },
    "sequence": {
        "id": "INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY",
        "projectId": "INT(11) NOT NULL",
        "name": "VARCHAR(255) NOT NULL"
    },
    "shot": {
        "id": "INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY",
        "projectId": "INT(11) NOT NULL",
        "name": "VARCHAR(255) NOT NULL",
        "type": "VARCHAR(255) NOT NULL",
        "task": "VARCHAR(255) NOT NULL",
        "variation": "VARCHAR(255) NOT NULL",
        "sequenceId": "INT(11) NOT NULL",
        "version": "INT(11) NOT NULL",
        "filePath": "VARCHAR(255) NOT NULL",
        "cutIn": "INT(11) NOT NULL",
        "cutOut": "INT(11) NOT NULL"
    },
    "asset": {
        "id": "INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY",
        "projectId": "INT(11) NOT NULL",
        "name": "VARCHAR(255) NOT NULL",
        "type": "VARCHAR(255) NOT NULL",
        "task": "VARCHAR(500) DEFAULT NULL",
        "variation": "VARCHAR(500) DEFAULT NULL",
        "version": "INT(11) DEFAULT 1",
        "filePath": "VARCHAR(255) NOT NULL",
        "status": "ENUM('In Progress', 'Approved', 'Deprecated') DEFAULT 'In Progress'"
    }
}
