def format_time(t1, t2):
    elapsed_time = t2 - t1
    if elapsed_time < 60:
        return f"{elapsed_time:.2f} seconds"
    elif elapsed_time < 3600:
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        return f"{minutes:.0f} minutes {seconds:.2f} seconds"
    elif elapsed_time < 86400:
        hours = elapsed_time // 3600
        remainder = elapsed_time % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        return f"{hours:.0f} hours {minutes:.0f} minutes {seconds:.2f} seconds"
    else:
        days = elapsed_time // 86400
        remainder = elapsed_time % 86400
        hours = remainder // 3600
        remainder = remainder % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        return f"{days:.0f} days {hours:.0f} hours {minutes:.0f} minutes {seconds:.2f} seconds"


def get_cuda_cores():
    device = torch.cuda.current_device()
    compute_capability = torch.cuda.get_device_capability(device)
    cores_per_sm = {2: 32, 3: 192, 5: 128, 6: 64, 7: 64, 8: 64}  # cores per streaming multiprocessor
    sm_count = torch.cuda.get_device_properties(device).multi_processor_count
    cores = sm_count * cores_per_sm[compute_capability[0]]
    return cores
