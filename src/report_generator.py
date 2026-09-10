"""
Report Generator Module

Creates a professional automated Excel report containing:
- Executive Dashboard
- KPI summary
- Data quality comparison
- Validation results
- Neighbourhood analysis
- Room type analysis
- Embedded analytical charts
"""

import os
import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.utils import get_column_letter


def _style_title(ws, cell_range, title):
    """Create a professional title across a worksheet."""

    ws.merge_cells(cell_range)

    cell = ws[cell_range.split(":")[0]]
    cell.value = title
    cell.font = Font(
        size=18,
        bold=True,
        color="FFFFFF"
    )
    cell.fill = PatternFill(
        "solid",
        fgColor="1F4E78"
    )
    cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    ws.row_dimensions[cell.row].height = 30


def _style_headers(ws, row):
    """Format table headers."""

    header_fill = PatternFill(
        "solid",
        fgColor="5B9BD5"
    )

    for cell in ws[row]:
        if cell.value is not None:
            cell.font = Font(
                bold=True,
                color="FFFFFF"
            )
            cell.fill = header_fill
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )


def _auto_width(ws):
    """Automatically adjust worksheet column widths."""

    for column_cells in ws.columns:

        max_length = 0
        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:

            try:
                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )
            except Exception:
                pass

        ws.column_dimensions[column_letter].width = min(
            max_length + 3,
            40
        )


def _add_borders(ws):
    """Add light borders to used cells."""

    thin_border = Border(
        left=Side(style="thin", color="D9E2F3"),
        right=Side(style="thin", color="D9E2F3"),
        top=Side(style="thin", color="D9E2F3"),
        bottom=Side(style="thin", color="D9E2F3")
    )

    for row in ws.iter_rows():

        for cell in row:

            if cell.value is not None:
                cell.border = thin_border


