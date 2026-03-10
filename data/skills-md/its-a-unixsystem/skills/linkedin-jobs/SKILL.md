---
name: linkedin-jobs
description: "Search and fetch LinkedIn job postings via BrightData. Use when the user wants to: (1) search LinkedIn for jobs by keyword, location, remote type, or date posted (e.g. 'find remote software engineering jobs posted this month'), (2) fetch a specific job by URL or numeric job ID (e.g. 'show me job 4358573391'), (3) analyze job postings for resume tailoring, gap analysis, or comparison."
---

# LinkedIn Jobs

Requires `BRIGHTDATA_API_KEY` environment variable.

Two operations: **search** (discover jobs by criteria) and **fetch** (get a specific job by URL or ID). Both return full raw JSON.

## Search jobs

**Cost: ~$1.50 per 1k records.** Always use `--limit` to control costs. Default limit is 25.

Script paths below are relative to this skill's directory.

```bash
python3 scripts/search_linkedin_jobs.py "software engineer" \
  --location "United States" \
  --remote Remote \
  --time-range "Past month" \
  --job-type Full-time \
  --experience "Mid-Senior level" \
  --limit 25
```

`keyword` and `--location` are required. All other flags are optional.

| Flag | Valid values |
|------|-------------|
| `--limit` | Max results (default 25). Keep low to control costs. |
| `--remote` | `Remote` \| `On-site` \| `Hybrid` |
| `--time-range` | `"Past 24 hours"` \| `"Past week"` \| `"Past month"` (default) |
| `--job-type` | `Full-time` \| `Part-time` \| `Contract` \| `Temporary` \| `Volunteer` |
| `--experience` | `"Entry level"` \| `Associate` \| `"Mid-Senior level"` \| `Director` \| `Executive` \| `Internship` |
| `--company` | Company name string |
| `--country` | Country code (e.g. `US`, `GB`) |

Returns an array of job objects.

## Fetch a specific job

Takes ~30 seconds. Accepts a full LinkedIn URL or numeric job ID.

```bash
python3 scripts/fetch_linkedin_job.py 4358573391
python3 scripts/fetch_linkedin_job.py "https://www.linkedin.com/jobs/view/4358573391"
```

Returns a single job object.

## Key output fields

`job_posting_id`, `job_title`, `company_name`, `job_location`, `job_summary`, `job_posted_date`, `job_employment_type`, `job_seniority_level`, `job_num_applicants`, `base_salary`, `is_easy_apply`, `application_availability`, `url`, `apply_link`, `job_description_formatted`.
