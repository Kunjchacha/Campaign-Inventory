import { useState, useEffect, useCallback } from 'react';
import type { DatabaseInventoryItem } from '../types';

// Mock MCP functions for now - these would be replaced with actual MCP calls
const mockMCPQuery = async (sql: string): Promise<any> => {
  // This is a placeholder - in reality, this would call the actual MCP functions
  console.log('MCP Query:', sql);
  
  // Return mock data based on the query
  if (sql.includes('aa_inventory')) {
    return [
      {
        id: 1,
        slot_name: 'PR-AA-Slot1',
        client: 'Client 1',
        status: 'Booked',
        start_date: '2024-01-01',
        end_date: '2024-01-07',
        product: 'Press Release',
        brand: 'AA'
      }
    ];
  }
  
  return [];
};

export const useDatabase = () => {
  const [inventoryData, setInventoryData] = useState<DatabaseInventoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchInventoryData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // In a real implementation, this would use the actual MCP functions
      // const result = await mcp_postgres_mcp_query({
      //   sql: "SELECT * FROM campaign_metadata.aa_inventory LIMIT 100"
      // });
      
      // For now, we'll use mock data that represents the structure
      const mockData: DatabaseInventoryItem[] = [
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
        },
        // Add more mock data for different products
        {
          id: 8,
          slot_name: 'NIAB-EC-AA-Slot1',
          client: 'Client 5',
          status: 'Booked',
          start_date: '2024-01-01',
          end_date: '2024-01-07',
          product: 'NIAB Event Cover',
          brand: 'AA',
          table_source: 'aa_inventory'
        },
        {
          id: 9,
          slot_name: 'OCP-GT-Slot1',
          client: 'Client 6',
          status: 'Booked',
          start_date: '2024-01-08',
          end_date: '2024-01-14',
          product: 'Original Content Production',
          brand: 'GT',
          table_source: 'gt_inventory'
        },
        {
          id: 10,
          slot_name: 'HC-CFO-Slot1',
          client: null,
          status: 'Available',
          start_date: '2024-01-15',
          end_date: '2024-01-21',
          product: 'Hosted Content',
          brand: 'CFO',
          table_source: 'cfo_inventory'
        }
      ];

      setInventoryData(mockData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch inventory data');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchInventoryData();
  }, [fetchInventoryData]);

  return {
    inventoryData,
    isLoading,
    error,
    refetch: fetchInventoryData,
    fetchInventoryData
  };
};
