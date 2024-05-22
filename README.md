# Project README

## Overview

This project involves processing and visualizing PhonePe transaction and user data using a combination of Python libraries and a PostgreSQL database. The script reads multiple JSON files, extracts relevant data, cleans it, and organizes it into Pandas DataFrames. It then connects to a PostgreSQL database to retrieve additional data and generates visualizations using Plotly and Streamlit.

## Project Structure

### Part 1: Data Processing

1. **Libraries Used**
   - `os`: Interact with the file system.
   - `json`: Parse JSON files.
   - `pandas` (as `pd`): Data manipulation and analysis.
   - `psycopg2`: PostgreSQL database operations (not used in the script).

2. **Process Overview**
   - **Path Setup**: Specify directory containing transaction data files.
   - **List Directories**: Hold the list of state directories.
   - **Initialize Columns**: Dictionary to store data for creating a DataFrame.
   - **Iterate Over Directories**: Loop through directories for states, years, and files.
   - **Read and Parse JSON**: Open, read, and parse each file.
   - **Extract Data**: Extract transaction type, count, and amount.
   - **Create DataFrame**: Convert extracted data into DataFrames.
   - **Clean Data**: Standardize state names and convert to title case.
   - **Repeat for User Data**: Follow a similar process for user data.
   - **Process Map Data**: Handle district-level transaction and user data.
   - **Create DataFrames**: For both transaction and user data at the district level.

### Part 2: Database Connection and Data Retrieval

1. **Prerequisites**
   - Python packages: `pandas`, `psycopg2`, `plotly`, `requests`.

2. **Database Connection**
   - Connect to a PostgreSQL database named `Phonepe_Data`.
   - Modify connection parameters (host, user, port, database, password) as needed.

3. **Table Retrieval**
   - Fetch the following tables and convert them into Pandas DataFrames:
     - `aggregated_transaction`
     - `aggregated_user`
     - `map_transaction`
     - `map_users`
     - `top_transaction`
     - `top_user`

### Part 3: Data Visualization Functions

1. **Functions Overview**
   - `top_chart_transaction_amount(table_name)`: Bar charts for top and bottom 10 states by transaction amount.
   - `top_chart_transaction_count(table_name)`: Bar charts for top and bottom 10 states by transaction count.
   - `top_chart_map_user(table_name, state)`: Bar charts for top and bottom 10 districts by registered users.
   - `top_chart_map_user_appOpens(table_name, state)`: Bar charts for top and bottom 10 districts by app opens.
   - `top_chart_top_user(table_name)`: Bar charts for top and bottom 10 states by registered users.
   - `Transaction_Amount_Count_Yearwise(df, year)`: Bar charts and choropleth maps for transaction data by year.
   - `Transaction_Amount_Count_Quartilewise(df, quartile)`: Similar to above but by quartile.
   - `Aggre_Tran_Transaction_Type(df, state)`: Pie charts for transaction data by type.
   - `Aggre_User_plot1(df, year)`: Bar chart for transaction counts by brand.
   - `Aggre_User_plot2(df, quartile)`: Similar to above but by quartile.
   - `Aggre_User_plot3(df, state)`: Area chart for transaction counts and percentages by brand.
   - `Map_Trans_District(df, state)`: Bar charts for district-level transaction data.
   - `Map_User_Plot1(df, year)`: Area chart for registered users and app opens per state.
   - `Map_User_Plot2(df, quartile)`: Similar to above but by quartile.
   - `Map_User_plot3(df, states)`: Bar charts for district-level user data.
   - `Top_Transaction_Plot1(df, states)`: Bar and area charts for transaction data by pincode.
   - `Top_User_P1(df, years)`: Visualizations for registered users by state and quartile.

### Part 4: Streamlit Application

1. **Imports**
   - `Streamlit`: Build the web application.
   - `psycopg2`: Interact with PostgreSQL database.
   - `pandas`: Data manipulation.
   - `json` and `requests`: Handle JSON data.
   - `plotly`: Interactive visualizations.
   - `PIL`: Image processing.

2. **Data Retrieval and Storage**
   - Fetch data from PostgreSQL database and store in DataFrames:
     - `Aggre_transaction`
     - `Aggre_user`
     - `Map_transaction`
     - `Map_user`
     - `Top_transaction`
     - `Top_user`

3. **Visualization Functions**
   - Define functions for various visualizations as listed in Part 3.

4. **User Interface**
   - **Data Expo**
     - `Aggregated Analysis`: Visualize transaction and user data by year, quartile, and state.
     - `Map Analysis`: Visualize map transaction and user data.
     - `Top Analysis`: Visualize top transaction and user data.
   - **Top List**
     - Display top lists based on different criteria (transaction amount/count, registered users, app openings).

## Usage

1. **Setup Environment**
   - Install required Python packages:

2. **Modify Database Connection**
   - Update connection parameters in the script as per your PostgreSQL database configuration.

3. **Run the Script**
   - Execute the script to start the Streamlit application:


4. **Navigate the Application**
   - Use the sidebar to select different analysis and visualization options.

## Assumptions

- The script assumes a specific directory structure and file naming convention.
- Missing or malformed data is handled with try-except blocks, which may result in skipped entries.

## Conclusion

This project provides a comprehensive tool for processing, analyzing, and visualizing PhonePe transaction and user data using Python, PostgreSQL, and Streamlit. The modular structure allows for easy extension and customization based on specific requirements.
