###########################################################################
# Circuit analyzer
print("\n##################################################################################")
print("Welcome!")
print()
print("This code simulates an LRCC circuit.")
print("The goal is to optimize the inductor voltage magnitude.")
print("Examples are provided under 3) Run calculations.")
print("##################################################################################\n\n")
###########################################################################

###########################################################################
# Default Defined Parameters
# These are variables that may be adjusted in the program.

# Voltage Supply
input_voltage, input_impedance = [1, 0], [50, 0] # Units of volts and ohms.
frequency, frequency_set = 10*(10**6), 10*(10**6) # Units of hertz. Enter the same value for both parameters.
angular_frequency = 2 * 3.14159265359 * frequency # Units of radians per second.
frequency_list = [] # List initialization.

# Components
inductor_resistance = 0.1 # Units of ohms.
inductance, inductance_set = 0.6*(10**(-6)), 0.6*(10**(-6)) # Units of henrys.
tuning_capacitance, tuning_capacitance_set = 25.2*(10**(-12)), 25.2*(10**(-12)) # Units of farads.
coupling_capacitance, coupling_capacitance_set = 1.19*(10**(-12)), 1.19*(10**(-12)) # Units of farads.
inductor_impedance = [0, 0] # Units of ohms. Serves as a placeholder until calculation.
tuning_impedance = [0, 0] # Units of ohms. Serves as a placeholder until calculation.
coupling_impedance = [0, 0] # Units of ohms. Serves as a placeholder until calculation.
inductor_list, tuning_list, coupling_list, total_list = [], [], [], [] # List initialization.
# list = [[Voltage (real), Voltage (imaginary)], [Current (real), Current (imaginary)], [Impedance (real), Impedance (imaginary)], capacitance]"

# Other
sampling_rate = 100 # Sets the number of datapoints calculated across the specified range.
fixed_calculation_counter = 0 # Used to correct undesired data duplication.
total_impedance, total_current = [], []
tuning_minimum, tuning_maximum, coupling_minimum, coupling_maximum, tuning_gradation, coupling_gradation = 0, 0, 0, 0, 0, 0 # Value initialization.
print_view = 0 # Used for troubleshooting. Set to 1 to view optional messages.


###########################################################################
# Basic Operations
# Here, z_n[0] is the real component, and z_n[1] is the imaginary component.

def add(z_1, z_2):
    """ Adds complex numbers. """
    real_sum = z_1[0] + z_2[0]
    imaginary_sum = z_1[1] + z_2[1]
    result = [real_sum, imaginary_sum]
    return result

def subtract(z_1, z_2):
    """ Subtracts complex numbers. """
    real_difference = z_1[0] - z_2[0]
    imaginary_difference = z_1[1] - z_2[1]
    result = [real_difference, imaginary_difference]
    return result
    
def multiply(z_1, z_2):
    """ Multiplies complex numbers. """
    real_product = (z_1[0] * z_2[0]) - (z_1[1] * z_2[1])
    imaginary_product = (z_1[0] * z_2[1]) + (z_1[1] * z_2[0])
    result = [real_product, imaginary_product]
    return result
    
def divide(z_1, z_2):
    """ Divides complex numbers. """
    real_numerator = (z_1[0] * z_2[0]) + (z_1[1] * z_2[1])
    imaginary_numerator = (z_1[1] * z_2[0]) - (z_1[0] * z_2[1])
    denominator = (z_2[0])**2 + (z_2[1])**2
    real_quotient = real_numerator / denominator
    imaginary_quotient = imaginary_numerator / denominator
    result = [real_quotient, imaginary_quotient]
    return result
    
def parallel(z_1, z_2):
    """ Adds two complex numbers as an inverse reciprocal sum. """
    numerator = multiply(z_1, z_2)
    denominator = add(z_1, z_2)
    result = divide(numerator, denominator)
    return result
    
def magnitude(z_1, z_2):
    result = (z_1**2 + z_2**2)**(1/2)
    return result
    

###########################################################################
# Functions

