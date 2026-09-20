import subprocess
import sys
import time
import webbrowser


STUDENT_URL = "http://localhost:8501"
PROFESSOR_URL = "http://localhost:8502"


def start_streamlit(script, port):
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            script,
            "--server.port",
            str(port),
        ]
    )


def stop_process(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def main():
    print("Starting Keepers of Akasha...")
    print(f"Student interface:   {STUDENT_URL}")
    print(f"Professor dashboard: {PROFESSOR_URL}")
    print("Press Ctrl+C to stop both servers.\n")

    student = start_streamlit("user_interface.py", 8501)
    professor = start_streamlit("dashboard.py", 8502)

    try:
        # Give Streamlit a moment to start, then open the student workspace.
        time.sleep(3)

        if student.poll() is not None:
            raise RuntimeError("Student interface failed to start.")

        if professor.poll() is not None:
            raise RuntimeError("Professor dashboard failed to start.")

        webbrowser.open(STUDENT_URL)

        while True:
            if student.poll() is not None:
                print("Student interface stopped unexpectedly.")
                break

            if professor.poll() is not None:
                print("Professor dashboard stopped unexpectedly.")
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping Keepers of Akasha...")

    finally:
        stop_process(student)
        stop_process(professor)
        print("Both servers stopped.")


if __name__ == "__main__":
    main()
