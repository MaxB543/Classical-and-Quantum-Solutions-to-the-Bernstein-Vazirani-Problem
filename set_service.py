# Used to create a qikskit runtime service
from qiskit_ibm_runtime import QiskitRuntimeService

# Set IBM Qiskit API token and credentials for future reference 
def set_service():
    print("Please input IBM Qiskist API token")
    token = input()

    QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, set_as_default=True, overwrite=True)

    # Load saved credentials to check that token was valid
    return QiskitRuntimeService()

# Return IBM service credentials, set new credentials with API token if required
def get_service():
    try:
        return QiskitRuntimeService()
    except:
        return set_service()
    

if __name__ == "__main__":
    set_service()
    