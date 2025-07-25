#!/usr/bin/env python3
"""
Test script for display position detection
"""

from display_manager import EnhancedDisplayManager

def test_display_positions():
    print("Testing Display Position Detection...")
    print("=" * 50)
    
    try:
        dm = EnhancedDisplayManager()
        displays = dm.get_display_devices()
        
        print(f"Found {len(displays)} display device(s):")
        print()
        
        for i, device_name in enumerate(displays, 1):
            print(f"Display {i}: {device_name}")
            
            # Get current settings
            config = dm.get_display_settings(device_name)
            if config:
                print(f"  Resolution: {config.resolution[0]}x{config.resolution[1]}")
                print(f"  Refresh Rate: {config.refresh_rate}Hz")
                print(f"  Position: {config.position}")
                print(f"  Orientation: {config.orientation}°")
                print(f"  Scale: {config.scale}%")
                
                # Test position detection specifically
                position = dm.get_display_position(device_name)
                print(f"  Detected Position: {position}")
                
            else:
                print(f"  Error: Could not get settings")
            print()
        
        print("Position detection test completed!")
        return True
        
    except Exception as e:
        print(f"Error during position test: {e}")
        return False

if __name__ == "__main__":
    test_display_positions() 