def impedance_calculations():
    """ Updates the impedance at a given frequency for all components. """
    global angular_frequency, inductor_impedance, tuning_impedance, coupling_impedance
    if print_view == 1: print("impedance_calculations():") # Used for troubleshooting.
    angular_frequency = 2 * 3.14159265359 * frequency # Units of radians per second.
    inductor_impedance = [inductor_resistance, angular_frequency * inductance] # Units of ohms.
    tuning_impedance = [0, -1/(angular_frequency * tuning_capacitance)] # Units of ohms.
    coupling_impedance = [0, -1/(angular_frequency * coupling_capacitance)] # Units of ohms.
    reduce_circuit()

def reduce_circuit():
    """ Determines the total impedance and current of the circuit, given some input voltage. """
    global total_impedance, total_current
    if print_view == 1: print("reduce_circuit():") # Used for troubleshooting.
    parallel_impedance = parallel(inductor_impedance, tuning_impedance) # Inductor and tuning capacitor.
    total_impedance = add(parallel_impedance, coupling_impedance) # Inductor, tuning capacitor, and coupling capacitor.
    effective_impedance = add(total_impedance, input_impedance) # Includes input resistance for total current.
    total_current = divide(input_voltage, effective_impedance) # Current as influenced by the input resistance.
    return total_current, parallel_impedance
    
def solve_circuit(total_current, parallel_impedance):
    """ Calculates the voltage and current across each component, given the total current of the circuit. """
    if print_view == 1: print("solve_circuit():\n") # Used for troubleshooting.
    coupling_voltage = multiply(total_current, coupling_impedance) # Coupling capacitor.
    parallel_voltage = multiply(total_current, parallel_impedance) # Tuning capacitor and inductor.
    tuning_current = divide(parallel_voltage, tuning_impedance) # Tuning capacitor.
    inductor_current = divide(parallel_voltage, inductor_impedance) # Inductor.
    total_values = [input_voltage, total_current, total_impedance] # Totals as seen from the voltage source.
    coupling_values = [coupling_voltage, total_current, coupling_impedance, coupling_capacitance]
    tuning_values = [parallel_voltage, tuning_current, tuning_impedance, tuning_capacitance]
    inductor_values = [parallel_voltage, inductor_current, inductor_impedance, inductance]
    frequency_list.append(frequency) # Logs the frequency used in the calculations.
    total_list.append(total_values) # Logs the results of the calculations.
    inductor_list.append(inductor_values) # Logs the results of the calculations.
    tuning_list.append(tuning_values) # Logs the results of the calculations.
    coupling_list.append(coupling_values) # Logs the results of the calculations.

def export_data():
    """ Saves current calculation lists to tab separated values in a text file. """
    global frequency_list, total_list, inductor_list, tuning_list, coupling_list
    if print_view == 1: print("export_data():\n") # Used for troubleshooting.
    #print(tuning_list[0])
    #print(coupling_list[0])
    #frequency_list.pop(0)
    #total_list.pop(0)
    #inductor_list.pop(0)
    #tuning_list.pop(0)
    #coupling_list.pop(0)
    with open("=data.txt", 'w', encoding='utf-8') as data_file:
        export_titles = ("Frequency [Hz]\t"
            "Total voltage (real) [V]\t"
            "Total voltage (imaginary) [V]\t"
            "Total current (real) [A]\t"
            "Total current (imaginary) [A]\t"
            "Total impedance (real) [Ω]\t"
            "Total impedance (imaginary) [Ω]\t"
            "Inductance [H]\t"
            "Inductor voltage (real) [V]\t"
            "Inductor voltage (imaginary) [V]\t"
            "Inductor current (real) [A]\t"
            "Inductor current (imaginary) [A]\t"
            "Inductor impedance (real) [Ω]\t"
            "Inductor impedance (imaginary) [Ω]\t"
            "Tuning capacitance [F]\t"
            "Tuning voltage (real) [V]\t"
            "Tuning voltage (imaginary) [V]\t"
            "Tuning current (real) [A]\t"
            "Tuning current (imaginary) [A]\t"
            "Tuning impedance (real) [Ω]\t"
            "Tuning impedance (imaginary) [Ω]\t"
            "Coupling capacitance [F]\t"
            "Coupling voltage (real) [V]\t"
            "Coupling voltage (imaginary) [V]\t"
            "Coupling current (real) [A]\t"
            "Coupling current (imaginary) [A]\t"
            "Coupling impedance (real) [Ω]\t"
            "Coupling impedance (imaginary) [Ω]\t")
        print(export_titles, file=data_file)
        for i in range(len(total_list)):
            export_values = (f"{frequency_list[i]}\t"
                f"{total_list[i][0][0]}\t"
                f"{total_list[i][0][1]}\t"
                f"{total_list[i][1][0]}\t"
                f"{total_list[i][1][1]}\t"
                f"{total_list[i][2][0]}\t"
                f"{total_list[i][2][1]}\t"
                f"{inductor_list[i][-1]}\t"
                f"{inductor_list[i][0][0]}\t"
                f"{inductor_list[i][0][1]}\t"
                f"{inductor_list[i][1][0]}\t"
                f"{inductor_list[i][1][1]}\t"
                f"{inductor_list[i][2][0]}\t"
                f"{inductor_list[i][2][1]}\t"
                f"{tuning_list[i][-1]}\t"
                f"{tuning_list[i][0][0]}\t"
                f"{tuning_list[i][0][1]}\t"
                f"{tuning_list[i][1][0]}\t"
                f"{tuning_list[i][1][1]}\t"
                f"{tuning_list[i][2][0]}\t"
                f"{tuning_list[i][2][1]}\t"
                f"{coupling_list[i][-1]}\t"
                f"{coupling_list[i][0][0]}\t"
                f"{coupling_list[i][0][1]}\t"
                f"{coupling_list[i][1][0]}\t"
                f"{coupling_list[i][1][1]}\t"
                f"{coupling_list[i][2][0]}\t"
                f"{coupling_list[i][2][1]}")
            print(export_values, file=data_file)

