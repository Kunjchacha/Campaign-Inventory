from flask import Flask, render_template_string, jsonify, request
import psycopg2
import psycopg2.extras
from datetime import datetime

app = Flask(__name__)

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
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise e

def get_inventory_summary():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
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
            available_with_unclassified = row['available'] + row['unclassified']
            summary.append({
                'brand': row['brand'],
                'total_slots': row['total_slots'],
                'booked': row['booked'],
                'available': available_with_unclassified,
                'on_hold': row['on_hold']
            })
        
        return summary
        
    finally:
        cursor.close()
        conn.close()

def get_recent_bookings():
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
    try:
        inventory_summary = get_inventory_summary()
        recent_bookings = get_recent_bookings()
        
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

@app.route('/api/bookings')
def api_bookings():
    try:
        recent_bookings = get_recent_bookings()
        return jsonify(recent_bookings)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fixed HTML Template - No Scrolling Issues
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commercial Inventory Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* COMPLETE SCROLLING FIX */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            height: 100%;
            overflow-x: hidden;
        }
        
        body {
            height: 100%;
            overflow-y: auto;
            overflow-x: hidden;
            background-color: #0f172a;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Prevent any infinite scrolling */
        .dashboard-container {
            min-height: 100vh;
            max-width: 100%;
            overflow-x: hidden;
        }
        
        /* Fixed height sections */
        .section {
            margin-bottom: 2rem;
        }
        
        /* Responsive grid */
        .grid-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
        }
        
        @media (min-width: 1024px) {
            .grid-container {
                grid-template-columns: 1fr 1fr;
            }
        }
        
        /* Fix Chart.js canvas height issues */
        canvas {
            max-height: 300px !important;
            height: 300px !important;
        }
        
        .chart-container {
            height: 300px;
            max-height: 300px;
            overflow: hidden;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- Header -->
        <header class="bg-gray-800 border-b border-gray-700 p-6">
            <div class="max-w-7xl mx-auto text-center">
                <h1 class="text-3xl font-bold text-white mb-2">📊 Commercial Inventory Dashboard</h1>
                <p class="text-gray-300 text-lg">Track available slots for booking across all brands and products</p>
                <p class="text-gray-400 text-sm mt-2">Last updated: {{ datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}</p>
            </div>
        </header>

        <div class="max-w-7xl mx-auto p-6">
            <!-- Brand Overview Section -->
            <section class="section">
                <h2 class="text-2xl font-bold text-white mb-6">📈 Brand Overview - Total Inventory</h2>
                <div class="bg-gray-800 border border-gray-700 rounded-lg p-6">
                    {% for item in inventory_summary %}
                    <div class="mb-6 last:mb-0">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-semibold text-gray-200">{{ item.brand }}</h3>
                            <span class="text-lg text-gray-400">Total: {{ item.total_slots }} slots</span>
                        </div>
                        
                        <!-- Progress Bar -->
                        <div class="w-full bg-gray-700 rounded-full h-12 relative overflow-hidden mb-4">
                            {% set booked_percent = (item.booked / item.total_slots * 100) if item.total_slots > 0 else 0 %}
                            {% set on_hold_percent = (item.on_hold / item.total_slots * 100) if item.total_slots > 0 else 0 %}
                            {% set available_percent = (item.available / item.total_slots * 100) if item.total_slots > 0 else 0 %}
                            
                            <div class="h-full bg-green-500 flex items-center justify-center relative" style="width: {{ booked_percent }}%">
                                {% if booked_percent > 15 %}
                                <span class="text-white text-sm font-medium">{{ "%.1f"|format(booked_percent) }}%</span>
                                {% endif %}
                            </div>
                            
                            <div class="h-full bg-yellow-500 flex items-center justify-center relative" style="width: {{ on_hold_percent }}%; margin-left: {{ booked_percent }}%">
                                {% if on_hold_percent > 15 %}
                                <span class="text-white text-sm font-medium">{{ "%.1f"|format(on_hold_percent) }}%</span>
                                {% endif %}
                            </div>
                            
                            <div class="h-full bg-blue-500 flex items-center justify-center relative" style="width: {{ available_percent }}%; margin-left: {{ booked_percent + on_hold_percent }}%">
                                {% if available_percent > 15 %}
                                <span class="text-white text-sm font-medium">{{ "%.1f"|format(available_percent) }}%</span>
                                {% endif %}
                            </div>
                        </div>
                        
                        <!-- Legend -->
                        <div class="flex justify-between text-base text-gray-400">
                            <span class="flex items-center">
                                <div class="w-4 h-4 bg-green-500 rounded mr-3"></div>
                                Booked: {{ item.booked }}
                            </span>
                            <span class="flex items-center">
                                <div class="w-4 h-4 bg-yellow-500 rounded mr-3"></div>
                                On Hold: {{ item.on_hold }}
                            </span>
                            <span class="flex items-center">
                                <div class="w-4 h-4 bg-blue-500 rounded mr-3"></div>
                                Available: {{ item.available }}
                            </span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <!-- Main Content Grid -->
            <div class="grid-container">
                <!-- Analytics Charts -->
                <section class="bg-gray-800 border border-gray-700 rounded-lg p-6">
                    <h2 class="text-xl font-semibold text-white mb-6">📊 Analytics Overview</h2>
                    <div class="space-y-6">
                        <div>
                            <h3 class="text-lg font-medium text-gray-300 mb-4">Overall Utilization</h3>
                            <div class="chart-container">
                                <canvas id="utilizationChart"></canvas>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-lg font-medium text-gray-300 mb-4">Brand Comparison</h3>
                            <div class="chart-container">
                                <canvas id="brandChart"></canvas>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Recent Activity -->
                <section class="bg-gray-800 border border-gray-700 rounded-lg p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-xl font-semibold text-white">📋 Recent Activity</h2>
                        <button onclick="openClientModal()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors">
                            👥 View Clients
                        </button>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-base">
                            <thead>
                                <tr class="border-b border-gray-700">
                                    <th class="text-left py-4 text-gray-400 font-medium">Client</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">Product</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">Brand</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for booking in recent_bookings[:8] %}
                                <tr class="border-b border-gray-700">
                                    <td class="py-4 text-gray-200">{{ booking.client }}</td>
                                    <td class="py-4 text-blue-400">{{ booking.product }}</td>
                                    <td class="py-4 text-gray-400">{{ booking.brand }}</td>
                                    <td class="py-4">
                                        <span class="px-4 py-2 text-sm rounded-full 
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
                </section>
            </div>
        </div>
    </div>

    <!-- Client Modal -->
    <div id="clientModal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50">
        <div class="flex items-center justify-center min-h-screen p-6">
            <div class="bg-gray-800 rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto">
                <div class="p-8">
                    <div class="flex justify-between items-center mb-8">
                        <h2 class="text-3xl font-semibold text-white">👥 Client Bookings</h2>
                        <button onclick="closeClientModal()" class="text-gray-400 hover:text-white text-4xl">&times;</button>
                    </div>
                    <div id="clientModalContent" class="text-center py-8">
                        <p class="text-gray-400">Loading client data...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let utilizationChart, brandChart;

        function initializeCharts() {
            const utilizationCtx = document.getElementById('utilizationChart').getContext('2d');
            utilizationChart = new Chart(utilizationCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Booked', 'On Hold', 'Available'],
                    datasets: [{
                        data: [{{ total_booked }}, {{ total_on_hold }}, {{ total_available }}],
                        backgroundColor: ['#10B981', '#F59E0B', '#3B82F6'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#D1D5DB',
                                padding: 20,
                                font: { size: 14 }
                            }
                        }
                    }
                }
            });

            const brandCtx = document.getElementById('brandChart').getContext('2d');
            brandChart = new Chart(brandCtx, {
                type: 'bar',
                data: {
                    labels: [{% for item in inventory_summary %}'{{ item.brand }}'{% if not loop.last %}, {% endif %}{% endfor %}],
                    datasets: [{
                        label: 'Booked',
                        data: [{% for item in inventory_summary %}{{ item.booked }}{% if not loop.last %}, {% endif %}{% endfor %}],
                        backgroundColor: '#10B981'
                    }, {
                        label: 'On Hold',
                        data: [{% for item in inventory_summary %}{{ item.on_hold }}{% if not loop.last %}, {% endif %}{% endfor %}],
                        backgroundColor: '#F59E0B'
                    }, {
                        label: 'Available',
                        data: [{% for item in inventory_summary %}{{ item.available }}{% if not loop.last %}, {% endif %}{% endfor %}],
                        backgroundColor: '#3B82F6'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2,
                    scales: {
                        x: {
                            ticks: { color: '#D1D5DB', font: { size: 12 } },
                            grid: { color: '#374151' }
                        },
                        y: {
                            ticks: { color: '#D1D5DB', font: { size: 12 } },
                            grid: { color: '#374151' }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: { color: '#D1D5DB', font: { size: 14 } }
                        }
                    }
                }
            });
        }

        function openClientModal() {
            document.getElementById('clientModal').classList.remove('hidden');
            loadClientData();
        }

        function closeClientModal() {
            document.getElementById('clientModal').classList.add('hidden');
        }

        async function loadClientData() {
            try {
                const response = await fetch('/api/bookings');
                const bookings = await response.json();
                
                const content = document.getElementById('clientModalContent');
                content.innerHTML = `
                    <div class="overflow-x-auto">
                        <table class="w-full text-base">
                            <thead>
                                <tr class="border-b border-gray-700">
                                    <th class="text-left py-4 text-gray-400 font-medium">Client</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">Product</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">Brand</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">Start Date</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">End Date</th>
                                    <th class="text-left py-4 text-gray-400 font-medium">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${bookings.map(booking => `
                                    <tr class="border-b border-gray-700">
                                        <td class="py-4 text-gray-200">${booking.client}</td>
                                        <td class="py-4 text-blue-400">${booking.product}</td>
                                        <td class="py-4 text-gray-400">${booking.brand}</td>
                                        <td class="py-4 text-gray-400">${booking.start_date}</td>
                                        <td class="py-4 text-gray-400">${booking.end_date}</td>
                                        <td class="py-4">
                                            <span class="px-4 py-2 text-sm rounded-full 
                                                ${booking.status === 'Active' ? 'bg-green-500 bg-opacity-20 text-green-400' :
                                                  booking.status === 'Pending' ? 'bg-yellow-500 bg-opacity-20 text-yellow-400' :
                                                  'bg-gray-500 bg-opacity-20 text-gray-400'}">
                                                ${booking.status}
                                            </span>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            } catch (error) {
                document.getElementById('clientModalContent').innerHTML = `
                    <div class="text-center py-8">
                        <p class="text-red-400">Error loading client data</p>
                    </div>
                `;
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            initializeCharts();
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True, port=5001)
