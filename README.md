# Ekta Medicose Website

A responsive Flask website for Ekta Medicose, a pharmaceutical distributor in Karnal, Haryana. It introduces the business, presents the company portfolios supplied by the owner, and provides a retailer and healthcare-business enquiry form.

The site is an information and business-enquiry website. It does not sell medicines to consumers. **Valid enquiries are saved in SQL Server when it is configured. Set up and verify the database before promoting the form on a public website.**

## Project features

- Responsive home, company portfolio, about, and retailer-enquiry pages.
- Business name, address, phone numbers, and company list kept in JSON data files.
- Searchable/filterable company portfolio cards with links to the company websites.
- Server-side enquiry validation and consent checkbox.
- Valid enquiries are saved to local SQL Server Express, or to the server in `SQLSERVER_CONNECTION_STRING` when that setting is provided.
- Company logo assets are loaded from their listed image URLs; the page therefore needs internet access to display those remote logos. The Ekta Medicose sign and office photos are local files.

## Run on Windows

Install Python 3.10 or later. From PowerShell, open this folder and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
python app.py
```

Open <http://127.0.0.1:5000>. To enable Flask's local debugging tools, set `$env:FLASK_DEBUG = "1"` before running the app. Do not enable debug mode on a public deployment.

## Project layout

```text
app.py                    Flask application and page routes
services/enquiries.py     Server-side validation for retailer enquiries
data/company.json         Public business details and company categories
data/products.json        Company display names, descriptions, links, and logos
templates/                Jinja page templates
static/css/               Shared, page-specific, and responsive styles
static/js/site.js         Browser-side filtering, menu, and UI behavior
static/images/            Ekta Medicose logo, sign, and office photos
requirements.txt          Python dependencies (Flask and Gunicorn)
DEPLOYMENT.md             Detailed production/deployment checklist
```

## Updating business information

- Edit `data/company.json` to change the business name, address, telephone numbers, and company categories.
- Edit `data/products.json` to change the company display names, descriptions, official-site links, and logo image URLs.
- Replace images in `static/images/` to update the local sign, mark, or office photographs. Keep the filenames used by the templates unless you also update the template paths.
- Check all company names, distribution relationships, phone numbers, addresses, URLs, logo permissions, and product claims with the business owner before publication.

## Enquiry handling

`app.py` validates and saves the enquiry in SQL Server. Locally it connects to `EnquiryDB` on `SQLEXPRESS`; in production it can use `SQLSERVER_CONNECTION_STRING`. See [SQL Server setup](#sql-server-setup). If the database is unreachable, the submission is not saved and the page asks the visitor to call.

### SQL Server setup

1. Install SQL Server Express and SQL Server Management Studio (SSMS) on the Windows computer that will host the database.
2. In SSMS, create a database named `EktaMedicose`.
3. Open and run [`sql/create_enquiries_table.sql`](sql/create_enquiries_table.sql) while connected to that database. This creates the `dbo.Enquiries` table.
4. Install Microsoft's ODBC Driver for SQL Server on the computer running this Flask app, then install Python dependencies with `pip install -r requirements.txt`.
5. The local app connects to `localhost\SQLEXPRESS` using Windows authentication. If needed, use this connection string in `get_db_connection()` in `app.py`:

   ```powershell
   Driver={ODBC Driver 18 for SQL Server};Server=.\SQLEXPRESS;Database=EnquiryDB;Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes
   ```

   `Trusted_Connection=yes` uses the Windows account running Flask, so give that account permission to insert rows in `dbo.Enquiries`.

The connection flow is: browser form -> Flask route in `app.py` -> validation and `save_enquiry` in `services/enquiries.py` -> `pyodbc` driver -> SQL Server table. The `?` marks in the INSERT statement are parameter placeholders; `pyodbc` passes each field separately.

For production, do not expose SQL Server's port to the public internet. Run the app and database on the same private network, restrict database access to the app, configure backups, and store credentials as a hosting environment secret. The current Render deployment guide runs the app on Linux; SQL Server Express is a Windows installation, so it cannot simply be installed inside that Render service. Render needs a separately hosted/reachable SQL Server, and its Linux environment needs Microsoft's SQL Server ODBC driver installed. Review hosting and database costs before launch.

Before public launch, choose and implement one or both of these:

1. Send enquiries to a monitored business email using a provider with server-side credentials stored as environment variables; or
2. Save enquiries to a database with restricted access, backups, a retention policy, and a way for staff to review them.

Then update the success message, privacy notice/consent wording, and operational process; verify delivery end to end with a test enquiry. Do not put email passwords or provider API keys in source files or commit them to Git.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for a step-by-step Render deployment path, production settings, domain checklist, and launch steps. Other Python web hosts can use the same WSGI entry point: `app:app`.

## Useful references

- [Flask production deployment guidance](https://flask.palletsprojects.com/en/stable/deploying/)
- [Render Flask deployment guide](https://render.com/docs/deploy-flask)
