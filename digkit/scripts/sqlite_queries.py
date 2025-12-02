import pandas as pd
import sqlite3
import os

QUERIES = {
    "dwbcommon": """
        SELECT 
        usageEvents.pkgId,
        datetime(usageEvents.timeStamp / 1000, 'unixepoch') AS timestamps, --UTC
        --datetime(usageEvents.timeStamp / 1000, 'unixepoch', '-5 hours') AS timestamps, --CDT (UTC-5:00)
        foundPackages.name, 
        usageEvents.eventType,
            CASE
                when usageEvents.eventType=0 THEN 'NONE'
                when usageEvents.eventType=1 THEN 'ACTIVITY_RESUMED'
                when usageEvents.eventType=2 THEN 'ACTIVITY_PAUSED'
                when usageEvents.eventType=5 THEN 'CONFIGURATION_CHANGE'
                when usageEvents.eventType=7 THEN 'USER_INTERACTION'
                when usageEvents.eventType=8 THEN 'SHORTCUT_INVOCATION'
                when usageEvents.eventType=11 THEN 'STANDBY_BUCKET_CHANGED'
                when usageEvents.eventType=12 THEN 'NOTIFICATION'
                when usageEvents.eventType=15 THEN 'SCREEN_INTERACTIVE'
                when usageEvents.eventType=16 THEN 'SCREEN_NON_INTERACTIVE'
                when usageEvents.eventType=17 THEN 'KEYGUARD_SHOWN'
                when usageEvents.eventType=18 THEN 'KEYGUARD_HIDDEN (DEVICE UNLOCK)'
                when usageEvents.eventType=19 THEN 'FOREGROUND_SERVICE START'
                when usageEvents.eventType=20 THEN 'FOREGROUND_SERVICE_STOP'
                when usageEvents.eventType=23 THEN 'ACTIVITY_STOPPED'
                when usageEvents.eventType=26 THEN 'DEVICE_SHUTDOWN'
                when usageEvents.eventType=27 THEN 'DEVICE_STARTUP'
            ELSE CAST(usageEvents.eventType AS TEXT)
        END AS eventTypeReadable
        FROM usageEvents
        INNER JOIN foundPackages ON usageEvents.pkgId = foundPackages.pkgId
        ORDER BY timestamps;
    """,
    "notestore": """
        SELECT Z_PK, ZCRYPTOITERATIONCOUNT, ZCRYPTOSALT, ZCRYPTOWRAPPEDKEY
        FROM ZICCLOUDSYNCINGOBJECT
        WHERE ZISPASSWORDPROTECTED = 1
    """,
    # add cache.sqlite query
}

def run_sql_by_label(query, db_path, output_type=None, output_dir=None):
    if query not in QUERIES:
        raise ValueError(f"Unknown query label: {query}")
    
    sql_query = QUERIES[query]
    
    output_dir = output_dir or "."
    os.makedirs(output_dir, exist_ok=True)

    try:
        uri = f"file:{db_path}?mode=ro"
        with sqlite3.connect(uri, uri=True) as db:
            cursor = db.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            if query == "notestore":
                output_type = output_type or "console"

                if output_type == "console":
                    for row in rows:
                        z_pk, iteration_count, salt, wrapped_key = row
                        salt_hex = salt.hex() if salt else ''
                        key_hex = wrapped_key.hex() if wrapped_key else ''
                        print(f"$ASN$*{z_pk}*{iteration_count}*{salt_hex}*{key_hex}")
                elif output_type == "txt":
                    output_file = os.path.join(output_dir, f"{query}.txt")
                    with open(output_file, "w") as f:
                        for row in rows:
                            z_pk, iteration_count, salt, wrapped_key = row
                            salt_hex = salt.hex() if salt else ''
                            key_hex = wrapped_key.hex() if wrapped_key else ''
                            f.write(f"$ASN$*{z_pk}*{iteration_count}*{salt_hex}*{key_hex}\n")
                    print(f"Saved TXT: {output_file}")
                else:
                    raise ValueError("Unsupported output_type for notestore. Use 'console' or 'txt'.")
            else:
                output_type = output_type or "csv"
                df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

                if output_type == "console":
                    print(df.to_string(index=False))
                elif output_type == "csv":
                    output_file = os.path.join(output_dir, f"{query}.csv")
                    df.to_csv(output_file, index=False)
                    print(f"Saved CSV: {output_file}")
                elif output_type == "html":
                    output_file = os.path.join(output_dir, f"{query}.html")
                    df.to_html(output_file, index=False)
                    print(f"Saved HTML: {output_file}")
                else:
                    raise ValueError(f"Unsupported output_type for {query}. Use 'console', 'csv', or 'html'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")