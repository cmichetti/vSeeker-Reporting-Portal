import reflex as rx
import os
import pymssql
import logging


class State(rx.State):
    companies: list[str] = []
    selected_company: str = ""
    hostnames: list[str] = []
    selected_hostname: str = ""
    scan_dates: list[str] = []
    selected_scan_date: str = ""
    scan_data: list[dict[str, str]] = []

    def _get_db_connection(self):
        connection_string = os.environ["AZURE_SQL_CONNECTION_STRING"]
        conn_parts = {}
        for part in connection_string.split(";"):
            if "=" in part:
                key, value = part.split("=", 1)
                conn_parts[key.strip()] = value.strip()
        server_part = conn_parts.get("Server")
        if server_part and server_part.startswith("tcp:"):
            server_part = server_part[4:]
        if server_part and "," in server_part:
            server = server_part.split(",")[0]
        else:
            server = server_part
        user = "vseekerdb"
        password = "TalixNetworkAssessments!@#$%"
        database = conn_parts.get("Initial Catalog")
        return pymssql.connect(
            server=server, user=user, password=password, database=database
        )

    @rx.event
    def on_load(self):
        self.companies = []
        self.hostnames = []
        self.scan_dates = []
        self.selected_company = ""
        self.selected_hostname = ""
        self.selected_scan_date = ""
        self.scan_data = []
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT Company FROM results")
            self.companies = [row[0] for row in cursor.fetchall()]
            conn.close()
        except Exception as e:
            logging.exception(f"Error fetching companies: {e}")

    @rx.event
    def on_company_change(self, company: str):
        self.selected_company = company
        self.hostnames = []
        self.scan_dates = []
        self.selected_hostname = ""
        self.selected_scan_date = ""
        self.scan_data = []
        if company:
            try:
                conn = self._get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT DISTINCT hostname FROM results WHERE Company = %s",
                    (company,),
                )
                fetched_hostnames = [row[0] for row in cursor.fetchall()]
                self.hostnames = ["All Servers"] + fetched_hostnames
                conn.close()
            except Exception as e:
                logging.exception(f"Error fetching hostnames: {e}")

    @rx.event
    def on_hostname_change(self, hostname: str):
        self.selected_hostname = hostname
        self.scan_dates = []
        self.selected_scan_date = ""
        self.scan_data = []
        if hostname and self.selected_company:
            if hostname == "All Servers":
                try:
                    conn = self._get_db_connection()
                    cursor = conn.cursor(as_dict=True)
                    query = "\n                        WITH LatestScans AS (\n                            SELECT\n                                *,\n                                ROW_NUMBER() OVER(PARTITION BY hostname ORDER BY scanDate DESC) as rn\n                            FROM results\n                            WHERE Company = %s\n                        )\n                        SELECT * FROM LatestScans WHERE rn = 1\n                    "
                    cursor.execute(query, (self.selected_company,))
                    rows = cursor.fetchall()
                    self.scan_data = [
                        {str(k): str(v) for k, v in row.items()} for row in rows
                    ]
                    conn.close()
                except Exception as e:
                    logging.exception(f"Error fetching all servers data: {e}")
            else:
                try:
                    conn = self._get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT DISTINCT scanDate FROM results WHERE Company = %s AND hostname = %s",
                        (self.selected_company, hostname),
                    )
                    self.scan_dates = [row[0] for row in cursor.fetchall()]
                    conn.close()
                except Exception as e:
                    logging.exception(f"Error fetching scan dates: {e}")

    @rx.event
    def on_scan_date_change(self, scan_date: str):
        self.selected_scan_date = scan_date
        self.scan_data = []
        if scan_date and self.selected_company and self.selected_hostname:
            try:
                conn = self._get_db_connection()
                cursor = conn.cursor(as_dict=True)
                cursor.execute(
                    "SELECT * FROM results WHERE Company = %s AND hostname = %s AND scanDate = %s",
                    (self.selected_company, self.selected_hostname, scan_date),
                )
                row = cursor.fetchone()
                if row:
                    self.scan_data = [{str(k): str(v) for k, v in row.items()}]
                conn.close()
            except Exception as e:
                logging.exception(f"Error fetching scan data: {e}")