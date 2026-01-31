---
name: database-skill
description: Implement database design and management skills including creating tables, writing migrations, and designing schemas.
---

# Database Skill

## Instructions

### 1. Database Setup
- Choose a relational database (PostgreSQL, MySQL) or NoSQL (MongoDB).
- Setup connection using environment variables.
- Test database connectivity.

### 2. Schema Design
- Identify entities and their relationships.
- Normalize tables to reduce redundancy.
- Define primary keys and foreign keys.
- Use appropriate data types for each field.
- Consider indexing for faster queries.

### 3. Create Tables
- Write SQL or migration scripts to create tables.
- Include constraints like `NOT NULL`, `UNIQUE`.
- Define relationships (1:1, 1:N, N:M).
- Ensure referential integrity.

### 4. Migrations
- Use a migration tool (Prisma, TypeORM, Sequelize, Alembic).
- Create initial migration for database setup.
- Apply migrations to the database.
- Track changes for future updates.

### 5. Data Seeding
- Add example data to test schema.
- Seed relationships (e.g., users and roles).
- Ensure seeding scripts are idempotent.

### 6. Best Practices
- Keep schema modular and easy to extend.
- Avoid redundant fields.
- Use migrations to safely update the database.
- Document schema for developers.

## Deliverables
- Database connection setup.
- Tables with proper schema design.
- Migration scripts for creating and updating tables.
- Seed scripts for example data.
- Documentation of schema and relationships.
