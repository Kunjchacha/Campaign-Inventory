from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'contentive-warehouse-instance-1.cq8sion7djdk.eu-west-2.rds.amazonaws.com',
    'port': 5432,
    'database': 'analytics',  # Connect to analytics database
    'user': 'kunj.chacha@contentive.com',
    'password': '(iRFw989b{5h'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Database connection successful!")
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise e

def map_product_to_dashboard(media_asset):
    """Map database products to dashboard products"""
    if not media_asset:
        return None
    
    asset = media_asset.lower()
    
    # Mailshots (includes LVB_Mailshots)
    if asset in ['mailshot', 'lvb_mailshot']:
        return 'Mailshots'
    
    # Newsletter Sponsorship - Weekly
    if asset == 'newsletter_sponsorship':
        return 'Newsletter Sponsorship - Weekly'
    
    # Newsletter Sponsorship - Weekender
    if asset == 'weekender_newsletter_sponsorship':
        return 'Newsletter Sponsorship - Weekender'
    
    # Newsletter Placement (including all Feature Placements)
    if asset in ['newsletter_featured_placement', 'original_content_newsletter_feature_placement']:
        return 'Newsletter Placement'
    
    # Newsletter Category Sponsorship
    if asset == 'newsletter_category_sponsorship':
        return 'Newsletter Category Sponsorship'
    
    # Return None for products we don't want to show
    return None

def normalize_status(status):
    """Normalize status values"""
    if not status:
        return 'Available'
    
    normalized = status.lower().strip()
    
    if normalized == 'booked':
        return 'Booked'
    
    if normalized in ['not booked', 'not booked ']:
        return 'Available'
    
    if normalized in ['hold', 'hold ', 'on hold', 'on hold ']:
        return 'On Hold'
    
    # Default to Available for unknown statuses
    return 'Available'

def map_brand_to_dashboard(website_name, table_source):
    """Map database brand names to dashboard brand names"""
    if not website_name:
        website_name = ''
    
    name = website_name.lower().strip()
    
    # Map based on website name
    if name == 'accountancy age':
        return 'Accountancy Age'
    if name == 'hrd':
        return 'HRD Connect'
    
    # Map based on table source as fallback
    brand_mapping = {
        'aa_inventory': 'Accountancy Age',
        'bob_inventory': 'Bobsguide',
        'cfo_inventory': 'The CFO',
        'gt_inventory': 'Global Treasurer',
        'hrd_inventory': 'HRD Connect'
    }
    
    return brand_mapping.get(table_source, website_name or 'Unknown')

def convert_excel_date(excel_date):
    """
    Convert Excel serial number to readable date
    Excel dates are number of days since January 1, 1900
    """
    if not excel_date:
        return None
    
    try:
        # If it's already a string date, return as is
        if isinstance(excel_date, str):
            # Check if it's already a readable date
            if '-' in excel_date or '/' in excel_date:
                return excel_date
            # Check if it's an Excel serial number
            if excel_date.isdigit():
                excel_serial = int(excel_date)
            else:
                return excel_date
        else:
            excel_serial = int(excel_date)
        
        # Excel epoch is January 1, 1900
        excel_epoch = datetime(1900, 1, 1)
        
        # Convert Excel serial to days (subtract 2 because Excel incorrectly treats 1900 as leap year)
        days = excel_serial - 2
        
        # Calculate the actual date
        actual_date = excel_epoch + timedelta(days=days)
        
        # Return in YYYY-MM-DD format
        return actual_date.strftime('%Y-%m-%d')
        
    except (ValueError, TypeError) as e:
        print(f"Error converting Excel date {excel_date}: {e}")
        return None

@app.route('/api/inventory', methods=['GET'])
def get_inventory_data():
    try:
        # Get query parameters for filtering
        brand = request.args.get('brand', 'All')
        product = request.args.get('product', 'Overall')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Call the synchronous function directly
        return _get_inventory_data_sync(brand, product, start_date, end_date)
    except Exception as error:
        print(f"Database error: {error}")
        return jsonify({'error': 'Database connection failed'}), 500

