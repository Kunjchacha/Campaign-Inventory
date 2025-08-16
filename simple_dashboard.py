from flask import Flask, render_template_string, jsonify, request
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'contentive-warehouse-instance-1.cq8sion7djdk.eu-west-2.rds.amazonaws.com',
    'port': 5432,
    'database': 'analytics',
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

def get_inventory_summary(product_filter=None, brand_filter=None, start_date=None, end_date=None):
    """Get summary of all inventory data with optional filters"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # Build base query with filters
        base_where = 'WHERE "ID" >= 8000'
        
        # Add date filter if specified (using the actual "Dates" column)
        if start_date and end_date:
            base_where += f' AND "Dates" >= \'{start_date}\' AND "Dates" <= \'{end_date}\''
        
        # Get summary from all inventory tables
        query = f"""
        SELECT 
            'Accountancy Age' as brand,
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Booked' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Not Booked' THEN 1 END) as available,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Hold' THEN 1 END) as on_hold,
            COUNT(CASE WHEN "Booked/Not Booked" IS NULL OR "Booked/Not Booked" NOT IN ('Booked', 'Not Booked', 'Hold') THEN 1 END) as unclassified
        FROM campaign_metadata.aa_inventory
        {base_where}
        """
        
        # Execute queries for each brand
        brands_data = []
        brand_tables = [
            ('Accountancy Age', 'aa_inventory'),
            ('Bobsguide', 'bob_inventory'),
            ('The CFO', 'cfo_inventory'),
            ('Global Treasurer', 'gt_inventory'),
            ('HRD Connect', 'hrd_inventory')
        ]
        
        for brand_name, table_name in brand_tables:
            # Skip if brand filter is specified and doesn't match
            if brand_filter and brand_filter != brand_name:
                continue
                
            try:
                brand_query = query.replace('aa_inventory', table_name)
                cursor.execute(brand_query)
                brand_data = cursor.fetchone()
                
                if brand_data:
                    # Add unclassified to available (they're essentially available slots)
                    available_with_unclassified = brand_data['available'] + brand_data['unclassified']
                    brands_data.append({
                        'brand': brand_name,
                        'total_slots': brand_data['total_slots'],
                        'booked': brand_data['booked'],
                        'available': available_with_unclassified,
                        'on_hold': brand_data['on_hold'],
                        'unclassified': brand_data['unclassified']
                    })
            except Exception as e:
                print(f"Error querying {table_name}: {e}")
                # Add empty data for this brand if query fails
                brands_data.append({
                    'brand': brand_name,
                    'total_slots': 0,
                    'booked': 0,
                    'available': 0,
                    'on_hold': 0,
                    'unclassified': 0
                })
        
        return brands_data
        
    except Exception as e:
        print(f"Error in get_inventory_summary: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_inventory_by_product_and_brand():
    """Get inventory breakdown by product and brand for default state using all_inventory view"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # Get inventory data from the all_inventory view for the target products
        # Use a simple approach to avoid date parsing issues
        query = """
        SELECT 
            "brand",
            "Product Name - As per Listing Hub" as product,
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Booked' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Hold' THEN 1 END) as on_hold,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Not Booked' OR "Booked/Not Booked" IS NULL THEN 1 END) as available
        FROM data_products.all_inventory
        WHERE "Product Name - As per Listing Hub" IN (
            'BM-S2-Newsletter Sponsorship',
            'MailShot', 
            'LB-1-Live Broadcast'
        )
        GROUP BY "brand", "Product Name - As per Listing Hub"
        ORDER BY "brand", "Product Name - As per Listing Hub"
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Process results to create summary data
        processed_results = []
        for row in results:
            if row['total_slots'] > 0:
                processed_results.append({
                    'brand': row['brand'],
                    'product': row['product'],
                    'total_slots': row['total_slots'],
                    'booked': row['booked'],
                    'available': row['available'],
                    'on_hold': row['on_hold'],
                    'unclassified': 0
                })
        
        return processed_results
        
    except Exception as e:
        print(f"Error in get_inventory_by_product_and_brand: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def parse_slot_id(slot_id_string):
    """Parse slot ID string to extract product, date, week, and slot information"""
    if not slot_id_string:
        return None
    
    try:
        # Example: "Newsletter_Sponsorship_BM-S2_2024_July_Week5_Slot1"
        parts = slot_id_string.split('_')
        
        if len(parts) >= 6:
            # Extract components
            product_type = parts[0]  # Newsletter, Gated_Content, etc.
            product_code = parts[2] if len(parts) > 2 else parts[1]  # BM-S2, LD-1, etc.
            year = parts[3] if len(parts) > 3 else None  # 2024
            month = parts[4] if len(parts) > 4 else None  # July
            week_info = parts[5] if len(parts) > 5 else None  # Week5
            slot_info = parts[6] if len(parts) > 6 else None  # Slot1
            
            # Extract week number and slot number
            week_num = None
            slot_num = None
            
            if week_info and 'Week' in week_info:
                week_num = week_info.replace('Week', '')
            
            if slot_info and 'Slot' in slot_info:
                slot_num = slot_info.replace('Slot', '')
            
            return {
                'product_type': product_type,
                'product_code': product_code,
                'year': year,
                'month': month,
                'week': week_num,
                'slot': slot_num,
                'full_string': slot_id_string
            }
    except Exception as e:
        print(f"Error parsing slot ID {slot_id_string}: {e}")
    
    return None

def get_filtered_inventory_slots(product_filter=None, brand_filter=None, start_date=None, end_date=None):
    """Get individual inventory slots with client information for filtered results using individual brand tables"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # Use individual brand tables instead of the problematic all_inventory view
        all_results = []
        
        # Define brand tables and their mappings
        brand_tables = [
            ('aa_inventory', 'AA'),
            ('bob_inventory', 'BG'),
            ('cfo_inventory', 'CFO'),
            ('gt_inventory', 'GT'),
            ('hrd_inventory', 'HRD')
        ]
        
        for table_name, brand_code in brand_tables:
            # Skip if brand filter is specified and doesn't match
            if brand_filter and brand_filter != brand_code:
                continue
                
            # Build query for this brand table
            query = f"""
            SELECT 
                "ID" as slot_id,
                "Dates" as slot_date,
                "Booked/Not Booked" as status,
                "Booking ID" as booking_id,
                '{brand_code}' as brand
            FROM campaign_metadata.{table_name}
            WHERE "ID" >= 8000
            """
            
            # Add date filter if specified
            if start_date and end_date:
                query += f" AND \"Dates\" >= '{start_date}' AND \"Dates\" <= '{end_date}'"
            
            cursor.execute(query)
            brand_results = cursor.fetchall()
            
            # Process results for this brand
            for row in brand_results:
                try:
                    # Convert Excel date to actual date
                    actual_date = None
                    if row['slot_date']:
                        try:
                            # Excel dates are days since 1900-01-01
                            # Convert to Python date
                            excel_date = int(row['slot_date'])
                            if excel_date > 0:
                                # Excel epoch starts from 1900-01-01
                                # But Excel incorrectly treats 1900 as leap year
                                if excel_date > 60:  # After 1900-02-28
                                    excel_date -= 1
                                actual_date = datetime(1900, 1, 1) + timedelta(days=excel_date - 1)
                        except (ValueError, TypeError):
                            # Skip invalid dates
                            continue
                    
                    # Skip dates outside reasonable range
                    if actual_date:
                        # Normalize to date object for comparison
                        if hasattr(actual_date, 'date'):
                            actual_date = actual_date.date()
                        elif hasattr(actual_date, 'date'):
                            actual_date = actual_date.date()
                        
                        if actual_date < datetime(2020, 1, 1).date() or actual_date > datetime(2030, 12, 31).date():
                            continue
                    
                    # Determine status
                    if row['status'] == 'Booked':
                        display_status = 'Booked'
                    elif row['status'] == 'Hold':
                        display_status = 'On Hold'
                    else:
                        display_status = 'Available'
                    
                    # Try to find client and product info from campaign_ledger
                    client_name = 'N/A'
                    product_name = 'N/A'
                    
                    if row['status'] == 'Booked' and row['booking_id']:
                        # Look for this slot in campaign_ledger
                        ledger_query = """
                        SELECT 
                            "Client Name",
                            "Product Name - As per Listing Hub"
                        FROM campaign_metadata.campaign_ledger
                        WHERE "Inventory Slot ID" LIKE %s
                        LIMIT 1
                        """
                        
                        # Create a pattern to search for this slot
                        # We'll search by brand and approximate date
                        if actual_date:
                            date_pattern = f"%{actual_date.strftime('%Y_%B_Week')}%"
                            cursor.execute(ledger_query, (f"%{brand_code}%{date_pattern}%",))
                            ledger_result = cursor.fetchone()
                            
                            if ledger_result:
                                client_name = ledger_result['Client Name'] or 'N/A'
                                product_name = ledger_result['Product Name - As per Listing Hub'] or 'N/A'
                    
                    all_results.append({
                        'slot_id': row['slot_id'],
                        'slot_date': actual_date,
                        'status': display_status,
                        'booking_id': row['booking_id'],
                        'brand': row['brand'],
                        'product': product_name,
                        'client_name': client_name,
                        'website_name': 'N/A',
                        'media_asset': 'N/A',
                        'format_code': 'N/A',
                        'slot_number': 'N/A'
                    })
                    
                except Exception as e:
                    # Skip problematic records
                    print(f"Skipping problematic record: {e}")
                    continue
        
        # Sort results by date, brand, and product
        all_results.sort(key=lambda x: (x['slot_date'] or datetime.min, x['brand'], x['product']))
        
        return all_results[:100]  # Limit to 100 results
        
    except Exception as e:
        print(f"Error in get_filtered_inventory_slots: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_filtered_inventory_by_product(product_filter, brand_filter=None, start_date=None, end_date=None):
    """Get inventory filtered by product using campaign_ledger join"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # This function will be implemented to handle product filtering
        # by joining inventory tables with campaign_ledger
        # For now, return basic summary
        return get_inventory_summary(brand_filter, start_date, end_date)
        
    except Exception as e:
        print(f"Error in get_filtered_inventory_by_product: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_upcoming_deliverables():
    """Get upcoming deliverables for next 2 weeks (current week + next week) from campaign ledger"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        query = """
        SELECT 
            "Client Name" as client,
            "Product Name - As per Listing Hub" as product,
            "Scheduled Live Date" as deliverable_date
        FROM campaign_metadata.campaign_ledger
        WHERE "Scheduled Live Date" >= CURRENT_DATE 
        AND "Scheduled Live Date" <= CURRENT_DATE + INTERVAL '14 days'
        AND "Status" = 'Active'
        ORDER BY "Scheduled Live Date" ASC
        LIMIT 20
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        deliverables = []
        for row in results:
            deliverables.append({
                'client': row['client'],
                'product': row['product'],
                'deliverable_date': row['deliverable_date']
            })
        
        return deliverables
        
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        # Use the new function that breaks down by product and brand by default
        inventory_summary = get_inventory_by_product_and_brand()
        upcoming_deliverables = get_upcoming_deliverables()
        
        # Calculate totals
        total_slots = sum(item['total_slots'] for item in inventory_summary)
        total_booked = sum(item['booked'] for item in inventory_summary)
        total_available = sum(item['available'] for item in inventory_summary)
        total_on_hold = sum(item['on_hold'] for item in inventory_summary)
        
        return render_template_string(HTML_TEMPLATE, 
                                    inventory_summary=inventory_summary,
                                    upcoming_deliverables=upcoming_deliverables,
                                    total_slots=total_slots,
                                    total_booked=total_booked,
                                    total_available=total_available,
                                    total_on_hold=total_on_hold,
                                    datetime=datetime)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/api/inventory')
def api_inventory():
    """API endpoint for inventory data with filters"""
    try:
        # Get filter parameters from request
        product_filter = request.args.get('product')
        brand_filter = request.args.get('brand')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Always use the filtered inventory slots function for detailed results
        inventory_slots = get_filtered_inventory_slots(
            product_filter=product_filter,
            brand_filter=brand_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify(inventory_slots)
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/bookings')
def api_bookings():
    """API endpoint for upcoming deliverables"""
    try:
        upcoming_deliverables = get_upcoming_deliverables()
        return jsonify(upcoming_deliverables)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# HTML Template for the dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campaign Inventory Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    
</head>
<body class="bg-gray-900 text-white">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-blue-400 mb-2">📊 Campaign Inventory Dashboard</h1>
            <p class="text-gray-400">Real-time inventory tracking across all brands</p>
            <p class="text-sm text-gray-500 mt-2">Last updated: {{ datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}</p>
        </header>

        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-blue-500 bg-opacity-20">
                        <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-gray-400 text-sm">Total Slots</p>
                        <p class="text-2xl font-bold text-white">{{ total_slots }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-green-500 bg-opacity-20">
                        <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-gray-400 text-sm">Booked</p>
                        <p class="text-2xl font-bold text-green-400">{{ total_booked }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-yellow-500 bg-opacity-20">
                        <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-gray-400 text-sm">On Hold</p>
                        <p class="text-2xl font-bold text-yellow-400">{{ total_on_hold }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-gray-500 bg-opacity-20">
                        <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
                        </svg>
                    </div>
                    <div class="ml-4">
                        <p class="text-gray-400 text-sm">Available</p>
                        <p class="text-2xl font-bold text-gray-400">{{ total_available }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Filters Section -->
        <div class="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-8">
            <h2 class="text-xl font-bold text-white mb-4">🔍 Filters</h2>
            <div class="flex items-center space-x-4">
                <!-- Product Filter -->
                <div class="flex-1">
                    <label class="block text-sm font-medium text-gray-400 mb-2">Product</label>
                    <select id="productFilter" class="w-full bg-gray-700 border border-gray-600 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">All Products</option>
                        <option value="BM-S2-Newsletter Sponsorship">Newsletter Sponsorship</option>
                        <option value="MailShot">Mailshot</option>
                        <option value="LB-1-Live Broadcast">Live Broadcast</option>
                    </select>
                </div>
                
                <!-- Brand Filter -->
                <div class="flex-1">
                    <label class="block text-sm font-medium text-gray-400 mb-2">Brand</label>
                    <select id="brandFilter" class="w-full bg-gray-700 border border-gray-600 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">All Brands</option>
                        <option value="AA">Accountancy Age</option>
                        <option value="BG">Bobsguide</option>
                        <option value="CFO">The CFO</option>
                        <option value="GT">Global Treasurer</option>
                        <option value="HRD">HRD Connect</option>
                    </select>
                </div>
                
                <!-- Date Range Filter -->
                <div class="flex-1">
                    <label class="block text-sm font-medium text-gray-400 mb-2">Date Range</label>
                    <div class="flex space-x-2">
                        <input type="date" id="startDate" class="flex-1 bg-gray-700 border border-gray-600 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <input type="date" id="endDate" class="flex-1 bg-gray-700 border border-gray-600 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                </div>
                
                <!-- Search Button -->
                <div class="flex items-end">
                    <button onclick="applyFilters()" class="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium transition-colors">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Real-time Data Display -->
        <div class="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-8">
            <h2 class="text-xl font-bold text-white mb-4">📊 Filtered Inventory Results</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="border-b border-gray-700">
                            <th class="text-left py-2 text-gray-400">Product</th>
                            <th class="text-left py-2 text-gray-400">Brand</th>
                            <th class="text-left py-2 text-gray-400">Date</th>
                            <th class="text-left py-2 text-gray-400">Status</th>
                            <th class="text-left py-2 text-gray-400">Client Name</th>
                            <th class="text-left py-2 text-gray-400">Booking ID</th>
                        </tr>
                    </thead>
                    <tbody id="filteredResultsTable">
                        <tr class="border-b border-gray-700">
                            <td class="py-2 text-center text-gray-500" colspan="6">Apply filters to see inventory results</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Upcoming Deliverables -->
        <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 class="text-xl font-bold text-white mb-4">📅 Upcoming Deliverables (Next 2 Weeks)</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="border-b border-gray-700">
                            <th class="text-left py-2 text-gray-400">Client</th>
                            <th class="text-left py-2 text-gray-400">Product</th>
                            <th class="text-left py-2 text-gray-400">Deliverable Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for deliverable in upcoming_deliverables %}
                        <tr class="border-b border-gray-700">
                            <td class="py-2 text-white">{{ deliverable.client }}</td>
                            <td class="py-2 text-blue-400">{{ deliverable.product }}</td>
                            <td class="py-2 text-gray-400">{{ deliverable.deliverable_date.strftime('%Y-%m-%d') if deliverable.deliverable_date else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
                 // Chart.js removed - no longer needed

                 // Auto-refresh every 30 seconds - refresh the page to get latest data
         setInterval(() => {
             location.reload();
         }, 30000);

        // Filter functions
        function applyFilters() {
            const product = document.getElementById('productFilter').value;
            const brand = document.getElementById('brandFilter').value;
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;
            
            // Build query parameters
            const params = new URLSearchParams();
            if (product) params.append('product', product);
            if (brand) params.append('brand', brand);
            if (startDate) params.append('start_date', startDate);
            if (endDate) params.append('end_date', endDate);
            
                         // Fetch filtered data
             fetch(`/api/inventory?${params.toString()}`)
                 .then(response => response.json())
                 .then(data => {
                     updateFilteredResultsTable(data);
                 })
                 .catch(error => console.log('Filter error:', error));
        }
        
                 function resetFilters() {
             document.getElementById('productFilter').value = '';
             document.getElementById('brandFilter').value = '';
             document.getElementById('startDate').value = '';
             document.getElementById('endDate').value = '';
             // Clear the results table
             updateFilteredResultsTable([]);
         }
        
                          function updateFilteredResultsTable(data) {
            const tbody = document.getElementById('filteredResultsTable');
            tbody.innerHTML = '';
            
            if (!data || data.length === 0) {
                tbody.innerHTML = `
                    <tr class="border-b border-gray-700">
                        <td class="py-2 text-center text-gray-500" colspan="6">No results found for the selected filters</td>
                    </tr>
                `;
                return;
            }
            
            data.forEach(slot => {
                const row = document.createElement('tr');
                row.className = 'border-b border-gray-700';
                
                // Format date - handle both string dates and parsed dates
                let dateDisplay = 'N/A';
                if (slot.slot_date) {
                    try {
                        if (typeof slot.slot_date === 'string') {
                            dateDisplay = new Date(slot.slot_date).toLocaleDateString();
                        } else {
                            // If it's already a parsed date object
                            dateDisplay = slot.slot_date;
                        }
                    } catch (e) {
                        dateDisplay = 'Invalid Date';
                    }
                }
                
                // Color code status
                let statusClass = 'text-gray-400';
                if (slot.status === 'Booked') statusClass = 'text-green-400';
                else if (slot.status === 'On Hold') statusClass = 'text-yellow-400';
                
                row.innerHTML = `
                    <td class="py-2 text-blue-400">${slot.product}</td>
                    <td class="py-2 text-white">${slot.brand}</td>
                    <td class="py-2 text-gray-400">${dateDisplay}</td>
                    <td class="py-2 ${statusClass}">${slot.status}</td>
                    <td class="py-2 text-white">${slot.client_name}</td>
                    <td class="py-2 text-gray-400">${slot.booking_id || 'N/A'}</td>
                `;
                tbody.appendChild(row);
            });
        }
        
        // Set default date range to next 2 weeks
        window.addEventListener('load', function() {
            const today = new Date();
            const twoWeeksLater = new Date(today.getTime() + (14 * 24 * 60 * 60 * 1000));
            
            document.getElementById('startDate').value = today.toISOString().split('T')[0];
            document.getElementById('endDate').value = twoWeeksLater.toISOString().split('T')[0];
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True, port=5000)
