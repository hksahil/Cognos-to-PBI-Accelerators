# Connect to Power BI Service
Connect-PowerBIServiceAccount

# Define output CSV file
$outputFile = "$env:TEMP\PBI_Metadata.csv"

# Initialize an array to store metadata
$metadata = @()

# Get all Workspaces
$workspaces = Get-PowerBIWorkspace 

foreach ($workspace in $workspaces) {
    Write-Host "Processing workspace: $($workspace.Name)"
    
    # Get all Datasets in the Workspace
    $datasets = Get-PowerBIDataset -WorkspaceId $workspace.Id

    # Get all Reports in the Workspace
    $reports = Get-PowerBIReport -WorkspaceId $workspace.Id

    foreach ($dataset in $datasets) {
        # Get Dataset Credentials (Only if you have permissions)
        $datasetCreds = Get-PowerBIDataset -Id $dataset.Id -WorkspaceId $workspace.Id | Select-Object -ExpandProperty GatewayId -ErrorAction SilentlyContinue
        
        # Get Storage Mode (DirectQuery or Import)
        $storageMode = (Get-PowerBIDataset -WorkspaceId $workspace.Id -Id $dataset.Id).DefaultMode
        
        # Store Metadata
        $metadata += [PSCustomObject]@{
            Workspace_Name  = $workspace.Name
            Workspace_ID    = $workspace.Id
            Dataset_ID      = $dataset.Id
            Dataset_Creds   = if ($datasetCreds) { $datasetCreds } else { "N/A" }
            Report_Name     = "N/A"
            Report_ID       = "N/A"
            Storage_Mode    = $storageMode
        }
    }

    foreach ($report in $reports) {
        # Store Report Metadata
        $metadata += [PSCustomObject]@{
            Workspace_Name  = $workspace.Name
            Workspace_ID    = $workspace.Id
            Dataset_ID      = "N/A"
            Dataset_Creds   = "N/A"
            Report_Name     = $report.Name
            Report_ID       = $report.Id
            Storage_Mode    = "N/A"  # Reports don’t have storage mode
        }
    }
}

# Export to CSV
$metadata | Export-Csv -Path $outputFile -NoTypeInformation

Write-Host "✅ Metadata exported to: $outputFile"
