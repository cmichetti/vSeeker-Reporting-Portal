import reflex as rx
from app.states.state import State


def result_item_with_description(item: rx.Var[tuple[str, str]]) -> rx.Component:
    key = item[0]
    value = item[1]
  
    return rx.el.li(  # if key isn't == company, return data
        # rx.el.span(key, class_name="font-normal"),
        rx.cond(
            key == "windowsfullypatched",
            rx.cond(
                value == 1,
                rx.el.span(rx.text.strong("√"), "- Windows is fully patched with Windows Updates.", class_name="font-normal bg-green-100 bg-cover"),
                rx.el.span(rx.text.strong("!"), "- Windows is not fully patched with Windows Updates.", class_name="font-normal bg-red-100 bg-cover"),
            )
        )
        #": ",
        #rx.cond(
        #    key.contains("disabled") | key.contains("enabled"),
        #    rx.cond(value == "1", "Enabled", rx.cond(value == "0", "Disabled", value)),
        #    value,
        #),
        #class_name=rx.cond(
        #    key.contains("disabled") | key.contains("enabled"),
        #    rx.cond(
        #        value == "1",
        #        "p-3 border-b bg-green-100",
        #        rx.cond(
        #            value == "0", "p-3 border-b bg-red-100", "p-3 border-b bg-white"
        #        ),
        #    ),
        #    "p-3 border-b bg-white",
        #),
    ),

    

def scan_results_list() -> rx.Component:
    return rx.el.div(
        rx.el.ul(
            rx.foreach(
                State.scan_data,
                lambda result: rx.cond(
                    State.scan_data.length() > 1,
                    rx.el.li(
                        rx.el.span(
                            result["hostname"],
                            class_name="text-xl font-bold text-gray-700",
                        ),
                        rx.el.ul(
                            rx.foreach(
                                result.items(),
                                lambda item: rx.cond(
                                    (item[0] != "id") & (item[0] != "hostname") & (item[0] != "company"),
                                    result_item_with_description(item),
                                    rx.fragment(),
                                ),
                            ),
                            class_name="list-none p-0 mt-2 mb-4 border rounded-md overflow-hidden shadow-sm",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.ul(
                        rx.foreach(
                            result.items(),
                            lambda item: rx.cond(
                                item[0] != "id",
                                result_item_with_description(item),
                                rx.fragment(),
                            ),
                        ),
                        class_name="w-full list-none p-0",
                    ),
                ),
            ),
            class_name="w-full max-w-4xl list-none p-0",
        ),
        class_name="w-full flex flex-col items-center mt-8",
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1(
                "vSeeker Reporting Portal",
                class_name="text-4xl font-bold text-gray-800 mb-6",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Select Company", value="", disabled=True),
                    rx.foreach(
                        State.companies,
                        lambda company: rx.el.option(company, value=company),
                    ),
                    value=State.selected_company,
                    on_change=State.on_company_change,
                    class_name="p-2 border rounded-md bg-white",
                ),
                rx.el.select(
                    rx.el.option("Select Hostname", value="", disabled=True),
                    rx.foreach(
                        State.hostnames,
                        lambda hostname: rx.el.option(hostname, value=hostname),
                    ),
                    value=State.selected_hostname,
                    on_change=State.on_hostname_change,
                    class_name="p-2 border rounded-md bg-white",
                    is_disabled=~State.selected_company.to(bool),
                ),
                rx.el.select(
                    rx.el.option("Select Scan Date", value="", disabled=True),
                    rx.foreach(
                        State.scan_dates,
                        lambda scan_date: rx.el.option(scan_date, value=scan_date),
                    ),
                    value=State.selected_scan_date,
                    on_change=State.on_scan_date_change,
                    class_name="p-2 border rounded-md bg-white",
                    is_disabled=~State.selected_hostname.to(bool)
                    | (State.selected_hostname == "All Servers"),
                ),
                class_name="flex flex-row space-x-4 mb-8",
            ),
            rx.cond(State.scan_data, scan_results_list(), rx.el.div()),
            class_name="w-full flex flex-col items-center pt-10 px-4",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=State.on_load)