def print_values():
    """ Prints values in the program. """
    print("##################################################################################")
    defined_parameters = (f"Sampling rate:\t\t\t{sampling_rate}\n"
        f"Supply voltage [V]:\t\t({input_voltage[0]:.2f})+i({input_voltage[1]:.2f})\n"
        f"Supply impedance [Ω]:\t\t({input_impedance[0]:.2f})+i({input_impedance[1]:.2f})\n"
        f"Frequency [Hz]:\t\t\t{(frequency):.2e}\n"
        f"Angular frequency [s⁻¹]:\t{angular_frequency:.2e}\n"
        f"Inductance [H]:\t\t\t{inductance:.2e}\n"
        f"Tuning capacitance [F]:\t\t{tuning_capacitance:.2e}\n"
        f"Coupling capacitance [F]:\t{coupling_capacitance:.2e}\n")
    calculated_values = (f"Total current [A]:\t\t({total_list[0][1][0]:.2e})+i({total_list[0][1][1]:.2e})\n"
        f"Total impedance [Ω]:\t\t({total_list[0][2][0]:.2e})+i({total_list[0][2][1]:.2e})\n"
        f"Inductor voltage [V]:\t\t({inductor_list[0][0][0]:.2e})+i({inductor_list[0][0][1]:.2e})\n"
        f"Inductor current [A]:\t\t({inductor_list[0][1][0]:.2e})+i({inductor_list[0][1][1]:.2e})\n"
        f"Inductor impedance [Ω]:\t\t({inductor_list[0][2][0]:.2e})+i({inductor_list[0][2][1]:.2e})\n"
        f"Tuning voltage [V]:\t\t({tuning_list[0][0][0]:.2e})+i({tuning_list[0][0][1]:.2e})\n"
        f"Tuning current [A]:\t\t({tuning_list[0][1][0]:.2e})+i({tuning_list[0][1][1]:.2e})\n"
        f"Tuning impedance [Ω]:\t\t({tuning_list[0][2][0]:.2e})+i({tuning_list[0][2][1]:.2e})\n"
        f"Coupling voltage [V]:\t\t({coupling_list[0][0][0]:.2e})+i({coupling_list[0][0][1]:.2e})\n"
        f"Coupling current [A]:\t\t({coupling_list[0][1][0]:.2e})+i({coupling_list[0][1][1]:.2e})\n"
        f"Coupling impedance [Ω]:\t\t({coupling_list[0][2][0]:.2e})+i({coupling_list[0][2][1]:.2e})")
    print(defined_parameters)
    print(calculated_values)
    print("##################################################################################\n\n")

