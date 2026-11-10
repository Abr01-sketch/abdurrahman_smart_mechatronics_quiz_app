"""
Smart Mechatronics Quiz App
---------------------------
A console quiz that tests basic to advanced mechatronics knowledge.

Features:
  - Welcome message and name entry
  - Difficulty selection (Beginner / Intermediate / Advanced)
  - Instructions shown before the quiz starts
  - 20 questions per level; 10 are picked at random every run
  - Answer options (A-D) shuffled so the correct answer moves around
  - Timer per question (a late answer counts as wrong)
  - Correct answer shown immediately when wrong
  - Score, percentage, grade and a personalized message
  - Review of all missed questions at the end
  - Play again option and a goodbye message
"""

import random   # used to shuffle and randomly pick questions
import time     # used for the per-question timer

# ---------------------------------------------------------------
# SETTINGS (easy to change)
# ---------------------------------------------------------------
QUESTIONS_PER_QUIZ = 10   # how many questions are asked each round
TIME_LIMIT = 20           # seconds allowed for each question


def make_q(question, correct, wrong1, wrong2, wrong3):
    """Build a question dictionary. The correct answer is listed first
    here for easy writing; the options are shuffled when asked."""
    return {"question": question,
            "options": [correct, wrong1, wrong2, wrong3],
            "answer": 0}


# ---------------------------------------------------------------
# QUESTION BANKS
# Each bank is a LIST of question dictionaries (20 per level).
# ---------------------------------------------------------------

beginner_questions = [
    make_q("Mechatronics combines mechanical engineering with what?",
           "Electronics and computing/control", "Chemistry and biology",
           "Architecture and law", "Agriculture and fishing"),
    make_q("Which sensor measures temperature?",
           "Thermistor", "Ultrasonic", "IR", "LDR"),
    make_q("Which component converts electrical energy into motion?",
           "Actuator", "Sensor", "Resistor", "Capacitor"),
    make_q("What does LED stand for?",
           "Light Emitting Diode", "Low Energy Device",
           "Linear Electric Driver", "Light Energy Display"),
    make_q("What is the unit of electrical resistance?",
           "Ohm", "Volt", "Ampere", "Watt"),
    make_q("Which sensor detects light intensity?",
           "LDR", "Thermocouple", "Strain gauge", "Potentiometer"),
    make_q("Which motor can rotate to a precise commanded angle?",
           "Servo Motor", "Brushed DC Motor",
           "Three-phase Induction Motor", "Universal Motor"),
    make_q("Which of these is a popular microcontroller board?",
           "Arduino Uno", "Hydraulic Pump", "Solenoid Valve", "Relay"),
    make_q("Which protective equipment shields your eyes in a workshop?",
           "Safety goggles", "Ear muffs", "Safety boots", "Apron"),
    make_q("Which device stops a machine immediately in an emergency?",
           "Emergency stop button", "Start button", "Limit switch",
           "Indicator lamp"),
    make_q("What does a sensor do?",
           "Detects a physical change and converts it to a signal",
           "Produces motion", "Stores electrical energy", "Cuts the power"),
    make_q("Which component stores electrical charge?",
           "Capacitor", "Resistor", "Diode", "Fuse"),
    make_q("Which unit measures electric current?",
           "Ampere", "Volt", "Ohm", "Henry"),
    make_q("Which component allows current to flow in one direction only?",
           "Diode", "Resistor", "Capacitor", "Inductor"),
    make_q("What does DC stand for in electronics?",
           "Direct Current", "Digital Control", "Dual Circuit",
           "Dynamic Charge"),
    make_q("Which tool measures voltage, current and resistance?",
           "Multimeter", "Vernier caliper", "Torque wrench", "Spirit level"),
    make_q("Which component protects a circuit from too much current?",
           "Fuse", "Switch", "LED", "Buzzer"),
    make_q("Which part of a mechatronic system processes the inputs "
           "and makes decisions?",
           "Controller", "Actuator", "Gearbox", "Sensor"),
    make_q("What is a gear train mainly used to change?",
           "Speed and torque", "Colour", "Temperature", "Resistance"),
    make_q("What does a push button do in a circuit?",
           "Makes or breaks the circuit manually", "Stores energy",
           "Measures voltage", "Amplifies current"),
]

