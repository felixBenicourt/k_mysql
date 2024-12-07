
# Database Wrapper Documentation

This project provides a Python wrapper for managing a relational database with the following tables: `project`, `sequence`, `shot`, and `asset`. The wrapper is designed to simplify database interactions by abstracting SQL commands into high-level Python operations.

---

## Table of Contents

- [Database Structure](#database-structure)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

---

## Database Structure

The database consists of the following tables:

### 1. **`project`**
| Field   | Type                              | Description               |
|---------|-----------------------------------|---------------------------|
| `id`    | INT(11) NOT NULL AUTO_INCREMENT   | Primary key               |
| `name`  | VARCHAR(255) NOT NULL            | Project name              |

### 2. **`sequence`**
| Field       | Type                              | Description               |
|-------------|-----------------------------------|---------------------------|
| `id`        | INT(11) UNSIGNED NOT NULL AUTO_INCREMENT | Primary key      |
| `projectId` | INT(11) NOT NULL                 | Foreign key to `project` |
| `name`      | VARCHAR(255) NOT NULL            | Sequence name            |

### 3. **`shot`**
| Field        | Type                              | Description               |
|--------------|-----------------------------------|---------------------------|
| `id`         | INT(11) NOT NULL AUTO_INCREMENT   | Primary key               |
| `projectId`  | INT(11) NOT NULL                 | Foreign key to `project` |
| `name`       | VARCHAR(255) NOT NULL            | Shot name                |
| `type`       | VARCHAR(255) NOT NULL            | Type of shot             |
| `task`       | VARCHAR(255) NOT NULL            | Task associated with shot |
| `variation`  | VARCHAR(255) NOT NULL            | Variation of the shot    |
| `sequenceId` | INT(11) NOT NULL                 | Foreign key to `sequence`|
| `version`    | INT(11) NOT NULL                 | Version number           |
| `cutIn`      | INT(11) NOT NULL                 | Start frame              |
| `cutOut`     | INT(11) NOT NULL                 | End frame                |

### 4. **`asset`**
| Field       | Type                              | Description               |
|-------------|-----------------------------------|---------------------------|
| `id`        | INT(11) NOT NULL AUTO_INCREMENT   | Primary key               |
| `projectId` | INT(11) NOT NULL                 | Foreign key to `project` |
| `name`      | VARCHAR(255) NOT NULL            | Asset name               |
| `type`      | VARCHAR(255) NOT NULL            | Type of asset            |
| `task`      | VARCHAR(500) DEFAULT NULL        | Task associated with asset|
| `variation` | VARCHAR(500) DEFAULT NULL        | Variation of asset       |
| `version`   | INT(11) DEFAULT 1                | Version number           |
| `status`    | ENUM('In Progress', 'Approved', 'Deprecated') DEFAULT 'In Progress' | Current status |

---

## Features

- **High-level abstraction:** Simplifies database interactions by encapsulating SQL operations.
- **CRUD Operations:** Easily manage projects, sequences, shots, and assets.
- **Relational Support:** Handles relationships between tables (e.g., `projectId` as a foreign key).

---

## Setup

### Prerequisites

1. Install Python (>= 3.8 recommended).
2. Install the required Python libraries:
   ```bash
   pip install mysql-connector-python
3. Use rez to create your custom management package with the alias.
    ```python
    name = "my_package"
    version = "1.0.0"
    author = "your name"

    description = ""

    build_command = False
    requires = []

    def commands():
        env.PATH.append(this.root)
        env.PATH.append("{root}\my_package")
        alias("my_file", "python {root}/my_package/my_file.py")
    ```
4. Execute your rez command
    ```bash
    rez env my_package -- my_file
    ```


## Usage
 ```python
 from k_mysql.mysql_wrapper import MySQLDatabase


 db_class = MySQLDatabase("localhost", "root", "", "home_db")

 db_class.setup_all_tables()

 db_class.insert_element(
     "project",
     {"name":"template"}
 )

 db_class.insert_element(
     "sequence",
     {"projectId":1,"name":"00003"}
 )

 db_class.insert_element(
     "asset",
     {"projectId":1,
     "name":"rocketGirl", 
     "type":"chr",
     "task":"mdl",
     "variation":"main",
     "version":1,
     "status":"Approved"}
 )

 db_class.insert_element(
     "shot",
     {"projectId":1,
     "name":"00000",
     "type":"shot",
     "task":"ani",
     "variation":"main",
     "sequenceId":0,
     "version":1}
 )

 assetsRktGrl = db_class.get_elements_by_name(
     table_name = "asset",
     name_column = "name",
     name_value = "rocketGirl"
 )


 filtered = db_class.filter_dicts(assetsRktGrl,"task","rig")
 latest = db_class.get_highest_value(filtered, "version")

 print(latest)

 db_class.disconnect()
 ```

## License
**MIT License**:

```text
MIT License

Copyright (c) felix benicourt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

