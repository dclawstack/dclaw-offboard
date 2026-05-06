# Troubleshooting

Common issues and solutions for DClaw Offboard.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-offboard

# Check logs
kubectl logs -n dclaw-offboard deployment/dclaw-offboard-backend

# Check database
kubectl get clusters -n dclaw-offboard
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
