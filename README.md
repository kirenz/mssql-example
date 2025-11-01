# SQL Server Connection Example

Use this repository to learn how to establish a Python connection against Microsoft SQL Server with the help of `uv`. 

You need to have uv installed on your machine (see [this repo](https://github.com/kirenz/uv-setup) for installation instructions).

## Step-by-step instructions

If you are on macOS, open the built-in **Terminal** app. On Windows, open **Git Bash**. 


1. Clone the repository  

   ```bash
   git clone https://github.com/kirenz/mssql-example.git
   ```
   Change into the repository folder
   ```bash
   cd mssql-example
   ```

2. Sync the Python environment defined in `pyproject.toml`  

   ```bash
   uv sync
   ```

   This installs all required packages in an isolated environment managed by `uv`.

3. Prepare your environment variables (this will copy the example file and create a new `.env` file)  

   ```bash
   cp .env.example .env
   ```


4. Open VS Code in the current folder

   ```bash
   code .
   ```
   Open the new `.env` file and replace the placeholder values with the SQL Server hostname, database, username, password, driver, and any TLS requirements provided by your instructor.

5. Test the SQL example script (you may use the integrated terminal in VS Code or your previous terminal window)  

   ```bash
   uv run python sql_example.py
   ```
   The script prints the SQL Server version and the top rows of the sample query if the connection succeeds.

6. Explore further  

   Update the SQL statement inside `sql_example.py` to work with tables you have access to, then rerun the command above.

7. Show the database schema  

   If you already connected to SQL Server with the VS Code **SQL Server** extension, open `sql/show_schema.sql`, click the **Run** button (▶️) in the editor toolbar and select your database connection. The extension executes the script and displays every table, column, data type, and nullability flag in the Results panel.

## Files

- `sql_example.py` – minimal script that loads environment variables, builds the ODBC connection string, and executes a sample query with `pandas`.

- `.env.example` – template with placeholders for your connection parameters. 

- `pyproject.toml` – dependency definition for `uv sync`. Don't edit this file directly; use `uv add <package>` to add new packages.

- `sql/show_schema.sql` – SQL script that retrieves the database schema information from the system catalog views.

## Python packages used

- `pyodbc` – provides the ODBC driver bindings that let Python talk to Microsoft SQL Server.
- `sqlalchemy` – builds the connection engine atop the ODBC driver and offers a composable SQL toolkit.
- `pandas` – turns query results into DataFrames so you can inspect and manipulate the data comfortably.
- `python-dotenv` – reads connection values from the `.env` file into environment variables before the script runs.
