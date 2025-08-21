# Campaign Inventory Dashboard

A modern, responsive dashboard for tracking campaign inventory across multiple brands and products. Built with HTML, CSS (Tailwind), and JavaScript for seamless deployment on GitHub Pages.

## 🚀 Live Demo

Visit the live dashboard: [Campaign Inventory Dashboard](https://Kunjchacha.github.io/Campaign-Inventory)

## ✨ Features

- **Real-time Inventory Tracking**: Monitor available, booked, and on-hold slots across all brands
- **Advanced Filtering**: Filter by product, brand, and date range
- **Upcoming Deliverables**: View next 2 weeks of scheduled deliverables
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations
- **Auto-refresh**: Automatically updates data every 30 seconds

## 🏗️ Project Structure

```
campaign-inventory/
├── index.html              # Main dashboard (GitHub Pages)
├── simple_dashboard.py     # Flask backend (local development)
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies (React app)
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## 🚀 Quick Start

### For GitHub Pages (Static Version)
The dashboard is automatically deployed to GitHub Pages and available at:
```
https://Kunjchacha.github.io/Campaign-Inventory
```

### For Local Development (Flask Backend)
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kunjchacha/Campaign-Inventory.git
   cd Campaign-Inventory
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application**:
   ```bash
   python simple_dashboard.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📊 Dashboard Components

### Summary Cards
- **Total Slots**: Overall inventory count
- **Booked**: Currently booked slots
- **On Hold**: Slots on hold status
- **Available**: Available for booking

### Filters
- **Product Filter**: Newsletter Sponsorship, Mailshot, Live Broadcast
- **Brand Filter**: AA, BG, CFO, GT, HRD
- **Date Range**: Custom date range selection

### Data Tables
- **Filtered Inventory Results**: Detailed slot information with client data
- **Upcoming Deliverables**: Next 2 weeks of scheduled deliverables

## 🎨 Technologies Used

- **Frontend**: HTML5, CSS3 (Tailwind CSS), JavaScript (ES6+)
- **Backend**: Python Flask (for local development)
- **Database**: PostgreSQL (AWS RDS)
- **Deployment**: GitHub Pages (static), Render (Flask)

## 🔧 Configuration

### Database Connection
The Flask backend connects to a PostgreSQL database with the following configuration:
- Host: AWS RDS instance
- Database: Analytics
- Tables: campaign_metadata schema

### Environment Variables
For local development, ensure your database credentials are properly configured in `simple_dashboard.py`.

## 📱 Responsive Design

The dashboard is fully responsive and optimized for:
- **Desktop**: Full feature set with side-by-side layouts
- **Tablet**: Adaptive grid layouts
- **Mobile**: Stacked layouts with touch-friendly controls

## 🔄 Auto-refresh

The dashboard automatically refreshes data every 30 seconds to ensure real-time information. In the static version, this updates the timestamp and would fetch new data in a production environment.

## 🚀 Deployment

### GitHub Pages (Current)
The static version is automatically deployed to GitHub Pages when changes are pushed to the main branch.

### Custom Deployment
For custom deployment:
1. Build the static files
2. Upload to your web server
3. Configure your domain

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary and confidential.

## 📞 Support

For support or questions, please contact the development team.

---

**Last Updated**: January 2025
**Version**: 2.0.0
