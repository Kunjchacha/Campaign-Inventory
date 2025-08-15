# Campaign Inventory Dashboard

A React-based dashboard for managing and visualizing campaign inventory data from PostgreSQL database with real-time data synchronization.

## 🚀 Live Demo

**Live URL**: https://kunjchacha.github.io/Campaign-Inventory/

## ✨ Features

- **📊 Real-time Data**: Live data from PostgreSQL database with automatic deduplication
- **🎯 Brand Overview**: Interactive pie charts showing slot distribution for each brand
- **🔍 Advanced Filtering**: Filter by brand, product, and date ranges with precise results
- **📱 Responsive Design**: Fully responsive design for mobile and desktop
- **👥 Client Management**: View detailed client information and campaign data
- **📈 Status Tracking**: Real-time tracking of Booked, On Hold, and Available slots
- **🔄 Latest Data**: Always shows the most recent data using timestamp-based deduplication

## 🛠️ Technology Stack

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS
- **Backend**: Python Flask, asyncpg (PostgreSQL)
- **Database**: PostgreSQL (AWS RDS)
- **Deployment**: GitHub Pages

## 🚀 Quick Start

### Prerequisites

- Node.js (v18 or higher)
- Python 3.8+
- PostgreSQL database access

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/kunjchacha/Campaign-Inventory.git
cd Campaign-Inventory
```

2. **Install frontend dependencies:**
```bash
npm install
```

3. **Install backend dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure database connection in `server.py`:**
```python
DB_CONFIG = {
    'host': 'your-database-host',
    'port': 5432,
    'user': 'your-username',
    'password': 'your-password',
    'database': 'analytics'
}
```

### Running Locally

1. **Start the backend server:**
```bash
python server.py
```

2. **Start the frontend development server:**
```bash
npm run dev
```

3. **Open your browser and navigate to `http://localhost:5173`**

## 📊 Database Schema

### Inventory Tables
- `aa_inventory` - Accountancy Age inventory
- `bob_inventory` - Bobsguide inventory  
- `cfo_inventory` - The CFO inventory
- `gt_inventory` - Global Treasurer inventory
- `hrd_inventory` - HRD Connect inventory

### Campaign Ledger
- `campaign_ledger` - Client campaign information

## 🔌 API Endpoints

- `GET /api/inventory` - Get all inventory data (deduplicated)
- `GET /api/campaign-ledger` - Get campaign ledger data
- `GET /api/brand-overview` - Get brand overview statistics (latest data)
- `GET /api/preview-data` - Get filtered preview data with date filtering

## 📖 Usage Guide

### 1. **Brand Overview Section**
- View total slots and distribution for each brand
- Interactive pie charts showing Booked, On Hold, and Available percentages
- Unfiltered data showing complete brand statistics

### 2. **Filtering System**
- **Brand Selection**: Choose specific brand or "All Brands"
- **Product Selection**: Filter by Mailshots, Newsletter Sponsorship, etc.
- **Date Range**: Select specific date ranges (Aug 11-15, 2025)
- **Quick Views**: Predefined filters for Current Week, Month, Quarter, Year

### 3. **Preview Section**
- Shows filtered results based on your selections
- Real-time counts and percentages
- Affected only by filter selections (not Brand Overview)

### 4. **Client Details**
- Click "View Clients" button to see campaign information
- Filtered by current brand, product, and date selections

## 🔧 Key Technical Features

### Data Deduplication
- **Latest Record Priority**: Uses `last_updated` timestamp to get most recent data
- **Slot-based Deduplication**: Groups by Date + Slot to avoid duplicates
- **Automatic Handling**: No manual intervention required

### Date Filtering
- **Server-side Filtering**: Handles complex date formats in database
- **Text Date Support**: "Monday, August 11, 2025" format
- **Range Filtering**: Precise date range selection

### Status Normalization
- **Standardized Statuses**: Booked, On Hold, Available
- **Cross-table Consistency**: Same status values across all brands
- **Real-time Updates**: Reflects latest database changes

## 📁 Project Structure

```
Campaign-Inventory/
├── App.tsx                 # Main application component
├── components/             # React components
│   ├── BrandOverviewCard.tsx
│   ├── ClientModal.tsx
│   ├── PieChart.tsx
│   ├── ProductDetailCard.tsx
│   └── StatCard.tsx
├── hooks/                  # Custom React hooks
│   └── useDatabase.ts     # Database data fetching
├── services/               # API services
├── server.py              # Flask backend server
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies
└── vite.config.ts         # Vite configuration
```

## 🚀 Deployment

### Automatic Deployment
The dashboard is automatically deployed to GitHub Pages when you push to the main branch.

### Manual Deployment
```bash
npm run build
npm run deploy
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify database credentials in `server.py`
   - Check network connectivity to database

2. **CORS Issues**
   - Ensure backend server is running on port 5000
   - Check browser console for CORS errors

3. **Date Filtering Issues**
   - Verify date format in database
   - Check server logs for date parsing errors

4. **Build Errors**
   - Run `npm install` to ensure all dependencies are installed
   - Check Node.js version compatibility

### Debug Mode

Enable debug logging in the backend:
```python
app.run(debug=True, port=5000)
```

## 📈 Recent Updates

### Latest Fixes (Current Version)
- ✅ **Fixed Data Deduplication**: Now uses latest records only
- ✅ **Improved Date Filtering**: Server-side filtering for accuracy
- ✅ **Enhanced Brand Overview**: Shows correct totals and percentages
- ✅ **Mobile Responsiveness**: Full responsive design
- ✅ **Real-time Data**: Always shows most recent database state

### Data Accuracy
- **CFO Mailshots Aug 11-15, 2025**: 1 Booked slot (CFO-LUC01-ML-MAIN-1)
- **Deduplication**: Handles duplicate records automatically
- **Latest Timestamps**: Uses `last_updated` for most recent data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions, please contact the development team or create an issue in the repository.
