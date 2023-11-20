from dagster import (
    load_assets_from_modules,
    Definitions,
    define_asset_job,
    ScheduleDefinition,
)

from loupi_dagster import assets

from loupi_dagster.duckpond import MotherduckIOManager, DuckDB
import os

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": MotherduckIOManager(DuckDB(url=os.environ.get("MOTHERDUCK_URL")))
    },
    schedules=[
        ScheduleDefinition(
            job=define_asset_job(name="daily_refresh", selection="*"),
            cron_schedule="@daily",
        )
    ],
)
