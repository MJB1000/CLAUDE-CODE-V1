#!/usr/bin/env bash
set -euo pipefail

# ── Wiper Intel Scraper — Cloud Run Job Deployment ──────────────────────────────
# Prerequisites:
#   - gcloud CLI authenticated (gcloud auth login)
#   - Project set (gcloud config set project PROJECT_ID)
#   - Artifact Registry repo created (see below)
#   - Required APIs enabled: Cloud Run, Artifact Registry, Cloud Scheduler
#
# Usage:
#   ./deploy.sh                    # Deploy with defaults
#   ./deploy.sh --schedule "0 7 * * *"  # Custom cron schedule
#   ./deploy.sh --dry-run          # Build only, don't deploy

PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"
REGION="${GCP_REGION:-australia-southeast1}"
JOB_NAME="wiper-intel-scraper"
REPO_NAME="wiper-intel"
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$JOB_NAME"
SCHEDULE="${SCHEDULE:-0 21 * * *}"  # 07:00 AEST daily (21:00 UTC previous day)
DRY_RUN=false

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --schedule) SCHEDULE="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=true; shift ;;
    --region)   REGION="$2"; shift 2 ;;
    --project)  PROJECT_ID="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$PROJECT_ID" ]]; then
  echo "ERROR: No GCP project set. Run: gcloud config set project PROJECT_ID"
  exit 1
fi

echo "╔══════════════════════════════════════════════════╗"
echo "║  Wiper Intel Scraper — Deploy to Cloud Run Jobs ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Project:   $PROJECT_ID"
echo "  Region:    $REGION"
echo "  Image:     $IMAGE"
echo "  Schedule:  $SCHEDULE (UTC)"
echo "  Dry run:   $DRY_RUN"
echo ""

# ── Step 1: Enable required APIs ────────────────────────────────────────────────
echo "→ Enabling required APIs..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudscheduler.googleapis.com \
  --project="$PROJECT_ID" \
  --quiet

# ── Step 2: Create Artifact Registry repo (if needed) ──────────────────────────
echo "→ Ensuring Artifact Registry repo exists..."
gcloud artifacts repositories describe "$REPO_NAME" \
  --location="$REGION" \
  --project="$PROJECT_ID" 2>/dev/null || \
gcloud artifacts repositories create "$REPO_NAME" \
  --repository-format=docker \
  --location="$REGION" \
  --project="$PROJECT_ID" \
  --description="Wiper Intel container images"

# ── Step 3: Configure Docker auth ──────────────────────────────────────────────
echo "→ Configuring Docker authentication..."
gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet

# ── Step 4: Build and push ──────────────────────────────────────────────────────
echo "→ Building container image..."
docker build -t "$IMAGE:latest" -t "$IMAGE:$(date +%Y%m%d-%H%M%S)" .

echo "→ Pushing to Artifact Registry..."
docker push "$IMAGE:latest"

if $DRY_RUN; then
  echo ""
  echo "DRY RUN — image built and pushed, skipping Cloud Run deployment."
  exit 0
fi

# ── Step 5: Deploy Cloud Run Job ────────────────────────────────────────────────
echo "→ Deploying Cloud Run Job..."

# Check required secrets exist
REQUIRED_SECRETS="WIPER_INTEL_SECRET INGEST_URL"
for secret in $REQUIRED_SECRETS; do
  if ! gcloud secrets describe "$secret" --project="$PROJECT_ID" &>/dev/null; then
    echo ""
    echo "WARNING: Secret '$secret' not found. Create it with:"
    echo "  echo -n 'value' | gcloud secrets create $secret --data-file=- --project=$PROJECT_ID"
    echo ""
  fi
done

gcloud run jobs deploy "$JOB_NAME" \
  --image="$IMAGE:latest" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --task-timeout=600 \
  --max-retries=1 \
  --memory=2Gi \
  --cpu=1 \
  --set-secrets="WIPER_INTEL_SECRET=WIPER_INTEL_SECRET:latest,INGEST_URL=INGEST_URL:latest" \
  --set-env-vars="GCS_BUCKET=${GCS_BUCKET:-}" \
  --quiet

# Optionally wire ANTHROPIC_API_KEY if secret exists
if gcloud secrets describe "ANTHROPIC_API_KEY" --project="$PROJECT_ID" &>/dev/null; then
  echo "→ Wiring ANTHROPIC_API_KEY secret..."
  gcloud run jobs update "$JOB_NAME" \
    --region="$REGION" \
    --project="$PROJECT_ID" \
    --update-secrets="ANTHROPIC_API_KEY=ANTHROPIC_API_KEY:latest" \
    --quiet
fi

# ── Step 6: Create/update Cloud Scheduler ───────────────────────────────────────
echo "→ Setting up Cloud Scheduler (${SCHEDULE})..."
SCHEDULER_JOB="$JOB_NAME-trigger"

if gcloud scheduler jobs describe "$SCHEDULER_JOB" --location="$REGION" --project="$PROJECT_ID" &>/dev/null; then
  gcloud scheduler jobs update http "$SCHEDULER_JOB" \
    --location="$REGION" \
    --project="$PROJECT_ID" \
    --schedule="$SCHEDULE" \
    --uri="https://$REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/$JOB_NAME:run" \
    --http-method=POST \
    --oauth-service-account-email="$PROJECT_ID@appspot.gserviceaccount.com" \
    --quiet
else
  gcloud scheduler jobs create http "$SCHEDULER_JOB" \
    --location="$REGION" \
    --project="$PROJECT_ID" \
    --schedule="$SCHEDULE" \
    --uri="https://$REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/$JOB_NAME:run" \
    --http-method=POST \
    --oauth-service-account-email="$PROJECT_ID@appspot.gserviceaccount.com" \
    --quiet
fi

# ── Step 7: Run once to verify ──────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════"
echo "  Deployment complete!"
echo ""
echo "  To run manually:"
echo "    gcloud run jobs execute $JOB_NAME --region=$REGION"
echo ""
echo "  To view logs:"
echo "    gcloud run jobs executions list --job=$JOB_NAME --region=$REGION"
echo "    gcloud logging read 'resource.type=\"cloud_run_job\" AND resource.labels.job_name=\"$JOB_NAME\"' --limit=50"
echo ""
echo "  To update secrets:"
echo "    echo -n 'value' | gcloud secrets versions add SECRET_NAME --data-file=-"
echo "════════════════════════════════════════════════════"
