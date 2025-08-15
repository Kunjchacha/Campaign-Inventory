import { Pool } from 'pg';
import type { DatabaseInventoryItem, CampaignLedgerItem } from '../types';

// Database configuration
const pool = new Pool({
  user: 'kunj.chacha@contentive.com',
  host: 'contentive-warehouse-instance-1.cq8sion7djdk.eu-west-2.rds.amazonaws.com',
  database: 'campaign_metadata',
  password: '(iRFw989b{5h',
  port: 5432,
});

// Function to map database products to dashboard products
const mapProductToDashboard = (mediaAsset: string): string | null => {
  const asset = mediaAsset?.toLowerCase() || '';
  
  // Mailshots (includes LVB_Mailshots)
  if (asset === 'mailshot' || asset === 'lvb_mailshot') {
    return 'Mailshots';
  }
  
  // Newsletter Sponsorship - Weekly
  if (asset === 'newsletter_sponsorship') {
    return 'Newsletter Sponsorship - Weekly';
  }
  
  // Newsletter Sponsorship - Weekender
  if (asset === 'weekender_newsletter_sponsorship') {
    return 'Newsletter Sponsorship - Weekender';
  }
  
  // Newsletter Placement (all Feature Placements)
  if (asset === 'newsletter_featured_placement' || asset === 'original_content_newsletter_feature_placement') {
    return 'Newsletter Placement';
  }
  
  // Newsletter Category Sponsorship
  if (asset === 'newsletter_category_sponsorship') {
    return 'Newsletter Category Sponsorship';
  }
  
  // Return null for products we don't want to show
  return null;
};

// Function to normalize status values
const normalizeStatus = (status: string): string => {
  const normalized = status?.toLowerCase().trim() || '';
  
  if (normalized === 'booked') {
    return 'Booked';
  }
  
  if (normalized === 'not booked' || normalized === 'not booked ') {
    return 'Available';
  }
  
  if (normalized === 'hold' || normalized === 'hold ' || normalized === 'on hold' || normalized === 'on hold ') {
    return 'On Hold';
  }
  
  // Default to Available for unknown statuses
  return 'Available';
};

// Function to map database brand names to dashboard brand names
const mapBrandToDashboard = (websiteName: string, tableSource: string): string => {
  const name = websiteName?.toLowerCase().trim() || '';
  
  // Map based on website name
  if (name === 'accountancy age') {
    return 'Accountancy Age';
  }
  if (name === 'hrd') {
    return 'HRD Connect';
  }
  
  // Map based on table source as fallback
  switch (tableSource) {
    case 'aa_inventory':
      return 'Accountancy Age';
    case 'bob_inventory':
      return 'Bobsguide';
    case 'cfo_inventory':
      return 'The CFO';
    case 'gt_inventory':
      return 'Global Treasurer';
    case 'hrd_inventory':
      return 'HRD Connect';
    default:
      return websiteName || 'Unknown';
  }
};

export class DatabaseService {
  static async fetchInventoryData(): Promise<DatabaseInventoryItem[]> {
    try {
      const inventoryTables = [
        'aa_inventory',
        'bob_inventory', 
        'cfo_inventory',
        'gt_inventory',
        'hrd_inventory'
      ];

      const allInventoryData: DatabaseInventoryItem[] = [];

      for (const table of inventoryTables) {
        try {
          const query = `SELECT * FROM campaign_metadata.${table} WHERE "ID" >= 8000 LIMIT 1000`;
          const result = await pool.query(query);
          
          if (result.rows && result.rows.length > 0) {
            console.log(`Processing ${result.rows.length} items from ${table}`);
            
            // Transform the data to match our interface
            const transformedData = result.rows.map((item: any) => {
              const mappedProduct = mapProductToDashboard(item["Media_Asset"] || item.product);
              
              // Only include items with mapped products (filter out unwanted products)
              if (!mappedProduct) {
                return null;
              }
              
              const transformedItem = {
                id: item.ID || item.id,
                slot_name: item["Inventory Slots"] || item.slot_name,
                client: item["Booking ID"] || item.client,
                status: normalizeStatus(item["Booked/Not Booked"] || item.status),
                start_date: item.Dates || item.start_date,
                end_date: item.Dates || item.end_date, // Using same date for now
                product: mappedProduct,
                brand: mapBrandToDashboard(item["Website_Name"] || item.brand, table),
                table_source: table
              };
              
              return transformedItem;
            }).filter(Boolean); // Remove null items
            
            console.log(`After filtering, ${transformedData.length} items from ${table}`);
            allInventoryData.push(...transformedData);
          }
        } catch (tableError) {
          console.warn(`Failed to fetch from ${table}:`, tableError);
          // Continue with other tables even if one fails
        }
      }

      return allInventoryData;
    } catch (error) {
      console.error('Database error:', error);
      throw error;
    }
  }

  static async fetchCampaignLedger(): Promise<CampaignLedgerItem[]> {
    try {
      const query = "SELECT * FROM campaign_metadata.campaign_ledger LIMIT 1000";
      const result = await pool.query(query);
      
      if (result.rows && result.rows.length > 0) {
        // Transform the campaign ledger data
        const transformedLedger = result.rows.map((item: any) => ({
          id: item.ID || item.id,
          campaign_name: item["Product Name - As per Listing Hub"] || item.campaign_name,
          client: item["Client Name"] || item.client,
          product: item["Product Name - As per Listing Hub"] || item.product,
          brand: item.Brand || item.brand,
          start_date: item["Scheduled Live Date"] || item.start_date,
          end_date: item["Schedule End Date"] || item.end_date,
          status: item.Status || item.status
        }));

        return transformedLedger;
      }
      
      return [];
    } catch (error) {
      console.error('Campaign ledger error:', error);
      throw error;
    }
  }

  static async closeConnection() {
    await pool.end();
  }
}
