#!/usr/bin/env python3
"""
Test script for display position changes
"""

from display_manager import EnhancedDisplayManager
import time

def test_position_change():
    print("Testing Display Position Changes...")
    print("=" * 50)
    
    try:
        dm = EnhancedDisplayManager()
        displays = dm.get_display_devices()
        
        print(f"Found {len(displays)} display device(s):")
        
        for i, device_name in enumerate(displays, 1):
            print(f"\nDisplay {i}: {device_name}")
            
            # Get current settings
            config = dm.get_display_settings(device_name)
            if config:
                print(f"  Current Position: {config.position}")
                print(f"  Resolution: {config.resolution[0]}x{config.resolution[1]}")
                print(f"  Refresh Rate: {config.refresh_rate}Hz")
                
                # Test position change for all displays
                print(f"  Testing position change...")
                
                # Create a test config with different position
                from display_manager import DisplayConfig
                
                # Test different positions based on display number
                if i == 1:
                    # Primary display - test moving to a different position
                    test_position = (100, 100)
                else:
                    # Secondary display - test moving to the right of primary
                    test_position = (1920, 0)
                
                test_config = DisplayConfig(
                    device_name=device_name,
                    resolution=config.resolution,
                    refresh_rate=config.refresh_rate,
                    position=test_position,
                    orientation=config.orientation,
                    scale=config.scale
                )
                
                print(f"  Attempting to change position from {config.position} to {test_config.position}")
                
                # Apply the new position
                success = dm.apply_display_settings(test_config)
                print(f"  Position change {'successful' if success else 'failed'}")
                
                # Wait a moment
                time.sleep(2)
                
                # Check if position changed
                new_config = dm.get_display_settings(device_name)
                if new_config:
                    print(f"  New Position: {new_config.position}")
                    if new_config.position == test_position:
                        print(f"  ✓ Position successfully changed!")
                    else:
                        print(f"  ✗ Position change may not have taken effect")
                else:
                    print(f"  Could not get new position")
                
                # Test restoring original position
                print(f"  Restoring original position...")
                original_config = DisplayConfig(
                    device_name=device_name,
                    resolution=config.resolution,
                    refresh_rate=config.refresh_rate,
                    position=config.position,
                    orientation=config.orientation,
                    scale=config.scale
                )
                
                restore_success = dm.apply_display_settings(original_config)
                print(f"  Position restore {'successful' if restore_success else 'failed'}")
                
            else:
                print(f"  Error: Could not get settings")
        
        print("\nPosition change test completed!")
        return True
        
    except Exception as e:
        print(f"Error during position change test: {e}")
        return False

if __name__ == "__main__":
    test_position_change() 