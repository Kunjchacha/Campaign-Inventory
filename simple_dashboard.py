from flask import Flask, render_template_string, jsonify
import psycopg2
import psycopg2.extras
from datetime import datetime

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

def get_inventory_summary():
    """Get summary of all inventory data"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # Get summary from all inventory tables
        query = """
        SELECT 
            'Accountancy Age' as brand,
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Booked' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Not Booked' THEN 1 END) as available,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Hold' THEN 1 END) as on_hold,
            COUNT(CASE WHEN "Booked/Not Booked" IS NULL OR "Booked/Not Booked" NOT IN ('Booked', 'Not Booked', 'Hold') THEN 1 END) as unclassified
        FROM campaign_metadata.aa_inventory
        WHERE "ID" >= 8000
        UNION ALL
        SELECT 
            'Bobsguide' as brand,
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Booked' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Not Booked' THEN 1 END) as available,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Hold' THEN 1 END) as on_hold,
            COUNT(CASE WHEN "Booked/Not Booked" IS NULL OR "Booked/Not Booked" NOT IN ('Booked', 'Not Booked', 'Hold') THEN 1 END) as unclassified
        FROM campaign_metadata.bob_inventory
        WHERE "ID" >= 8000
        UNION ALL
        SELECT 
            'The CFO' as brand,
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Booked' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Not Booked' THEN 1 END) as available,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Hold' THEN 1 END) as on_hold,
            COUNT(CASE WHEN "Booked/Not Booked" IS NULL OR "Booked/Not Booked" NOT IN ('Booked', 'Not Booked', 'Hold') THEN 1 END) as unclassified
        FROM campaign_metadata.cfo_inventory
        WHERE "ID" >= 8000
        UNION ALL
        SELECT 
            'Global Treasurer' as brand,
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Booked' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Not Booked' THEN 1 END) as available,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Hold' THEN 1 END) as on_hold,
            COUNT(CASE WHEN "Booked/Not Booked" IS NULL OR "Booked/Not Booked" NOT IN ('Booked', 'Not Booked', 'Hold') THEN 1 END) as unclassified
        FROM campaign_metadata.gt_inventory
        WHERE "ID" >= 8000
        UNION ALL
        SELECT 
            'HRD Connect' as brand,
            COUNT(*) as total_slots,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Booked' THEN 1 END) as booked,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Not Booked' THEN 1 END) as available,
            COUNT(CASE WHEN "Booked/Not Booked" = 'Hold' THEN 1 END) as on_hold,
            COUNT(CASE WHEN "Booked/Not Booked" IS NULL OR "Booked/Not Booked" NOT IN ('Booked', 'Not Booked', 'Hold') THEN 1 END) as unclassified
        FROM campaign_metadata.hrd_inventory
        WHERE "ID" >= 8000
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        summary = []
        for row in results:
            # Add unclassified to available (they're essentially available slots)
            available_with_unclassified = row['available'] + row['unclassified']
            summary.append({
                'brand': row['brand'],
                'total_slots': row['total_slots'],
                'booked': row['booked'],
                'available': available_with_unclassified,
                'on_hold': row['on_hold'],
                'unclassified': row['unclassified']
            })
        
        return summary
        
    finally:
        cursor.close()
        conn.close()

def get_recent_bookings():
    """Get recent bookings from campaign ledger"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        query = """
        SELECT 
            "Client Name" as client,
            "Product Name - As per Listing Hub" as product,
            "Brand" as brand,
            "Scheduled Live Date" as start_date,
            "Schedule End Date" as end_date,
            "Status" as status
        FROM campaign_metadata.campaign_ledger
        ORDER BY "Scheduled Live Date" DESC
        LIMIT 10
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        bookings = []
        for row in results:
            bookings.append({
                'client': row['client'],
                'product': row['product'],
                'brand': row['brand'],
                'start_date': row['start_date'],
                'end_date': row['end_date'],
                'status': row['status']
            })
        
        return bookings
        
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        inventory_summary = get_inventory_summary()
        recent_bookings = get_recent_bookings()
        
        # Calculate totals
        total_slots = sum(item['total_slots'] for item in inventory_summary)
        total_booked = sum(item['booked'] for item in inventory_summary)
        total_available = sum(item['available'] for item in inventory_summary)
        total_on_hold = sum(item['on_hold'] for item in inventory_summary)
        
        return render_template_string(HTML_TEMPLATE, 
                                    inventory_summary=inventory_summary,
                                    recent_bookings=recent_bookings,
                                    total_slots=total_slots,
                                    total_booked=total_booked,
                                    total_available=total_available,
                                    total_on_hold=total_on_hold,
                                    datetime=datetime)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/api/inventory')
