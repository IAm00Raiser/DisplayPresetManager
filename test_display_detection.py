#!/usr/bin/env python3
"""
Test script for display detection functionality
"""

from display_manager import EnhancedDisplayManager

def test_display_detection():
    print("Testing Display Detection...")
    print("=" * 40)
    
    try:
        # Create display manager
        dm = EnhancedDisplayManager()
        
        # Get display devices
        displays = dm.get_display_devices()
        print(f"Found {len(displays)} display device(s):")
        
        for i, device_name in enumerate(displays, 1):
            print(f"  {i}. {device_name}")
            
            # Get current settings
            config = dm.get_display_settings(device_name)
            if config:
                print(f"     Resolution: {config.resolution[0]}x{config.resolution[1]}")
                print(f"     Refresh Rate: {config.refresh_rate}Hz")
                print(f"     Position: {config.position}")
                print(f"     Orientation: {config.orientation}°")
                print(f"     Scale: {config.scale}%")
                
                # Get available resolutions
                resolutions = dm.get_available_resolutions(device_name)
                print(f"     Available resolutions: {len(resolutions)}")
                if resolutions:
                    print(f"       Sample: {resolutions[:3]}...")
            else:
                print(f"     Error: Could not get settings for {device_name}")
            print()
        
        print("Display detection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during display detection test: {e}")
        return False

if __name__ == "__main__":
    test_display_detection() 