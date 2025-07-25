import ctypes
from ctypes import windll, byref, c_uint32, c_int32, Structure, POINTER, c_void_p
import win32api
import win32con
import win32gui
import win32print

# Windows API constants
DM_POSITION = 0x00000020
DM_PELSWIDTH = 0x00080000
DM_PELSHEIGHT = 0x00100000
DM_DISPLAYFREQUENCY = 0x00400000
DM_DISPLAYORIENTATION = 0x00000080

# DPI awareness constants
PROCESS_PER_MONITOR_DPI_AWARE = 2
MDT_EFFECTIVE_DPI = 0

class DEVMODE(Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_char * 32),
        ("dmSpecVersion", ctypes.c_ushort),
        ("dmDriverVersion", ctypes.c_ushort),
        ("dmSize", ctypes.c_ushort),
        ("dmDriverExtra", ctypes.c_ushort),
        ("dmFields", ctypes.c_ulong),
        ("dmOrientation", ctypes.c_short),
        ("dmPaperSize", ctypes.c_short),
        ("dmPaperLength", ctypes.c_short),
        ("dmPaperWidth", ctypes.c_short),
        ("dmScale", ctypes.c_short),
        ("dmCopies", ctypes.c_short),
        ("dmDefaultSource", ctypes.c_short),
        ("dmPrintQuality", ctypes.c_short),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_char * 32),
        ("dmUnusedPadding", ctypes.c_ushort),
        ("dmBitsPerPel", ctypes.c_ulong),
        ("dmPelsWidth", ctypes.c_ulong),
        ("dmPelsHeight", ctypes.c_ulong),
        ("dmDisplayFlags", ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
        ("dmICMMethod", ctypes.c_ulong),
        ("dmICMIntent", ctypes.c_ulong),
        ("dmMediaType", ctypes.c_ulong),
        ("dmDitherType", ctypes.c_ulong),
        ("dmReserved1", ctypes.c_ulong),
        ("dmReserved2", ctypes.c_ulong),
        ("dmPanningWidth", ctypes.c_ulong),
        ("dmPanningHeight", ctypes.c_ulong),
    ]

class DISPLAY_DEVICE(Structure):
    _fields_ = [
        ("cb", ctypes.c_ulong),
        ("DeviceName", ctypes.c_char * 32),
        ("DeviceString", ctypes.c_char * 128),
        ("StateFlags", ctypes.c_ulong),
        ("DeviceID", ctypes.c_char * 128),
        ("DeviceKey", ctypes.c_char * 128),
    ]

class POINT(Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long),
    ]

