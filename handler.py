import runpod
import os


def handler(job):
    job_input = job['input']
    user_id = job_input['user_id']
    bucket_path = job_input['bucket_path']
    
    # Execute the flow
    try:
        print(f"Secret: {os.getenv('test-secret')}")
        print("..::Flow Completed::..") 
        return {"status": "success", "message": "Flow completed successfully"}
    except Exception as e:
        print(f"Flow failed with error: {str(e)}")
        return {"status": "error", "message": str(e)}

runpod.serverless.start({"handler": handler})
