# Install Power BI Module (if not installed)
Install-Module -Name MicrosoftPowerBIMgmt -Scope CurrentUser -Force -AllowClobber

# Connect to Power BI Service (Prompts for Login)
Connect-PowerBIServiceAccount

# Define Source & Target Workspaces
$sourceWorkspaceName = "prod"
$targetWorkspaceName = "Test"

# Get Workspace IDs
$sourceWorkspace = Get-PowerBIWorkspace -Name $sourceWorkspaceName
$targetWorkspace = Get-PowerBIWorkspace -Name $targetWorkspaceName

if (!$sourceWorkspace -or !$targetWorkspace) {
    Write-Host "Error: One or both workspaces not found. Check workspace names."
    exit
}

# Get Reports & Datasets from Source Workspace
$sourceReports = Get-PowerBIReport -WorkspaceId $sourceWorkspace.Id
$sourceDatasets = Get-PowerBIDataset -WorkspaceId $sourceWorkspace.Id

Write-Host "Found $($sourceReports.Count) reports and $($sourceDatasets.Count) datasets in the source workspace."

# Migrate Reports
foreach ($report in $sourceReports) {
    Write-Host "Exporting report: $($report.Name)"
    
    # Export Report from Source
    $exportPath = "$env:TEMP\$($report.Name).pbix"
    Export-PowerBIReport -WorkspaceId $sourceWorkspace.Id -Id $report.Id -OutFile $exportPath

    # Import Report into Target
    New-PowerBIReport -WorkspaceId $targetWorkspace.Id -Path $exportPath -Name $report.Name

    Write-Host "Successfully migrated report: $($report.Name)"
}

# Migrate Datasets (Reports need to be rebound)
$targetDatasets = Get-PowerBIDataset -WorkspaceId $targetWorkspace.Id

foreach ($report in (Get-PowerBIReport -WorkspaceId $targetWorkspace.Id)) {
    $matchingDataset = $targetDatasets | Where-Object { $_.Name -eq $report.Name }

    if ($matchingDataset) {
        Set-PowerBIReport -Id $report.Id -WorkspaceId $targetWorkspace.Id -DatasetId $matchingDataset.Id
        Write-Host "Rebound report '$($report.Name)' to dataset '$($matchingDataset.Name)'"
    }
}

Write-Host "✅ Migration Completed Successfully!"