def update_fixed_values():
    """ Updates a parameter based on user entry. It accepts scientific notation (ex. 6.63e-34). """
    global frequency, sampling_rate, inductance, tuning_capacitance, coupling_capacitance, frequency_set, inductance_set, tuning_capacitance_set, coupling_capacitance_set
    action = int(input("Select a value to change:\n1) Frequency\n2) Sampling rate\n3) Inductance\n4) Inductor resistance\n5) Tuning capacitance\n6) Coupling capacitance\n0) Quit to main menu.\n\n"))
    print("\n")
    if action == 0:
        main()
    elif action == 1:
        frequency = float(input("Enter frequency [Hz]:\t"))
    elif action == 2:
        sampling_rate = int(float(input("Enter sampling rate:\t")))
    elif action == 3:
        inductance = float(input("Enter inductance [H]:\t"))
    elif action == 4:
        inductor_resistance = float(input("Enter resistance [Ω]:\t"))
    elif action == 5:
        tuning_capacitance = float(input("Enter tuning capacitance [F]:\t"))
    elif action == 6:
        coupling_capacitance = float(input("Enter coupling capacitance [F]:\t"))
    frequency_set, inductance_set, tuning_capacitance_set, coupling_capacitance_set = frequency, inductance, tuning_capacitance, coupling_capacitance
    print("\n")
    impedance_calculations()

def fixed_calculation():
    """ Solves the circuit with one set of parameters. """
    global tuning_impedance, fixed_calculation_counter
    impedance_calculations()
    total_current, parallel_impedance = reduce_circuit()
    solve_circuit(total_current, parallel_impedance)

def cluster_calculation():
    """ Solves the circuit with one parameter as a variable. """
    global tuning_capacitance, coupling_capacitance, frequency
    reset_variables() # Prepares the program for the next calculation.
    reset_lists() # Prepares the program for the next calculation.
    action = int(input("Select a variable:\n1) Tuning capacitance.\n2) Coupling capacitance.\n3) Frequency.\n0) Quit to main menu.\n\n"))
    print("\n")
    if action == 0:
        main()
    else:
        print("Enter 0 for each variable to quit to main menu.")
        if action == 1: # Sets the tuning capacitor as a variable.
            minimum = float(input("Enter a minimum value [F]:\t")) # Sets minimum capacitance.
            maximum = float(input("Enter a maximum value [F]:\t")) # Sets maximum capacitance.
            print("\n")
            if (minimum + maximum) != 0:
                tuning_capacitance = minimum # Sets the minimum as the first value in the series.
                gradation = ((maximum - minimum)/sampling_rate) # Sets the number of farads between each value.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation:.2e}\n")
                for i in range(sampling_rate+1): # Cycles through each value in the chosen interval.
                    fixed_calculation() # Calculates values for the current parameters.
                    tuning_capacitance += gradation # Sets the next parameter.
                return True
            else:
                print("\n")
                main()
        if action == 2: # Sets the coupling capacitor as the variable.
            minimum = float(input("Enter a minimum value [F]:\t")) # Sets minimum capacitance.
            maximum = float(input("Enter a maximum value [F]:\t")) # Sets maximum capacitance.
            if (minimum + maximum) != 0:
                coupling_capacitance = minimum # Sets the minimum as the first value in the series.
                gradation = ((maximum - minimum)/sampling_rate) # Sets the number of farads between each value.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation:.2e}\n")
                for i in range(sampling_rate+1): # Cycles through each value in the chosen interval.
                    fixed_calculation() # Calculates values for the current parameters.
                    coupling_capacitance += gradation # Sets the next parameter.
                return True
            else:
                print("\n")
                main()
        if action == 3: # Sets the input frequency as the variable.
            minimum = float(input("Enter a minimum value [Hz]:\t")) # Sets minimum frequency.
            maximum = float(input("Enter a maximum value [Hz]:\t")) # Sets maximum frequency.
            if (minimum + maximum) != 0:
                frequency = minimum # Sets the minimum as the first value in the series.
                gradation = ((maximum - minimum)/sampling_rate) # Sets the number of hertz between each value.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation:.2e}\n")
                for i in range(sampling_rate+1): # Cycles through each value in the chosen interval.
                    fixed_calculation() # Calculates values for the current parameters.
                    frequency += gradation # Sets the next parameter.
                return True
            else:
                print("\n")
                main()

