from app.calculator import Calculator
from app.history import LoggingObserver, AutoSaveObserver

def main():
    calc = Calculator()
    # observers
    calc.add_observer(LoggingObserver())
    if calc.config.auto_save:
        calc.add_observer(AutoSaveObserver())

    print("Calculator started. Type 'help' for commands.")
    while True:
        cmd = input("\nEnter command: ").strip()
        if not cmd:
            continue
        if cmd == "help":
            print("""
Available commands:
  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
  history, clear, undo, redo, save, load, exit
""")
            continue
        if cmd == "exit":
            print("Goodbye!")
            break
        if cmd == "history":
            for row in calc.get_history_dataframe().itertuples(index=False):
                print(f"{row.operation}({row.operand1}, {row.operand2}) = {row.result} @ {row.timestamp}")
            continue
        if cmd == "clear":
            calc.clear(); print("History cleared."); continue
        if cmd == "undo":
            print("Undone." if calc.undo() else "Nothing to undo."); continue
        if cmd == "redo":
            print("Redone." if calc.redo() else "Nothing to redo."); continue
        if cmd == "save":
            p = calc.save_history(); print(f"Saved to {p}"); continue
        if cmd == "load":
            calc.load_history(); print("History loaded."); continue

        # operation commands: op a b
        parts = cmd.split()
        if len(parts) == 3:
            op, a, b = parts
            try:
                result = calc.perform(op, a, b)
                print(f"= {result}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()
