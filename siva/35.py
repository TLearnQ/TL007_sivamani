import logging

logging.basicConfig(
    filename="audit_errors.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def safe_log(message, level="INFO"):
    if level == "ERROR":
        logging.error(message)
    elif level == "WARNING":
        logging.warning(message)
    else:
        logging.info(message)

def process_log_lines(log_lines, audit_filename="audit.log"):
    processed = 0
    failed = 0

    try:
        audit_file = open(audit_filename, "w")
    except Exception as e:
        safe_log(f"Failed to open audit file: {e}", "ERROR")
        return

    for line in log_lines:
        try:
            processed += 1
            if not isinstance(line, str):
                raise ValueError("Malformed log entry (not a string)")
            if line.startswith("ERROR") or line.startswith("WARNING"):
                audit_file.write(line + "\n")
                safe_log(f"Audit entry recorded: {line}", "INFO")
            else:
                safe_log(f"Ignored line: {line}", "INFO")

        except Exception as e:
            failed += 1
            safe_log(f"Failed to process line '{line}': {e}", "ERROR")

    audit_file.close()
    summary = f"Processed: {processed}, Failed: {failed}"
    safe_log(summary, "INFO")
    print(summary)

if __name__== "__main__":
    input_lines = ["INFO: Connection successful", "ERROR: Timeout", "INFO: Retry"]
    process_log_lines(input_lines)