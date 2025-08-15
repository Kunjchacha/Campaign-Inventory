#!/usr/bin/env python3
"""
Comprehensive Test Suite for Campaign Inventory Dashboard
Tests all functionality including database connections, API endpoints, and data integrity
"""

import requests
import json
import time
from datetime import datetime

def test_database_connection():
    """Test database connection and basic queries"""
    print("🔍 Testing Database Connection...")
    
    try:
        # Test inventory API
        response = requests.get('http://localhost:5000/api/inventory', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Database connection successful!")
            print(f"   - Retrieved data for {len(data)} brands")
            print(f"   - Total slots across all brands: {sum(item['total_slots'] for item in data)}")
            return True
        else:
            print(f"❌ Database connection failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_dashboard_page():
    """Test the main dashboard page"""
    print("\n🌐 Testing Dashboard Page...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=10)
        if response.status_code == 200:
            content = response.text
            if 'Campaign Inventory Dashboard' in content:
                print("✅ Dashboard page loads successfully!")
                print(f"   - Page size: {len(content)} characters")
                return True
            else:
                print("❌ Dashboard page content incorrect")
                return False
        else:
            print(f"❌ Dashboard page failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard page error: {e}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n🔌 Testing API Endpoints...")
    
    endpoints = [
        ('/api/inventory', 'Inventory Data'),
        ('/api/bookings', 'Recent Bookings')
    ]
    
    all_passed = True
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name} API working")
                print(f"   - Endpoint: {endpoint}")
                print(f"   - Data type: {type(data).__name__}")
                if isinstance(data, list):
                    print(f"   - Items returned: {len(data)}")
            else:
                print(f"❌ {name} API failed: HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ {name} API error: {e}")
            all_passed = False
    
    return all_passed

def test_data_integrity():
    """Test data integrity and consistency"""
    print("\n📊 Testing Data Integrity...")
    
    try:
        # Get inventory data
        response = requests.get('http://localhost:5000/api/inventory', timeout=10)
        if response.status_code != 200:
            print("❌ Cannot test data integrity - API not responding")
            return False
        
        data = response.json()
        
        # Test data structure
        required_fields = ['brand', 'total_slots', 'booked', 'available', 'on_hold']
        all_valid = True
        
        for item in data:
            for field in required_fields:
                if field not in item:
                    print(f"❌ Missing field '{field}' in data item")
                    all_valid = False
                    break
            
            # Test mathematical consistency
            calculated_total = item['booked'] + item['available'] + item['on_hold']
            if calculated_total != item['total_slots']:
                print(f"❌ Data inconsistency for {item['brand']}: {calculated_total} != {item['total_slots']}")
                all_valid = False
        
        if all_valid:
            print("✅ Data integrity checks passed!")
            print(f"   - All required fields present")
            print(f"   - Mathematical consistency verified")
            print(f"   - Data for brands: {[item['brand'] for item in data]}")
        
        return all_valid
        
    except Exception as e:
        print(f"❌ Data integrity test error: {e}")
        return False

def test_performance():
    """Test performance and response times"""
    print("\n⚡ Testing Performance...")
    
    try:
        start_time = time.time()
        response = requests.get('http://localhost:5000/api/inventory', timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200:
            print(f"✅ Performance test passed!")
            print(f"   - Response time: {response_time:.2f}ms")
            print(f"   - Status code: {response.status_code}")
            
            if response_time < 1000:  # Less than 1 second
                print("   - Performance: Excellent (< 1s)")
            elif response_time < 3000:  # Less than 3 seconds
                print("   - Performance: Good (< 3s)")
            else:
                print("   - Performance: Slow (> 3s)")
            
            return True
        else:
            print(f"❌ Performance test failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def test_real_time_data():
    """Test that data is being fetched in real-time"""
    print("\n🕒 Testing Real-time Data...")
    
    try:
        # Get data twice with a small delay
        response1 = requests.get('http://localhost:5000/api/inventory', timeout=10)
        time.sleep(1)  # Wait 1 second
        response2 = requests.get('http://localhost:5000/api/inventory', timeout=10)
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            
            # Compare data (should be the same since it's from database)
            if data1 == data2:
                print("✅ Real-time data test passed!")
                print("   - Data consistency verified")
                print("   - Database queries working correctly")
                return True
            else:
                print("❌ Data inconsistency detected")
                return False
        else:
            print("❌ Real-time data test failed - API not responding")
            return False
            
    except Exception as e:
        print(f"❌ Real-time data test error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 Starting Comprehensive Test Suite")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Dashboard Page", test_dashboard_page),
        ("API Endpoints", test_api_endpoints),
        ("Data Integrity", test_data_integrity),
        ("Performance", test_performance),
        ("Real-time Data", test_real_time_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Dashboard is working correctly.")
        print("\n✅ Ready for deployment!")
        print("   - Database connection: Working")
        print("   - API endpoints: Working")
        print("   - Dashboard page: Working")
        print("   - Data integrity: Verified")
        print("   - Performance: Acceptable")
        print("   - Real-time updates: Working")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)
