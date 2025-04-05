import torch

def get_gpu_cores():
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            device = torch.cuda.get_device_properties(i)
            sm_count = device.multi_processor_count
            compute_capability = device.major
            cores_per_sm = {
              1: 8,    # Tesla
              2: 32,   # Fermi
              3: 192,  # Kepler
              5: 128,  # Maxwell
              6: 64,   # Pascal
              7: 64,   # Volta, Turing
              8: 64    # Ampere
            }.get(compute_capability, 64)
            total_cores = sm_count * cores_per_sm
            print(f"GPU {i}: {device.name}")
            print(f"  SM Count: {sm_count}")
            print(f"  Cores per SM: {cores_per_sm}")
            print(f"  Total CUDA Cores: {total_cores}")
            print(f"  Memory: {device.total_memory / (1024**3):.2f} GB\n")
    else:
        print("CUDA is not available.")

get_gpu_cores()



# curl -H 'Cache-Control: no-cache' -s "https://raw.githubusercontent.com/akuresonite/Helpers/main/Gpu_cores.py" | python

