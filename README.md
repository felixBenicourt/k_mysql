

# Database Wrapper Documentation

This project provides a Python wrapper for managing a relational database with the following tables: `project`, `sequence`, `shot`, and `asset`. The wrapper is designed to simplify database interactions by abstracting SQL commands into high-level Python operations.

---

## Table of Contents

- [Database Structure](#database-structure)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
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
