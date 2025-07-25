!define APPNAME "Display Preset Manager"
!define COMPANYNAME "Your Company"
!define DESCRIPTION "A Windows system tray application for managing display configuration presets"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/yourusername/DisplayManager"
!define UPDATEURL "https://github.com/yourusername/DisplayManager/releases"
!define ABOUTURL "https://github.com/yourusername/DisplayManager"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
LicenseData "LICENSE.txt"
Name "${APPNAME}"
Icon "icon.ico"
outFile "DisplayPresetManager-Setup.exe"

!include LogicLib.nsh

page license
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
        messageBox mb_iconstop "Administrator rights required!"
        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        quit
${EndIf}
!macroend

function .onInit
        setShellVarContext all
        !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
        setOutPath $INSTDIR
        file "dist\DisplayPresetManager.exe"
        file "display_presets.json"
        file "README.md"
        file "LICENSE.txt"
        
        writeUninstaller "$INSTDIR\uninstall.exe"
        
        createDirectory "$SMPROGRAMS\${APPNAME}"
        createShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\DisplayPresetManager.exe"
        createShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
        
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\DisplayPresetManager.exe$\""
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "$\"${COMPANYNAME}$\""
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "$\"${HELPURL}$\""
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "$\"${UPDATEURL}$\""
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "$\"${ABOUTURL}$\""
        writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "$\"${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}$\""
        writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
        writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
        writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
        writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
        writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd

section "uninstall"
        delete "$INSTDIR\DisplayPresetManager.exe"
        delete "$INSTDIR\display_presets.json"
        delete "$INSTDIR\README.md"
        delete "$INSTDIR\LICENSE.txt"
        delete "$INSTDIR\uninstall.exe"
        
        rmDir "$INSTDIR"
        
        delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
        delete "$SMPROGRAMS\${APPNAME}\Uninstall.lnk"
        rmDir "$SMPROGRAMS\${APPNAME}"
        
        deleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
sectionEnd