def _get_inventory_data_sync(brand='All', product='Overall', start_date=None, end_date=None):
    conn = get_db_connection()
    
    inventory_tables = [
        'aa_inventory',
        'bob_inventory', 
        'cfo_inventory',
        'gt_inventory',
        'hrd_inventory'
    ]
    
    all_inventory_data = []
    
    for table in inventory_tables:
        try:
            # Use the same logic as PG Admin query - get latest records for each slot
            query = f'''
            WITH latest_slots AS (
                SELECT DISTINCT ON ("Inventory Slots")
                    "ID",
                    "Inventory Slots",
                    "Booked/Not Booked",
                    "Dates",
                    "Media_Asset",
                    "Website_Name",
                    "Booking ID",
                    last_updated
                FROM campaign_metadata.{table}
                WHERE "ID" >= 8000
                  AND "Inventory Slots" IS NOT NULL
                ORDER BY "Inventory Slots", last_updated DESC
            )
            SELECT * FROM latest_slots
            '''
            
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            
            if result:
                print(f"Processing {len(result)} latest items from {table}")
                
                # Transform the data - include ALL items without deduplication
                for item in result:
                    mapped_product = map_product_to_dashboard(item.get('Media_Asset'))
                    
                    # Include all items with mapped products
                    if mapped_product:
                        transformed_item = {
                            'id': item.get('ID'),
                            'slot_name': item.get('Inventory Slots'),
                            'client': item.get('Booking ID'),
                            'status': normalize_status(item.get('Booked/Not Booked')),
                            'start_date': convert_excel_date(item.get('Dates')),
                            'end_date': convert_excel_date(item.get('Dates')),
                            'product': mapped_product,
                            'brand': map_brand_to_dashboard(item.get('Website_Name'), table),
                            'table_source': table,
                            'last_updated': item.get('last_updated')
                        }
                        all_inventory_data.append(transformed_item)
                
                print(f"Processed {table}, total items so far: {len(all_inventory_data)}")
                
        except Exception as table_error:
            print(f"Failed to fetch from {table}: {table_error}")
            continue
    
    print(f"Final all_inventory data: {len(all_inventory_data)} total items (latest records only)")
    
    # Apply filters to the complete data
    filtered_data = apply_filters_to_inventory(all_inventory_data, brand, product, start_date, end_date)
    
    conn.close()
    return jsonify(filtered_data)

def apply_filters_to_inventory(inventory_data, brand, product, start_date, end_date):
    """
    Apply filters to the consolidated inventory data
    """
    filtered_data = inventory_data.copy()
    
    # Filter by brand
    if brand and brand != 'All':
        filtered_data = [item for item in filtered_data if item['brand'] == brand]
    
    # Filter by product
    if product and product != 'Overall':
        filtered_data = [item for item in filtered_data if item['product'] == product]
    
    # Filter by date range
    if start_date and end_date and start_date.strip() and end_date.strip():
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            
            def is_date_in_range(item_date):
                """Check if item date is within the specified range"""
                if not item_date:
                    return False
                
                try:
                    # Parse the item date
                    if isinstance(item_date, str):
                        # Handle different date formats
                        if '-' in item_date:
                            item_date_obj = datetime.strptime(item_date, '%Y-%m-%d')
                        elif '/' in item_date:
                            item_date_obj = datetime.strptime(item_date, '%m/%d/%Y')
                        else:
                            return False
                    else:
                        return False
                    
                    # Check if date is within range
                    return start_date_obj <= item_date_obj <= end_date_obj
                    
                except (ValueError, TypeError):
                    return False
            
            # Apply date filtering
            filtered_data = [item for item in filtered_data if is_date_in_range(item['start_date'])]
            
            print(f"Date filtering applied: {start_date} to {end_date}, filtered to {len(filtered_data)} items")
            
        except ValueError as e:
            print(f"Date parsing error: {e}")
            # If date parsing fails, return unfiltered data
    
    return filtered_data

@app.route('/api/campaign-ledger', methods=['GET'])
def get_campaign_ledger():
    try:
        # Call the synchronous function directly
        return _get_campaign_ledger_sync()
    except Exception as error:
        print(f"Campaign ledger error: {error}")
        return jsonify({'error': 'Database connection failed'}), 500

def _get_campaign_ledger_sync():
    conn = get_db_connection()
    
    query = "SELECT * FROM campaign_metadata.campaign_ledger LIMIT 1000"
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    
    if result:
        # Transform the campaign ledger data
        transformed_ledger = []
        for item in result:
            transformed_item = {
                'id': item.get('ID'),
                'campaign_name': item.get('Product Name - As per Listing Hub'),
                'client': item.get('Client Name'),
                'product': item.get('Product Name - As per Listing Hub'),
                'brand': item.get('Brand'),
                'start_date': item.get('Scheduled Live Date'),
                'end_date': item.get('Schedule End Date'),
                'status': item.get('Status')
            }
            transformed_ledger.append(transformed_item)
        
        conn.close()
        return jsonify(transformed_ledger)
    else:
        conn.close()
        return jsonify([])

