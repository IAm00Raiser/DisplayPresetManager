#!/usr/bin/env python3
"""
Helper module for better display position detection
"""

import ctypes
from ctypes import windll, byref, Structure, c_uint32, c_int32, c_void_p, POINTER
import win32api
import win32con

# Windows Display API structures
class DISPLAYCONFIG_DEVICE_INFO_HEADER(Structure):
    _fields_ = [
        ("type", c_uint32),
        ("size", c_uint32),
        ("adapterId", c_uint32 * 2),  # LUID
        ("id", c_uint32),
    ]

class DISPLAYCONFIG_SOURCE_MODE(Structure):
    _fields_ = [
        ("width", c_uint32),
        ("height", c_uint32),
        ("pixelFormat", c_uint32),
        ("position", c_int32 * 2),  # x, y coordinates
    ]

class DISPLAYCONFIG_TARGET_MODE(Structure):
    _fields_ = [
        ("targetVideoSignalInfo", c_uint32 * 4),
    ]

class DISPLAYCONFIG_DESKTOP_IMAGE_INFO(Structure):
    _fields_ = [
        ("PathSourceSize", c_uint32 * 2),
        ("DesktopImageRegion", c_uint32 * 4),
        ("DesktopImageClip", c_uint32 * 4),
    ]

class DISPLAYCONFIG_MODE_INFO(Structure):
    _fields_ = [
        ("infoType", c_uint32),
        ("id", c_uint32),
        ("adapterId", c_uint32 * 2),
        ("union", c_uint32 * 8),  # Union of different mode types
    ]

class DisplayPositionHelper:
    def __init__(self):
        self.user32 = windll.user32
        
    def get_display_positions(self):
        """Get positions of all displays using Windows Display API"""
        try:
            # Get the size needed for the buffer
            path_count = c_uint32()
            mode_count = c_uint32()
            
            result = self.user32.GetDisplayConfigBufferSizes(
                0x00000001,  # QDC_ONLY_ACTIVE_PATHS
                byref(path_count),
                byref(mode_count)
            )
            
            if result != 0:  # ERROR_SUCCESS
                return {}
            
            # Allocate buffers
            paths = (ctypes.c_uint32 * (path_count.value * 8))()  # Simplified path structure
            modes = (ctypes.c_uint32 * (mode_count.value * 8))()  # Simplified mode structure
            
            # Get the display configuration
            result = self.user32.QueryDisplayConfig(
                0x00000001,  # QDC_ONLY_ACTIVE_PATHS
                byref(path_count),
                paths,
                byref(mode_count),
                modes,
                None
            )
            
            if result != 0:
                return {}
            
            # Parse the results to get positions
            positions = {}
            # This is a simplified parsing - full implementation would require
            # more complex structure handling
            
            return positions
            
        except:
            return {}
    
    def get_display_positions_simple(self):
        """Get display positions using a simpler approach"""
        positions = {}
        
        try:
            # Use EnumDisplayMonitors to get monitor positions
            monitors = []
            
            def enum_monitor_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
                try:
                    # Define MONITORINFO structure inline
                    class MONITORINFO(Structure):
                        _fields_ = [
                            ("cbSize", ctypes.c_ulong),
                            ("rcMonitor", ctypes.c_int32 * 4),  # left, top, right, bottom
                            ("rcWork", ctypes.c_int32 * 4),
                            ("dwFlags", ctypes.c_ulong),
                        ]
                    
                    monitor_info = MONITORINFO()
                    monitor_info.cbSize = ctypes.sizeof(monitor_info)
                    
                    if self.user32.GetMonitorInfoA(hMonitor, byref(monitor_info)):
                        # Get device name for this monitor
                        device_name = f"\\\\.\\DISPLAY{len(dwData) + 1}"
                        position = (monitor_info.rcMonitor[0], monitor_info.rcMonitor[1])
                        size = (monitor_info.rcMonitor[2] - monitor_info.rcMonitor[0],
                               monitor_info.rcMonitor[3] - monitor_info.rcMonitor[1])
                        dwData.append({
                            'name': device_name,
                            'position': position,
                            'size': size
                        })
                except Exception as e:
                    print(f"Error in enum_monitor_proc: {e}")
                return True
            
            MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, 
                                                ctypes.c_void_p, ctypes.POINTER(ctypes.c_int32 * 4), 
                                                ctypes.c_void_p)
            self.user32.EnumDisplayMonitors(None, None, MonitorEnumProc(enum_monitor_proc), monitors)
            
            # Convert to dictionary
            for i, monitor in enumerate(monitors):
                device_name = f"\\\\.\\DISPLAY{i + 1}"
                positions[device_name] = monitor['position']
                
        except:
            pass
        
        return positions

def test_position_detection():
    """Test the position detection"""
    helper = DisplayPositionHelper()
    
    print("Testing Display Position Detection...")
    print("=" * 50)
    
    # Try simple method
    positions = helper.get_display_positions_simple()
    
    print(f"Found {len(positions)} display(s) with positions:")
    for device_name, position in positions.items():
        print(f"  {device_name}: {position}")
    
    return positions

if __name__ == "__main__":
    test_position_detection() 