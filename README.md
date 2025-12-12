# LEMP Containers CI/CD with GitHub Actions

This project uses GitHub Actions for CI/CD, including Docker image build, push, and remote deployment via SSH.

## Prerequisites

1. **Docker Hub Account**
   - Create a Docker Hub account if you don't have one.
   - Generate a Docker Hub access token (Account Settings → Security → New Access Token).

2. **Remote Server**
   - A server accessible via SSH (for deployment).
   - Your public SSH key added to the server's `~/.ssh/authorized_keys`.

3. **GitHub Repository Secrets**
   Go to your repository → Settings → Secrets and variables → Actions → New repository secret. Add the following:

   | Name                | Description                        |
   |---------------------|------------------------------------|
   | DOCKERHUB_USERNAME  | Your Docker Hub username           |
   | DOCKERHUB_TOKEN     | Docker Hub access token            |
   | SSH_HOST            | Server IP or hostname              |
   | SSH_USER            | SSH username for your server       |
   | SSH_KEY             | Private SSH key (PEM format)       |

## Workflow Overview

The GitHub Actions workflow (`.github/workflows/deploy.yml`) does the following:

1. **Builds Docker images** for backend and frontend.
2. **Logs in to Docker Hub** using secrets.
3. **Pushes images** to Docker Hub.
4. **Deploys to your server** using SSH and runs deployment commands.

## Example Workflow Step (deploy.yml)

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

- name: Build and push backend image
  uses: docker/build-push-action@v5
  with:
    context: ./backend
    push: true
    tags: ${{ secrets.DOCKERHUB_USERNAME }}/lemp-backend:latest

- name: Deploy via SSH
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.SSH_HOST }}
    username: ${{ secrets.SSH_USER }}
    key: ${{ secrets.SSH_KEY }}
    port: 22
    script: |
      docker pull ${{ secrets.DOCKERHUB_USERNAME }}/lemp-backend:latest
      docker-compose -f docker-compose.prod.yml up -d --build
```

## Notes
- Never commit your private SSH key or Docker credentials to the repository.
- Update the workflow as needed for your project structure.
- Ensure your server has Docker and Docker Compose installed.

## Local environment file

Copy `.env.example` to `.env` and fill in real values before running the production compose or the deploy action. Example:

```bash
cp .env.example .env
# edit .env and set MYSQL_ROOT_PASSWORD and DOCKERHUB_USERNAME
```

xTo run the production compose on the server (or locally with a proper `.env`):

```bash
docker-compose --env-file .env -f docker-compose.prod.yml pull
docker-compose --env-file .env -f docker-compose.prod.yml up -d
```

If `DOCKERHUB_USERNAME` is empty, image references like `${DOCKERHUB_USERNAME}/lemp-backend:latest` become invalid and `docker-compose` will fail with `invalid reference format`.

---

For more details, see the workflow file in `.github/workflows/deploy.yml`.
