CI/CD for flask-task-manager

Overview

This repo contains a small Flask app (flask-task-manager). The CI/CD pipeline uses GitHub Actions to run unit tests and build a Docker image which is pushed to GitHub Container Registry (GHCR) — no external container registry secrets are required.

Why GitHub Actions

- Native integration with GitHub repositories — no extra service required.
- Free tier for public repos and simple to configure YAML workflows.
- Rich marketplace of actions (Docker, setup-python, etc.) so the workflow stays concise.

What the workflow does

1. Trigger: runs on push and pull_request to the `main` branch. This provides an automated trigger for every commit or PR.
2. Test job: checks out code, sets up Python 3.11, installs dependencies from `requirements.txt`, and runs `pytest`.
3. Build_and_push job: runs after tests pass. It sets up Docker buildx, logs into GitHub Container Registry using the built-in `GITHUB_TOKEN`, builds a multi-platform image (via buildx/qemu), then pushes tags `latest` and the commit SHA.

Secrets to set

No external registry secrets are required when pushing to GHCR. The workflow uses the repository's `GITHUB_TOKEN` to authenticate with GHCR. If you prefer Docker Hub you can switch back (see "Switching registries" below).

How to capture screenshots

1. Open your GitHub repo in a browser.
2. Go to the "Actions" tab and pick the workflow run.
3. Capture the run overview (shows jobs and status).
4. Click into a job to capture the step-by-step logs and take screenshots for each step you want to document.

Challenges & notes

- Secrets: Make sure secrets are configured in the repo; builds that need push will fail without them.
-- Docker Hub rate limits: hitting Docker Hub limits can cause the push to fail — use authenticated pushes and consider GitHub Container Registry (ghcr.io) for higher limits.
- Local debugging: Workflow steps run on hosted runners that may differ from local dev machines. Reproduce by running the same commands locally or using act (https://github.com/nektos/act) to emulate actions.

Quality gates

- Tests must pass before images are built and pushed.
- You can extend the pipeline with linting (flake8), security scans, or deployment to a cloud service.

What to submit for the assignment

- The workflow file: `.github/workflows/ci-cd.yml`
- A short write-up (this file) explaining decisions and setup steps.
-- Screenshots of the Actions run showing tests passing and the container registry push. Include captions describing each step.

Switching registries

If you want to push to Docker Hub instead of GHCR, revert the workflow's login step and build tags to use Docker Hub credentials; you will need to add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` to repository secrets.

Continuous Deployment (deploy to local machine)

This repository includes a `deploy_to_local` job in the workflow that is intended to run on a self-hosted runner (your local machine). The job pulls the image from GHCR and runs it as a container on the machine.

Two options to make this work:

1) Self-hosted runner (recommended)

- On GitHub: go to Settings -> Actions -> Runners -> Add runner and follow the instructions for your OS.
- When registering the runner, assign it a label `local-deploy` (or adjust the workflow `runs-on` to match your label).
- Ensure the runner has Docker installed and the runner service user can run Docker commands (or use root).
- Once the runner is online, pushes to `main` will trigger the `deploy_to_local` job which will:
	- login to GHCR using `GITHUB_TOKEN` (the runner will use the token provided by the workflow)
	- pull `ghcr.io/<owner>/<repo>:latest`
	- stop and remove any existing container named `flask-task-manager`
	- run the new image exposing port 5000

2) SSH deploy (alternative)

If you can't or don't want to register a self-hosted runner, you can deploy via SSH from the workflow to your machine. This requires adding an SSH private key as a secret and enabling the corresponding public key in `~/.ssh/authorized_keys` on your machine. The workflow would use `appleboy/ssh-action` or a simple SSH command to run the `docker pull` and `docker run` commands.

Security notes

- Self-hosted runners run arbitrary workflow code — only register one you control and understand the security implications.
- For SSH deploys, protect your SSH private key with repository secrets and restrict the key's permissions on the server.

If you'd like, I can add a ready-to-use SSH-based job in the workflow that runs when `deploy_to_local` is requested; you'll then need to add `SSH_HOST`, `SSH_USER`, and `SSH_PRIVATE_KEY` secrets.

*** End of file
