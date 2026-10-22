# Deployment Guide

This guide describes how to prepare the Ekta Medicose Flask site for a public URL. The app can be hosted on Render or another provider that runs Python WSGI apps. A public deployment is a separate step from running the local preview.

## Read this before publishing

The retailer enquiry form saves valid submissions to SQL Server. Locally it uses the `EnquiryDB` database on `SQLEXPRESS`; production can set `SQLSERVER_CONNECTION_STRING` privately. Create `dbo.Enquiries` with `sql/create_enquiries_table.sql` and verify a test enquiry before advertising the form. If the database is unreachable, the submission is not saved and the page asks the visitor to call.

Also verify the public business details, company names and URLs, distribution relationships, phone numbers, image/logo permissions, privacy wording, and the business's authority to describe the listed portfolios. This website does not support online medicine sales.

## Step 1: Prepare the project

1. Extract the supplied website ZIP into a folder.
2. Run it locally by following the Windows steps in `README.md`.
3. Replace any placeholder or unverified public business text and confirm the content with Ekta Medicose.
4. Set up a reachable SQL Server database and create its enquiry table (see `README.md`). Render runs the app on Linux; SQL Server Express is a Windows installation and must run on a separate reachable Windows machine or be replaced with hosted SQL Server. Install Microsoft's SQL Server ODBC driver in the app environment.
5. Generate a long random secret for Flask sessions. Do not use the local fallback secret on a public service.

The project includes `gunicorn` in `requirements.txt`; `app:app` is the WSGI application entry point. The included `app.py` development runner has debugging disabled unless `FLASK_DEBUG=1` is set. Do not set that variable in production. Flask recommends a production WSGI server instead of its development server.

## Step 2: Put the code in a Git repository

Most managed Python hosts deploy from a Git provider. Create a private repository if you prefer to keep the source private, then add the extracted project files and push them to the provider. Do not upload `.venv`, `.env`, credentials, customer data, or enquiry exports. The included `.gitignore` excludes `.venv`, `.env`, and Python cache files.

## Step 3: Create a Render web service

In Render, create a **Web Service** and connect the Git repository. Use these settings:

| Setting | Value |
| --- | --- |
| Language/runtime | Python 3 |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app` |
| Health check path (if requested) | `/` |

Add an environment variable named `SECRET_KEY` with a newly generated random value. Keep it private and do not add it to the repository. Add `SQLSERVER_CONNECTION_STRING` as a private environment variable after configuring a remotely reachable SQL Server. A local Windows Express connection string using Windows authentication will not work from Render; use credentials and network settings supported by the chosen database host, with encrypted connections. Do not set `FLASK_DEBUG` to `1` in the service. Pick a region close to the business and review the host's current plan, pricing, sleep/availability limits, and data-persistence behavior before choosing a plan.

Render's current Flask guide uses a Python web service, `pip install -r requirements.txt`, and `gunicorn app:app`; see [Render's official Flask guide](https://render.com/docs/deploy-flask). The platform's behavior, plans, regions, and pricing can change, so confirm them in the dashboard before launch.

## Step 4: Deploy and verify

After the first deploy completes, open the assigned HTTPS URL and check:

- Home, company list, About, and retailer enquiry pages load.
- The menu and company search/filter work at phone and desktop widths.
- Phone links, map link, company links, and images work.
- Invalid form entries show useful validation messages.
- Valid enquiries are inserted into `dbo.Enquiries` and visible to authorized staff.
- No private environment values appear in the page, logs, or repository.
- The public success message accurately describes what happens to an enquiry.

If the database is not configured and verified, keep the site private or remove/disable the form until it is ready. Do not leave a public form that looks like it accepts leads while dropping them.

## Step 5: Add a custom domain (optional)

1. Purchase or choose a domain controlled by the business.
2. Add it to the host's custom-domain settings and follow the provider's DNS instructions exactly.
3. Wait for DNS and HTTPS certificate provisioning, then test the root domain and `www` behavior.
4. Keep the hosting provider's assigned URL available for troubleshooting.

## Step 6: Ongoing operation

- Restrict access to the deployment account and environment variables.
- Keep dependencies updated and redeploy after reviewing updates.
- Monitor application logs and enquiry delivery; avoid logging full enquiry contents unnecessarily.
- If storing enquiries, set an access policy, backup/restore procedure, and retention/deletion schedule.
- Keep company, address, phone, portfolio, privacy, and legal details current.
- Make a backup of the source repository and any persistent enquiry data.

## Alternative hosting providers

Any provider that supports Python and WSGI can generally run this project with:

```text
Build/install: pip install -r requirements.txt
Application:   app:app
Start:         gunicorn app:app
```

Use that provider's current instructions for environment variables, ports, domains, HTTPS, persistent storage, and deployment. Never run the Flask development server as the public production server. See [Flask's production deployment guide](https://flask.palletsprojects.com/en/stable/deploying/).