def dense_calculation(force=False):
    """ Solves the circuit with both capacitance values as variables. """
    global tuning_capacitance, coupling_capacitance, tuning_minimum, tuning_maximum, coupling_minimum, coupling_maximum, tuning_gradation, coupling_gradation
    reset_variables() # Prepares the program for the next calculation.
    reset_lists() # Prepares the program for the next calculation.
    if force:
        tuning_minimum, tuning_maximum, coupling_minimum, coupling_maximum = 1e-14, 1e-3, 1e-14, 1e-3
    else:
        print("Enter 0 for each variable to quit to main menu.")
        tuning_minimum = float(input("Enter a minimum tuning capacitance [F]:\t\t")) # Sets minimum capacitance.
        tuning_maximum = float(input("Enter a maximum tuning capacitance [F]:\t\t")) # Sets maximum capacitance.
        coupling_minimum = float(input("Enter a minimum coupling capacitance [F]:\t")) # Sets minimum capacitance.
        coupling_maximum = float(input("Enter a maximum coupling capacitance [F]:\t")) # Sets maximum capacitance.
    print("\n")
    if (tuning_minimum + tuning_maximum + coupling_minimum + coupling_maximum) != 0:
        tuning_capacitance = tuning_minimum # Sets the minimum as the first value in the series.
        coupling_capacitance = coupling_minimum # Sets the minimum as the first value in the series.
        tuning_gradation = (tuning_maximum - tuning_minimum)/sampling_rate # Sets the number of farads between each value.
        coupling_gradation = (coupling_maximum - coupling_minimum)/sampling_rate # Sets the number of farads between each value.
        print(f"Sampling rate:\t\t\t{sampling_rate}\nTuning gradation [F]:\t\t{tuning_gradation:.2e}\nCoupling gradation [F]:\t\t{coupling_gradation:.2e}\n")
        for i in range(sampling_rate+1): # Cycles through tuning parameters.
            for i in range(sampling_rate+1): # Cycles through coupling parameters.
                fixed_calculation() # Calculates values for the current parameters.
                coupling_capacitance += coupling_gradation # Sets the next parameter.
            coupling_capacitance = coupling_minimum # Sets the minimum as the first value in the series.
            tuning_capacitance += tuning_gradation # Sets the next parameter.
    else:
        main()

def complex_algebra():
    """ Computes binary operations on complex numbers. """
    print("Enter 0 for each variable to quit to main menu.")
    x_1 = float(input("Enter Re(z_1):\t")) # Sets first real component.
    y_1 = float(input("Enter Im(z_1):\t")) # Sets first imaginary component.
    x_2 = float(input("Enter Re(z_2):\t")) # Sets second real component.
    y_2 = float(input("Enter Im(z_2):\t")) # Sets second imaginary component.
    print("\n")
    if (x_1 + y_1 + x_2 + y_2) != 0:
        z_1, z_2 = [x_1, y_1], [x_2, y_2] # Pairs each component as a list.
        operation = int(input("Select an operation:\n1) Addition.\n2) Subtraction.\n3) Multiplication.\n4) Division.\n5) Parallel components.\n0) Quit to main menu.\n\n"))
        print("\n")
        if operation != 0:
            if operation == 1:
                result = add(z_1, z_2)
            if operation == 2:
                result = subtract(z_1, z_2)
            if operation == 3:
                result = multiply(z_1, z_2)
            if operation == 4:
                result = divide(z_1, z_2)
            if operation == 5:
                result = parallel(z_1, z_2)
            print(f"Result:\t({result[0]})+i({result[1]})\n\n")
        else:
            main()
    else:
        main()

def brute_force():
    global sampling_rate
    action = int(input("Warning! This function makes millions of computations and may take some time.\n1) Confirm.\n0) Exit.\n\n"))
    print("\n")
    if action == 1:
        sampling_rate = 3000
        dense_calculation(True)
    else:
        main()

