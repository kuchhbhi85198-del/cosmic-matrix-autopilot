$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 15)
Set-ScheduledTask -TaskName 'CosmicMatrix_Morning_09AM' -Settings $settings
Set-ScheduledTask -TaskName 'CosmicMatrix_Evening_06PM' -Settings $settings
Write-Host "Cosmic Morning StartWhenAvailable:" (Get-ScheduledTask -TaskName 'CosmicMatrix_Morning_09AM').Settings.StartWhenAvailable
Write-Host "Cosmic Evening StartWhenAvailable:" (Get-ScheduledTask -TaskName 'CosmicMatrix_Evening_06PM').Settings.StartWhenAvailable
