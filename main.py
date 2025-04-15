import speech
import commands

def main():
    speech.listen_for_wake_word()  # Listen for wake word once
    while True:
        command = speech.get_command()
        if command:
            commands.handle_command(command)

if __name__ == "__main__":
    main()