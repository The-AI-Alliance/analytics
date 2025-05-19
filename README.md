# AI Alliance Analytics

## Purpose
The purpose of this repository is to host code and documentation for measuring and presenting key process indicators (KPIs) for measturing AI Alliance effectiveness. Intent:

### 🔍 1. Data-Driven Decision Making
- Enables strategic and operational decisions based on actual data.
- Supports A/B testing and performance comparisons.

### 📊 2. Improved Operational Efficiency
- Identifies working group bottlenecks, redundancies, and inefficiencies.
- Optimizes resource allocation, staffing, and workflows.

### 📈 3. Performance Monitoring
- Tracks Key Performance Indicators (KPIs) in real time.
- Highlights underperforming areas for targeted improvements.

### 💡 4. Participant Insights
- Analyzes participant behavior, preferences, and patterns.
- Aids in project segmentation and marketing.

### 🚀 5. Competitive Advantage
- Provides insights into production and consumption trends and competitors.
- Enables quick adaptation to changing environments.

### 📉 6. Risk Management
- Flags compliance issues, and anomalies early.
- Supports scenario modeling and forecasting.

### 📚 7. Knowledge Sharing
- Centralizes insights for consistent reporting.
- Fosters collaboration across departments through shared data.

## Metrics Sources

| Metrics Source | Metric List |
|-----------------|-----------------|
| GitHub   | [aialliance.github_analytics](./scripts/github_analytics.sql) |
| PyPi    | [aialliance.pypi](./scripts/pypi_analytics.sql)   |
| HuggingFace Data Sets   |  [huggingface.datasets](https://github.com/The-AI-Alliance/open-trusted-data-initiative/blob/main/src/src/analytics/query.sql) | 
| HuggingFace Data Sets Detail  |  [huggingface.datasets_detail](https://github.com/The-AI-Alliance/open-trusted-data-initiative/blob/main/src/src/analytics/query.sql) | 



## How to Contribute

You can contribute in several ways:

### Add an Existing GitHub Repository

Adding a daily job to collect metrics from an existing GitHub repository is easy:

1. Add the [collect_metrics.yml](https://github.com/The-AI-Alliance/gofannon/blob/main/.github/workflows/collect_metrics.yml) as a workflow to your project.

2. Add the following secrets to your project:

| Secret | Value |
|-----------------|-----------------|
| AWS_S3_BUCKET | See AI Alliance analytics team |
| AWS_REGION | See AI Alliance analytics team |

### Add a New Metrics Source

Adding a new metrics source can be accomplished as follows:
1. Use Python and the source API to query out the desired metrics. [Here is an example for PyPi](./src/pypi/src/pypi.py).
2. Build the Python code into a Docker container. [Here is an example build script for PyPi](./src/pypi/build.sh), and [here is an example Dockerfile for PyPi](./src/pypi/Dockerfile).
3. Test the Docker container locally. [Here is an example local run script for PyPi](./src/pypi/run.sh). You will need AWS access to verify the execution. See the AI Alliance analytics team for assistance.
4. Push the Docker container to the AI Alliance Docker store. [Here is an example push script for PyPi](./src/pypi/push.sh).
5. To schedule the job for recurring execution, see the AI Alliance analytics team.
6. To access the nightly execution logs for the job, see the AI Alliance analytics team.


### Create a New or Modify an Existing Dashboard

The AI Alliance presentation layer uses [Grafana](https://grafana.com/). Creating a new dashboard will require access to the AI Alliance Grafana server. See the AI Alliance analytics team.

Creating or modifying a dashboard will require basic SQL query / filtering / aggregating / joining skills.