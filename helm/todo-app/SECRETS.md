# Deployment with Secrets

## Local Development (Minikube)

For local development, use `values-local.yaml` (gitignored) with your actual secrets:

```bash
# Deploy with local secrets
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values-local.yaml

# Or upgrade existing deployment
helm upgrade todo-app ./helm/todo-app --values ./helm/todo-app/values-local.yaml
```

## Production Deployment

For production, pass secrets via command line or CI/CD environment variables:

```bash
helm install todo-app ./helm/todo-app \
  --set secrets.databaseUrl="postgresql://user:pass@host:5432/db?sslmode=require" \
  --set secrets.groqApiKey="gsk_your_key" \
  --set secrets.betterAuthSecret="your_secret" \
  --set secrets.jwtSecretKey="your_jwt_secret"
```

## GitHub Actions / CI/CD

Store secrets in GitHub Secrets and reference them in your workflow:

```yaml
- name: Deploy to Kubernetes
  run: |
    helm upgrade --install todo-app ./helm/todo-app \
      --set secrets.databaseUrl="${{ secrets.DATABASE_URL }}" \
      --set secrets.groqApiKey="${{ secrets.GROQ_API_KEY }}" \
      --set secrets.betterAuthSecret="${{ secrets.BETTER_AUTH_SECRET }}" \
      --set secrets.jwtSecretKey="${{ secrets.JWT_SECRET_KEY }}"
```

## Security Notes

- **Never commit** `values-local.yaml` - it's in `.gitignore`
- **Never commit** actual secrets in `values-dev.yaml` or `values.yaml`
- Use environment-specific values files as templates only
- Store production secrets in secure secret managers (AWS Secrets Manager, HashiCorp Vault, etc.)
