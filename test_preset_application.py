#!/usr/bin/env python3
"""
Test script for preset application with position verification
"""

from display_manager import EnhancedDisplayManager
from display_presets import PresetManager
import time

def test_preset_application():
    print("Testing Preset Application with Position Verification...")
    print("=" * 60)
    
    try:
        dm = EnhancedDisplayManager()
        preset_manager = PresetManager()
        
        # Get available presets
        preset_names = preset_manager.get_preset_names()
        print(f"Found {len(preset_names)} preset(s): {preset_names}")
        
        if not preset_names:
            print("No presets found. Please create some presets first.")
            return False
        
        # Test each preset
        for preset_name in preset_names:
            print(f"\nTesting preset: {preset_name}")
            print("-" * 40)
            
            preset = preset_manager.presets[preset_name]
            
            # Show preset details
            print(f"Preset contains {len(preset.displays)} display(s):")
            for i, display_config in enumerate(preset.displays, 1):
                print(f"  Display {i}: {display_config.device_name}")
                print(f"    Resolution: {display_config.resolution[0]}x{display_config.resolution[1]}")
                print(f"    Position: {display_config.position}")
                print(f"    Refresh Rate: {display_config.refresh_rate}Hz")
            
            # Get current settings before applying
            print(f"\nCurrent settings before applying preset:")
            displays = dm.get_display_devices()
            current_configs = {}
            for device_name in displays:
                config = dm.get_display_settings(device_name)
                if config:
                    current_configs[device_name] = config
                    print(f"  {device_name}: Position {config.position}")
            
            # Apply the preset
            print(f"\nApplying preset '{preset_name}'...")
            success_count = 0
            
            for display_config in preset.displays:
                if dm.apply_display_settings(display_config):
                    success_count += 1
                    print(f"  ✓ Applied settings to {display_config.device_name}")
                else:
                    print(f"  ✗ Failed to apply settings to {display_config.device_name}")
            
            print(f"Applied settings to {success_count}/{len(preset.displays)} display(s)")
            
            # Wait a moment for changes to take effect
            time.sleep(3)
            
            # Verify the changes
            print(f"\nVerifying applied settings:")
            verification_success = True
            
            for display_config in preset.displays:
                device_name = display_config.device_name
                new_config = dm.get_display_settings(device_name)
                
                if new_config:
                    print(f"  {device_name}:")
                    print(f"    Expected Position: {display_config.position}")
                    print(f"    Actual Position: {new_config.position}")
                    
                    # Check if position was applied correctly
                    if new_config.position == display_config.position:
                        print(f"    ✓ Position correctly applied")
                    else:
                        print(f"    ✗ Position not applied correctly")
                        verification_success = False
                    
                    # Check other settings
                    if new_config.resolution == display_config.resolution:
                        print(f"    ✓ Resolution correctly applied")
                    else:
                        print(f"    ✗ Resolution not applied correctly")
                        verification_success = False
                        
                    if new_config.refresh_rate == display_config.refresh_rate:
                        print(f"    ✓ Refresh rate correctly applied")
                    else:
                        print(f"    ✗ Refresh rate not applied correctly")
                        verification_success = False
                else:
                    print(f"  ✗ Could not get settings for {device_name}")
                    verification_success = False
            
            if verification_success:
                print(f"\n✓ Preset '{preset_name}' applied successfully!")
            else:
                print(f"\n✗ Preset '{preset_name}' had issues with some settings")
            
            # Wait before testing next preset
            time.sleep(2)
        
        print(f"\nPreset application test completed!")
        return True
        
    except Exception as e:
        print(f"Error during preset application test: {e}")
        return False

if __name__ == "__main__":
    test_preset_application() 