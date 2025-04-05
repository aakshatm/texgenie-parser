import subprocess

def run_commands(input_pdf):
    try:
        # Activate conda environment
        # subprocess.run("conda activate MinerU", shell=True, check=True, executable="/bin/bash")
        
        # Run magic-pdf command
        subprocess.run(f"magic-pdf -p {input_pdf} -o ./input", shell=True, check=True, executable="/bin/bash")
        
        # Run the Python script
        subprocess.run("python modifiedCodev5.py", shell=True, check=True, executable="/bin/bash")
        
        print("All commands executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    input_pdf = input("Enter the PDF filename: ")
    run_commands(input_pdf)