intermediate_questions = [
    make_q("What does PLC stand for?",
           "Programmable Logic Controller", "Power Line Controller",
           "Primary Load Circuit", "Parallel Logic Converter"),
    make_q("Pneumatic systems use which working medium?",
           "Compressed air", "Hydraulic oil", "Steam", "Water only"),
    make_q("Hydraulic systems transmit power using what?",
           "Pressurised liquid (oil)", "Compressed air",
           "Electric current", "Magnetic fields"),
    make_q("In an Arduino sketch, which function runs repeatedly?",
           "loop()", "setup()", "main()", "begin()"),
    make_q("What does PWM stand for?",
           "Pulse Width Modulation", "Power Wire Management",
           "Phase Wave Motor", "Peak Wattage Meter"),
    make_q("Which circuit lets a microcontroller control the speed AND "
           "direction of a DC motor?",
           "H-bridge", "Voltage divider", "Rectifier", "Oscillator"),
    make_q("Which sensor measures distance using sound waves?",
           "Ultrasonic sensor", "LDR", "Thermistor", "Hall sensor"),
    make_q("Which component protects a transistor from the voltage spike "
           "produced by a relay coil or motor?",
           "Flyback diode", "LED", "Fuse holder", "Potentiometer"),
    make_q("Which AC motor is the most widely used in industry?",
           "Three-phase induction motor", "Stepper motor",
           "Brushed DC motor", "Servo motor"),
    make_q("Which PLC programming language is drawn with rungs, "
           "like an electrical circuit?",
           "Ladder logic", "Python", "Assembly only", "HTML"),
    make_q("Which valve controls the direction of air flow in a "
           "pneumatic system?",
           "Directional control valve", "Air filter", "Silencer",
           "Pressure gauge"),
    make_q("Which sensor detects metal objects without touching them?",
           "Inductive proximity sensor", "LDR", "Thermistor", "Microphone"),
    make_q("What does a relay do?",
           "Acts as an electrically controlled switch",
           "Amplifies sound", "Measures temperature", "Stores data"),
    make_q("Which motor moves in fixed angular steps?",
           "Stepper motor", "Brushed DC motor", "Induction motor",
           "Generator"),
    make_q("Which equation represents Ohm's law?",
           "V = I x R", "F = m x a", "E = m x c squared", "P = h / t"),
    make_q("Which Arduino function sets a pin as INPUT or OUTPUT?",
           "pinMode()", "digitalRead()", "delay()", "Serial.begin()"),
    make_q("What is the job of a hydraulic pump?",
           "Moves fluid to create flow in the system",
           "Stores oil", "Filters the oil", "Cools the oil"),
    make_q("Which component smooths the ripple in a DC power supply?",
           "Capacitor", "Diode", "Fuse", "Relay"),
    make_q("What does HMI stand for in automation?",
           "Human Machine Interface", "High Motor Input",
           "Hybrid Mechanical Interface", "Hydraulic Machine Indicator"),
    make_q("What do the input modules of a PLC connect to?",
           "Sensors and push buttons", "Only motors",
           "Only power cables", "Printers"),
]