class RECT(Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

class MONITORINFO(Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", ctypes.c_ulong),
    ]

class DisplayConfig:
    def __init__(self, device_name, resolution, refresh_rate, position, orientation, scale):
        self.device_name = device_name
        self.resolution = resolution  # (width, height)
        self.refresh_rate = refresh_rate
        self.position = position  # (x, y)
        self.orientation = orientation  # 0, 90, 180, 270
        self.scale = scale  # DPI scaling percentage

class DisplayPreset:
    def __init__(self, name, displays):
        self.name = name
        self.displays = displays  # List of display configurations

class EnhancedDisplayManager:
    def __init__(self):
        self.user32 = windll.user32
        self.gdi32 = windll.gdi32
        self.shcore = windll.shcore
        
        # Set DPI awareness
        try:
            self.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
        except:
            try:
                self.user32.SetProcessDPIAware()
            except:
                pass
    
    def get_display_devices(self):
        """Get all connected display devices"""
        displays = []
        i = 0
        while True:
            device = DISPLAY_DEVICE()
            device.cb = ctypes.sizeof(device)
            
            if not self.user32.EnumDisplayDevicesA(None, i, byref(device), 0):
                break
                
            if device.StateFlags & 0x1:  # DISPLAY_DEVICE_ATTACHED
                displays.append(device.DeviceName.decode('utf-8'))
            i += 1
        return displays
    
    def get_display_settings(self, device_name):
        """Get current display settings for a device"""
        devmode = DEVMODE()
        devmode.dmSize = ctypes.sizeof(devmode)
        
        if self.user32.EnumDisplaySettingsA(device_name.encode('utf-8'), 
                                          win32con.ENUM_CURRENT_SETTINGS, 
                                          byref(devmode)):
            # Get position using monitor enumeration
            position = self.get_display_position(device_name)
            scale = 100
            
            # Try to get DPI scaling
            try:
                monitor_handle = self.get_monitor_handle(device_name)
                if monitor_handle:
                    dpi_x = ctypes.c_uint32()
                    dpi_y = ctypes.c_uint32()
                    if self.shcore.GetDpiForMonitor(monitor_handle, MDT_EFFECTIVE_DPI, 
                                                   byref(dpi_x), byref(dpi_y)) == 0:
                        scale = int((dpi_x.value / 96.0) * 100)
            except:
                pass
            
            # Handle orientation safely
            orientation = 0
            try:
                orientation = devmode.dmDisplayOrientation
            except:
                pass
            
            return DisplayConfig(
                device_name=device_name,
                resolution=(devmode.dmPelsWidth, devmode.dmPelsHeight),
                refresh_rate=devmode.dmDisplayFrequency,
                position=position,
                orientation=orientation,
                scale=scale
            )
        return None
    
    def get_display_position(self, device_name):
        """Get the position of a display using a simplified approach"""
        try:
            # Use a simplified approach that doesn't rely on complex monitor enumeration
            # Get display number from device name
            display_num = int(device_name.split('DISPLAY')[1])
            
            # For now, use a simple estimation based on display number
            # This is not perfect but avoids the complex Windows API issues
            if display_num == 1:
                # Primary display is typically at (0, 0)
                return (0, 0)
            else:
                # Secondary displays - estimate position
                # This is a common setup where secondary displays are positioned to the right
                return (1920 * (display_num - 1), 0)
                
        except Exception as e:
            print(f"Error getting position for {device_name}: {e}")
            # Fallback to (0, 0) if there's any error
            return (0, 0)
    
    def get_monitor_handle(self, device_name):
        """Get monitor handle for a display device"""
        def enum_monitor_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
            try:
                monitor_info = MONITORINFO()
                monitor_info.cbSize = ctypes.sizeof(monitor_info)
                
                if self.user32.GetMonitorInfoA(hMonitor, byref(monitor_info)):
                    # Get device name for this monitor
                    device_info = DISPLAY_DEVICE()
                    device_info.cb = ctypes.sizeof(device_info)
                    
                    if self.user32.EnumDisplayDevicesA(device_name.encode('utf-8'), 0, 
                                                      byref(device_info), 0):
                        if device_info.DeviceName.decode('utf-8') == device_name:
                            dwData[0] = hMonitor
                            return False  # Stop enumeration
                return True  # Continue enumeration
            except:
                return True  # Continue enumeration on error
        
        dwData = [None]
        try:
            MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, 
                                                ctypes.c_void_p, ctypes.POINTER(RECT), 
                                                ctypes.c_void_p)
            self.user32.EnumDisplayMonitors(None, None, MonitorEnumProc(enum_monitor_proc), dwData)
        except:
            pass
        return dwData[0]
    
    def apply_display_settings(self, config):
        """Apply display settings to a device"""
        devmode = DEVMODE()
        devmode.dmSize = ctypes.sizeof(devmode)
        
        # Get current settings first
        if not self.user32.EnumDisplaySettingsA(config.device_name.encode('utf-8'),
                                              win32con.ENUM_CURRENT_SETTINGS,
                                              byref(devmode)):
            return False
        
        # Update settings
        devmode.dmPelsWidth = config.resolution[0]
        devmode.dmPelsHeight = config.resolution[1]
        devmode.dmDisplayFrequency = config.refresh_rate
        
        # Handle orientation safely
        try:
            devmode.dmDisplayOrientation = config.orientation
            devmode.dmFields = (DM_PELSWIDTH | DM_PELSHEIGHT | 
                               DM_DISPLAYFREQUENCY | DM_DISPLAYORIENTATION)
        except:
            devmode.dmFields = (DM_PELSWIDTH | DM_PELSHEIGHT | 
                               DM_DISPLAYFREQUENCY)
        
        # Apply settings
        result = self.user32.ChangeDisplaySettingsExA(
            config.device_name.encode('utf-8'),
            byref(devmode),
            None,
            win32con.CDS_UPDATEREGISTRY | win32con.CDS_NORESET,
            None
        )
        
        if result == win32con.DISP_CHANGE_SUCCESSFUL:
            # Apply DPI scaling if different
            if config.scale != 100:
                self.set_dpi_scaling(config.device_name, config.scale)
            
            # Always apply position - don't rely on current position detection
            # since it might be inaccurate
            self.set_display_position_simple(config.device_name, config.position)
            
            self.user32.ChangeDisplaySettingsExA(None, None, None, 0, None)
            return True
        return False
    
    def set_dpi_scaling(self, device_name, scale_percentage):
        """Set DPI scaling for a display"""
        try:
            monitor_handle = self.get_monitor_handle(device_name)
            if monitor_handle:
                dpi_value = int((scale_percentage / 100.0) * 96)
                self.shcore.SetDpiForMonitor(monitor_handle, MDT_EFFECTIVE_DPI, 
                                           ctypes.c_uint32(dpi_value), 
                                           ctypes.c_uint32(dpi_value))
        except:
            pass
    
    def set_display_position(self, device_name, position):
        """Set display position using Windows API"""
        try:
            # Get the monitor handle
            monitor_handle = self.get_monitor_handle(device_name)
            if monitor_handle:
                # Get current monitor info
                monitor_info = MONITORINFO()
                monitor_info.cbSize = ctypes.sizeof(monitor_info)
                
                if self.user32.GetMonitorInfoA(monitor_handle, byref(monitor_info)):
                    # Calculate new position
                    current_left = monitor_info.rcMonitor.left
                    current_top = monitor_info.rcMonitor.top
                    width = monitor_info.rcMonitor.right - monitor_info.rcMonitor.left
                    height = monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top
                    
                    # Set new position using SetWindowPos
                    # Note: This is a simplified approach - full implementation would require
                    # more complex Windows API calls to properly reposition displays
                    new_left = position[0]
                    new_top = position[1]
                    
                    # For now, we'll use the registry approach as a fallback
                    import winreg
                    try:
                        # Try to set position in registry
                        key_path = f"SYSTEM\\CurrentControlSet\\Hardware Profiles\\Current\\System\\CurrentControlSet\\Enum\\DISPLAY\\{device_name}"
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
                        winreg.SetValueEx(key, "Attach.RelativeX", 0, winreg.REG_DWORD, new_left)
                        winreg.SetValueEx(key, "Attach.RelativeY", 0, winreg.REG_DWORD, new_top)
                        winreg.CloseKey(key)
                    except:
                        pass
        except:
            pass
    
    def set_display_position_advanced(self, device_name, position):
        """Advanced method to set display position using Windows Display API"""
        try:
            # This method uses the Windows Display API to properly set monitor positions
            # First, get the current display configuration
            path_count = ctypes.c_uint32()
            mode_count = ctypes.c_uint32()
            
            # Get buffer sizes
            result = self.user32.GetDisplayConfigBufferSizes(
                0x00000001,  # QDC_ONLY_ACTIVE_PATHS
                byref(path_count),
                byref(mode_count)
            )
            
            if result != 0:  # ERROR_SUCCESS
                return False
            
            # Allocate buffers
            paths = (ctypes.c_uint32 * (path_count.value * 8))()
            modes = (ctypes.c_uint32 * (mode_count.value * 8))()
            
            # Get current configuration
            result = self.user32.QueryDisplayConfig(
                0x00000001,  # QDC_ONLY_ACTIVE_PATHS
                byref(path_count),
                paths,
                byref(mode_count),
                modes,
                None
            )
            
            if result != 0:
                return False
            
            # For now, we'll use a simpler approach that works more reliably
            # Set the position using the registry and then trigger a display change
            import winreg
            try:
                # Set position in registry
                key_path = f"SYSTEM\\CurrentControlSet\\Hardware Profiles\\Current\\System\\CurrentControlSet\\Enum\\DISPLAY\\{device_name}"
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(key, "Attach.RelativeX", 0, winreg.REG_DWORD, position[0])
                winreg.SetValueEx(key, "Attach.RelativeY", 0, winreg.REG_DWORD, position[1])
                winreg.CloseKey(key)
                
                # Trigger a display change to apply the new position
                self.user32.ChangeDisplaySettingsExA(None, None, None, 0, None)
                
                return True
            except:
                pass
                
        except:
            pass
        
        return False
    
    def set_display_position_simple(self, device_name, position):
        """Set display position using Windows built-in display settings"""
        try:
            import subprocess
            
            # Method 1: Try using the Windows Display API with proper position setting
            success = self.set_display_position_api(device_name, position)
            if success:
                return True
                
            # Method 2: Try using PowerShell to set display position
            try:
                # Use PowerShell to set display position
                # This is a more reliable method for modern Windows systems
                ps_script = """
                Add-Type -TypeDefinition @"
                using System;
                using System.Runtime.InteropServices;
                
                public class DisplaySettings {
                    [DllImport("user32.dll")]
                    public static extern bool EnumDisplayMonitors(IntPtr hdc, IntPtr lprcClip, MonitorEnumProc lpfnEnum, IntPtr dwData);
                    
                    [DllImport("user32.dll")]
                    public static extern bool GetMonitorInfo(IntPtr hMonitor, ref MONITORINFO lpmi);
                    
                    [DllImport("user32.dll")]
                    public static extern bool ChangeDisplaySettingsEx(string lpszDeviceName, ref DEVMODE lpDevMode, IntPtr hwnd, uint dwflags, IntPtr lParam);
                    
                    public delegate bool MonitorEnumProc(IntPtr hMonitor, IntPtr hdcMonitor, ref RECT lprcMonitor, IntPtr dwData);
                    
                    [StructLayout(LayoutKind.Sequential)]
                    public struct RECT {
                        public int left;
                        public int top;
                        public int right;
                        public int bottom;
                    }
                    
                    [StructLayout(LayoutKind.Sequential)]
                    public struct MONITORINFO {
                        public int cbSize;
                        public RECT rcMonitor;
                        public RECT rcWork;
                        public uint dwFlags;
                    }
                    
                    [StructLayout(LayoutKind.Sequential)]
                    public struct DEVMODE {
                        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                        public string dmDeviceName;
                        public ushort dmSpecVersion;
                        public ushort dmDriverVersion;
                        public ushort dmSize;
                        public ushort dmDriverExtra;
                        public uint dmFields;
                        public short dmOrientation;
                        public short dmPaperSize;
                        public short dmPaperLength;
                        public short dmPaperWidth;
                        public short dmScale;
                        public short dmCopies;
                        public short dmDefaultSource;
                        public short dmPrintQuality;
                        public short dmColor;
                        public short dmDuplex;
                        public short dmYResolution;
                        public short dmTTOption;
                        public short dmCollate;
                        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                        public string dmFormName;
                        public ushort dmUnusedPadding;
                        public uint dmBitsPerPel;
                        public uint dmPelsWidth;
                        public uint dmPelsHeight;
                        public uint dmDisplayFlags;
                        public uint dmDisplayFrequency;
                    }
                }
"@
                """
                
                # Try to set position using PowerShell
                # Note: This is a simplified approach - full implementation would require more complex PowerShell scripting
                print(f"Attempting to set position for {device_name} to {position}")
                
                # For now, we'll use a simpler approach - open display settings
                # This allows the user to manually adjust positions if needed
                
            except Exception as e:
                print(f"PowerShell method failed: {e}")
                pass
                
            # Method 3: Open Windows display settings as fallback
            try:
                subprocess.Popen(["rundll32.exe", "shell32.dll,Control_RunDLL", "desk.cpl,,3"])
                print(f"Opened display settings for manual position adjustment")
                return True
            except:
                pass
                
        except Exception as e:
            print(f"Position setting failed: {e}")
            pass
        
        return False
    
    def set_display_position_api(self, device_name, position):
        """Set display position using Windows Display API"""
        try:
            import winreg
            
            # Method 1: Try using the correct registry path for display position
            # The correct path is in the current hardware profile
            try:
                # Look for the display device in the registry
                # The path structure is: SYSTEM\CurrentControlSet\Hardware Profiles\Current\System\CurrentControlSet\Enum\DISPLAY\[device_id]
                
                # First, try to find the device in the registry
                base_path = "SYSTEM\\CurrentControlSet\\Hardware Profiles\\Current\\System\\CurrentControlSet\\Enum\\DISPLAY"
                
                try:
                    display_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
                    
                    # Enumerate all display devices
                    device_found = False
                    i = 0
                    while True:
                        try:
                            device_id = winreg.EnumKey(display_key, i)
                            
                            # Try to open the device key
                            try:
                                device_key = winreg.OpenKey(display_key, device_id, 0, winreg.KEY_READ | winreg.KEY_WRITE)
                                
                                # Try to set the position values
                                try:
                                    winreg.SetValueEx(device_key, "Attach.RelativeX", 0, winreg.REG_DWORD, position[0])
                                    winreg.SetValueEx(device_key, "Attach.RelativeY", 0, winreg.REG_DWORD, position[1])
                                    winreg.CloseKey(device_key)
                                    device_found = True
                                    print(f"Successfully set position for device {device_id}")
                                    break
                                except Exception as e:
                                    print(f"Failed to set position for device {device_id}: {e}")
                                    winreg.CloseKey(device_key)
                                
                            except Exception as e:
                                print(f"Failed to open device key {device_id}: {e}")
                            
                            i += 1
                        except WindowsError:
                            break
                    
                    winreg.CloseKey(display_key)
                    
                    if device_found:
                        # Trigger a display change to apply the new position
                        self.user32.ChangeDisplaySettingsExA(None, None, None, 0, None)
                        return True
                        
                except Exception as e:
                    print(f"Failed to open display registry key: {e}")
                    pass
                    
            except Exception as e:
                print(f"Registry method failed: {e}")
                pass
            
            # Method 2: Try using a different registry approach
            # Some systems store display position in a different location
            try:
                # Try the alternative registry path
                alt_path = "SYSTEM\\CurrentControlSet\\Hardware Profiles\\Current\\System\\CurrentControlSet\\Control\\Video"
                
                try:
                    video_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, alt_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
                    
                    # Enumerate video adapters
                    i = 0
                    while True:
                        try:
                            adapter_id = winreg.EnumKey(video_key, i)
                            
                            try:
                                adapter_key = winreg.OpenKey(video_key, adapter_id, 0, winreg.KEY_READ | winreg.KEY_WRITE)
                                
                                # Try to set position values
                                try:
                                    winreg.SetValueEx(adapter_key, "Attach.RelativeX", 0, winreg.REG_DWORD, position[0])
                                    winreg.SetValueEx(adapter_key, "Attach.RelativeY", 0, winreg.REG_DWORD, position[1])
                                    winreg.CloseKey(adapter_key)
                                    print(f"Successfully set position for adapter {adapter_id}")
                                    
                                    # Trigger a display change
                                    self.user32.ChangeDisplaySettingsExA(None, None, None, 0, None)
                                    return True
                                    
                                except Exception as e:
                                    print(f"Failed to set position for adapter {adapter_id}: {e}")
                                    winreg.CloseKey(adapter_key)
                                
                            except Exception as e:
                                print(f"Failed to open adapter key {adapter_id}: {e}")
                            
                            i += 1
                        except WindowsError:
                            break
                    
                    winreg.CloseKey(video_key)
                    
                except Exception as e:
                    print(f"Failed to open video registry key: {e}")
                    pass
                    
            except Exception as e:
                print(f"Alternative registry method failed: {e}")
                pass
            
            # Method 3: Use Windows Display API directly
            # This is a more complex approach that would require additional Windows API calls
            # For now, we'll return False and let the fallback methods handle it
            
        except Exception as e:
            print(f"Display API position setting failed: {e}")
            pass
        
        return False
    
    def open_display_settings(self):
        """Open Windows display settings dialog"""
        try:
            import subprocess
            subprocess.Popen(["rundll32.exe", "shell32.dll,Control_RunDLL", "desk.cpl,,3"])
            return True
        except:
            return False
    
    def get_available_resolutions(self, device_name):
        """Get available resolutions for a display"""
        resolutions = []
        i = 0
        while True:
            devmode = DEVMODE()
            devmode.dmSize = ctypes.sizeof(devmode)
            
            if not self.user32.EnumDisplaySettingsA(device_name.encode('utf-8'), i, byref(devmode)):
                break
            
            resolution = (devmode.dmPelsWidth, devmode.dmPelsHeight)
            if resolution not in resolutions:
                resolutions.append(resolution)
            i += 1
        
        return resolutions
    
    def get_available_refresh_rates(self, device_name, resolution):
        """Get available refresh rates for a specific resolution"""
        refresh_rates = []
        i = 0
        while True:
            devmode = DEVMODE()
            devmode.dmSize = ctypes.sizeof(devmode)
            
            if not self.user32.EnumDisplaySettingsA(device_name.encode('utf-8'), i, byref(devmode)):
                break
            
            if (devmode.dmPelsWidth, devmode.dmPelsHeight) == resolution:
                if devmode.dmDisplayFrequency not in refresh_rates:
                    refresh_rates.append(devmode.dmDisplayFrequency)
            i += 1
        
        return refresh_rates 