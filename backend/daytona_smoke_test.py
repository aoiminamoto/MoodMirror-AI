from daytona import Daytona


def main():
    daytona = Daytona()

    print("Creating Daytona sandbox...")
    sandbox = daytona.create()

    try:
        result = sandbox.process.code_run(
            'print("MoodMirror Daytona OK")'
        )

        print("Sandbox result:")
        print(result.result)

    finally:
        try:
            sandbox.delete()
        except Exception:
            pass


if __name__ == "__main__":
    main()