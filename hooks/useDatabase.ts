import { useState, useEffect, useCallback } from 'react';
import type { DatabaseInventoryItem, CampaignLedgerItem } from '../types';

// Backend API URL - configurable for different environments
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://campaign-inventory-api.onrender.com/api'  // Update this with your actual deployed backend URL
  : 'http://localhost:5000/api';





export const useDatabase = () => {
  const [inventoryData, setInventoryData] = useState<DatabaseInventoryItem[]>([]);
  const [campaignLedger, setCampaignLedger] = useState<CampaignLedgerItem[]>([]);
  const [brandOverview, setBrandOverview] = useState<{[key: string]: any}>({});
  const [previewData, setPreviewData] = useState<DatabaseInventoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isUsingFallback, setIsUsingFallback] = useState(false);
  const [currentWeekData, setCurrentWeekData] = useState<any[]>([]);
  const [isLoadingCurrentWeek, setIsLoadingCurrentWeek] = useState(false);

  const fetchInventoryData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('Fetching consolidated inventory data from backend API...');
      const response = await fetch(`${API_BASE_URL}/inventory`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log(`Fetched ${data.length} consolidated inventory items from database`);
      
      setInventoryData(data);
      setIsUsingFallback(false);
    } catch (err) {
      console.error('Error fetching consolidated inventory data:', err);
      setInventoryData([]);
      setIsUsingFallback(false);
      setError('Database connection failed');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchCampaignLedger = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('Fetching campaign ledger from backend API...');
      const response = await fetch(`${API_BASE_URL}/campaign-ledger`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log(`Fetched ${data.length} campaign ledger items from database`);
      
      setCampaignLedger(data);
      setIsUsingFallback(false);
    } catch (err) {
      console.error('Error fetching campaign ledger:', err);
      setCampaignLedger([]);
      setIsUsingFallback(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchBrandOverview = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('Fetching brand overview from backend API...');
      const response = await fetch(`${API_BASE_URL}/brand-overview`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Fetched brand overview data:', data);
      
      setBrandOverview(data);
      setIsUsingFallback(false);
    } catch (err) {
      console.error('Error fetching brand overview:', err);
      setBrandOverview({});
      setIsUsingFallback(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchPreviewData = useCallback(async (brand: string, product: string, startDate?: string, endDate?: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('Fetching consolidated inventory data from backend API...');
      const params = new URLSearchParams({
        brand,
        product,
        ...(startDate && { start_date: startDate }),
        ...(endDate && { end_date: endDate })
      });
      
      // Use the consolidated inventory endpoint instead of preview-data
      const response = await fetch(`${API_BASE_URL}/inventory?${params}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log(`Fetched ${data.length} consolidated inventory items from database`);
      
      setPreviewData(data);
      setIsUsingFallback(false);
    } catch (err) {
      console.error('Error fetching consolidated inventory data:', err);
      setPreviewData([]);
      setIsUsingFallback(false);
      setError('Failed to fetch consolidated inventory data from backend.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchCurrentWeekData = useCallback(async () => {
    console.log('fetchCurrentWeekData: Starting...');
    setIsLoadingCurrentWeek(true);
    setError(null);
    
    try {
      console.log('Fetching current week inventory data...');
      const response = await fetch(`${API_BASE_URL}/current-week-inventory`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Current week data fetched successfully:', data);
      console.log('Current week data length:', data.length);
      setCurrentWeekData(data);
      console.log('Current week data set in state');
    } catch (err) {
      console.error('Error fetching current week data:', err);
      setCurrentWeekData([]);
      setError('Failed to fetch current week data');
    } finally {
      setIsLoadingCurrentWeek(false);
      console.log('fetchCurrentWeekData: Completed');
    }
  }, []);

  const fetchData = useCallback(async () => {
    await Promise.all([
      fetchInventoryData(),
      fetchCampaignLedger(),
      fetchBrandOverview(),
      fetchCurrentWeekData()
    ]);
  }, [fetchInventoryData, fetchCampaignLedger, fetchBrandOverview, fetchCurrentWeekData]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    inventoryData,
    campaignLedger,
    brandOverview,
    previewData,
    currentWeekData,
    isLoading,
    isLoadingCurrentWeek,
    error,
    isUsingFallback,
    refetch: fetchData,
    fetchInventoryData,
    fetchCampaignLedger,
    fetchBrandOverview,
    fetchPreviewData,
    fetchCurrentWeekData
  };
};
