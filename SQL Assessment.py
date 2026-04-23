'''Query from SQL table 'NAL Pro Players R6S' '''

import sqlite3

#open file
DATABASE = "NAL_R6S_Pros.db"


def execute_query(query, params=()):
    with sqlite3.connect(DATABASE) as db:
        #access columns by name, changing tuples into a dictionary type data
        db.row_factory = sqlite3.Row
        #initiate cursor, separates query from parameters
        cursor = db.cursor()
        cursor.execute(query, params)
        #fetch results
        results = cursor.fetchall()
        #check for no results
        if not results:
            print("\nNo players found matching that criteria.")
            return
        headers = results[0].keys()
        #get headers to print on top of data
        column_width = 20
        print(" | ".join(name.ljust(column_width) for name in headers))
        print("-" * (column_width * len(headers)))
        #print data
        for row in results:
            print(" | ".join(str(row[column]).ljust(column_width) for column in headers))


def user_search():
    #create dictionary with questions for each column
    search_fields = {"player_name": "Player name",
                     "team_name": "Team name",
                     "role": "Role",
                     "lifetime_rating_siegegg": "Lifetime SiegeGG rating",
                     "notable_achievements": "Notable achievements"}
    query = 'SELECT * FROM NAL_R6S_Pros WHERE 1=1'
    params = []
    print("Search Filters (Leave blank to skip)")
    for col, label in search_fields.items():
        # Handle text-based search for name, role and team
        if col in ["player_name", "team_name", "role"]:
            val = input(f"{label} (contains): ").strip()
            if val:
                query += f" AND {col} LIKE ?"
                params.append(f"%{val}%")
        #extra information for achievement formating
        elif col in ["notable_achievements"]:
            print("Format is [Event name] [year]")
            print("eg. Manchester Major 2024, SI 2025, Esports World Cup 2024")
            val = input(f"{label} (contains): ").strip()
            if val:
                query += f" AND {col} LIKE ?"
                params.append(f"%{val}%")
        # Handle numerical range search for Siege GG rating
        else:
            val = input(f"Enter {label} value: ").strip()
            if val:
                print(f"Match {label}: [1] Exactly  [2] Greater Than  [3] Less Than")
                choice = input("Select (1/2/3): ")
                
                # give user choice of operator
                operators = {"1": "=", "2": ">=", "3": "<="}
                op = operators.get(choice, "=") # default is equals
                
                query += f" AND {col} {op} ?"
                params.append(float(val))
    if "lifetime_rating_siegegg" in query:
        query += " ORDER BY lifetime_rating_siegegg DESC"
    # Convert list to tuple for sqlite3
    execute_query(query, tuple(params))

if __name__ == "__main__":
    user_search()