advanced_questions = [
    make_q("In a PID controller, what does the Integral (I) term mainly do?",
           "Removes steady-state error", "Predicts future error",
           "Filters sensor noise", "Increases motor torque directly"),
    make_q("Which hydraulic component produces linear motion from "
           "fluid pressure?",
           "Hydraulic cylinder", "Hydraulic motor", "Accumulator",
           "Pressure relief valve"),
    make_q("How many ports does a 5/2 directional control valve have?",
           "5", "2", "3", "7"),
    make_q("What is the minimum number of degrees of freedom a robot "
           "arm needs to place AND orient its tool anywhere in 3D space?",
           "6", "3", "4", "5"),
    make_q("What does a rotary encoder measure?",
           "Shaft position and speed", "Temperature",
           "Gas concentration", "Humidity"),
    make_q("A 10-bit ADC (like the one on an Arduino Uno) can output "
           "how many different values?",
           "1024", "256", "512", "4096"),
    make_q("In an induction motor, what is 'slip'?",
           "Difference between synchronous speed and rotor speed",
           "Loss of insulation", "Voltage drop in the cable",
           "Wear of the brushes"),
    make_q("What does a closed-loop control system use that an "
           "open-loop system does not?",
           "Feedback from a sensor", "A bigger motor",
           "A hydraulic pump", "Higher voltage"),
    make_q("Which communication protocol uses the SDA and SCL lines?",
           "I2C", "UART", "SPI", "CAN"),
    make_q("What is the purpose of a pull-up resistor on a digital input?",
           "Keeps the input at a defined HIGH when the switch is open",
           "Increases motor speed", "Stores energy", "Amplifies the signal"),
    make_q("Which PID term responds to the rate of change of the error?",
           "Derivative", "Proportional", "Integral", "On-off"),
    make_q("What is the purpose of an optocoupler?",
           "Electrically isolates two circuits", "Amplifies current",
           "Stores charge", "Generates PWM"),
    make_q("In robotics, what does forward kinematics calculate?",
           "End-effector position from the joint angles",
           "Joint angles from a target position", "Battery life",
           "Program execution speed"),
    make_q("Which protocol is widely used in industrial automation to "
           "link PLCs, drives and I/O devices?",
           "Modbus", "HTML", "HDMI", "Bluetooth audio"),
    make_q("What does a variable frequency drive (VFD) mainly control?",
           "The speed of an AC induction motor",
           "Sensor accuracy", "Hydraulic oil temperature", "Air pressure"),
    make_q("According to Pascal's law, pressure applied to a confined "
           "fluid is transmitted how?",
           "Equally in all directions", "Only upward",
           "Only to the piston", "It decreases with distance"),
    make_q("What does a pressure relief valve do?",
           "Limits the maximum system pressure", "Directs the flow",
           "Measures the flow", "Cools the oil"),
    make_q("What is aliasing in signal sampling?",
           "Distortion when sampling below twice the signal frequency",
           "Excess heat in a motor", "Motor overload", "Wire corrosion"),
    make_q("Which microcontroller peripheral is normally used to "
           "generate PWM signals?",
           "Timer", "ADC", "UART", "EEPROM"),
    make_q("What is the role of a watchdog timer?",
           "Resets the microcontroller if the software hangs",
           "Tells the time of day", "Generates PWM", "Limits motor speed"),
]

# Dictionary that maps the menu choice (int) to a level name and its questions
levels = {
    1: ("Beginner", beginner_questions),
    2: ("Intermediate", intermediate_questions),
    3: ("Advanced", advanced_questions),
}


# ---------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------

def calculate_grade(percentage, name):
    """Return a (grade, personalized message) pair for a percentage.
    This function RETURNS a value (project requirement)."""
    # if/elif/else chain assigns the grade based on the score range
    if percentage >= 95:
        return "A+", f"🏆 Excellent, {name}! You are a Future Mechatronics Engineer!"
    elif percentage >= 80:
        return "A", f"🌟 Very Good, {name}! Almost perfect!"
    elif percentage >= 60:
        return "B", f"👍 Good Job, {name}! Keep it up!"
    elif percentage >= 40:
        return "C", f"📚 Keep Practicing, {name}. You are getting there!"
    else:
        return "D", f"💪 Don't Give Up, {name}. Every engineer started here!"


def get_menu_choice(prompt, valid_options):
    """Keep asking until the user types a valid whole number from the menu.
    Uses int() conversion with error handling."""
    while True:
        try:
            choice = int(input(prompt))      # convert text to an integer
        except ValueError:                   # user typed letters/blank
            print("❌ Invalid input. Please enter a number.")
            continue
        if choice in valid_options:          # check it is on the menu
            return choice
        print("❌ Invalid option. Choose from:", list(valid_options))


def shuffle_options(q):
    """Return a copy of the question with the A-D options shuffled,
    and 'answer' updated to the correct option's new position."""
    correct_text = q["options"][q["answer"]]   # remember the right answer
    options = q["options"][:]                  # copy so the bank is unchanged
    random.shuffle(options)
    return {"question": q["question"],
            "options": options,
            "answer": options.index(correct_text)}


def show_instructions(name, level_name):
    """Display the rules before the quiz starts."""
    print("\n" + "-" * 40)
    print(f"📋 INSTRUCTIONS FOR {name.upper()} ({level_name} level)")
    print("-" * 40)
    print(f"1. You will answer {QUESTIONS_PER_QUIZ} multiple-choice questions.")
    print("2. Type A, B, C or D and press Enter to answer.")
    print(f"3. You have {TIME_LIMIT} seconds per question.")
    print("   A late answer counts as wrong.")
    print("4. Each correct answer earns 1 point.")
    print("5. If you are wrong, the correct answer is shown at once.")
    print("6. Missed questions are reviewed at the end.")
    print("-" * 40)
    input("Press Enter when you are ready to start...")


