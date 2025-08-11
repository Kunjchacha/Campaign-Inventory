export interface DatabaseInventoryItem {
  id: number;
  slot_name: string;
  client: string | null;
  status: string;
  start_date: string;
  end_date: string;
  revenue: number;
  product: string;
  brand: string;
  table_source: string;
}

export interface CampaignLedgerItem {
  id: number;
  campaign_name: string;
  client: string;
  product: string;
  brand: string;
  start_date: string;
  end_date: string;
  revenue: number;
  status: string;
}

export class DatabaseService {
  private static instance: DatabaseService;
  private baseUrl: string;

  private constructor() {
    this.baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:3001';
  }

  public static getInstance(): DatabaseService {
    if (!DatabaseService.instance) {
      DatabaseService.instance = new DatabaseService();
    }
    return DatabaseService.instance;
  }

  async fetchInventoryData(): Promise<DatabaseInventoryItem[]> {
    try {
      // For now, we'll use mock data structure based on the table names
      // In a real implementation, this would connect to your PostgreSQL database
      const mockData: DatabaseInventoryItem[] = [
        {
          id: 1,
          slot_name: 'PR-AA-Slot1',
          client: 'Client 1',
          status: 'Booked',
          start_date: '2024-01-01',
          end_date: '2024-01-07',
          revenue: 2500,
          product: 'Press Release',
          brand: 'AA',
          table_source: 'aa_inventory'
        },
        {
          id: 2,
          slot_name: 'PR-CFO-Slot1',
          client: 'Client 2',
          status: 'On Hold',
          start_date: '2024-01-08',
          end_date: '2024-01-14',
          revenue: 3000,
          product: 'Press Release',
          brand: 'CFO',
          table_source: 'cfo_inventory'
        },
        {
          id: 3,
          slot_name: 'PR-GT-Slot1',
          client: null,
          status: 'Available',
          start_date: '2024-01-15',
          end_date: '2024-01-21',
          revenue: 0,
          product: 'Press Release',
          brand: 'GT',
          table_source: 'gt_inventory'
        }
      ];

      return mockData;
    } catch (error) {
      console.error('Error fetching inventory data:', error);
      return [];
    }
  }

  async fetchCampaignLedger(): Promise<CampaignLedgerItem[]> {
    try {
      // Mock data for campaign ledger
      const mockData: CampaignLedgerItem[] = [
        {
          id: 1,
          campaign_name: 'Q1 Press Release Campaign',
          client: 'Client 1',
          product: 'Press Release',
          brand: 'AA',
          start_date: '2024-01-01',
          end_date: '2024-03-31',
          revenue: 25000,
          status: 'Active'
        },
        {
          id: 2,
          campaign_name: 'Q1 Newsletter Campaign',
          client: 'Client 2',
          product: 'Newsletter Lead Sponsor',
          brand: 'CFO',
          start_date: '2024-01-01',
          end_date: '2024-03-31',
          revenue: 15000,
          status: 'Active'
        }
      ];

      return mockData;
    } catch (error) {
      console.error('Error fetching campaign ledger:', error);
      return [];
    }
  }

  async fetchInventoryByBrand(brand: string): Promise<DatabaseInventoryItem[]> {
    const allData = await this.fetchInventoryData();
    return allData.filter(item => item.brand === brand);
  }

  async fetchInventoryByProduct(product: string): Promise<DatabaseInventoryItem[]> {
    const allData = await this.fetchInventoryData();
    return allData.filter(item => item.product === product);
  }

  async fetchInventoryByDateRange(startDate: string, endDate: string): Promise<DatabaseInventoryItem[]> {
    const allData = await this.fetchInventoryData();
    return allData.filter(item => {
      const itemStart = new Date(item.start_date);
      const itemEnd = new Date(item.end_date);
      const rangeStart = new Date(startDate);
      const rangeEnd = new Date(endDate);
      
      return itemStart <= rangeEnd && itemEnd >= rangeStart;
    });
  }
}
