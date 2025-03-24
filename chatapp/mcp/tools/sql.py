from typing import Any
import sqlite3
from fastmcp import FastMCP
from jinja2 import Template
from pyecharts.charts import Bar
from pyecharts import options as opts

# I was not able to import this from config.py
SQLITE_PATH = "C:\\Users\\acivi\\chatapp\\chinook.sqlite"


# Initialize FastMCP server
mcp = FastMCP("sql")

HTML = """
<style>
    table {
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    th {
        background-color: #f2f2f2;
        text-align: left;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
</style>
<table>
    <thead>
        <tr>
            {% for col in columns %}
                <th>{{ col }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for row in rows %}
            <tr>
                {% for cell in row %}
                    <td>{{ cell }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>
"""


def get_database_cursor():
    con = sqlite3.connect(SQLITE_PATH)
    return con.cursor()

def get_html_table(rows: list, columns: list):
    template = Template(HTML)
    return template.render(columns=columns, rows=rows)


@mcp.tool()
async def get_sql_database_tables():
    """Run a SQL query to show the list of `tables` inside the database.
    """
    cursor = get_database_cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return  get_html_table(rows, columns)

@mcp.tool()
async def run_sql_sample_query(table:str):
    """Run a SQL query to show sample data for a specific `table` {table_name}.
    """
    sql = f"SELECT * FROM {table} LIMIT 10"
    cursor = get_database_cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return get_html_table(rows, columns)

@mcp.tool()
async def group_and_summarize_as_chart(table: str, group_by_column: str, sum_column: str) -> str:
    """
    Create a bar chart summarizing `sum_column` grouped by `group_by_column` from the given table.
    Returns a rendered HTML chart.
    """
    sql = f"""
        SELECT {group_by_column}, SUM({sum_column}) as total
        FROM {table}
        GROUP BY {group_by_column}
        ORDER BY total DESC
        LIMIT 20
    """

    cursor = get_database_cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    # Separate x and y data
    categories = [str(row[0]) for row in rows]
    totals = [row[1] for row in rows]

    # Create chart
    bar = (
        Bar()
        .add_xaxis(categories)
        .add_yaxis(f"Sum of {sum_column}", totals)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{sum_column} by {group_by_column}"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
            toolbox_opts=opts.ToolboxOpts(),
            datazoom_opts=[opts.DataZoomOpts()]
        )
    )

    return bar.render_embed()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')