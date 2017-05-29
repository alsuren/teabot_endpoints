web: gunicorn --log-level debug -w 4 -b 0.0.0.0:${PORT:-8000} teabot_endpoints.endpoints:app
#web: python teabot_endpoints/endpoints.py