param(
    [ValidateSet('Start', 'Stop', 'Status', 'InstallStartup', 'RemoveStartup')]
    [string]$Action = 'Status',
    [string]$Root = (Join-Path $env:LOCALAPPDATA 'HMSDeployment')
)

$ErrorActionPreference = 'Stop'
$Root = [System.IO.Path]::GetFullPath($Root)
$operationsPath = Join-Path $Root 'operations.json'
$operations = Get-Content -LiteralPath $operationsPath -Raw | ConvertFrom-Json
if ([System.IO.Path]::GetFullPath($operations.root) -ne $Root) {
    throw 'The operations root does not match the selected private directory.'
}
$controlPath = Join-Path $Root 'control.ps1'
$launcherPath = Join-Path $Root 'launch.py'
$pythonw = Join-Path (Split-Path -Parent $operations.python) 'pythonw.exe'
$stopPath = Join-Path $Root 'stop.request'
$taskName = 'HMS-se.d3va.dev'

function Test-Supervisor {
    $lockPath = Join-Path $Root 'supervisor.lock'
    if (-not (Test-Path -LiteralPath $lockPath)) { return $false }
    $stream = $null
    try {
        $stream = [System.IO.File]::Open($lockPath, 'Open', 'ReadWrite', 'ReadWrite')
        $stream.Lock(0, 1)
        $stream.Unlock(0, 1)
        return $false
    } catch [System.IO.IOException] {
        return $true
    } finally {
        if ($null -ne $stream) { $stream.Dispose() }
    }
}

switch ($Action) {
    'Start' {
        if (Test-Supervisor) { Write-Output 'HMS is already running.'; break }
        Remove-Item -LiteralPath $stopPath -ErrorAction SilentlyContinue
        if (-not (Test-Path -LiteralPath $controlPath)) {
            Copy-Item -LiteralPath $PSCommandPath -Destination $controlPath
        }
        if (-not (Test-Path -LiteralPath $launcherPath)) {
            Copy-Item -LiteralPath (Join-Path $operations.release 'deployment\launch.py') -Destination $launcherPath
        }
        $arguments = '"{0}" --config "{1}"' -f $launcherPath, $operationsPath
        $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
        if ($null -ne $task) {
            Start-ScheduledTask -TaskName $taskName
        } else {
            Start-Process -FilePath $pythonw -ArgumentList $arguments -WindowStyle Hidden | Out-Null
        }
        Write-Output 'HMS startup requested; inspect Status and the private logs.'
    }
    'Stop' {
        New-Item -ItemType File -Path $stopPath -Force | Out-Null
        $deadline = (Get-Date).AddSeconds(100)
        while ((Test-Supervisor) -and (Get-Date) -lt $deadline) { Start-Sleep -Seconds 1 }
        if (Test-Supervisor) { throw 'Shutdown is still in progress; inspect private logs. No unrelated process was killed.' }
        Write-Output 'HMS supervisor stopped. Startup remains paused until Start is used.'
    }
    'Status' {
        [pscustomobject]@{
            URL = 'https://se.d3va.dev/'
            SupervisorRunning = (Test-Supervisor)
            StopRequested = (Test-Path -LiteralPath $stopPath)
            Source = $operations.release
            PrivateLogs = (Join-Path $Root 'logs')
        }
    }
    'InstallStartup' {
        if ([System.IO.Path]::GetFullPath($PSCommandPath) -ne $controlPath) {
            Copy-Item -LiteralPath $PSCommandPath -Destination $controlPath -Force
        }
        Copy-Item -LiteralPath (Join-Path $operations.release 'deployment\launch.py') -Destination $launcherPath -Force
        $identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $arguments = '"{0}" --config "{1}"' -f $launcherPath, $operationsPath
        $taskAction = New-ScheduledTaskAction -Execute $pythonw -Argument $arguments -WorkingDirectory $Root
        $trigger = New-ScheduledTaskTrigger -AtLogOn -User $identity
        $principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
        $settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
        Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger $trigger -Principal $principal -Settings $settings -Description 'Private HMS laptop origin and Cloudflare Tunnel; starts after this user signs in.' -Force | Out-Null
        Write-Output 'HMS current-user logon startup registered. Sleep, shutdown and sign-out interrupt hosting.'
    }
    'RemoveStartup' {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
        Write-Output 'HMS logon startup removed; use Stop to stop an existing instance.'
    }
}
