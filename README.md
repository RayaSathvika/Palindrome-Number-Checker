# Palindrome Checker

A small web application that checks whether a string (or a number written as text) is a palindrome. Letters and digits are compared without case or punctuation.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python app.py
```

Open http://127.0.0.1:7070.

## Tests

Unit tests:

```powershell
pytest tests/test_palindrome.py
```

Selenium drives the page in headless Chrome. With no `PALINDROME_BASE_URL`, the suite starts the app itself:

```powershell
pytest tests/test_selenium.py
```

Against a deployed instance:

```powershell
$env:PALINDROME_BASE_URL = "http://127.0.0.1:7070"
pytest tests/test_selenium.py
```

## Container and Kubernetes

```powershell
docker build -t palindrome-checker:7070 .
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
kubectl rollout status deployment/palindrome-checker
```

The container listens on port 7070 and is published as `7070:7070`, clear of the ports already used by the other containers (3001 and 5000). The Kubernetes Service uses port 7070 and NodePort 30770.

```powershell
docker run -d --name palindrome-checker -p 7070:7070 palindrome-checker:7070
```

## Source control

```powershell
git init
git add .
git commit -m "Add palindrome checker with Kubernetes and Selenium tests"
git branch -M main
gh repo create palindrome-checker --public --source=. --remote=origin --push
```
