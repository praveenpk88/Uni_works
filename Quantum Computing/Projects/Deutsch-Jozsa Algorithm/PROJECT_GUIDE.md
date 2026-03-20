# Deutsch-Jozsa Algorithm Project - Complete Guide

## 📋 Project Overview

**Goal:** Implement and analyze the Deutsch-Jozsa algorithm to determine if a black-box function is constant or balanced using only **1 quantum query** (vs up to 2^(n-1)+1 classical queries).

---

## 🎯 All Deliverables Checklist

- [ ] **Deliverable 1:** Multiple oracle functions (constant and balanced)
- [ ] **Deliverable 2:** Working n-qubit DJ algorithm implementation
- [ ] **Deliverable 3:** Phase kickback explanation
- [ ] **Deliverable 4:** Circuit depth & gate complexity analysis
- [ ] **Deliverable 5:** Quantum vs classical query complexity comparison
- [ ] **Deliverable 6:** Testing on ideal (and optionally noisy) simulator

---

## 📚 Key Concepts You Must Understand

### 1. **The Problem**
- **Input:** A black-box function f(x) that takes n-bit binary input
- **Output:** Single bit (0 or 1)
- **Function Types:**
  - **Constant:** Always returns 0 OR always returns 1
  - **Balanced:** Returns 0 for exactly 50% of inputs, 1 for the other 50%
- **Question:** Is f(x) constant or balanced?

### 2. **Quantum States You'll Use**
- **|0⟩ state:** Ground state (default qubit initialization)
- **|1⟩ state:** Excited state (apply X gate to |0⟩)
- **|+⟩ state:** (|0⟩ + |1⟩)/√2 (apply H gate to |0⟩)
- **|−⟩ state:** (|0⟩ - |1⟩)/√2 (apply X then H to |0⟩)
- **Superposition:** Linear combination of basis states