def api_inventory():
    """API endpoint for inventory data"""
    try:
        inventory_summary = get_inventory_summary()
        return jsonify(inventory_summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bookings')
def api_bookings():
    """API endpoint for recent bookings"""
    try:
        recent_bookings = get_recent_bookings()
        return jsonify(recent_bookings)
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
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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

        <!-- Brand Overview -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <!-- Brand Summary Table -->
            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h2 class="text-xl font-bold text-white mb-4">📈 Brand Overview</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead>
                            <tr class="border-b border-gray-700">
                                <th class="text-left py-2 text-gray-400">Brand</th>
                                <th class="text-right py-2 text-gray-400">Total</th>
                                <th class="text-right py-2 text-gray-400">Booked</th>
                                <th class="text-right py-2 text-gray-400">Available</th>
                                <th class="text-right py-2 text-gray-400">On Hold</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for brand in inventory_summary %}
                            <tr class="border-b border-gray-700">
                                <td class="py-2 text-white">{{ brand.brand }}</td>
                                <td class="py-2 text-right text-white">{{ brand.total_slots }}</td>
                                <td class="py-2 text-right text-green-400">{{ brand.booked }}</td>
                                <td class="py-2 text-right text-gray-400">{{ brand.available }}</td>
                                <td class="py-2 text-right text-yellow-400">{{ brand.on_hold }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Chart -->
            <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h2 class="text-xl font-bold text-white mb-4">📊 Utilization Chart</h2>
                <canvas id="utilizationChart" width="400" height="200"></canvas>
            </div>
        </div>

        <!-- Recent Bookings -->
        <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 class="text-xl font-bold text-white mb-4">📋 Recent Bookings</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="border-b border-gray-700">
                            <th class="text-left py-2 text-gray-400">Client</th>
                            <th class="text-left py-2 text-gray-400">Product</th>
                            <th class="text-left py-2 text-gray-400">Brand</th>
                            <th class="text-left py-2 text-gray-400">Start Date</th>
                            <th class="text-left py-2 text-gray-400">End Date</th>
                            <th class="text-left py-2 text-gray-400">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for booking in recent_bookings %}
                        <tr class="border-b border-gray-700">
                            <td class="py-2 text-white">{{ booking.client }}</td>
                            <td class="py-2 text-blue-400">{{ booking.product }}</td>
                            <td class="py-2 text-gray-400">{{ booking.brand }}</td>
                            <td class="py-2 text-gray-400">{{ booking.start_date }}</td>
                            <td class="py-2 text-gray-400">{{ booking.end_date }}</td>
                            <td class="py-2">
                                <span class="px-2 py-1 text-xs rounded-full 
                                    {% if booking.status == 'Active' %}bg-green-500 bg-opacity-20 text-green-400
                                    {% elif booking.status == 'Pending' %}bg-yellow-500 bg-opacity-20 text-yellow-400
                                    {% else %}bg-gray-500 bg-opacity-20 text-gray-400{% endif %}">
                                    {{ booking.status }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Chart.js configuration
        const ctx = document.getElementById('utilizationChart').getContext('2d');
        const chartData = {
            labels: ['Booked', 'Available', 'On Hold'],
            datasets: [{
                data: [{{ total_booked }}, {{ total_available }}, {{ total_on_hold }}],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(107, 114, 128, 0.8)',
                    'rgba(234, 179, 8, 0.8)'
                ],
                borderColor: [
                    'rgba(34, 197, 94, 1)',
                    'rgba(107, 114, 128, 1)',
                    'rgba(234, 179, 8, 1)'
                ],
                borderWidth: 2
            }]
        };

        new Chart(ctx, {
            type: 'doughnut',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'white',
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });

        // Auto-refresh every 30 seconds
        setTimeout(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True, port=5000)
