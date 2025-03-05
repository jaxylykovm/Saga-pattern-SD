# Saga-pattern-SD
# Saga Pattern in a Single Microservice

## Overview
This project implements the **Saga Pattern** within a single microservice to handle an e-commerce checkout workflow. The workflow consists of three key services: **Payment, Inventory, and Shipping**. Each service supports **"do"** and **"compensate"** actions to ensure a rollback mechanism in case of failures, ensuring system consistency.

## Features
- **Saga-based transaction management**
- **Asynchronous processing with SQLAlchemy and Asyncpg**
- **Database persistence using PostgreSQL**
- **Automatic rollback if a step fails**
- **Logging for tracking order state changes**
- **Simple test script to verify the process**

## Installation & Setup
### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- Virtual environment (optional but recommended)

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/saga_checkout.git
   cd saga_checkout
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure the PostgreSQL database:
   ```sh
   psql -U your_user -d saga_checkout -f setup.sql
   ```
5. Initialize the database schema:
   ```sh
   python init_db.py
   ```

## Running the Saga Process
To run the checkout saga workflow, execute:
```sh
python test_saga.py
```
If successful, you should see logs indicating each step's execution and possible rollback in case of failure.

## Workflow Details
1. **Reserve inventory**
2. **Process payment**
3. **Ship order**
4. If any step fails, the previous steps will be **compensated**:
   - If payment fails → Inventory is released
   - If shipping fails → Payment is refunded & inventory is released

## Testing
You can manually insert test orders into the database:
```sql
INSERT INTO orders (id, status) VALUES (1, 'pending');
INSERT INTO inventory (id, stock, reserved) VALUES (101, 100, false);
```
Then rerun the saga process to observe transaction handling.

## Logging
Logs are stored in `saga.log` to track each step in the order process.

## Future Improvements
- Implement a message broker (e.g., Kafka) for event-driven transactions
- Add a REST API for external interactions
- Implement retry mechanisms for transient failures

## License
MIT License