### 3. **Quantum Gates**
- **H (Hadamard):** Creates superposition, basis transformation
- **X (NOT/Pauli-X):** Bit flip (|0⟩ ↔ |1⟩)
- **CNOT (Controlled-NOT):** Flips target if control is |1⟩
- **Barrier:** Visual separator (doesn't affect computation)

### 4. **Phase Kickback**
- Key mechanism that makes DJ algorithm work
- When target qubit is in |−⟩ state and a controlled operation is applied:
  - If f(x) = 0: no phase change
  - If f(x) = 1: introduces (-1) phase to the control qubit
- This phase affects interference patterns after final H gates

### 5. **Why DJ Algorithm Works**
- **Constant function:** All phases are the same → constructive interference → measure |00...0⟩
- **Balanced function:** Half phases positive, half negative → destructive interference at |00...0⟩ → measure non-zero

---

## 🔧 Essential Qiskit Methods

### Circuit Creation
```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Create registers
qreg = QuantumRegister(n, name="input")
output = QuantumRegister(1, name="output")
creg = ClassicalRegister(n, name="result")

# Create circuit
circuit = QuantumCircuit(qreg, output, creg)
```

### Gate Operations
```python
# Single-qubit gates
circuit.x(qubit)        # X gate (NOT)
circuit.h(qubit)        # Hadamard gate
circuit.barrier()       # Visual barrier

# Two-qubit gates
circuit.cx(control, target)  # CNOT gate

# Apply to multiple qubits
for i in range(n):
    circuit.h(qreg[i])

# Measurement
circuit.measure(qreg, creg)  # Measure quantum register to classical register
```

### Combining Circuits
```python
# Add one circuit to another
main_circuit.compose(oracle_circuit, inplace=True)
# OR
main_circuit = main_circuit.compose(oracle_circuit)
```

### Simulation
```python
from qiskit_aer import AerSimulator
from qiskit import transpile

# Create simulator
simulator = AerSimulator()

# Transpile circuit
transpiled = transpile(circuit, simulator)

# Run circuit
job = simulator.run(transpiled, shots=1024)
result = job.result()
counts = result.get_counts()
```

### Circuit Analysis
```python
# Get circuit depth
depth = circuit.depth()

# Count operations
ops = circuit.count_ops()

# Visualize circuit
circuit.draw('mpl')  # Returns matplotlib figure
```

---

## 📝 Step-by-Step Implementation Guide

### **DELIVERABLE 1: Oracle Functions**

#### **Part A: Constant Oracle**

**Location:** Cell marked "### WRITE YOUR CODE BELOW THIS CELL ###" in Constant oracle section

**What to do:**
```python
# The variable 'output' is already defined (0 or 1)
# If output == 1: apply X gate to output qubit
# If output == 0: do nothing

if output == 1:
    constant_oracle.x(qreg_output[0])
```

**Why it works:**
- No operation → output always 0 (constant)
- X gate on output → output always 1 (constant)

---

#### **Part B: Balanced Oracle**

**Location:** Cell marked "### WRITE YOUR CODE BELOW THIS CELL ###" in Balanced oracle section

**What to do:**
```python
# Step 1: Apply X gates based on random string 'qstr'
for i in range(n_input):
    if qstr[i] == '1':  # Check each character in string
        balanced_oracle.x(qreg_input[i])

# Step 2: Apply CNOT gates (input qubits control, output is target)
for i in range(n_input):
    balanced_oracle.cx(qreg_input[i], qreg_output[0])

# Step 3: Undo X gates from step 1
for i in range(n_input):
    if qstr[i] == '1':
        balanced_oracle.x(qreg_input[i])
```

**Why it works:**
- CNOT gates ensure output flips based on input qubits
- Random X gates increase diversity of output ordering
- Results in exactly 50% 0s and 50% 1s across all inputs

---

### **DELIVERABLE 2: Full DJ Algorithm**

**Location:** Cell under "Build the full DJ circuit"

**What to do:**
```python
# Step 1: Prepare |−⟩ state on output qubit
dj_circuit.x(qreg_output[0])
dj_circuit.h(qreg_output[0])

# Step 2: Apply H gates to all input qubits (create superposition)
for i in range(n_input):
    dj_circuit.h(qreg_input[i])

# Step 3: Add barrier for visualization (optional but recommended)
dj_circuit.barrier()

# Step 4: Apply the oracle (the mystery function)
if oracle == "constant":
    dj_circuit = dj_circuit.compose(constant_oracle)
elif oracle == "balanced":
    dj_circuit = dj_circuit.compose(balanced_oracle)

# Step 5: Add barrier
dj_circuit.barrier()

# Step 6: Apply H gates to all input qubits again
for i in range(n_input):
    dj_circuit.h(qreg_input[i])

# Step 7: Measure input qubits
dj_circuit.measure(qreg_input, creg)
```

---

### **DELIVERABLE 6 (Part 1): Ideal Simulator**

**Location:** Cell under "Run on ideal simulator"

**What to do:**
```python
# Create simulator
simulator = AerSimulator()

# Transpile circuit for simulator
transpiled_circuit = transpile(dj_circuit, simulator)

# Run simulation with 1024 shots
job = simulator.run(transpiled_circuit, shots=1024)

# Get results
result = job.result()
counts = result.get_counts()
```

**How to interpret:**
- If `counts = {'00': 1024}` → Constant function
- If `counts = {'01': 512, '10': 512}` (or similar non-zero) → Balanced function

---

### **DELIVERABLE 3: Phase Kickback Explanation**

**Location:** Markdown cell under "Why the algorithm works"

**What to write (in your own words):**

Key points to cover:
1. The output qubit is initialized to |−⟩ = (|0⟩ - |1⟩)/√2
2. When oracle applies f(x) to the circuit:
   - If f(x) = 0: state remains unchanged
   - If f(x) = 1: introduces a global phase of (-1)
3. This phase "kicks back" to the input qubits (phase kickback)
4. For constant functions: all inputs have same phase → after final H gates, constructive interference at |00...0⟩
5. For balanced functions: half inputs phase +1, half phase -1 → destructive interference at |00...0⟩

**Mathematical expression:**
- After oracle: |x⟩ ⊗ |−⟩ → (-1)^f(x) |x⟩ ⊗ |−⟩
- The (-1)^f(x) is the phase that affects interference

---

### **DELIVERABLE 4: Circuit Depth & Gate Complexity**

**Location:** Code cell under this deliverable

**What to do:**
```python
import matplotlib.pyplot as plt

# Test different values of n
n_values = [2, 3, 4, 5, 6, 7, 8]
depths = []
gate_counts = []

for n in n_values:
    # Create registers
    qreg = QuantumRegister(n, name="input")
    output_reg = QuantumRegister(1, name="output")
    creg = ClassicalRegister(n, name="result")
    
    # Create test circuit with just the DJ structure (no oracle for simplicity)
    test_circuit = QuantumCircuit(qreg, output_reg, creg)
    
    # Prepare output qubit
    test_circuit.x(output_reg[0])
    test_circuit.h(output_reg[0])
    
    # H gates on inputs
    for i in range(n):
        test_circuit.h(qreg[i])
    
    test_circuit.barrier()
    
    # Simple balanced oracle (CNOT gates)
    for i in range(n):
        test_circuit.cx(qreg[i], output_reg[0])
    
    test_circuit.barrier()
    
    # H gates on inputs again
    for i in range(n):
        test_circuit.h(qreg[i])
    
    # Measure
    test_circuit.measure(qreg, creg)
    
    # Transpile and get metrics
    transpiled = transpile(test_circuit, simulator)
    depths.append(transpiled.depth())
    gate_counts.append(sum(transpiled.count_ops().values()))

# Plot results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(n_values, depths, 'o-', linewidth=2, markersize=8)
ax1.set_xlabel('Number of input qubits (n)')
ax1.set_ylabel('Circuit Depth')
ax1.set_title('Circuit Depth vs n')
ax1.grid(True)

ax2.plot(n_values, gate_counts, 'o-', linewidth=2, markersize=8, color='orange')
ax2.set_xlabel('Number of input qubits (n)')
ax2.set_ylabel('Total Gate Count')
ax2.set_title('Gate Count vs n')
ax2.grid(True)

plt.tight_layout()
plt.show()

print("Analysis:")
print(f"Circuit depth scales: O(n) - linear")
print(f"Gate count scales: O(n) - linear")
print(f"\nFor n={n_values[-1]}: Depth={depths[-1]}, Gates={gate_counts[-1]}")
```

**What to write in markdown:**
- Circuit depth grows linearly with n: O(n)
- Gate count grows linearly with n: O(n)
- Most depth comes from CNOT gates in oracle (for balanced function)
- H gates and measurements contribute 2n + 2 gates

---

### **DELIVERABLE 5: Query Complexity Comparison**

**Location:** Markdown cell under this deliverable

**What to write:**

**Classical Approach:**
- **Worst case:** 2^(n-1) + 1 queries
- **Best case:** 2 queries (if you get different outputs)
- **Why:** Must check more than half the inputs to be certain
- **Example:** For n=3 (8 inputs), need up to 5 queries

**Quantum Approach:**
- **Always:** 1 query
- **Why:** Superposition allows checking all inputs simultaneously
- **Speedup:** Exponential advantage

**Comparison Table:**
| n (qubits) | Classical (worst) | Quantum | Advantage |
|------------|-------------------|---------|-----------|
| 2          | 3                 | 1       | 3x        |
| 3          | 5                 | 1       | 5x        |
| 4          | 9                 | 1       | 9x        |
| 10         | 513               | 1       | 513x      |
| 20         | 524,289           | 1       | >500,000x |

---

### **DELIVERABLE 6 (Optional): Noisy Simulator**

**Location:** Code cell under "Noisy simulator"

**What to do:**
```python
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error

# Create noise model
noise_model = NoiseModel()

# Add depolarizing error to gates
error_1q = depolarizing_error(0.001, 1)  # 0.1% error on single-qubit gates
error_2q = depolarizing_error(0.01, 2)   # 1% error on two-qubit gates

noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x'])
noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

# Create noisy simulator
noisy_simulator = AerSimulator(noise_model=noise_model)

# Run circuit on noisy simulator
transpiled_noisy = transpile(dj_circuit, noisy_simulator)
noisy_job = noisy_simulator.run(transpiled_noisy, shots=1024)
noisy_result = noisy_job.result()
noisy_counts = noisy_result.get_counts()

# Compare results
print("Ideal simulator results:")
print(counts)
print("\nNoisy simulator results:")
print(noisy_counts)

# Plot comparison
from qiskit.visualization import plot_histogram
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
plot_histogram(counts, ax=ax1, title='Ideal Simulator')
plot_histogram(noisy_counts, ax=ax2, title='Noisy Simulator')
plt.tight_layout()
plt.show()
```

**What to observe:**
- Ideal: Should see clean results (all 1024 shots in one or two states)
- Noisy: May see errors (small counts in wrong states)
- Success rate may be lower (but still very high for small n)

---

## 🧪 Testing Your Code

### **Verify Constant Oracle:**
```python
# Test constant oracle with all input combinations
test_circuit = QuantumCircuit(qreg_input, qreg_output, creg)
test_circuit = test_circuit.compose(constant_oracle)
test_circuit.measure(qreg_output[0], creg[0])

# Run multiple times with different inputs
# Should always get same output (0 or 1)
```

### **Verify Balanced Oracle:**
```python
# For 2 qubits: should get 0 twice and 1 twice
# Test all 4 combinations: 00, 01, 10, 11
```

### **Debug Visualization:**
```python
circuit.draw('mpl')  # See your circuit visually
print(circuit)       # Text representation
```

---

## 📖 Learning Resources

### **Qiskit Documentation:**
- Official Textbook: https://qiskit.org/learn
- Deutsch-Jozsa Tutorial: Search "Qiskit Deutsch-Jozsa"
- API Reference: https://docs.quantum.ibm.com/api/qiskit

### **Concepts to Study:**
1. **Superposition:** How H gates create equal probability states
2. **Interference:** How quantum amplitudes add/cancel
3. **Phase kickback:** How |−⟩ state enables phase manipulation
4. **Quantum parallelism:** Processing multiple inputs simultaneously
5. **Measurement:** Collapsing superposition to classical bits

### **Videos/Articles:**
- Search: "Deutsch-Jozsa algorithm explained"
- Search: "Phase kickback quantum computing"
- Search: "Qiskit tutorial Deutsch-Jozsa"

---

## 🐛 Common Issues & Solutions

### **Issue 1: "IndexError: list index out of range"**
**Solution:** Check qubit indexing. Remember qreg_output is size 1, so use qreg_output[0]

### **Issue 2: Circuit doesn't show oracle**
**Solution:** Make sure you use `compose()` correctly:
```python
dj_circuit = dj_circuit.compose(oracle_circuit)  # OR
dj_circuit.compose(oracle_circuit, inplace=True)
```

### **Issue 3: All measurements are wrong**
**Solution:** Check that you:
- Applied X then H to output qubit (not just H)
- Applied H to inputs BEFORE and AFTER oracle
- Measured input qubits (not output qubit)

### **Issue 4: "No counts in result"**
**Solution:** Make sure you added `measure()` to your circuit

### **Issue 5: Can't see plot**
**Solution:** Add `%matplotlib inline` at top of notebook (Jupyter magic)

---

## ✅ Validation Checklist

Before submitting, verify:

- [ ] Constant oracle works (returns same output for all inputs)
- [ ] Balanced oracle works (returns 0 for half, 1 for half)
- [ ] DJ circuit has correct structure (H → Oracle → H → Measure)
- [ ] Output qubit is in |−⟩ state
- [ ] Simulator correctly identifies constant vs balanced
- [ ] All code cells execute without errors
- [ ] All outputs (plots, histograms) display correctly
- [ ] Markdown explanations are in your own words
- [ ] Analysis includes numerical results and plots
- [ ] You understand WHY the algorithm works (not just that it works)

---

## 🎓 Learning Tips

1. **Experiment:** Change n_input from 2 to 3 or 4 and see what happens
2. **Visualize:** Always use `draw('mpl')` to see your circuits
3. **Test incrementally:** Run each cell as you complete it
4. **Understand before coding:** Read the theory sections carefully
5. **Compare results:** Run constant vs balanced oracles multiple times
6. **Ask "why":** Don't just copy code—understand each gate's purpose

---

## 📊 Expected Outputs

### **Constant Function:**
```
Counts: {'00': 1024}
Conclusion: Oracle is constant
```

### **Balanced Function:**
```
Counts: {'01': 256, '10': 384, '11': 384}  # (example, varies)
Conclusion: Oracle is balanced
```

### **Key Insight:**
If any measurement shows non-zero state → balanced
If ALL measurements show '00...0' → constant

---

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start Jupyter (if needed)
jupyter notebook DJ-Project-Notebook.ipynb
```

---

## 📝 Summary

**The Big Picture:**
1. Build two types of oracles (constant and balanced)
2. Build DJ algorithm that uses these oracles
3. Run on simulator - should correctly identify function type in 1 query
4. Analyze why it works (phase kickback)
5. Analyze how it scales (linear in n)
6. Compare to classical (exponential speedup)

**Key Takeaway:** DJ algorithm demonstrates quantum advantage through superposition, interference, and phase kickback - achieving exponential speedup over classical approaches.

---

Good luck with your project! Work through each deliverable systematically, test frequently, and make sure you understand the concepts, not just the code. 🎉
