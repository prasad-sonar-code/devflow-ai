import random
import json

def analyze_pipeline_failure(log: str) -> dict:
    """Mock AI analyzer — replace with OpenAI when ready"""
    
    log_lower = log.lower()
    
    # Detect failure type from log
    if "permission denied" in log_lower or "access denied" in log_lower:
        return {
            "root_cause": "Insufficient permissions — the pipeline user lacks required access rights to the resource.",
            "fix": [
                "Check IAM role attached to your CI/CD pipeline",
                "Add missing permissions: s3:GetObject, ecr:GetAuthorizationToken",
                "Re-run the pipeline after updating permissions"
            ],
            "prevention": "Use least-privilege IAM roles and audit permissions before deploying.",
            "severity": "High",
            "estimated_fix_time": "10 minutes"
        }
    
    elif "connection refused" in log_lower or "timeout" in log_lower:
        return {
            "root_cause": "Network connectivity issue — the pipeline cannot reach the target service or database.",
            "fix": [
                "Verify the target service is running: kubectl get pods",
                "Check security group rules allow traffic on required ports",
                "Verify VPC peering or private endpoint configuration",
                "Test connectivity: curl -v <service-url>"
            ],
            "prevention": "Add health check retries in your pipeline and set up uptime monitoring.",
            "severity": "Critical",
            "estimated_fix_time": "20 minutes"
        }
    
    elif "image" in log_lower and ("not found" in log_lower or "pull" in log_lower):
        return {
            "root_cause": "Docker image not found — the specified image tag does not exist in the registry.",
            "fix": [
                "Check image name and tag: docker images | grep <image-name>",
                "Verify ECR/DockerHub repository exists and is accessible",
                "Ensure the build step ran before the deploy step",
                "Check image tag matches what was built: latest vs commit SHA"
            ],
            "prevention": "Pin image tags to commit SHAs instead of 'latest' in production pipelines.",
            "severity": "High",
            "estimated_fix_time": "5 minutes"
        }
    
    elif "test" in log_lower and ("failed" in log_lower or "error" in log_lower):
        return {
            "root_cause": "Unit or integration tests are failing — code changes broke existing test cases.",
            "fix": [
                "Run tests locally: pytest -v or npm test",
                "Check the failing test names in the log output",
                "Fix the code causing test failures",
                "Add mock data if tests need environment variables"
            ],
            "prevention": "Run tests locally before pushing. Add pre-commit hooks to catch failures early.",
            "severity": "Medium",
            "estimated_fix_time": "30 minutes"
        }
    
    elif "out of memory" in log_lower or "oom" in log_lower:
        return {
            "root_cause": "Container or process ran out of memory during pipeline execution.",
            "fix": [
                "Increase memory limits in your pipeline config",
                "For Kubernetes: update resources.limits.memory in deployment.yaml",
                "Optimize the build process to use less memory",
                "Split the build into smaller stages"
            ],
            "prevention": "Set appropriate resource limits and monitor memory usage with Prometheus.",
            "severity": "High",
            "estimated_fix_time": "15 minutes"
        }
    
    elif "syntax error" in log_lower or "unexpected token" in log_lower:
        return {
            "root_cause": "Syntax error in configuration file or script — invalid YAML, JSON, or shell syntax.",
            "fix": [
                "Check the line number mentioned in the error",
                "Validate YAML: python3 -c 'import yaml; yaml.safe_load(open(\"file.yml\"))'",
                "Use a linter: yamllint, jsonlint, or shellcheck",
                "Fix indentation — YAML is whitespace sensitive"
            ],
            "prevention": "Add linting steps at the start of your pipeline before any builds.",
            "severity": "Medium",
            "estimated_fix_time": "5 minutes"
        }

    elif "disk" in log_lower and ("full" in log_lower or "space" in log_lower):
        return {
            "root_cause": "Insufficient disk space on the CI/CD runner — build artifacts filled the disk.",
            "fix": [
                "Clean Docker: docker system prune -af",
                "Remove old artifacts: find /tmp -mtime +1 -delete",
                "Increase runner disk size in cloud settings",
                "Add disk cleanup step at start of pipeline"
            ],
            "prevention": "Add automated disk cleanup jobs and monitor disk usage with alerts.",
            "severity": "Critical",
            "estimated_fix_time": "10 minutes"
        }
    
    else:
        return {
            "root_cause": "Pipeline failed due to an unhandled error in the build or deployment stage.",
            "fix": [
                "Check the full error message in the pipeline logs",
                "Re-run the pipeline to rule out transient failures",
                "Add verbose logging: set -x in shell scripts",
                "Check environment variables are correctly set"
            ],
            "prevention": "Add detailed logging and error handling to all pipeline stages.",
            "severity": "Medium",
            "estimated_fix_time": "15 minutes"
        }