def information():
    print("Circuit diagram:\n")
    print(".................................................................................\n"
        "....................|  |.........................................................\n"
        "....................|  |.........................................................\n"
        "...OOOOOOOOOOOOOOOOO|  |OOOOOOOOOOOOOOOOOOO......................................\n"
        "...OO...............|  |.................OO......................................\n"
        "...OO...............|  |.................OO......................................\n"
        "...//....................................OO............../\\..../\\................\n"
        "...\\\\.......COUPLING CAPACITOR...........OOOOOOOOOOOO\\\\///\\\\\\///\\\\OOOOOOOOOOOO...\n"
        "....\\\\...................................OO...........\\/....\\/..............OO...\n"
        "....//..INPUT IMPEDANCE..................OO...............................((())).\n"
        "...//................................----------.....WIRE RESISTANCE........(())..\n"
        "...\\\\..............TUNING CAPACITOR..          ...........................((())).\n"
        "...OO................................----------............................(())..\n"
        "...OO....................................OO.....................INDUCTOR..((())).\n"
        ".[ ~~ ]..................................OO.................................OO...\n"
        ".[ ~~ ]..AC INPUT/OUTPUT.................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO...\n"
        ".[ ~~ ]..................................OO......................................\n"
        "...OO....................................OO......................................\n"
        "...OO....................................OO......................................\n"
        "...OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO......................................\n"
        ".................................................................................\n"
        ".......................................PROBE CIRCUIT.............................\n"
        ".................................................................................\n\n")
    main()

def reset_variables():
    """ Reverts to the default values, rather than the last values calculated. Used in main(). """
    global frequency, inductance, tuning_capacitance, coupling_capacitance
    if print_view == 1: print("reset_variables():\n") # Used for troubleshooting.
    frequency, inductance, tuning_capacitance, coupling_capacitance = frequency_set, inductance_set, tuning_capacitance_set, coupling_capacitance_set
    
def reset_lists():
    """ Clears the data from the last calculation to prepare for the next. Used in main(). """
    global total_list, frequency_list, inductor_list, tuning_list, coupling_list
    if print_view == 1: print("reset_lists():\n") # Used for troubleshooting.
    total_list.clear()
    frequency_list.clear()
    inductor_list.clear()
    tuning_list.clear()
    coupling_list.clear()
    total_impedance.clear()
    total_current.clear()
    fixed_calculation_counter = 0

def maximum_inductance_voltage(index):
    inductor_voltage_list, loop_kill, tip_counter = [], 0, 0
    for i in range(len(inductor_list)):
        mag = magnitude(inductor_list[i][1][0],inductor_list[i][1][1])
        inductor_voltage_list.append(mag)
    maximum_voltage = max(inductor_voltage_list)
    if index == 0:
        for i in range(len(inductor_voltage_list)):
            if (inductor_voltage_list[i] == maximum_voltage) and (loop_kill == 0):
                loop_kill = 1
                print(f"Maximum inductor voltage [V]:\t{maximum_voltage:.2e}\n"
                        f"Frequency [Hz]:\t\t\t{frequency_list[i]:.2e}\n"
                        f"Tuning capacitance [F]:\t\t{tuning_list[i][-1]:.2e}\n"
                        f"Coupling capacitance [F]:\t{coupling_list[i][-1]:.2e}\n")
                if (tuning_minimum-tuning_gradation) <= tuning_list[i][-1] <= (tuning_minimum+tuning_gradation):
                    print("!! Try a lower tuning capacitance. !!")
                    tip_counter += 1
                if (tuning_maximum-tuning_gradation) <= tuning_list[i][-1] <= (tuning_maximum+tuning_gradation):
                    print("!! Try a lower tuning capacitance. !!")
                    tip_counter += 1
                if (coupling_minimum-tuning_gradation) <= coupling_list[i][-1] <= (coupling_minimum+tuning_gradation):
                    print("!! Try a lower coupling capacitance. !!")
                    tip_counter += 1
                if (coupling_maximum-tuning_gradation) <= coupling_list[i][-1] <= (coupling_maximum+tuning_gradation):
                    print("!! Try a higher coupling capacitance. !!")
                    tip_counter += 1
                if tip_counter == 2:
                    print("!! Try increasing the sampling rate or changing the range of values. !!")
    elif index == 1:
        return inductor_voltage_list

