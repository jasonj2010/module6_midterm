from __future__ import annotations
from pathlib import Path
from app.calculator import Calculator

HELP = """\
Available commands:
  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff - Perform calculations
  history - Show calculation history
  clear - Clear calculation history
  undo - Undo the last calculation
  redo - Redo the last undone calculation
  save - Save calculation history to file
  load - Load calculation history from file
  help - Show this help
  exit - Exit the calculator
"""

def main() -> None:
    calc = Calculator(Path.cwd())
    print("Calculator started. Type 'help' for commands.")
    while True:
        try:
            raw = input("\nEnter command: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not raw:
            continue

        if raw.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if raw.lower() in {"help", "h", "?"}:
            print("\n" + HELP)
            continue

        if raw.lower() == "history":
            df = calc.get_history_dataframe()
            if df.empty:
                print("No history.")
            else:
                print(df.to_string(index=False))
            continue

        if raw.lower() == "clear":
            calc.clear()
            print("History cleared.")
            continue

        if raw.lower() == "undo":
            ok = calc.undo()
            print("Undone." if ok else "Nothing to undo.")
            continue

        if raw.lower() == "redo":
            ok = calc.redo()
            print("Redone." if ok else "Nothing to redo.")
            continue

        if raw.lower() == "save":
            p = calc.save_history()
            print(f"Saved to: {p}")
            continue

        if raw.lower() == "load":
            calc.load_history()
            print("History loaded (if file existed).")
            continue

        # operations: op a b
        parts = raw.split()
        if len(parts) == 3:
            op, a, b = parts[0], parts[1], parts[2]
            try:
                result = calc.perform(op, a, b)
                print(f"{op}({a}, {b}) = {result}")
            except Exception as e:  # pragma: no cover (interactive)
                print(f"Error: {e}")
            continue

        print("Unknown command. Type 'help'.")

if __name__ == "__main__":  # pragma: no cover (script entry)
    main()
