this is the backup script
# === Power BI Connection Setup ===
Connect-PowerBIServiceAccount

# Define the workspace
$workspaceName = "APAC Managed - Plant Maintenance"
$workspace = Get-PowerBIWorkspace -Name $workspaceName

# === Define Local Output Folder with Today's Date ===
$today = Get-Date -Format "yyyy-MM-dd"
$localRootFolder = "/Users/nehashete/Downloads/Reports_$today"

# Create root folder if it doesn't exist
if (-not (Test-Path -Path $localRootFolder)) {
    New-Item -ItemType Directory -Force -Path $localRootFolder
}

# Check if workspace exists
if ($workspace) {
    Write-Host "Connected to workspace: $workspaceName"

    # Get all reports in the workspace
    $reports = Get-PowerBIReport -WorkspaceId $workspace.Id

    foreach ($report in $reports) {
        $reportName = $report.Name -replace '[\\/:*?"<>|]', ''  # Clean name for file system
        $outputFilePath = "$localRootFolder/$reportName.pbix"

        Write-Host "Exporting report: $reportName to $outputFilePath"

        try {
            # Export the report to a local file
            Export-PowerBIReport -Id $report.Id -WorkspaceId $workspace.Id -OutFile $outputFilePath -Verbose
            Write-Host "Exported: $reportName"
        } catch {
            Write-Host "Failed to export report: $reportName. Error: $_"
        }
    }
} else {
    Write-Host "The workspace named $workspaceName does not exist."
}
