# Dashboard Refactoring: Consolidated Inventory View

## Overview
This refactoring eliminates duplicate data fetching logic and consolidates all inventory data into a single, efficient endpoint that serves as the dashboard's data source.

## What Changed

### 1. **Backend (server.py)**
- **Enhanced `/api/inventory` endpoint**: Now supports filtering by brand, product, and date range
- **Removed `/api/preview-data` endpoint**: Deprecated in favor of the consolidated approach
- **Added filtering function**: `apply_filters_to_inventory()` handles all filtering logic
- **Single data source**: All inventory data comes from one consolidated query

### 2. **Frontend (hooks/useDatabase.ts)**
- **Updated `fetchPreviewData()`**: Now uses `/api/inventory` instead of `/api/preview-data`
- **Updated `fetchInventoryData()`**: Also uses the consolidated endpoint for consistency
- **Eliminated duplicate API calls**: Single endpoint serves all inventory needs

## Benefits

### ✅ **No More Duplicates**
- Single deduplication logic in one place
- Consistent data structure across all views
- No risk of mismatched data between endpoints

### ✅ **Better Performance**
- **Before**: Multiple database queries + frontend processing
- **After**: Single database query + server-side filtering
- Reduced network overhead and processing time

### ✅ **Easier Maintenance**
- One place to update inventory logic
- Consistent error handling
- Unified data transformation

### ✅ **Data Consistency**
- Same deduplication rules applied everywhere
- Consistent brand and product mapping
- Unified date handling (Excel serial numbers + text dates)

## Data Flow

### **Before (Multiple Endpoints)**
```
Dashboard → Multiple API calls → Different data sources → Potential inconsistencies
```

### **After (Consolidated)**
```
Dashboard → Single API call → Consolidated data → Consistent results
```

## Technical Details

### **Consolidated Data Structure**
```python
# Single query across all inventory tables
inventory_tables = [
    'aa_inventory',      # Accountancy Age
    'bob_inventory',     # Bobsguide
    'cfo_inventory',     # The CFO
    'gt_inventory',      # Global Treasurer
    'hrd_inventory'      # HRD Connect
]
```

### **Deduplication Logic**
```python
# Create unique key for each slot (Date + Slot)
slot_key = f"{item.get('Dates')}_{item.get('Slot', '')}"

# Keep the most recent record for each slot
if slot_key not in slot_records or (last_updated and 
    slot_records[slot_key]['last_updated'] and 
    last_updated > slot_records[slot_key]['last_updated']):
    slot_records[slot_key] = item
```

### **Filtering Support**
- **Brand filtering**: Filter by specific publication
- **Product filtering**: Filter by product type
- **Date filtering**: Filter by date range (handles Excel serial numbers)

## Migration Notes

### **For Developers**
- Use `/api/inventory` endpoint for all inventory data needs
- The old `/api/preview-data` endpoint is deprecated
- All filtering parameters work the same way

### **For Frontend**
- No changes needed in component logic
- Same data structure returned
- Better performance and reliability

## Testing

### **Verify the Changes**
1. Start the server: `python server.py`
2. Test the consolidated endpoint: `GET /api/inventory`
3. Test filtering: `GET /api/inventory?brand=Accountancy Age&product=Mailshots`
4. Verify no duplicate data is returned

### **Expected Results**
- Single, consistent data source
- No duplicate inventory slots
- Proper filtering by brand, product, and date
- Better performance and reliability

## Future Improvements

### **Potential Enhancements**
1. **Caching**: Add Redis caching for frequently accessed data
2. **Pagination**: Add pagination for large datasets
3. **Real-time updates**: WebSocket support for live inventory changes
4. **Advanced filtering**: Add more sophisticated filtering options

### **Monitoring**
- Track API response times
- Monitor data consistency
- Log any filtering or deduplication issues

## Conclusion

This refactoring transforms the dashboard from a system with multiple, potentially inconsistent data sources into a streamlined, efficient, and reliable single-source-of-truth architecture. The benefits in terms of performance, maintainability, and data consistency make this a significant improvement for the campaign inventory dashboard.
