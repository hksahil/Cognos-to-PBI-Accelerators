// Keep changing Table name to create same formulas in all tables
// How to use? Press run button then do CTRL+S

var table = Model.Tables["BrandSummary"];

string Variable = "TS";  
string Table = "'Tire Summary'";  


var measures = new[]

{  
new { Name = "CM Margin Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[CM_Margin]), SUM(" + Table + "[CM_Billed_Sales]), 0)" },
new { Name = "CM SOP CM Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[CM_SOP_CM_AMT]), SUM(" + Table + "[CM_SOP_UNITS]), 0)" },
new { Name = "CM AOP CM Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[CM_AOP_CM_AMT]), SUM(" + Table + "[CM_AOP_UNITS]), 0)" },
new { Name = "CMPY Margin Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[CMPY_Margin]), SUM(" + Table + "[CMPY_Billed_Sales]), 0)" },
new { Name = "PM Margin Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[PM_Margin]), SUM(" + Table + "[PM_Billed_SALES]), 0)" },
new { Name = "PM AOP CM Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[PM_AOP_CM_AMT]), SUM(" + Table + "[PM_AOP_UNITS]), 0)" },
new { Name = "PY Margin Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[PY_Collectible_Margin]), SUM(" + Table + "[PY_Billed_Sales]), 0)" },
new { Name = "SOP CM Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[SOP_CM_AMT]), SUM(" + Table + "[SOP_UNITS]), 0)" },
new { Name = "AOP CM Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[AOP_CM_AMT]), SUM(" + Table + "[AOP_UNITS]), 0)" },
new { Name = "YTD Margin Per Tire_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[YTD_Margin]), SUM(" + Table + "[YTD_Billed_Sales]), 0)" },
new { Name = "MTD Unit PAR_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[CM_BILLED_SALES]), SUM(" + Table + "[CM_SOP_UNITS]), 0)" },
new { Name = "Ship + Shippable Par_" + Variable, Formula = "DIVIDE(SUM(" + Table + "[SHIPPED___SHIPPABLE]), SUM(" + Table + "[CM_SOP_UNITS]), 0)" }
};


foreach (var x in measures)
{
    var newMeasure = table.AddMeasure(x.Name, x.Formula);
    newMeasure.FormatString = "0.00";
    newMeasure.Description = "This measure is " + measure.Name;
}