def plot_data(action_1=None, action_2=None, action_3=None):
    if action_1 is None:
        action_1 = int(input("Select a variable for the x-axis:\n1) Tuning capacitance.\n2) Coupling capacitance.\n3) Inductor voltage magnitude.\n4) Frequency.\n0) Quit to main menu.\n\n"))
        print("\n")
        action_2 = 0
        if action_1 == 0:
            main()
    if action_2 is None:
        action_2 = int(input("Select a variable for the y-axis:\n1) Tuning capacitance.\n2) Coupling capacitance.\n3) Inductor voltage magnitude.\n4) Frequency.\n0) Quit to main menu.\n\n"))
        print("\n")
        if action_2 == 0:
            main()
    if action_3 is None:
        action_3 = int(input("Select a variable for the z-axis:\n1) Tuning capacitance.\n2) Coupling capacitance.\n3) Inductor voltage magnitude.\n4) Frequency.\n0) No z-axis.\n\n"))
        print("\n")
    
    import matplotlib.pyplot as plt
    import matplotlib.axes as axes
    from math import log
    
    list_1, list_1_name, list_2, list_2_name, list_3, list_3_name = [], 0, [], 0, [], 0
    if action_1 == 1:
        list_1_name = "Tuning capacitance [F]"
        for i in range(len(tuning_list)):
            list_1.append(tuning_list[i][-1])
    elif action_1 == 2:
        list_1_name = "Coupling capacitance [F]"
        for i in range(len(tuning_list)):
            list_1.append(coupling_list[i][-1])
    elif action_1 == 3:
        list_1_name = "Inductor voltage magnitude [V]"
        list_1 = maximum_inductance_voltage(1)
    elif action_1 == 4:
        list_1_name = "Frequency [Hz]"
        for i in range(len(frequency_list)):
            list_1.append(frequency_list[i])
    if action_2 == 1:
        list_2_name = "Tuning capacitance [F]"
        for i in range(len(tuning_list)):
            list_2.append(tuning_list[i][-1])
    elif action_2 == 2:
        list_2_name = "Coupling capacitance [F]"
        for i in range(len(tuning_list)):
            list_2.append(coupling_list[i][-1])
    elif action_2 == 3:
        list_2_name = "Inductor voltage [V]"
        list_2 = maximum_inductance_voltage(1)
    elif action_2 == 4:
        list_2_name = "Frequency [Hz]"
        for i in range(len(frequency_list)):
            list_2.append(frequency_list[i])
    if action_3 == 1:
        list_3_name = "Tuning capacitance [F]"
        for i in range(len(tuning_list)):
            list_3.append(tuning_list[i][-1])
    elif action_3 == 2:
        list_3_name = "Coupling capacitance [F]"
        for i in range(len(tuning_list)):
            list_3.append(coupling_list[i][-1])
    elif action_3 == 3:
        list_3_name = "Inductor voltage [V]"
        list_3 = maximum_inductance_voltage(1)
    elif action_3 == 4:
        list_3_name = "Frequency [Hz]"
        for i in range(len(frequency_list)):
            list_3.append(frequency_list[i])
    if action_3 == 0:
        list_of_tuples = list(zip(list_1, list_2))
        list_of_tuples = [(x, y) for x, y in list_of_tuples]
        plt.scatter(*zip(*list_of_tuples)) # [(x_1, x_2, ...), (y_1, y_2, ...)]
        plt.xlabel(list_1_name)
        plt.ylabel(list_2_name)
    else:
        from matplotlib import cm
        import numpy as np
        #list_of_tuples = list(zip(list_1, list_2, list_3)) # Old method.
        #list_of_tuples = [(x, y, z) for x, y, z in list_of_tuples] # Old method.
        #fig = plt.figure() # Old method.
        #ax = fig.add_subplot(projection='3d') # Old method.
        #ax.scatter(*zip(*list_of_tuples)) # Old method.
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        list_1 = np.array(list_1)
        list_2 = np.array(list_2)
        list_3 = np.array(list_3)
        surf = ax.plot_trisurf(list_1, list_2, list_3, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.xaxis._axinfo['label']['space_factor'] = 2.8
        fig.colorbar(surf, shrink=0.5, aspect=5, location='left')
        ax.set_xlabel(list_1_name)
        ax.set_ylabel(list_2_name)
        ax.set_zlabel(list_3_name)
    plt.show()

def examples(num=0):
    global frequency
    global tuning_capacitance, coupling_capacitance, tuning_minimum, tuning_maximum, coupling_minimum, coupling_maximum, tuning_gradation, coupling_gradation

    if num == 0:
        minimum = 1e6
        maximum = 1e8
        frequency = minimum # Sets the minimum as the first value in the series.
        gradation = ((maximum - minimum)/sampling_rate) # Sets the number of hertz between each value.
        print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation:.2e}\n")
        for i in range(sampling_rate+1): # Cycles through each value in the chosen interval.
            fixed_calculation() # Calculates values for the current parameters.
            frequency += gradation # Sets the next parameter.
        plot_data(action_1=4, action_2=3, action_3=0)

    elif num == 1:
        reset_variables() # Prepares the program for the next calculation.
        reset_lists() # Prepares the program for the next calculation.
        
        frequency = 4e7
        tuning_minimum = 2e-11
        tuning_maximum = 3e-11
        coupling_minimum = 1e-13
        coupling_maximum = 1e-11
        
        tuning_capacitance = tuning_minimum # Sets the minimum as the first value in the series.
        coupling_capacitance = coupling_minimum # Sets the minimum as the first value in the series.
        tuning_gradation = (tuning_maximum - tuning_minimum)/sampling_rate # Sets the number of farads between each value.
        coupling_gradation = (coupling_maximum - coupling_minimum)/sampling_rate # Sets the number of farads between each value.
        print(f"Sampling rate:\t\t\t{sampling_rate}\nTuning gradation [F]:\t\t{tuning_gradation:.2e}\nCoupling gradation [F]:\t\t{coupling_gradation:.2e}\n")
        for i in range(sampling_rate+1): # Cycles through tuning parameters.
            for i in range(sampling_rate+1): # Cycles through coupling parameters.
                fixed_calculation() # Calculates values for the current parameters.
                coupling_capacitance += coupling_gradation # Sets the next parameter.
            coupling_capacitance = coupling_minimum # Sets the minimum as the first value in the series.
            tuning_capacitance += tuning_gradation # Sets the next parameter.
        plot_data(action_1=2, action_2=1, action_3=3)

