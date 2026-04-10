$outputFile = "$env:USERPROFILE\laptop_metrics.txt"

# Force invariant culture for numeric formatting
$culture = [System.Globalization.CultureInfo]::InvariantCulture

if (!(Test-Path $outputFile)) {
    'date,hostname,os,uptime_hours,active_session_minutes,cpu_usage_percent,memory_usage_percent,disk_free_gb,health_status' | Out-File -FilePath $outputFile -Encoding utf8
}

while ($true) {
    $now = Get-Date
    $date = $now.ToString('yyyy-MM-dd HH:mm:ss')
    $hostname = $env:COMPUTERNAME

    $osInfo = Get-CimInstance Win32_OperatingSystem
    $os = $osInfo.Caption

    $lastBoot = $osInfo.LastBootUpTime
    $uptime = New-TimeSpan -Start $lastBoot -End $now

    $uptime_hours = [string]::Format($culture, "{0:F2}", $uptime.TotalHours)
    $active_session_minutes = [string]::Format($culture, "{0:F2}", $uptime.TotalMinutes)

    $cpuSample = Get-Counter '\Processor(_Total)\% Processor Time'
    $cpu_usage_percent = [string]::Format($culture, "{0:F1}", $cpuSample.CounterSamples[0].CookedValue)

    $totalMem = [double]$osInfo.TotalVisibleMemorySize
    $freeMem = [double]$osInfo.FreePhysicalMemory
    $usedMemPercent = (1 - ($freeMem / $totalMem)) * 100
    $memory_usage_percent = [string]::Format($culture, "{0:F1}", $usedMemPercent)

    $systemDrive = $env:SystemDrive
    $disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$systemDrive'"
    $disk_free_gb = [string]::Format($culture, "{0:F1}", ($disk.FreeSpace / 1GB))

    # Convert to numbers for logic (safe)
    $cpuNum = [double]$cpuSample.CounterSamples[0].CookedValue
    $memNum = $usedMemPercent
    $diskNum = $disk.FreeSpace / 1GB

    $health_status = 'Healthy'

    if ($cpuNum -ge 90 -or $memNum -ge 90 -or $diskNum -lt 10) {
        $health_status = 'Failure'
    }
    elseif ($cpuNum -ge 75 -or $memNum -ge 75 -or $diskNum -lt 25) {
        $health_status = 'Warning'
    }

    $line = '"' + $date + '","' + $hostname + '","' + $os + '",' +
            $uptime_hours + ',' +
            $active_session_minutes + ',' +
            $cpu_usage_percent + ',' +
            $memory_usage_percent + ',' +
            $disk_free_gb + ',"' +
            $health_status + '"'

    Add-Content -Path $outputFile -Value $line -Encoding utf8

    Start-Sleep -Seconds 1
}