@app.route('/api/test', methods=['GET'])
def test_connection():
    try:
        # Call the synchronous function directly
        return _test_connection_sync()
    except Exception as error:
        print(f"Test connection error: {error}")
        return jsonify({'error': str(error)}), 500

def _test_connection_sync():
    conn = get_db_connection()
    
    # Test query to list available databases
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
    databases_result = cursor.fetchall()
    databases = [row['datname'] for row in databases_result]
    
    # Test query to list available schemas
    cursor.execute("SELECT schema_name FROM information_schema.schemata")
    result = cursor.fetchall()
    schemas = [row['schema_name'] for row in result]
    
    # Test query to list available tables in all schemas
    cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog')")
    tables_result = cursor.fetchall()
    tables_by_schema = {}
    for row in tables_result:
        schema = row['table_schema']
        table = row['table_name']
        if schema not in tables_by_schema:
            tables_by_schema[schema] = []
        tables_by_schema[schema].append(table)
    
    cursor.close()
    conn.close()
    return jsonify({'databases': databases, 'schemas': schemas, 'tables_by_schema': tables_by_schema, 'message': 'Connection successful'})

@app.route('/api/brand-overview', methods=['GET'])
def get_brand_overview():
    try:
        # Call the synchronous function directly
        return _get_brand_overview_sync()
    except Exception as error:
        print(f"Brand overview error: {error}")
        return jsonify({'error': 'Database connection failed'}), 500

def _get_brand_overview_sync():
    conn = get_db_connection()
    
    brand_overview = {}
    
    # Get counts for each brand (ALL items, not filtered by product)
    brand_queries = {
        'Accountancy Age': 'aa_inventory',
        'Bobsguide': 'bob_inventory',
        'The CFO': 'cfo_inventory', 
        'Global Treasurer': 'gt_inventory',
        'HRD Connect': 'hrd_inventory'
    }
    
    for brand_name, table_name in brand_queries.items():
        # Simple count query - show all records
        query = f"""
        SELECT 
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" ILIKE '%booked%' AND "Booked/Not Booked" NOT ILIKE '%not booked%' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" ILIKE '%not booked%' THEN 1 END) as not_booked,
            COUNT(CASE WHEN "Booked/Not Booked" ILIKE '%hold%' THEN 1 END) as on_hold
        FROM campaign_metadata.{table_name}
        WHERE "ID" >= 8000
        """
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        if result:
            row = result[0]
            brand_overview[brand_name] = {
                'total_slots': row['total_slots'],
                'booked': row['booked'],
                'not_booked': row['not_booked'],
                'on_hold': row['on_hold']
            }
    
    conn.close()
    return jsonify(brand_overview)

@app.route('/api/test-filter', methods=['GET'])
def test_filter():
    try:
        # Get query parameters
        brand = request.args.get('brand', 'Accountancy Age')
        product = request.args.get('product', 'Mailshots')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Call the synchronous function directly
        return _test_filter_sync(brand, product, start_date, end_date)
    except Exception as error:
        print(f"Test filter error: {error}")
        return jsonify({'error': str(error)}), 500

