# Campaign Inventory Dashboard

A real-time dashboard for tracking campaign inventory across all brands and products. Built with Python Flask and PostgreSQL, featuring a modern web interface with live data updates.

## 🚀 Features

- **Real-time Data**: Live inventory data from PostgreSQL database
- **Brand Overview**: Summary statistics for all brands (Accountancy Age, Bobsguide, The CFO, Global Treasurer, HRD Connect)
- **Interactive Charts**: Visual representation of inventory utilization
- **Recent Bookings**: Latest campaign bookings from the ledger
- **Auto-refresh**: Dashboard updates every 30 seconds
- **Responsive Design**: Works on desktop and mobile devices

## 📊 Dashboard Components

### Summary Cards
- **Total Slots**: Overall inventory capacity
- **Booked**: Currently booked slots
- **On Hold**: Slots on hold
- **Available**: Available slots for booking

### Brand Overview Table
- Detailed breakdown by brand
- Shows total, booked, available, and on-hold slots
- Real-time data from database

### Utilization Chart
- Interactive doughnut chart
- Visual representation of slot utilization
- Color-coded by status

### Recent Bookings
- Latest 10 bookings from campaign ledger
- Shows client, product, brand, dates, and status

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL with psycopg2
- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **Charts**: Chart.js
- **Deployment**: Ready for Render/Railway/Heroku

## 📋 Requirements

- Python 3.8+
- PostgreSQL database
- Required Python packages (see requirements.txt)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Update the database configuration in `simple_dashboard.py`:
```python
DB_CONFIG = {
    'host': 'your-database-host',
    'port': 5432,
    'database': 'your-database-name',
    'user': 'your-username',
    'password': 'your-password'
}
```

### 3. Run the Dashboard
```bash
python simple_dashboard.py
```

### 4. Access Dashboard
Open your browser and go to: `http://localhost:5000`

## 🧪 Testing

Run the comprehensive test suite:
```bash
python comprehensive_test.py
```

This will test:
- Database connection
- Dashboard page loading
- API endpoints
- Data integrity
- Performance
- Real-time data updates

## 📡 API Endpoints

### GET /api/inventory
Returns summary data for all brands:
```json
[
  {
    "brand": "Accountancy Age",
    "total_slots": 3363,
    "booked": 222,
    "available": 3078,
    "on_hold": 23,
    "unclassified": 40
  }
]
```

### GET /api/bookings
Returns recent bookings:
```json
[
  {
    "client": "Client Name",
    "product": "Product Name",
    "brand": "Brand Name",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "status": "Active"
  }
]
```

## 🗄️ Database Schema

The dashboard connects to PostgreSQL tables:
- `campaign_metadata.aa_inventory` - Accountancy Age inventory
- `campaign_metadata.bob_inventory` - Bobsguide inventory
- `campaign_metadata.cfo_inventory` - The CFO inventory
- `campaign_metadata.gt_inventory` - Global Treasurer inventory
- `campaign_metadata.hrd_inventory` - HRD Connect inventory
- `campaign_metadata.campaign_ledger` - Campaign bookings

## 🚀 Deployment

### Render (Recommended)
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn simple_dashboard:app`
4. Add environment variables if needed

### Railway
1. Connect your repository
2. Railway will auto-detect Python
3. Set start command: `gunicorn simple_dashboard:app`

### Heroku
1. Create a new Heroku app
2. Connect your repository
3. Add PostgreSQL addon
4. Deploy

## 📈 Performance

- **Response Time**: ~3-4 seconds for full dashboard load
- **Auto-refresh**: Every 30 seconds
- **Database Queries**: Optimized with proper indexing
- **Caching**: Built-in browser caching for static assets

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: Set to 'production' for deployment

### Customization
- Modify `HTML_TEMPLATE` in `simple_dashboard.py` for UI changes
- Update database queries for different data requirements
- Adjust auto-refresh interval in the JavaScript section

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check database credentials
   - Verify network connectivity
   - Ensure database is running

2. **Dashboard Not Loading**
   - Check if Flask server is running
   - Verify port 5000 is available
   - Check browser console for errors

3. **Data Not Updating**
   - Verify database has recent data
   - Check auto-refresh is enabled
   - Clear browser cache

### Debug Mode
Run with debug mode for detailed error messages:
```python
app.run(debug=True, port=5000)
```

## 📝 License

This project is proprietary and confidential.

## 🤝 Support

For technical support or questions, contact the development team.

---

**Last Updated**: August 15, 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready
