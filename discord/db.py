import psycopg2

def db_write(table, action, sql_command):
    
    if action == "insert":
        #sql builder for insert
        db_action(f"INSERT INTO public.{table} (username, email) VALUES ({sql_command})")
        return
    
    elif action == "select":
        #sql builder for select
        
        return db_action(f"SELECT count(*) FROM {table}")
    
    elif action == "create":
        #sql builder for create
        return

# Connect to the database
def db_action(sql_command):
    conn = psycopg2.connect(
    host="postgres",
    port=5432,
    user="postgres",
    password="changeme",
    database="postgres")
    cur = conn.cursor()

    cur.execute(sql_command)
    try:
        result = cur.fetchall()
        if result != []:
            for res in result:
                print(res)
        else:
            result = "No results"
    except:
        result = "No results"
    
    # Commit the changes to the database
    conn.commit()

    cur.close()
    conn.close()

    return result