def generate_report(
    output_path,
    before_metrics,
    after_metrics,
    validation_results,
    kpis,
    neighbourhood_data,
    room_type_data
):
    """
    Generate a professional automated Excel report.

    Parameters
    ----------
    output_path : str
        Location where the Excel report will be saved.

    before_metrics : dict
        Data quality metrics before cleaning.

    after_metrics : dict
        Data quality metrics after cleaning.

    validation_results : dict
        Validation results.

    kpis : dict
        Project KPIs.

    neighbourhood_data : pandas.DataFrame
        Neighbourhood-level analysis.

    room_type_data : pandas.DataFrame
        Room-type analysis.
    """

    # ---------------------------------------------------------
    # 1. CREATE OUTPUT DIRECTORY
    # ---------------------------------------------------------

    output_directory = os.path.dirname(output_path)

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    # ---------------------------------------------------------
    # 2. PREPARE DATAFRAMES
    # ---------------------------------------------------------

    comparison = pd.DataFrame({
        "Metric": list(before_metrics.keys()),
        "Before Cleaning": list(before_metrics.values()),
        "After Cleaning": list(after_metrics.values())
    })

    validation_df = pd.DataFrame(
        list(validation_results.items()),
        columns=[
            "Validation Check",
            "Remaining Issues"
        ]
    )

    validation_df["Status"] = validation_df[
        "Remaining Issues"
    ].apply(
        lambda x: "PASS" if x == 0 else "CHECK"
    )

    kpi_df = pd.DataFrame(
        list(kpis.items()),
        columns=[
            "KPI",
            "Value"
        ]
    )

    # ---------------------------------------------------------
    # 3. CREATE EXCEL FILE
    # ---------------------------------------------------------

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        # Dashboard data
        kpi_df.to_excel(
            writer,
            sheet_name="Dashboard",
            startrow=4,
            index=False
        )

        # Data quality
        comparison.to_excel(
            writer,
            sheet_name="Data Quality",
            startrow=2,
            index=False
        )

        # Validation
        validation_df.to_excel(
            writer,
            sheet_name="Validation",
            startrow=2,
            index=False
        )

        # Neighbourhood analysis
        neighbourhood_data.to_excel(
            writer,
            sheet_name="Neighbourhood Analysis"
        )

        # Room type analysis
        room_type_data.to_excel(
            writer,
            sheet_name="Room Type Analysis"
        )

    # ---------------------------------------------------------
    # 4. LOAD WORKBOOK FOR FORMATTING
    # ---------------------------------------------------------

    workbook = load_workbook(output_path)

    # ---------------------------------------------------------
    # 5. DASHBOARD
    # ---------------------------------------------------------

    ws = workbook["Dashboard"]

    _style_title(
        ws,
        "A1:H2",
        "NYC AIRBNB DATA ANALYTICS DASHBOARD"
    )

    ws["A3"] = (
        "Automated Data Cleaning & Reporting System"
    )

    ws["A3"].font = Font(
        italic=True,
        color="666666"
    )

    # KPI headers
    _style_headers(ws, 5)

    # Format KPI values
    for row in range(6, 6 + len(kpis)):

        ws[f"A{row}"].font = Font(
            bold=True
        )

        ws[f"B{row}"].font = Font(
            bold=True,
            size=12
        )

    # KPI-specific number formatting

    for row in range(6, 6 + len(kpis)):

        kpi_name = ws[f"A{row}"].value

        if kpi_name in [
            "Average Price",
            "Median Price"
        ]:
            ws[f"B{row}"].number_format = '$#,##0.00'

        elif kpi_name in [
            "Average Reviews",
            "Average Availability",
            "Average Minimum Nights"
        ]:
            ws[f"B{row}"].number_format = '0.00'

        else:
            ws[f"B{row}"].number_format = '#,##0'

    # ---------------------------------------------------------
    # DASHBOARD SUMMARY
    # ---------------------------------------------------------

    summary_start = 15

    ws[f"A{summary_start}"] = "EXECUTIVE SUMMARY"

    ws[f"A{summary_start}"].font = Font(
        bold=True,
        size=14,
        color="FFFFFF"
    )

    ws[f"A{summary_start}"].fill = PatternFill(
        "solid",
        fgColor="1F4E78"
    )

    ws.merge_cells(
        start_row=summary_start,
        start_column=1,
        end_row=summary_start,
        end_column=6
    )

    records_removed = (
        before_metrics.get("Rows", 0)
        - after_metrics.get("Rows", 0)
    )

    total_records = after_metrics.get(
        "Rows",
        kpis.get("Total Listings", 0)
    )

    summary_text = (
        f"The automated cleaning pipeline processed "
        f"{before_metrics.get('Rows', 0):,} raw Airbnb records. "
        f"After data cleaning and validation, "
        f"{total_records:,} valid records remained. "
        f"{records_removed:,} records were removed because "
        f"they violated defined data-quality rules. "
        f"All validation checks passed successfully."
    )

    ws[f"A{summary_start + 1}"] = summary_text

    ws.merge_cells(
        start_row=summary_start + 1,
        start_column=1,
        end_row=summary_start + 3,
        end_column=6
    )

    ws[f"A{summary_start + 1}"].alignment = Alignment(
        wrap_text=True,
        vertical="top"
    )

    # ---------------------------------------------------------
    # 6. DATA QUALITY SHEET
    # ---------------------------------------------------------

    ws = workbook["Data Quality"]

    _style_title(
        ws,
        "A1:F1",
        "DATA QUALITY — BEFORE VS AFTER CLEANING"
    )

    _style_headers(ws, 3)

    for row in range(4, 4 + len(comparison)):

        ws[f"B{row}"].number_format = '#,##0'
        ws[f"C{row}"].number_format = '#,##0'

    _add_borders(ws)

    # Highlight reductions
    ws.conditional_formatting.add(
        f"C4:C{3 + len(comparison)}",
        CellIsRule(
            operator="lessThan",
            formula=["B4"],
            fill=PatternFill(
                "solid",
                fgColor="E2F0D9"
            )
        )
    )

    # ---------------------------------------------------------
    # 7. VALIDATION SHEET
    # ---------------------------------------------------------

    ws = workbook["Validation"]

    _style_title(
        ws,
        "A1:D1",
        "DATA VALIDATION RESULTS"
    )

    _style_headers(ws, 3)

    # PASS / CHECK formatting
    for row in range(4, 4 + len(validation_df)):

        status_cell = ws[f"C{row}"]

        if status_cell.value == "PASS":

            status_cell.fill = PatternFill(
                "solid",
                fgColor="C6EFCE"
            )

            status_cell.font = Font(
                bold=True,
                color="006100"
            )

        else:

            status_cell.fill = PatternFill(
                "solid",
                fgColor="FFC7CE"
            )

            status_cell.font = Font(
                bold=True,
                color="9C0006"
            )

    _add_borders(ws)

    # ---------------------------------------------------------
    # 8. NEIGHBOURHOOD ANALYSIS
    # ---------------------------------------------------------

    ws = workbook["Neighbourhood Analysis"]

    _style_title(
        ws,
        "A1:E1",
        "NEIGHBOURHOOD GROUP ANALYSIS"
    )

    _style_headers(ws, 2)

    _add_borders(ws)

    # Format numeric columns
    for row in range(
        3,
        3 + len(neighbourhood_data)
    ):

        ws[f"C{row}"].number_format = '$#,##0.00'
        ws[f"D{row}"].number_format = '0.00'
        ws[f"E{row}"].number_format = '0.00'

    # ---------------------------------------------------------
    # 9. ROOM TYPE ANALYSIS
    # ---------------------------------------------------------

    ws = workbook["Room Type Analysis"]

    _style_title(
        ws,
        "A1:D1",
        "ROOM TYPE ANALYSIS"
    )

    _style_headers(ws, 2)

    _add_borders(ws)

    for row in range(
        3,
        3 + len(room_type_data)
    ):

        ws[f"C{row}"].number_format = '$#,##0.00'
        ws[f"D{row}"].number_format = '0.00'

    # ---------------------------------------------------------
    # 10. EMBED CHARTS INTO DASHBOARD
    # ---------------------------------------------------------

    dashboard = workbook["Dashboard"]

    charts_directory = os.path.abspath(
        os.path.join(
            os.path.dirname(output_path),
            "..",
            "charts"
        )
    )

    chart_files = [
        "room_type_distribution.png",
        "listings_by_borough.png",
        "average_price_by_borough.png",
        "price_distribution.png"
    ]

    positions = [
        "D5",
        "D20",
        "L5",
        "L20"
    ]

    for filename, position in zip(
        chart_files,
        positions
    ):

        chart_path = os.path.join(
            charts_directory,
            filename
        )

        if os.path.exists(chart_path):

            try:

                image = ExcelImage(chart_path)

                image.width = 480
                image.height = 280

                dashboard.add_image(
                    image,
                    position
                )

            except Exception as e:

                print(
                    f"⚠ Could not embed chart "
                    f"{filename}: {e}"
                )

    # ---------------------------------------------------------
    # 11. FREEZE PANES
    # ---------------------------------------------------------

    workbook["Data Quality"].freeze_panes = "A4"
    workbook["Validation"].freeze_panes = "A4"
    workbook["Neighbourhood Analysis"].freeze_panes = "A3"
    workbook["Room Type Analysis"].freeze_panes = "A3"

    # ---------------------------------------------------------
    # 12. AUTO WIDTH
    # ---------------------------------------------------------

    for worksheet in workbook.worksheets:
        _auto_width(worksheet)

    # Dashboard needs wider columns
    dashboard.column_dimensions["A"].width = 28
    dashboard.column_dimensions["B"].width = 18

    # ---------------------------------------------------------
    # 13. ALIGNMENT
    # ---------------------------------------------------------

    for worksheet in workbook.worksheets:

        for row in worksheet.iter_rows():

            for cell in row:

                if cell.value is not None:

                    cell.alignment = Alignment(
                        vertical="center",
                        wrap_text=True
                    )

    # ---------------------------------------------------------
    # 14. SAVE FINAL REPORT
    # ---------------------------------------------------------

    workbook.save(output_path)

    print(
        f"✓ Professional Excel report generated: "
        f"{output_path}"
    )