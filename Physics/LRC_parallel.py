###########################################################################
###########################################################################
#
# Alex Heinrich
# Circuit Analyzer
#
###########################################################################
###########################################################################

###########################################################################
# Global Values

# Voltage Supply Values
input_voltage, input_impedance = [1, 0], [50, 0] # Units of volts and ohms.
frequency, frequency_set = 40*(10**6), 40*(10**6) # Units of hertz. Enter the same value for both parameters.
angular_frequency = 2 * 3.14159265359 * frequency

# Component Values
inductor_resistance = 0.1
inductance, inductance_set, inductor_impedance, inductor_list = 0.6*(10**(-6)), 0.6*(10**(-6)), [0, 0], []
tuning_capacitance, tuning_capacitance_set, tuning_impedance, tuning_list = 25.2*(10**(-12)), 25.2*(10**(-12)), [0, 0], []
total_list, frequency_list = [], []

# Calculation Values
sampling_rate = 100 # Sets the number of datapoints calculated across the specified range.
fixed_calculation_counter = 0
total_impedance, total_current = [], []

# Other
print_view = 0 # Used for troubleshooting.


###########################################################################
# Basic Operations

def add(z_1, z_2):
    """ Adds complex numbers as two-item lists. """
    real_sum = z_1[0] + z_2[0]
    imaginary_sum = z_1[1] + z_2[1]
    result = [real_sum, imaginary_sum]
    return result

def subtract(z_1, z_2):
    """ Subtracts complex numbers as two-item lists. """
    real_difference = z_1[0] - z_2[0]
    imaginary_difference = z_1[1] - z_2[1]
    result = [real_difference, imaginary_difference]
    return result
    
def multiply(z_1, z_2):
    """ Multiplies complex numbers as two-item lists. """
    real_product = (z_1[0] * z_2[0]) - (z_1[1] * z_2[1])
    imaginary_product = (z_1[0] * z_2[1]) + (z_1[1] * z_2[0])
    result = [real_product, imaginary_product]
    return result
    
def divide(z_1, z_2):
    """ Divides complex numbers as two-item lists. """
    real_numerator = (z_1[0] * z_2[0]) + (z_1[1] * z_2[1])
    imaginary_numerator = (z_1[1] * z_2[0]) - (z_1[0] * z_2[1])
    denominator = (z_2[0])**2 + (z_2[1])**2
    real_quotient = real_numerator / denominator
    imaginary_quotient = imaginary_numerator / denominator
    result = [real_quotient, imaginary_quotient]
    return result
    
def parallel(z_1, z_2):
    """ Adds two components in parallel. """
    numerator = multiply(z_1, z_2)
    denominator = add(z_1, z_2)
    result = divide(numerator, denominator)
    return result
    

###########################################################################
# Functions

def impedance_calculations():
    """ Updates the impedance at a given frequency for all components. """
    global angular_frequency, inductor_impedance, tuning_impedance
    if print_view == 1: print("impedance_calculations():")
    angular_frequency = 2 * 3.14159265359 * frequency
    inductor_impedance = [inductor_resistance, angular_frequency * inductance]
    tuning_impedance = [0, -1/(angular_frequency * tuning_capacitance)]
    reduce_circuit()

def reduce_circuit():
    """ Determines the total impedance and current of the circuit, given some input voltage. """
    global total_impedance, total_current
    if print_view == 1: print("reduce_circuit():")
    total_impedance = parallel(inductor_impedance, tuning_impedance)
    effective_impedance = add(total_impedance, input_impedance)
    total_current = divide(input_voltage, effective_impedance)
    return total_current, total_impedance
    
def solve_circuit(total_current, total_impedance):
    if print_view == 1: print("solve_circuit():\n")
    parallel_voltage = multiply(total_current, total_impedance)
    tuning_current = divide(parallel_voltage, tuning_impedance)
    inductor_current = divide(parallel_voltage, inductor_impedance)
    total_values = [input_voltage, total_current, total_impedance]
    tuning_values = [parallel_voltage, tuning_current, tuning_impedance, tuning_capacitance]
    inductor_values = [parallel_voltage, inductor_current, inductor_impedance, inductance]
    frequency_list.append(frequency)
    total_list.append(total_values)
    inductor_list.append(inductor_values)
    tuning_list.append(tuning_values)

