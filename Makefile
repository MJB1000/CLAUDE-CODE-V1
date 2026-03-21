# ── Wiper Intel — Makefile ────────────────────────────────────────────────────────

.PHONY: help test-local deploy deploy-dry-run backfill backfill-dry-run vercel-dev secrets logs run-once

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Local Development ───────────────────────────────────────────────────────────

test-local: ## Run scraper locally (dry-run mode)
	cd cloud-run-job && bash test_local.sh

test-live: ## Run scraper locally against real ingest endpoint
	cd cloud-run-job && bash test_local.sh --live

vercel-dev: ## Start Vercel dev server for dashboard
	cd dashboard && npx vercel dev

# ── Deployment ──────────────────────────────────────────────────────────────────

deploy: ## Deploy scraper to Cloud Run
	cd cloud-run-job && bash deploy.sh

deploy-dry-run: ## Build and push image only (no Cloud Run deploy)
	cd cloud-run-job && bash deploy.sh --dry-run

vercel-deploy: ## Deploy dashboard to Vercel
	cd dashboard && npx vercel --prod

# ── Operations ──────────────────────────────────────────────────────────────────

run-once: ## Execute the Cloud Run job manually
	gcloud run jobs execute wiper-intel-scraper --region=$${GCP_REGION:-australia-southeast1}

logs: ## View recent Cloud Run job logs
	gcloud logging read \
		'resource.type="cloud_run_job" AND resource.labels.job_name="wiper-intel-scraper"' \
		--limit=50 --format="table(timestamp,textPayload)"

# ── Backfill ────────────────────────────────────────────────────────────────────

backfill: ## Backfill 90 days from Wayback Machine (LIVE)
	cd cloud-run-job && python3 backfill_wayback.py

backfill-dry-run: ## Backfill dry run (no POST to ingest)
	cd cloud-run-job && python3 backfill_wayback.py --dry-run

backfill-30: ## Backfill last 30 days
	cd cloud-run-job && python3 backfill_wayback.py --days 30

# ── Secrets ─────────────────────────────────────────────────────────────────────

secrets: ## Create GCP secrets (interactive)
	@echo "Creating WIPER_INTEL_SECRET..."
	@read -rp "Enter API secret: " secret && \
		echo -n "$$secret" | gcloud secrets create WIPER_INTEL_SECRET --data-file=- 2>/dev/null || \
		echo -n "$$secret" | gcloud secrets versions add WIPER_INTEL_SECRET --data-file=-
	@echo "Creating INGEST_URL..."
	@read -rp "Enter ingest URL [https://wt-dashboards.vercel.app/api/ingest]: " url && \
		url=$${url:-https://wt-dashboards.vercel.app/api/ingest} && \
		echo -n "$$url" | gcloud secrets create INGEST_URL --data-file=- 2>/dev/null || \
		echo -n "$$url" | gcloud secrets versions add INGEST_URL --data-file=-
	@echo "Done. Secrets created."
