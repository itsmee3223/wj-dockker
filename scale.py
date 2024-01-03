from flask import Flask, request
import docker
import os

app = Flask(__name__)
client = docker.from_env()

# Set environment variables for the service name and the scale factors.
SERVICE_NAME = os.getenv('SERVICE_NAME', 'wj-wordpress_wordpress')
SCALE_UP_FACTOR = int(os.getenv('SCALE_UP_FACTOR', 1))
SCALE_DOWN_FACTOR = int(os.getenv('SCALE_DOWN_FACTOR', 1))
MAX_REPLICAS = int(os.getenv('MAX_REPLICAS', 5))
MIN_REPLICAS = int(os.getenv('MIN_REPLICAS', 1))

@app.route('/scale', methods=['POST'])
def scale():
    data = request.json
    alerts = data.get('alerts', [])
    service = client.services.get(SERVICE_NAME)
    current_replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']

    # Count the number of firing and resolved alerts.
    firing_alerts = sum(1 for alert in alerts if alert['status'] == 'firing')
    resolved_alerts = sum(1 for alert in alerts if alert['status'] == 'resolved')

    # Calculate the new number of replicas.
    new_replicas = current_replicas + (firing_alerts * SCALE_UP_FACTOR) - (resolved_alerts * SCALE_DOWN_FACTOR)
    new_replicas = max(min(new_replicas, MAX_REPLICAS), MIN_REPLICAS)

    # Scale the service to the new number of replicas.
    if new_replicas != current_replicas:
        service.scale(new_replicas)
        action = 'scaled up' if new_replicas > current_replicas else 'scaled down'
        return f"Service {SERVICE_NAME} {action} to {new_replicas} replicas", 200
    else:
        return "No scaling action taken", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
