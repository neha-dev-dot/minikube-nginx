import subprocess
import sys
import os

def run_command(command, capture_output=False, check=True):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        if capture_output:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with return code {e.returncode}\n{e.stderr}")
        sys.exit(1)

def install_dependencies():
    """Installs necessary dependencies."""
    print("Installing dependencies...")
    run_command("sudo apt-get update")
    run_command("sudo apt-get install -y curl wget apt-transport-https conntrack")

def install_minikube():
    """Downloads and installs Minikube."""
    print("Installing Minikube...")
    minikube_latest_url = "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
    run_command(f"wget -O minikube {minikube_latest_url}")
    run_command("sudo install minikube /usr/local/bin/")
    os.remove("minikube")  # Clean up the downloaded binary

def install_kubectl():
    """Installs kubectl for interacting with the Kubernetes cluster."""
    print("Installing kubectl...")
    kubectl_latest_url = "https://storage.googleapis.com/kubernetes-release/release/stable.txt"
    latest_version = run_command(f"curl -s {kubectl_latest_url}", capture_output=True)
    kubectl_binary_url = f"https://storage.googleapis.com/kubernetes-release/release/{latest_version}/bin/linux/amd64/kubectl"
    run_command(f"curl -LO {kubectl_binary_url}")
    run_command("sudo install kubectl /usr/local/bin/")
    os.remove("kubectl")  # Clean up the downloaded binary

def start_minikube():
    """Starts Minikube with a single-node cluster."""
    print("Starting Minikube...")
    run_command("minikube start --driver=docker")

def verify_installation():
    """Verifies the Minikube installation."""
    print("Verifying Minikube installation...")
    minikube_version = run_command("minikube version", capture_output=True)
    kubectl_version = run_command("kubectl version --client=true --short", capture_output=True)
    print(f"Minikube installed successfully: {minikube_version}")
    print(f"kubectl installed successfully: {kubectl_version}")

def main():
    print("Starting Minikube installation...")
    install_dependencies()
    install_minikube()
    install_kubectl()
    start_minikube()
    verify_installation()
    print("Minikube single-node cluster setup completed successfully.")

if __name__ == "__main__":
    main()
