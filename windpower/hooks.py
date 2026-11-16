# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "windpower"
app_title = "Frappe Renewable Wind Turbine Scada Curtailment"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Renewable Wind Turbine Scada Curtailment for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/windpower/css/windpower.bundle.css"
app_include_js = "/assets/windpower/js/windpower.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "windpower.engine.on_document_submit",
        "on_cancel": "windpower.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "windpower.engine.daily_scheduled_sync"
    ]
}