def export_data():
    """ Saves current calculation lists to tab separated values in a text file. """
    if print_view == 1: print("export_data():\n")
    with open("=data.txt", 'w', encoding='utf-8') as data_file:
        print(f"Frequency [Hz]\tTotal voltage (real) [V]\tTotal voltage (imaginary) [V]\tTotal current (real) [A]\tTotal current (imaginary) [A]\tTotal impedance (real) [Ω]\tTotal impedance (imaginary) [Ω]\tInductance [H]\tInductor voltage (real) [V]\tInductor voltage (imaginary) [V]\tInductor current (real) [A]\tInductor current (imaginary) [A]\tInductor impedance (real) [Ω]\tInductor impedance (imaginary) [Ω]\tTuning capacitance [F]\tTuning voltage (real) [V]\tTuning voltage (imaginary) [V]\tTuning current (real) [A]\tTuning current (imaginary) [A]\tTuning impedance (real) [Ω]\tTuning impedance (imaginary) [Ω]\t", file=data_file)
        for i in range(len(total_list)):
            print(f"{frequency_list[i]}\t{total_list[i][0][0]}\t{total_list[i][0][1]}\t{total_list[i][1][0]}\t{total_list[i][1][1]}\t{total_list[i][2][0]}\t{total_list[i][2][1]}\t{inductor_list[i][-1]}\t{inductor_list[i][0][0]}\t{inductor_list[i][0][1]}\t{inductor_list[i][1][0]}\t{inductor_list[i][1][1]}\t{inductor_list[i][2][0]}\t{inductor_list[i][2][1]}\t{tuning_list[i][-1]}\t{tuning_list[i][0][0]}\t{tuning_list[i][0][1]}\t{tuning_list[i][1][0]}\t{tuning_list[i][1][1]}\t{tuning_list[i][2][0]}\t{tuning_list[i][2][1]}", file=data_file)

def print_values():
    print("##################################################################################")
    print(f"Sampling rate:\t\t\t{sampling_rate}\n\nSupply voltage [V]:\t\t({input_voltage[0]:.2f})+i({input_voltage[1]:.2f})\nSupply impedance [Ω]:\t\t({input_impedance[0]:.2f})+i({input_impedance[1]:.2f})\nFrequency [Hz]:\t\t\t{(frequency):.2e}\nAngular frequency [s⁻¹]:\t{angular_frequency:.2e}\n")
    print(f"Total current [A]:\t\t({total_list[0][1][0]:.2e})+i({total_list[0][1][1]:.2e})\nTotal impedance [Ω]:\t\t({total_list[0][2][0]:.2e})+i({total_list[0][2][1]:.2e})\nInductor voltage [V]:\t\t({inductor_list[0][0][0]:.2e})+i({inductor_list[0][0][1]:.2e})\nInductor current [A]:\t\t({inductor_list[0][1][0]:.2e})+i({inductor_list[0][1][1]:.2e})\nInductor impedance [Ω]:\t\t({inductor_list[0][2][0]:.2e})+i({inductor_list[0][2][1]:.2e})\nTuning voltage [V]:\t\t({tuning_list[0][0][0]:.2e})+i({tuning_list[0][0][1]:.2e})\nTuning current [A]:\t\t({tuning_list[0][1][0]:.2e})+i({tuning_list[0][1][1]:.2e})\nTuning impedance [Ω]:\t\t({tuning_list[0][2][0]:.2e})+i({tuning_list[0][2][1]:.2e})")
    print("##################################################################################\n\n")

def update_fixed_values():
    global frequency, sampling_rate, inductance, tuning_capacitance, frequency_set, inductance_set, tuning_capacitance_set
    action = int(input("Select a value to change:\n1) Frequency\n2) Sampling rate\n3) Inductance\n4) Inductor resistance\n5) Tuning capacitance\n0) Quit to main menu.\n\n"))
    print()
    if action == 1:
        frequency = float(input("Enter frequency [Hz]:\t"))
    elif action == 2:
        sampling_rate = int(input("Enter sampling rate:\t"))
    elif action == 3:
        inductance = float(input("Enter inductance [H]:\t"))
    elif action == 4:
        inductor_resistance = float(input("Enter resistance [Ω]:\t"))
    elif action == 5:
        tuning_capacitance = float(input("Enter tuning capacitance [F]:\t"))
    frequency_set, inductance_set, tuning_capacitance_set = frequency, inductance, tuning_capacitance
    print("\n")
    impedance_calculations()

def fixed_calculation():
    """ Solves the circuit with its current parameters. """
    global tuning_impedance, fixed_calculation_counter
    impedance_calculations()
    total_current, parallel_impedance = reduce_circuit()
    solve_circuit(total_current, parallel_impedance)