def _test_filter_sync(brand, product, start_date, end_date):
    conn = get_db_connection()
    
    # Map brand to table
    brand_to_table = {
        'Accountancy Age': 'aa_inventory',
        'Bobsguide': 'bob_inventory',
        'The CFO': 'cfo_inventory',
        'Global Treasurer': 'gt_inventory',
        'HRD Connect': 'hrd_inventory'
    }
    
    table_name = brand_to_table.get(brand, 'aa_inventory')
    
    # Build query
    query = f"""
    SELECT 
        COUNT(DISTINCT "ID") as total_slots,
        COUNT(DISTINCT CASE WHEN "Booked/Not Booked" ILIKE '%booked%' THEN "ID" END) as booked,
        COUNT(DISTINCT CASE WHEN "Booked/Not Booked" ILIKE '%not booked%' THEN "ID" END) as not_booked,
        COUNT(DISTINCT CASE WHEN "Booked/Not Booked" ILIKE '%hold%' THEN "ID" END) as on_hold
    FROM campaign_metadata.{table_name}
    WHERE "ID" >= 8000
    """
    
    # Add product filter if specified
    if product and product != 'Overall':
        # Map product to Media_Asset values
        product_mapping = {
            'Mailshots': ['mailshot', 'lvb_mailshot'],
            'Newsletter Sponsorship - Weekly': ['newsletter_sponsorship'],
            'Newsletter Sponsorship - Weekender': ['weekender_newsletter_sponsorship'],
            'Newsletter Placement': ['newsletter_featured_placement', 'original_content_newsletter_feature_placement'],
            'Newsletter Category Sponsorship': ['newsletter_category_sponsorship']
        }
        
        if product in product_mapping:
            asset_values = product_mapping[product]
            asset_conditions = " OR ".join([f'"Media_Asset" ILIKE \'%{asset}%\'' for asset in asset_values])
            query += f" AND ({asset_conditions})"
    
    # Add date filter if specified
    if start_date and end_date and start_date.strip() and end_date.strip():
        print(f"Date filtering requested: {start_date} to {end_date}")
        # For now, we'll do client-side date filtering
        # The date filtering will be handled in the frontend
    
    print(f"Final query: {query}")
    
    print(f"Executing query: {query}")
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if result:
        row = result[0]
        return jsonify({
            'brand': brand,
            'product': product,
            'start_date': start_date,
            'end_date': end_date,
            'total_slots': row['total_slots'],
            'booked': row['booked'],
            'not_booked': row['not_booked'],
            'on_hold': row['on_hold']
        })
    else:
        return jsonify({'error': 'No data found'})

@app.route('/api/current-week-inventory', methods=['GET'])
def get_current_week_inventory():
    try:
        # Call the synchronous function directly
        return _get_current_week_inventory_sync()
    except Exception as error:
        print(f"Current week inventory error: {error}")
        return jsonify({'error': 'Database connection failed'}), 500

def _get_current_week_inventory_sync():
    conn = get_db_connection()
    
    inventory_tables = [
        ('aa_inventory', 'Accountancy Age'),
        ('bob_inventory', 'Bobsguide'),
        ('cfo_inventory', 'The CFO'),
        ('gt_inventory', 'Global Treasurer'),
        ('hrd_inventory', 'HRD Connect')
    ]
    
    current_week_data = []
    
    for table, brand_name in inventory_tables:
        try:
            # Use the exact same logic as PG Admin query
            query = f'''
            WITH latest_slots AS (
                SELECT DISTINCT ON ("Inventory Slots")
                    "Inventory Slots",
                    "Booked/Not Booked",
                    last_updated
                FROM campaign_metadata.{table}
                WHERE "Inventory Slots" IS NOT NULL
                  AND last_updated >= date_trunc('week', CURRENT_DATE)  -- start of this week (Monday)
                ORDER BY "Inventory Slots", last_updated DESC
            )
            SELECT
                COUNT(*) AS total_slots,
                COUNT(*) FILTER (WHERE "Booked/Not Booked" = 'Booked') AS booked_slots,
                ROUND(
                    100.0 * COUNT(*) FILTER (WHERE "Booked/Not Booked" = 'Booked') / NULLIF(COUNT(*), 0),
                    2
                ) AS booked_percentage
            FROM latest_slots
            '''
            
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                current_week_data.append({
                    'brand': brand_name,
                    'table': table,
                    'total_slots': result['total_slots'],
                    'booked_slots': result['booked_slots'],
                    'booked_percentage': result['booked_percentage']
                })
                print(f"Current week data for {brand_name}: {result['total_slots']} total, {result['booked_slots']} booked ({result['booked_percentage']}%)")
                
        except Exception as table_error:
            print(f"Failed to fetch current week data from {table}: {table_error}")
            continue
    
    conn.close()
    return jsonify(current_week_data)

# Remove the old preview-data endpoint since we're now using the consolidated inventory endpoint
# @app.route('/api/preview-data', methods=['GET'])
# def get_preview_data():
#     # This endpoint is now deprecated - use /api/inventory instead
#     return jsonify({'error': 'Use /api/inventory endpoint instead'}), 410

# Note: The /api/inventory endpoint now serves as the single source of truth for all inventory data
# It consolidates data from all inventory tables, applies deduplication, and supports filtering
# This eliminates the need for separate preview-data logic and ensures data consistency

if __name__ == '__main__':
    app.run(debug=True, port=5000)