def ask_question(number, total, q):
    """Display one question, read and validate the answer, apply the timer.
    Returns True if correct (and in time), False otherwise."""
    q = shuffle_options(q)                   # randomize A-D order
    print(f"\nQuestion {number} of {total}")
    print(q["question"], "\n")

    # Print the options labelled A, B, C, D
    for i, option in enumerate(q["options"]):
        print(f"{chr(65 + i)}. {option}")

    start = time.time()                      # start the timer

    # Keep asking until the user enters A, B, C or D (error handling)
    while True:
        answer = input(f"\nYour answer ({TIME_LIMIT}s): ").strip().upper()
        if answer in ("A", "B", "C", "D"):
            break
        print("❌ Invalid choice. Please type A, B, C or D.")

    elapsed = time.time() - start            # how long the user took
    correct_text = q["options"][q["answer"]]

    # Check the time first, then the answer
    if elapsed > TIME_LIMIT:
        print(f"⏰ Time's up! You took {elapsed:.0f} seconds.")
        print("Correct Answer:")
        print(correct_text)
        return False

    user_index = ord(answer) - 65            # convert 'A'->0, 'B'->1 ...

    if user_index == q["answer"]:
        print(f"✅ Correct! ({elapsed:.1f}s)")
        return True
    else:
        print("❌ Wrong!")
        print("Correct Answer:")
        print(correct_text)                  # show the right answer at once
        return False


def run_quiz(name):
    """Run one full round of the quiz and display the results."""
    # --- Choose difficulty ---
    print("\nChoose Difficulty:")
    print("1. Beginner")
    print("2. Intermediate")
    print("3. Advanced")
    choice = get_menu_choice("Enter 1, 2 or 3: ", levels.keys())
    level_name, question_bank = levels[choice]

    # Instructions after the name and level are known
    show_instructions(name, level_name)

    # Pick 10 random questions from the bank of 20 (random order too)
    questions = random.sample(question_bank, QUESTIONS_PER_QUIZ)

    score = 0
    missed = []   # stores (question number, question dict) for wrong answers

    print(f"\n🚀 Starting the {level_name} quiz, {name}. Good luck!")

    # --- Main loop: go through every question ---
    for number, q in enumerate(questions, start=1):
        if ask_question(number, len(questions), q):
            score += 1                       # update score
        else:
            missed.append((number, q))       # remember the mistake

    # --- Results ---
    total = len(questions)
    percentage = (score / total) * 100       # float division
    grade, message = calculate_grade(percentage, name)

    print("\n" + "=" * 40)
    print(f"Quiz complete, {name}!")
    print(f"Level      : {level_name}")
    print(f"Score      : {score}/{total}")
    print(f"Percentage : {percentage:.1f}%")
    print(f"Grade      : {grade}")
    print(message)
    print("=" * 40)

    # --- Review of incorrect answers ---
    if missed:
        print("\nQuestions you missed:")
        for number, q in missed:
            print(f"\nQuestion {number}: {q['question']}")
            print(f"Correct Answer: {q['options'][q['answer']]}")
    else:
        print("\n🎉 Perfect score, nothing to review!")


def main():
    """Program entry point: welcome, name, quiz, replay loop, goodbye."""
    print("=" * 40)
    print("  ⚙️  SMART MECHATRONICS QUIZ APP  ⚙️")
    print("=" * 40)
    print("Test your mechatronics knowledge!\n")

    try:
        # Ask for the name; keep asking if the user leaves it blank
        name = input("Enter your name: ").strip()
        while name == "":
            print("❌ Name cannot be empty.")
            name = input("Enter your name: ").strip()
        print(f"\nWelcome, {name}!")

        # Replay loop
        while True:
            run_quiz(name)

            print("\nPlay again?")
            print("1. Yes")
            print("2. No")
            again = get_menu_choice("Enter 1 or 2: ", [1, 2])
            if again == 2:
                break
    except (KeyboardInterrupt, EOFError):
        print()   # user pressed Ctrl+C: exit politely

    # Goodbye message
    print("\n" + "=" * 40)
    print("Thank you for playing the Smart Mechatronics Quiz!")
    print("Keep learning, keep building, and keep innovating. 🔧🤖")
    print("See you next time!")
    print("=" * 40)


# Run the program only when this file is executed directly
if __name__ == "__main__":
    main()
