import psycopg2
import json

# --------------------
# Database connection settings
# --------------------
DB_CONFIG = {
    "dbname": "analytics",            # your DB name
    "user": "kunj.chacha@contentive.com",           # your DB username
    "password": "(iRFw989b{5h",       # your DB password
    "host": "contentive-warehouse-instance-1.cq8sion7djdk.eu-west-2.rds.amazonaws.com",            # often localhost or IP
    "port": 5432                       # default PostgreSQL port
}

# --------------------
# SQL query for multi-brand inventory with safe date parsing
# --------------------
SQL_QUERY = """
SELECT inv."ID",
       inv."Inventory Slots",
       CASE
         WHEN inv."Dates" ~ '^\\d+$' THEN 
           to_date('1899-12-30', 'YYYY-MM-DD') + inv."Dates"::int
         WHEN inv."Dates" ~ '^[A-Za-z]+,\\s+[A-Za-z]+\\s+\\d{1,2},\\s+\\d{4}$' THEN
           to_date(inv."Dates", 'FMDay, FMMonth DD, YYYY')
         WHEN inv."Dates" ~ '^\\d{1,2}/\\d{1,2}/\\d{4}$' THEN
           to_date(inv."Dates", 'DD/MM/YYYY')
         WHEN inv."Dates" ~ '^\\d{4}-\\d{2}-\\d{2}$' THEN
           inv."Dates"::date
         ELSE NULL
       END AS "Dates",
       inv."Media_Asset",
       inv."Website_Name",
       inv."Media_Location",
       inv."Format_Code",
       inv."Slot",
       inv."Booked/Not Booked",
       inv."Booking ID",
       led."Client Name",
       led."Contract Value",
       led."Scheduled Live Date",
       led."Schedule End Date",
       'AA' AS brand
FROM campaign_metadata.aa_inventory inv
LEFT JOIN campaign_metadata.campaign_ledger led
       ON inv."Booking ID" = led."Booking ID"
WHERE inv."ID" >= 8000

UNION ALL

SELECT inv."ID", inv."Inventory Slots",
       CASE
         WHEN inv."Dates" ~ '^\\d+$' THEN 
           to_date('1899-12-30', 'YYYY-MM-DD') + inv."Dates"::int
         WHEN inv."Dates" ~ '^[A-Za-z]+,\\s+[A-Za-z]+\\s+\\d{1,2},\\s+\\d{4}$' THEN
           to_date(inv."Dates", 'FMDay, FMMonth DD, YYYY')
         WHEN inv."Dates" ~ '^\\d{1,2}/\\d{1,2}/\\d{4}$' THEN
           to_date(inv."Dates", 'DD/MM/YYYY')
         WHEN inv."Dates" ~ '^\\d{4}-\\d{2}-\\d{2}$' THEN
           inv."Dates"::date
         ELSE NULL
       END AS "Dates",
       inv."Media_Asset", inv."Website_Name", inv."Media_Location", inv."Format_Code",
       inv."Slot", inv."Booked/Not Booked", inv."Booking ID",
       led."Client Name", led."Contract Value", led."Scheduled Live Date", led."Schedule End Date",
       'BOB' AS brand
FROM campaign_metadata.bob_inventory inv
LEFT JOIN campaign_metadata.campaign_ledger led
       ON inv."Booking ID" = led."Booking ID"
WHERE inv."ID" >= 8000

-- Repeat same block for CFO, CZ, GT, HRD, SEW with correct table name and brand string
"""

# --------------------
# Function to fetch & export data
# --------------------
def fetch_inventory_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        data = [dict(zip(colnames, row)) for row in rows]

        # Save JSON into React src/ folder
        with open('src/inventoryData.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

        print(f"✅ Exported {len(data)} records to src/inventoryData.json")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    fetch_inventory_data()
