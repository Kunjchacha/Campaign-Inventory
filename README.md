# Campaign Inventory Dashboard

A comprehensive React-based dashboard for managing and visualizing campaign inventory data from multiple PostgreSQL database tables.

## Features

### 🗄️ Database Integration
- **Real-time Data**: Connected to PostgreSQL database tables via MCP (Model Context Protocol)
- **Multiple Table Sources**: 
  - `aa_inventory` - Accountancy Age inventory
  - `bob_inventory` - Business of Business inventory
  - `cfo_inventory` - CFO inventory
  - `cz_inventory` - CZ inventory
  - `gt_inventory` - GT inventory
  - `hrd_inventory` - HR Director inventory
  - `sew_inventory` - SEW inventory
  - `campaign_ledger` - Campaign tracking and revenue data

### 📊 Dashboard Components
- **Database Tables Overview**: Visual representation of all inventory tables with slot counts
- **Campaign Ledger**: Comprehensive view of active campaigns, revenue, and status
- **Real-time Statistics**: Live counts of booked, on-hold, and available slots
- **Advanced Filtering**: Filter by brand, product, table source, and date ranges
- **Interactive Charts**: Pie charts showing inventory distribution
- **Brand Overview Cards**: Individual statistics for each brand

### 🎯 Filtering & Search
- **Quick View Options**: Current month, next month, quarter, year views
- **Custom Date Ranges**: Flexible start/end date selection
- **Multi-level Filtering**: Combine brand, product, and table source filters
- **Real-time Updates**: Filters update statistics and charts instantly

## Technology Stack

- **Frontend**: React 19 + TypeScript
- **Build Tool**: Vite
- **Database**: PostgreSQL via MCP
- **Styling**: Tailwind CSS
- **Charts**: Custom PieChart component
- **State Management**: React Hooks (useState, useMemo, useCallback)

## Getting Started

### Prerequisites
- Node.js 18+ 
- PostgreSQL database access
- MCP server configured for PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd campaign-inventory
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   REACT_APP_API_URL=http://localhost:3001
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:5174` (or the port shown in your terminal)

## Database Schema

### Inventory Tables Structure
Each inventory table (`aa_inventory`, `bob_inventory`, etc.) contains:
- `id`: Unique identifier
- `slot_name`: Inventory slot identifier
- `client`: Client name (nullable for available slots)
- `status`: Slot status (Booked, On Hold, Available)
- `start_date`: Campaign start date
- `end_date`: Campaign end date
- `revenue`: Revenue amount
- `product`: Product type
- `brand`: Brand identifier
- `table_source`: Source table name

### Campaign Ledger Structure
The `campaign_ledger` table contains:
- `id`: Unique identifier
- `campaign_name`: Campaign name
- `client`: Client name
- `product`: Product type
- `brand`: Brand identifier
- `start_date`: Campaign start date
- `end_date`: Campaign end date
- `revenue`: Total campaign revenue
- `status`: Campaign status

## Usage

### Viewing Database Tables
1. **Database Overview Section**: See all inventory tables with slot counts
2. **Click on Table Cards**: Filter data by specific table source
3. **Table Source Filter**: Use the dropdown to filter by table source

### Filtering Data
1. **Quick Views**: Select predefined time periods
2. **Custom Dates**: Set specific start and end dates
3. **Brand Filter**: Filter by specific brand (AA, CFO, GT, etc.)
4. **Product Filter**: Filter by product type
5. **Combined Filters**: Use multiple filters simultaneously

### Analyzing Campaigns
1. **Campaign Ledger**: View all active campaigns
2. **Revenue Tracking**: Monitor total revenue across all campaigns
3. **Status Overview**: Track campaign status and performance

## Development

### Project Structure
```
campaign-inventory/
├── components/           # React components
│   ├── BrandOverviewCard.tsx
│   ├── CampaignLedgerCard.tsx
│   ├── ClientsModal.tsx
│   ├── DatabaseOverviewCard.tsx
│   ├── PieChart.tsx
│   └── ProductDetailCard.tsx
├── hooks/               # Custom React hooks
│   └── useDatabase.ts
├── services/            # Service layer
│   ├── DatabaseService.ts
│   ├── PostgresService.ts
│   └── GeminiService.ts
├── types.ts             # TypeScript type definitions
├── constants.ts         # Application constants
└── App.tsx             # Main application component
```

### Adding New Database Tables
1. **Update Types**: Add new table structure to `types.ts`
2. **Update Services**: Modify database services to include new tables
3. **Update UI**: Add new table cards to the overview section
4. **Update Filters**: Include new tables in filtering options

### Customizing Data Display
1. **Components**: Modify existing components or create new ones
2. **Hooks**: Extend `useDatabase` hook for additional functionality
3. **Services**: Add new database queries and data processing

## API Integration

### MCP PostgreSQL Functions
The application uses MCP (Model Context Protocol) to connect to PostgreSQL:
- `mcp_postgres_mcp_query`: Execute SQL queries
- `mcp_postgres_mcp_list_tables`: List available tables
- `mcp_postgres_mcp_describe_table`: Get table structure
- `mcp_postgres_mcp_get_table_sample`: Get sample data

### Custom Queries
Example queries for common operations:
```sql
-- Get inventory data from specific table
SELECT * FROM campaign_metadata.aa_inventory LIMIT 100;

-- Get campaign ledger data
SELECT * FROM campaign_metadata.campaign_ledger;

-- Filter by date range
SELECT * FROM campaign_metadata.aa_inventory 
WHERE start_date >= '2024-01-01' AND end_date <= '2024-12-31';
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes**
4. **Test thoroughly**: Ensure all filters and displays work correctly
5. **Submit a pull request**

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support, please contact the development team or create an issue in the repository.
