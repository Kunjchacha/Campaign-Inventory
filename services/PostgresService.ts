import type { DatabaseInventoryItem, CampaignLedgerItem } from './DatabaseService';

export interface PostgresInventoryItem {
  id: number;
  slot_name: string;
  client: string | null;
  status: string;
  start_date: string;
  end_date: string;
  product: string;
  brand: string;
  table_source: string;
}

export interface PostgresCampaignLedgerItem {
  id: number;
  campaign_name: string;
  client: string;
  product: string;
  brand: string;
  start_date: string;
  end_date: string;
  status: string;
}

export class PostgresService {
  private static instance: PostgresService;

  private constructor() {}

  public static getInstance(): PostgresService {
    if (!PostgresService.instance) {
      PostgresService.instance = new PostgresService();
    }
    return PostgresService.instance;
  }

  // This method will be called by the MCP server to fetch data
  async fetchInventoryData(): Promise<PostgresInventoryItem[]> {
    try {
      // This is a placeholder - in reality, the MCP server would handle the database queries
      // and return the results through the mcp_postgres_mcp_query function
      
      // For now, we'll return mock data that represents the structure
      // In the real implementation, this would be replaced with actual database queries
      
      const mockData: PostgresInventoryItem[] = [
        {
          id: 1,
          slot_name: 'PR-AA-Slot1',
          client: 'Client 1',
          status: 'Booked',
          start_date: '2024-01-01',
          end_date: '2024-01-07',
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
          product: 'Press Release',
          brand: 'GT',
          table_source: 'gt_inventory'
        },
        {
          id: 4,
          slot_name: 'PR-BOB-Slot1',
          client: 'Client 3',
          status: 'Booked',
          start_date: '2024-01-22',
          end_date: '2024-01-28',
          product: 'Press Release',
          brand: 'BOB',
          table_source: 'bob_inventory'
        },
        {
          id: 5,
          slot_name: 'PR-CZ-Slot1',
          client: null,
          status: 'Available',
          start_date: '2024-01-29',
          end_date: '2024-02-04',
          product: 'Press Release',
          brand: 'CZ',
          table_source: 'cz_inventory'
        },
        {
          id: 6,
          slot_name: 'PR-HRD-Slot1',
          client: 'Client 4',
          status: 'On Hold',
          start_date: '2024-02-05',
          end_date: '2024-02-11',
          product: 'Press Release',
          brand: 'HRD',
          table_source: 'hrd_inventory'
        },
        {
          id: 7,
          slot_name: 'PR-SEW-Slot1',
          client: null,
          status: 'Available',
          start_date: '2024-02-12',
          end_date: '2024-02-18',
          product: 'Press Release',
          brand: 'SEW',
          table_source: 'sew_inventory'
        }
      ];

      return mockData;
    } catch (error) {
      console.error('Error fetching inventory data from PostgreSQL:', error);
      return [];
    }
  }

  async fetchCampaignLedger(): Promise<PostgresCampaignLedgerItem[]> {
    try {
      const mockData: PostgresCampaignLedgerItem[] = [
        {
          id: 1,
          campaign_name: 'Q1 Press Release Campaign',
          client: 'Client 1',
          product: 'Press Release',
          brand: 'AA',
          start_date: '2024-01-01',
          end_date: '2024-03-31',
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
          status: 'Active'
        },
        {
          id: 3,
          campaign_name: 'Q1 Content Production',
          client: 'Client 3',
          product: 'Original Content Production',
          brand: 'GT',
          start_date: '2024-01-01',
          end_date: '2024-03-31',
          status: 'Active'
        }
      ];

      return mockData;
    } catch (error) {
      console.error('Error fetching campaign ledger from PostgreSQL:', error);
      return [];
    }
  }

  async fetchInventoryByBrand(brand: string): Promise<PostgresInventoryItem[]> {
    const allData = await this.fetchInventoryData();
    return allData.filter(item => item.brand === brand);
  }

  async fetchInventoryByProduct(product: string): Promise<PostgresInventoryItem[]> {
    const allData = await this.fetchInventoryData();
    return allData.filter(item => item.product === product);
  }

  async fetchInventoryByDateRange(startDate: string, endDate: string): Promise<PostgresInventoryItem[]> {
    const allData = await this.fetchInventoryData();
    return allData.filter(item => {
      const itemStart = new Date(item.start_date);
      const itemEnd = new Date(item.end_date);
      const rangeStart = new Date(startDate);
      const rangeEnd = new Date(endDate);
      
      return itemStart <= rangeEnd && itemEnd >= rangeStart;
    });
  }

  async fetchInventoryByTableSource(tableSource: string): Promise<PostgresInventoryItem[]> {
    const allData = await this.fetchInventoryData();
    return allData.filter(item => item.table_source === tableSource);
  }

  // Method to get all available table sources
  getAvailableTableSources(): string[] {
    return [
      'aa_inventory',
      'bob_inventory', 
      'cfo_inventory',
      'cz_inventory',
      'gt_inventory',
      'hrd_inventory',
      'sew_inventory'
    ];
  }

  // Method to get all available brands
  getAvailableBrands(): string[] {
    return ['AA', 'BOB', 'CFO', 'CZ', 'GT', 'HRD', 'SEW'];
  }

  // Method to get all available products
  getAvailableProducts(): string[] {
    return [
      'Press Release',
      'Release Promotion',
      'NIAB Event Cover',
      'Original Content Production',
      'Hosted Content',
      'Newsletter Lead Sponsor',
      'Newsletter Sponsorship-W',
      'Newsletter Featured Placement',
      'Newsletter Feature',
      'Newsletter Category Sponsor',
      'Newsletter Category Sponsor-CUSTOM1',
      'Newsletter Category Sponsor-CUSTOM2',
      'MailShot',
      'LVB_Mailshot',
      'Linkedin_Sponsor_Post',
      'In_Social_Media'
    ];
  }
}