def main():
    fixed_calculation() # Solves the circuit for the default or updated parameters.
    try: action_1 = int(input("Enter an action:\n1) View fixed values.\n2) Change a value.\n3) Run calculations.\n4) Help.\n0) Quit.\n\n"))
    except: action_1 = 0
    print("\n")
    if action_1 == 0:
        print("##################################################################################")
        print("Farewell!")
        print("##################################################################################\n\n")
        quit()
    else:
        if action_1 == 1:
            print_values() # Prints parameters and calculations within the program.
        elif action_1 == 2:
            update_fixed_values() # Allows the user to change a parameter.
        elif action_1 == 3:
            action_2 = int(input("Select calculation:\n1) Fixed calculation (no variables).\n2) Cluster calculation (one variable).\n3) Dense calculation (two capacitors).\n4) Brute force (two capacitors).\n5) Complex algebra (four variables).\n6) Example (frequency).\n7) Example (capacitance).\n0) Quit to main menu.\n\n"))
            print("\n")
            if action_2 != 0:
                if action_2 == 5:
                    complex_algebra() # Operates on complex numbers.
                else:
                    operation = 1
                    
                    if action_2 == 1:
                        reset_lists()
                        fixed_calculation() # Solves the circuit for one set of parameters.
                        
                    elif action_2 == 2:
                        reset_lists()
                        operation = cluster_calculation() # Solves the circuit for one variable.
                        operation = 1
                        
                    elif action_2 == 3:
                        dense_calculation() # Solves the circuit for two variables.
                        
                    elif action_2 == 4:
                        brute_force() # Calls dense_calculation with an exceedingly large sample_rate and range of capacitance values.

                    elif action_2 == 6:
                        examples(0)

                    elif action_2 == 7:
                        examples(1)
                        
                    if operation:
                        maximum_inductance_voltage(0)
                        if action_2 != 4:
                            export_data() # Exports the resulting data to a text file.
                            action_3 = int(input("\nData exported successfully. Do you want to plot data?\n1) Yes.\n0) No.\n\n"))
                        else:
                            action_3 = int(input("\nDo you want to plot data?\n1) Yes.\n0) No.\n\n"))
                        print("\n")
                        if action_3 == 1:
                            plot_data()
                        while action_3 != 0:
                            action_3 = int(input("Do you want to plot more data?\n1) Yes.\n0) No.\n\n"))
                            print("\n")
                            if action_3 == 1:
                                plot_data()
                print("Please wait while lists reset.\n\n")
                reset_variables() # Prepares the program for the next calculation.
                reset_lists() # Prepares the program for the next calculation.
            else:
                main()
        elif action_1 == 4:
            information()
        main()

###########################################################################
# Global Script
main()

###########################################################################