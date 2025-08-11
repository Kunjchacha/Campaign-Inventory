import type { InventoryItem, Status } from './types';

// Master list of inventory capacity, transcribed from the provided spreadsheet image.
// 'monthly' represents the total number of slots available per month for that product/brand.
const masterInventoryConfig = [
  { productName: 'Press Release', productId: 'PR', brand: 'AA', monthly: 8 },
  { productName: 'Press Release', productId: 'PR', brand: 'CFO', monthly: 8 },
  { productName: 'Press Release', productId: 'PR', brand: 'GT', monthly: 8 },
  { productName: 'Press Release', productId: 'PR', brand: 'BG', monthly: 8 },
  { productName: 'Press Release', productId: 'PR', brand: 'HRD', monthly: 8 },
  { productName: 'Press Release', productId: 'PR', brand: 'CZ', monthly: 8 },
  { productName: 'Press Release', productId: 'PR', brand: 'SEW', monthly: 8 },
  { productName: 'Release Promotion', productId: 'PRP', brand: 'AA', monthly: 8 },
  { productName: 'Release Promotion', productId: 'PRP', brand: 'CFO', monthly: 8 },
  { productName: 'Release Promotion', productId: 'PRP', brand: 'GT', monthly: 8 },
  { productName: 'Release Promotion', productId: 'PRP', brand: 'BG', monthly: 8 },
  { productName: 'Release Promotion', productId: 'PRP', brand: 'HRD', monthly: 8 },
  { productName: 'Release Promotion', productId: 'PRP', brand: 'CZ', monthly: 8 },
  { productName: 'Release Promotion', productId: 'PRP', brand: 'SEW', monthly: 8 },
  { productName: 'NIAB Event Cover', productId: 'NIAB-EC', brand: 'AA', monthly: 4 },
  { productName: 'NIAB Event Cover', productId: 'NIAB-EC', brand: 'CFO', monthly: 4 },
  { productName: 'NIAB Event Cover', productId: 'NIAB-EC', brand: 'GT', monthly: 4 },
  { productName: 'NIAB Event Cover', productId: 'NIAB-EC', brand: 'BG', monthly: 4 },
  { productName: 'NIAB Event Cover', productId: 'NIAB-EC', brand: 'HRD', monthly: 4 },
  { productName: 'NIAB Event Cover', productId: 'NIAB-EC', brand: 'CZ', monthly: 4 },
  { productName: 'NIAB Event Cover', productId: 'NIAB-EC', brand: 'SEW', monthly: 4 },
  { productName: 'Original Content Production', productId: 'OCP', brand: 'AA', monthly: 12 },
  { productName: 'Original Content Production', productId: 'OCP', brand: 'CFO', monthly: 12 },
  { productName: 'Original Content Production', productId: 'OCP', brand: 'GT', monthly: 12 },
  { productName: 'Original Content Production', productId: 'OCP', brand: 'BG', monthly: 12 },
  { productName: 'Original Content Production', productId: 'OCP', brand: 'HRD', monthly: 12 },
  { productName: 'Original Content Production', productId: 'OCP', brand: 'CZ', monthly: 12 },
  { productName: 'Original Content Production', productId: 'OCP', brand: 'SEW', monthly: 12 },
  { productName: 'Hosted Content', productId: 'HC', brand: 'AA', monthly: 12 },
  { productName: 'Hosted Content', productId: 'HC', brand: 'CFO', monthly: 12 },
  { productName: 'Hosted Content', productId: 'HC', brand: 'GT', monthly: 12 },
  { productName: 'Hosted Content', productId: 'HC', brand: 'BG', monthly: 12 },
  { productName: 'Hosted Content', productId: 'HC', brand: 'HRD', monthly: 12 },
  { productName: 'Hosted Content', productId: 'HC', brand: 'CZ', monthly: 12 },
  { productName: 'Hosted Content', productId: 'HC', brand: 'SEW', monthly: 12 },
  { productName: 'Newsletter Lead Sponsor', productId: 'NLS-W', brand: 'AA', monthly: 4 },
  { productName: 'Newsletter Lead Sponsor', productId: 'NLS-W', brand: 'CFO', monthly: 4 },
  { productName: 'Newsletter Lead Sponsor', productId: 'NLS-W', brand: 'GT', monthly: 4 },
  { productName: 'Newsletter Lead Sponsor', productId: 'NLS-W', brand: 'BG', monthly: 4 },
  { productName: 'Newsletter Lead Sponsor', productId: 'NLS-W', brand: 'HRD', monthly: 4 },
  { productName: 'Newsletter Lead Sponsor', productId: 'NLS-W', brand: 'CZ', monthly: 4 },
  { productName: 'Newsletter Lead Sponsor', productId: 'NLS-W', brand: 'SEW', monthly: 4 },
  { productName: 'Newsletter Sponsorship-W', productId: 'NLS-WKD', brand: 'AA', monthly: 4 },
  { productName: 'Newsletter Sponsorship-W', productId: 'NLS-WKD', brand: 'CFO', monthly: 4 },
  { productName: 'Newsletter Sponsorship-W', productId: 'NLS-WKD', brand: 'GT', monthly: 4 },
  { productName: 'Newsletter Sponsorship-W', productId: 'NLS-WKD', brand: 'BG', monthly: 4 },
  { productName: 'Newsletter Sponsorship-W', productId: 'NLS-WKD', brand: 'HRD', monthly: 4 },
  { productName: 'Newsletter Sponsorship-W', productId: 'NLS-WKD', brand: 'CZ', monthly: 4 },
  { productName: 'Newsletter Sponsorship-W', productId: 'NLS-WKD', brand: 'SEW', monthly: 4 },
  { productName: 'Newsletter Featured Placement', productId: 'NLP-W', brand: 'AA', monthly: 8 },
  { productName: 'Newsletter Featured Placement', productId: 'NLP-W', brand: 'CFO', monthly: 8 },
  { productName: 'Newsletter Featured Placement', productId: 'NLP-W', brand: 'GT', monthly: 8 },
  { productName: 'Newsletter Featured Placement', productId: 'NLP-W', brand: 'BG', monthly: 8 },
  { productName: 'Newsletter Featured Placement', productId: 'NLP-W', brand: 'HRD', monthly: 8 },
  { productName: 'Newsletter Featured Placement', productId: 'NLP-W', brand: 'CZ', monthly: 8 },
  { productName: 'Newsletter Featured Placement', productId: 'NLP-W', brand: 'SEW', monthly: 8 },
  { productName: 'Newsletter Feature', productId: 'OCNP-W', brand: 'AA', monthly: 8 },
  { productName: 'Newsletter Feature', productId: 'OCNP-W', brand: 'CFO', monthly: 8 },
  { productName: 'Newsletter Feature', productId: 'OCNP-W', brand: 'GT', monthly: 8 },
  { productName: 'Newsletter Feature', productId: 'OCNP-W', brand: 'BG', monthly: 8 },
  { productName: 'Newsletter Feature', productId: 'OCNP-W', brand: 'HRD', monthly: 8 },
  { productName: 'Newsletter Feature', productId: 'OCNP-W', brand: 'CZ', monthly: 8 },
  { productName: 'Newsletter Feature', productId: 'OCNP-W', brand: 'SEW', monthly: 8 },
  { productName: 'Newsletter Category Sponsor', productId: 'NLC-TBI', brand: 'AA', monthly: 4 },
  { productName: 'Newsletter Category Sponsor', productId: 'NLC-TBI', brand: 'CFO', monthly: 4 },
  { productName: 'Newsletter Category Sponsor', productId: 'NLC-TBI', brand: 'GT', monthly: 4 },
  { productName: 'Newsletter Category Sponsor', productId: 'NLC-TBI', brand: 'BG', monthly: 4 },
  { productName: 'Newsletter Category Sponsor', productId: 'NLC-TBI', brand: 'HRD', monthly: 4 },
  { productName: 'Newsletter Category Sponsor', productId: 'NLC-TBI', brand: 'CZ', monthly: 4 },
  { productName: 'Newsletter Category Sponsor', productId: 'NLC-TBI', brand: 'SEW', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM1', productId: 'NLC-CUSTOM1', brand: 'AA', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM1', productId: 'NLC-CUSTOM1', brand: 'CFO', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM1', productId: 'NLC-CUSTOM1', brand: 'GT', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM1', productId: 'NLC-CUSTOM1', brand: 'BG', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM1', productId: 'NLC-CUSTOM1', brand: 'HRD', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM1', productId: 'NLC-CUSTOM1', brand: 'CZ', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM1', productId: 'NLC-CUSTOM1', brand: 'SEW', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM2', productId: 'NLC-CUSTOM2', brand: 'AA', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM2', productId: 'NLC-CUSTOM2', brand: 'CFO', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM2', productId: 'NLC-CUSTOM2', brand: 'GT', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM2', productId: 'NLC-CUSTOM2', brand: 'BG', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM2', productId: 'NLC-CUSTOM2', brand: 'HRD', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM2', productId: 'NLC-CUSTOM2', brand: 'CZ', monthly: 4 },
  { productName: 'Newsletter Category Sponsor-CUSTOM2', productId: 'NLC-CUSTOM2', brand: 'SEW', monthly: 4 },
  { productName: 'MailShot', productId: 'ML', brand: 'AA', monthly: 4 },
  { productName: 'MailShot', productId: 'ML', brand: 'CFO', monthly: 4 },
  { productName: 'MailShot', productId: 'ML', brand: 'GT', monthly: 4 },
  { productName: 'MailShot', productId: 'ML', brand: 'BG', monthly: 4 },
  { productName: 'MailShot', productId: 'ML', brand: 'HRD', monthly: 4 },
  { productName: 'MailShot', productId: 'ML', brand: 'CZ', monthly: 4 },
  { productName: 'MailShot', productId: 'ML', brand: 'SEW', monthly: 4 },
  { productName: 'LVB_Mailshot', productId: 'LVBML', brand: 'AA', monthly: 4 },
  { productName: 'Linkedin_Sponsor_Post', productId: 'LKSP', brand: 'AA', monthly: 20 },
  { productName: 'Linkedin_Sponsor_Post', productId: 'LKSP', brand: 'CFO', monthly: 20 },
  { productName: 'Linkedin_Sponsor_Post', productId: 'LKSP', brand: 'GT', monthly: 20 },
  { productName: 'Linkedin_Sponsor_Post', productId: 'LKSP', brand: 'BG', monthly: 20 },
  { productName: 'Linkedin_Sponsor_Post', productId: 'LKSP', brand: 'HRD', monthly: 20 },
  { productName: 'Linkedin_Sponsor_Post', productId: 'LKSP', brand: 'CZ', monthly: 20 },
  { productName: 'Linkedin_Sponsor_Post', productId: 'LKSP', brand: 'SEW', monthly: 20 },
  { productName: 'In_Social_Media', productId: 'LKDP', brand: 'AA', monthly: 8 },
  { productName: 'In_Social_Media', productId: 'LKDP', brand: 'CFO', monthly: 8 },
  { productName: 'In_Social_Media', productId: 'LKDP', brand: 'GT', monthly: 8 },
  { productName: 'In_Social_Media', productId: 'LKDP', brand: 'BG', monthly: 8 },
  { productName: 'In_Social_Media', productId: 'LKDP', brand: 'HRD', monthly: 8 },
  { productName: 'In_Social_Media', productId: 'LKDP', brand: 'CZ', monthly: 8 },
  { productName: 'In_Social_Media', productId: 'LKDP', brand: 'SEW', monthly: 8 },
  { productName: 'Under 35 Sponsor', productId: '35U35', brand: 'AA', monthly: 0 },
  { productName: '50 + 50 Sponsors', productId: '50+50', brand: 'AA', monthly: 0 },
  { productName: 'Sponsorship Event', productId: 'SE', brand: 'AA', monthly: 0 },
  { productName: 'Sponsorship Video Pro', productId: 'SVP', brand: 'AA', monthly: 0 },
  { productName: 'Sponsorship Survey', productId: 'SS', brand: 'AA', monthly: 0 },
  { productName: 'Sponsorship Report', productId: 'SR', brand: 'AA', monthly: 0 },
  { productName: 'Sponsorship Report Plan', productId: 'SRP', brand: 'AA', monthly: 0 },
  { productName: 'Sponsorship Video Pro', productId: 'SVP', brand: 'GT', monthly: 0 },
];

/**
 * Generates a detailed inventory list from the master configuration.
 * Each entry in the master list is expanded into individual slots based on 'monthly' count.
 * Statuses and mock data are assigned programmatically to create a realistic dataset.
 */
const generateInventoryData = (): InventoryItem[] => {
  const data: InventoryItem[] = [];
  let idCounter = 1;
  const clientPool = Array.from({ length: 20 }, (_, i) => `Client ${i + 1}`);

  masterInventoryConfig.forEach(config => {
    const totalSlots = config.monthly;
    if (totalSlots > 0) {
      // Define a realistic distribution for statuses
      const bookedCount = Math.ceil(totalSlots * (0.4 + Math.random() * 0.2)); // 40-60% booked
      const onHoldCount = Math.floor(totalSlots * (0.1 + Math.random() * 0.1)); // 10-20% on hold

      for (let i = 1; i <= totalSlots; i++) {
        let status: Status;
        let client: string | null = null;

        if (i <= bookedCount) {
          status = 'Booked';
          client = clientPool[Math.floor(Math.random() * clientPool.length)];
        } else if (i <= bookedCount + onHoldCount) {
          status = 'On Hold';
          client = clientPool[Math.floor(Math.random() * clientPool.length)];
        } else {
          status = 'Available';
        }

        const weekNum = Math.floor(Math.random() * 52) + 1;
        const startDate = new Date(2024, 0, (weekNum * 7) - 6);
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 6);

        data.push({
          id: idCounter++,
          slotName: `${config.productId}-${config.brand}-Slot${i}`,
          client: client,
          status: status,
          startDate: startDate.toISOString().split('T')[0],
          endDate: endDate.toISOString().split('T')[0],
          revenue: Math.floor(Math.random() * 4000) + 1000,
          product: config.productName,
          brand: config.brand,
        });
      }
    }
  });
  return data;
};

// --- EXPORTED CONSTANTS ---

export const inventoryData: InventoryItem[] = generateInventoryData();

export const statusStyles: Record<Status, { base: string; color: string; colorHex: string; }> = {
  Booked: {
    base: 'bg-green-500/20 text-green-300 border-green-500/30',
    color: 'bg-green-500',
    colorHex: '#22c55e'
  },
  'On Hold': {
    base: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
    color: 'bg-yellow-500',
    colorHex: '#eab308'
  },
  Available: {
    base: 'bg-slate-600/20 text-slate-300 border-slate-600/30',
    color: 'bg-slate-600',
    colorHex: '#475569'
  },
};

// Dynamically get unique products and brands from the master list
export const products: string[] = [...new Set(masterInventoryConfig.filter(i => i.monthly > 0).map(item => item.productName))].sort();
export const brands: string[] = [...new Set(masterInventoryConfig.map(item => item.brand))].sort();