def cluster_calculation():
    """ Solves the circuit as one parameter changes. """
    global tuning_capacitance, frequency
    action = int(input("Select a variable:\n1) Tuning capacitance.\n2) Coupling capacitance.\n3) Frequency.\n0) Quit to main menu.\n\n"))
    print("\n")
    if action != 0:
        print("Enter 0 for each variable to quit to main menu.")
        if action == 1:
            minimum = float(input("Enter a minimum value [F]:\t"))
            maximum = float(input("Enter a maximum value [F]:\t"))
            if (minimum + maximum) != 0:
                tuning_capacitance = minimum
                gradation = ((maximum - minimum)/sampling_rate) # Allows for a variable number of datapoints.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1):
                    fixed_calculation() # Calculates values for the current parameters.
                    tuning_capacitance += gradation # Sets the next parameter.
                return True
            else:
                return False
        if action == 2:
            minimum = float(input("Enter a minimum value [Hz]:\t"))
            maximum = float(input("Enter a maximum value [Hz]:\t"))
            if (minimum + maximum) != 0:
                frequency = minimum
                gradation = ((maximum - minimum)/sampling_rate) # Allows for a variable number of datapoints.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1):
                    fixed_calculation() # Calculates values for the current parameters.
                    frequency += gradation # Sets the next parameter.
                return True
            else:
                return False
    else:
        return False

def dense_calculation():
    """ Solves the circuit for a number of capacitor combinations. """
    global tuning_capacitance, inductance
    print("Enter 0 for each variable to quit to main menu.")
    tuning_minimum = float(input("Enter a minimum tuning capacitance [F]:\t"))
    tuning_maximum = float(input("Enter a maximum tuning capacitance [F]:\t"))
    inductance_minimum = float(input("Enter a minimum inductance [H]:\t"))
    inductance_maximum = float(input("Enter a maximum inductance [H]:\t"))
    print("\n")
    if (tuning_minimum + tuning_maximum + inductance_minimum + inductance_maximum) != 0:
        tuning_capacitance = tuning_minimum
        inductance = inductance_minimum
        tuning_gradation = (tuning_maximum - tuning_minimum)/sampling_rate # Allows for a variable number of datapoints.
        inductance_gradation = (inductance_maximum - inductance_minimum)/sampling_rate
        print(f"Sampling rate:\t\t\t{sampling_rate}\nTuning gradation [F]:\t\t{tuning_gradation}\nInductance gradation [H]:\t\t{inductance_gradation}\n")
        for i in range(sampling_rate+1): # Cycles through tuning parameters.
            for i in range(sampling_rate+1): # Cycles through coupling parameters.
                fixed_calculation() # Calculates values for the current parameters.
                inductance += inductance_gradation # Sets the next parameter.
            inductance = inductance_minimum
            tuning_capacitance += tuning_gradation # Sets the next parameter.

def complex_algebra():
    """ Computes binary operations on complex numbers. """
    print("Enter 0 for each variable to quit to main menu.")
    x_1 = float(input("Enter Re(z_1):\t"))
    y_1 = float(input("Enter Im(z_1):\t"))
    x_2 = float(input("Enter Re(z_2):\t"))
    y_2 = float(input("Enter Im(z_2):\t"))
    print("\n")
    if (x_1 + y_1 + x_2 + y_2) != 0:
        z_1, z_2 = [x_1, y_1], [x_2, y_2]
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

def reset_variables():
    global frequency, inductance, tuning_capacitance, coupling_capacitance
    if print_view == 1: print("reset_variables():\n")
    frequency, inductance, tuning_capacitance, coupling_capacitance = frequency_set, inductance_set, tuning_capacitance_set, coupling_capacitance_set
    
def reset_lists():
    global total_list, frequency_list, inductor_list, tuning_list, coupling_list
    if print_view == 1: print("reset_lists():\n")
    total_list.clear()
    frequency_list.clear()
    inductor_list.clear()
    tuning_list.clear()
    coupling_list.clear()
    total_impedance.clear()
    total_current.clear()
    fixed_calculation_counter = 0

def main():
    fixed_calculation()
    action_1 = int(input("Enter an action:\n1) View fixed values.\n2) Change a value.\n3) Run calculations.\n0) Quit.\n\n"))
    print("\n")
    if action_1 == 0:
        pass
    else:
        if action_1 == 1:
            print_values()
        elif action_1 == 2:
            update_fixed_values()
        elif action_1 == 3:
            action_2 = int(input("Select calculation:\n1) Fixed calculation (no variables).\n2) Cluster calculation (one variable).\n3) Dense calculation (two variables).\n4) Complex algebra (four variables).\n0) Quit to main menu.\n\n"))
            print("\n")
            if action_2 != 0:
                if action_2 == 1:
                    reset_lists()
                    fixed_calculation()
                    print("Data exported successfully.\n\n")
                elif action_2 == 2:
                    reset_lists()
                    operation = cluster_calculation()
                    if operation:
                        print("Data exported successfully.\n\n")
                elif action_2 == 3:
                    dense_calculation()
                    print("Data exported successfully.\n\n")
                elif action_2 == 4:
                    complex_algebra()
                export_data()
        reset_variables()
        reset_lists()
        main()

###########################################################################
# Global Script

print("\n##################################################################################")
print("Welcome!")
print("##################################################################################\n\n")
main()


###########################################################################
###########################################################################
